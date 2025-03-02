#!/usr/bin/env python3
"""
Main entry point for the Python Grader Tool.

This module handles the command-line interface, validates inputs,
and orchestrates the execution of the student script, output validation,
and code analysis.
"""

import os
import sys
import click
from typing import List, Optional

from . import utils


@click.command()
@click.option(
    "--file", "-f",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="Path to the student's Python script to grade."
)
@click.option(
    "--input", "-i",
    required=True,
    type=str,
    help="Input data for the script. Can be a file path or inline string."
)
@click.option(
    "--expected", "-e",
    required=True,
    multiple=True,
    help="Expected output snippets or regex patterns. Can be specified multiple times."
)
@click.option(
    "--timeout", "-t",
    default=5,
    type=int,
    help="Timeout in seconds for script execution. Default is 5 seconds."
)
@click.option(
    "--output-file", "-o",
    type=click.Path(file_okay=True, dir_okay=False, writable=True),
    help="Optional file path to save the grading report."
)
def main(file: str, input: str, expected: List[str], timeout: int, output_file: Optional[str]) -> None:
    """
    Execute the grading process for a student's Python script.
    
    This tool executes a Python script with the provided input, validates
    its output against expected snippets, analyzes the code for adherence to
    programming standards, and generates a comprehensive grading report.
    """
    # Validate inputs
    if not os.path.isfile(file):
        click.echo(f"Error: The file '{file}' does not exist or is not accessible.")
        sys.exit(1)
    
    if not expected:
        click.echo("Error: At least one expected output snippet must be provided.")
        sys.exit(1)
    
    input_data = input
    # Check if input is a file path
    if os.path.isfile(input):
        try:
            with open(input, 'r') as f:
                input_data = f.read()
        except Exception as e:
            click.echo(f"Error reading input file: {e}")
            sys.exit(1)
    
    # Execute the student's script and capture output
    click.echo(f"Executing: {file}")
    execution_result = utils.execute_script(file, input_data, timeout)
    
    # Validate output against expected snippets
    output_validation = utils.validate_output(execution_result.stdout, expected)
    
    # Analyze the code
    code_analysis = utils.analyze_code(file)
    
    # Generate and display the report
    report = utils.generate_report(
        file, 
        execution_result, 
        output_validation, 
        code_analysis
    )
    
    click.echo("\nGrading Report:")
    click.echo("-" * 40)
    click.echo(report)
    
    # Save report to file if requested
    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write(report)
            click.echo(f"\nReport saved to: {output_file}")
        except Exception as e:
            click.echo(f"Error saving report to file: {e}")
    
    # Return exit code based on execution success/failure
    if execution_result.error:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter 