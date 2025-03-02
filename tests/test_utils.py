"""Tests for the utility functions in the grader tool."""

import os
import tempfile
import pytest
from typing import List, Tuple

from grader import utils


def create_temp_script(content: str) -> Tuple[str, str]:
    """Create a temporary Python script file for testing."""
    fd, path = tempfile.mkstemp(suffix=".py")
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        return path, os.path.basename(path)
    except Exception:
        os.unlink(path)
        raise


def test_execute_script_success():
    """Test execution of a script that runs successfully."""
    script_content = 'print("Hello, World!")'
    path, _ = create_temp_script(script_content)
    
    try:
        result = utils.execute_script(path, "", 5)
        assert not result.error
        assert "Hello, World!" in result.stdout
        assert not result.stderr
        assert result.return_code == 0
        assert not result.timeout_occurred
    finally:
        os.unlink(path)


def test_execute_script_with_input():
    """Test execution of a script that requires input."""
    script_content = 'name = input("Name: "); print(f"Hello, {name}!")'
    path, _ = create_temp_script(script_content)
    
    try:
        result = utils.execute_script(path, "John", 5)
        assert not result.error
        assert "Hello, John!" in result.stdout
        assert not result.stderr
        assert result.return_code == 0
    finally:
        os.unlink(path)


def test_execute_script_timeout():
    """Test that script execution timeouts are caught correctly."""
    script_content = 'import time; time.sleep(2)'
    path, _ = create_temp_script(script_content)
    
    try:
        result = utils.execute_script(path, "", 1)  # Set timeout to 1 second
        assert result.error
        assert result.timeout_occurred
        assert "timed out" in result.error_message
    finally:
        os.unlink(path)


def test_validate_output_all_found():
    """Test output validation when all patterns are found."""
    output = "Hello, World!\nThis is a test.\nValue: 42"
    expected = ["Hello", "test", r"Value: \d+"]
    
    result = utils.validate_output(output, expected)
    assert len(result.found_patterns) == 3
    assert len(result.missing_patterns) == 0
    assert result.total_patterns == 3


def test_validate_output_some_missing():
    """Test output validation when some patterns are missing."""
    output = "Hello, World!\nThis is a test."
    expected = ["Hello", "missing", "also missing"]
    
    result = utils.validate_output(output, expected)
    assert len(result.found_patterns) == 1
    assert len(result.missing_patterns) == 2
    assert "missing" in result.missing_patterns
    assert "also missing" in result.missing_patterns
    assert result.total_patterns == 3


def test_analyze_code():
    """Test code analysis functionality."""
    script_content = """# This is a comment
def test_function():
    if True:
        # Another comment
        return 42
    else:
        return 0  # Multiple returns!

# Banned pattern
while True:
    break  # Another banned pattern
"""
    path, _ = create_temp_script(script_content)
    
    try:
        result = utils.analyze_code(path)
        
        # Check comment count
        assert result.comment_count == 5
        
        # Check banned patterns
        assert result.banned_patterns_count == 2
        assert any("break" in issue.description for issue in result.line_issues)
        assert any("while True" in issue.description for issue in result.line_issues)
        
        # Check multiple returns
        assert result.multiple_returns_count == 1
        assert any("multiple_returns" in issue.issue_type.lower() for issue in result.line_issues)
    finally:
        os.unlink(path)


def test_count_words_in_line():
    """Test word counting in a line of code."""
    line = "def function(a, b, c):  # This is a comment"
    assert utils.count_words_in_line(line) == 4  # The comment should be excluded


def test_generate_report():
    """Test report generation with various inputs."""
    # Create mock objects
    execution_result = utils.ExecutionResult(
        stdout="Hello, World!",
        stderr="",
        timeout_occurred=False,
        error=False,
        return_code=0
    )
    
    output_validation = utils.OutputValidation(
        found_patterns=["Hello"],
        missing_patterns=["Missing"],
        total_patterns=2
    )
    
    line_issue = utils.LineIssue(
        line_number=10,
        issue_type="BANNED_PATTERN",
        line_content="while True:",
        description="Use of 'while True' infinite loop"
    )
    
    code_analysis = utils.CodeAnalysis(
        line_issues=[line_issue],
        comment_count=3,
        long_lines_count=0,
        banned_patterns_count=1,
        multiple_returns_count=0
    )
    
    # Generate report
    report = utils.generate_report("test.py", execution_result, output_validation, code_analysis)
    
    # Check that report contains key information
    assert "Grading Report for test.py" in report
    assert "Script executed successfully" in report
    assert "Found: \"Hello\"" in report
    assert "Missing: \"Missing\"" in report
    assert "Comment count: 3" in report
    assert "Use of 'while True'" in report
    assert "Output Validation: 1/2 checks passed" in report
    assert "Code Analysis: 1 issues found" in report 