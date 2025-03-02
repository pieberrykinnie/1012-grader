"""
Utility functions for the Python Grader Tool.

This module contains functions for executing scripts, validating output,
analyzing code, and generating reports.
"""

import ast
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ExecutionResult:
    """Dataclass to store the result of script execution."""

    stdout: str
    stderr: str
    timeout_occurred: bool
    error: bool
    return_code: Optional[int] = None
    error_message: Optional[str] = None


@dataclass
class OutputValidation:
    """Dataclass to store the result of output validation."""

    found_patterns: List[str]
    missing_patterns: List[str]
    total_patterns: int


@dataclass
class LineIssue:
    """Dataclass to store information about issues with specific lines."""

    line_number: int
    issue_type: str
    line_content: str
    description: str


@dataclass
class CodeAnalysis:
    """Dataclass to store the result of code analysis."""

    line_issues: List[LineIssue]
    comment_count: int
    long_lines_count: int
    banned_patterns_count: int
    multiple_returns_count: int


def execute_script(script_path: str, input_data: str, timeout: int) -> ExecutionResult:
    """
    Execute a Python script with the given input and capture its output.

    Args:
        script_path: Path to the Python script to execute
        input_data: Input to provide to the script via stdin
        timeout: Maximum execution time in seconds

    Returns:
        ExecutionResult containing stdout, stderr, and error information
    """
    try:
        # Run the script with the provided input
        process = subprocess.run(
            [sys.executable, script_path],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        return ExecutionResult(
            stdout=process.stdout,
            stderr=process.stderr,
            timeout_occurred=False,
            error=process.returncode != 0,
            return_code=process.returncode,
        )

    except subprocess.TimeoutExpired:
        return ExecutionResult(
            stdout="",
            stderr="",
            timeout_occurred=True,
            error=True,
            error_message=f"Execution timed out after {timeout} seconds",
        )

    except Exception as e:
        return ExecutionResult(
            stdout="",
            stderr="",
            timeout_occurred=False,
            error=True,
            error_message=f"Error executing script: {str(e)}",
        )


def validate_output(output: str, expected_patterns: List[str]) -> OutputValidation:
    """
    Validate that the output contains the expected patterns.

    Args:
        output: The stdout captured from script execution
        expected_patterns: List of strings or regex patterns to search for

    Returns:
        OutputValidation containing lists of found and missing patterns
    """
    found_patterns = []
    missing_patterns = []

    for pattern in expected_patterns:
        if re.search(pattern, output, re.MULTILINE):
            found_patterns.append(pattern)
        else:
            missing_patterns.append(pattern)

    return OutputValidation(
        found_patterns=found_patterns,
        missing_patterns=missing_patterns,
        total_patterns=len(expected_patterns),
    )


class ReturnStatementVisitor(ast.NodeVisitor):
    """AST visitor that counts return statements in each function."""

    def __init__(self):
        self.functions_with_multiple_returns = {}

    def visit_FunctionDef(self, node):
        """Visit a function definition and count its return statements."""
        return_count = 0

        # Count return statements
        for child in ast.walk(node):
            if isinstance(child, ast.Return):
                return_count += 1

        # Record functions with multiple returns
        if return_count > 1:
            self.functions_with_multiple_returns[node.name] = return_count

        self.generic_visit(node)


def count_words_in_line(line: str) -> int:
    """Count the number of words in a line of code."""
    # Remove comments
    line = re.sub(r"#.*$", "", line)
    # Split by whitespace and filter out empty strings
    words = [word for word in line.split() if word.strip()]
    return len(words)


def analyze_code(script_path: str) -> CodeAnalysis:
    """
    Analyze a Python script for programming standards compliance.

    Args:
        script_path: Path to the Python script to analyze

    Returns:
        CodeAnalysis containing information about code issues
    """
    line_issues = []
    comment_count = 0
    long_lines_count = 0
    banned_patterns_count = 0

    # Banned patterns to search for
    banned_patterns = {
        r"\bbreak\b": "Use of 'break' statement",
        r"\bcontinue\b": "Use of 'continue' statement",
        r"\bwhile\s+True\b": "Use of 'while True' infinite loop",
    }

    # Read the file line by line
    with open(script_path, "r") as file:
        for line_number, line in enumerate(file, 1):
            # Count comments
            if line.strip().startswith("#") or "#" in line:
                comment_count += 1

            # Check line length (words)
            word_count = count_words_in_line(line)
            if word_count > 100:
                long_lines_count += 1
                line_issues.append(
                    LineIssue(
                        line_number=line_number,
                        issue_type="LONG_LINE",
                        line_content=line.strip(),
                        description=(
                            f"Line exceeds 100 words " f"(contains {word_count} words)"
                        ),
                    )
                )

            # Check for banned patterns
            for pattern, description in banned_patterns.items():
                if re.search(pattern, line):
                    banned_patterns_count += 1
                    line_issues.append(
                        LineIssue(
                            line_number=line_number,
                            issue_type="BANNED_PATTERN",
                            line_content=line.strip(),
                            description=description,
                        )
                    )

    # Check for multiple return statements using AST
    with open(script_path, "r") as file:
        try:
            tree = ast.parse(file.read())
            visitor = ReturnStatementVisitor()
            visitor.visit(tree)

            multiple_returns_count = len(visitor.functions_with_multiple_returns)

            # Add multiple return issues
            for (
                func_name,
                return_count,
            ) in visitor.functions_with_multiple_returns.items():
                line_issues.append(
                    LineIssue(
                        line_number=0,  # AST doesn't provide line numbers easily
                        issue_type="MULTIPLE_RETURNS",
                        line_content=f"Function: {func_name}",
                        description=(
                            f"Function contains {return_count} return statements"
                        ),
                    )
                )

        except SyntaxError as e:
            line_issues.append(
                LineIssue(
                    line_number=(
                        e.lineno if hasattr(e, "lineno") and e.lineno is not None else 0
                    ),
                    issue_type="SYNTAX_ERROR",
                    line_content="",
                    description=f"Syntax error: {str(e)}",
                )
            )
            multiple_returns_count = 0

    return CodeAnalysis(
        line_issues=line_issues,
        comment_count=comment_count,
        long_lines_count=long_lines_count,
        banned_patterns_count=banned_patterns_count,
        multiple_returns_count=multiple_returns_count,
    )


def generate_report(
    script_path: str,
    execution_result: ExecutionResult,
    output_validation: OutputValidation,
    code_analysis: CodeAnalysis,
) -> str:
    """
    Generate a comprehensive grading report.

    Args:
        script_path: Path to the Python script that was analyzed
        execution_result: Result of script execution
        output_validation: Result of output validation
        code_analysis: Result of code analysis

    Returns:
        A formatted string containing the complete report
    """
    report_lines = []

    # Script information
    script_name = os.path.basename(script_path)
    report_lines.append(f"Grading Report for {script_name}")
    report_lines.append("-" * 40)

    # Execution information
    report_lines.append("Execution:")
    if execution_result.timeout_occurred:
        report_lines.append(f"[!] {execution_result.error_message}")
    elif execution_result.error:
        report_lines.append(
            f"[!] Script exited with error (return code: {execution_result.return_code})"
        )
        if execution_result.stderr:
            report_lines.append("\nError output:")
            report_lines.append(execution_result.stderr)
    else:
        report_lines.append("[✓] Script executed successfully")

    # Output validation
    report_lines.append("\nOutput Validation:")
    for pattern in output_validation.found_patterns:
        report_lines.append(f'[✓] Found: "{pattern}"')
    for pattern in output_validation.missing_patterns:
        report_lines.append(f'[✗] Missing: "{pattern}"')

    # Code analysis
    report_lines.append("\nCode Analysis:")
    report_lines.append(f"[i] Comment count: {code_analysis.comment_count}")

    if code_analysis.line_issues:
        report_lines.append("\nIssues Found:")
        for issue in code_analysis.line_issues:
            if issue.issue_type == "LONG_LINE":
                report_lines.append(
                    f"[!] Line {issue.line_number}: {issue.description}"
                )
            elif issue.issue_type == "BANNED_PATTERN":
                report_lines.append(
                    f"[!] Line {issue.line_number}: {issue.description}"
                )
                report_lines.append(f"    {issue.line_content}")
            elif issue.issue_type == "MULTIPLE_RETURNS":
                report_lines.append(f"[!] {issue.description} in {issue.line_content}")
            elif issue.issue_type == "SYNTAX_ERROR":
                report_lines.append(
                    f"[!] Line {issue.line_number}: {issue.description}"
                )
    else:
        report_lines.append("[✓] No code issues found")

    # Summary
    report_lines.append("\nSummary:")
    report_lines.append(
        f"- Output Validation: "
        f"{len(output_validation.found_patterns)}/{output_validation.total_patterns} "
        f"checks passed"
    )

    issue_count = (
        code_analysis.long_lines_count
        + code_analysis.banned_patterns_count
        + code_analysis.multiple_returns_count
    )
    report_lines.append(f"- Code Analysis: {issue_count} issues found")

    return "\n".join(report_lines)


def read_expected_patterns(file_path: str) -> List[str]:
    """
    Read expected output patterns from a file.

    Args:
        file_path: Path to the file containing output patterns

    Returns:
        List of strings, one for each non-empty line in the file

    Raises:
        FileNotFoundError: If the file doesn't exist
        PermissionError: If the file can't be read
        IOError: For other file-related errors
    """
    patterns = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:  # Skip empty lines
                patterns.append(line)

    return patterns
