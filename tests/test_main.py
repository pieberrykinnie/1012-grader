"""Tests for the main CLI interface of the grader tool."""

import os
import tempfile
import pytest
from click.testing import CliRunner

from grader.main import main


def create_temp_script(content: str) -> str:
    """Create a temporary Python script file for testing."""
    fd, path = tempfile.mkstemp(suffix=".py")
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        return path
    except Exception:
        os.unlink(path)
        raise


def create_temp_input_file(content: str) -> str:
    """Create a temporary input file for testing."""
    fd, path = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        return path
    except Exception:
        os.unlink(path)
        raise


def test_main_with_valid_inputs():
    """Test the main CLI with valid inputs."""
    script_content = 'print("Hello, World!")'
    script_path = create_temp_script(script_content)
    
    runner = CliRunner()
    
    try:
        result = runner.invoke(main, [
            '--file', script_path,
            '--input', 'test_input',
            '--expected', 'Hello'
        ])
        
        assert result.exit_code == 0
        assert "Executing" in result.output
        assert "Grading Report" in result.output
        assert "Found: \"Hello\"" in result.output
    finally:
        os.unlink(script_path)


def test_main_with_input_file():
    """Test the main CLI using an input file."""
    script_content = 'name = input("Name: "); print(f"Hello, {name}!")'
    script_path = create_temp_script(script_content)
    
    input_content = "John Doe"
    input_path = create_temp_input_file(input_content)
    
    runner = CliRunner()
    
    try:
        result = runner.invoke(main, [
            '--file', script_path,
            '--input', input_path,
            '--expected', 'Hello, John Doe!'
        ])
        
        assert result.exit_code == 0
        assert "Executing" in result.output
        assert "Found: \"Hello, John Doe!\"" in result.output
    finally:
        os.unlink(script_path)
        os.unlink(input_path)


def test_main_with_missing_expected_pattern():
    """Test the main CLI when an expected pattern is missing."""
    script_content = 'print("Hello, World!")'
    script_path = create_temp_script(script_content)
    
    runner = CliRunner()
    
    try:
        result = runner.invoke(main, [
            '--file', script_path,
            '--input', 'test_input',
            '--expected', 'Missing Pattern'
        ])
        
        assert result.exit_code == 0  # The script executes successfully, even though the pattern is missing
        assert "Executing" in result.output
        assert "Missing: \"Missing Pattern\"" in result.output
        assert "Output Validation: 0/1 checks passed" in result.output
    finally:
        os.unlink(script_path)


def test_main_with_multiple_expected_patterns():
    """Test the main CLI with multiple expected patterns."""
    script_content = 'print("First Line\\nSecond Line\\nThird Line")'
    script_path = create_temp_script(script_content)
    
    runner = CliRunner()
    
    try:
        result = runner.invoke(main, [
            '--file', script_path,
            '--input', 'test_input',
            '--expected', 'First',
            '--expected', 'Second',
            '--expected', 'Missing'
        ])
        
        assert result.exit_code == 0
        assert "Found: \"First\"" in result.output
        assert "Found: \"Second\"" in result.output
        assert "Missing: \"Missing\"" in result.output
        assert "Output Validation: 2/3 checks passed" in result.output
    finally:
        os.unlink(script_path)


def test_main_with_timeout():
    """Test the main CLI with a script that times out."""
    script_content = 'import time; time.sleep(2)'
    script_path = create_temp_script(script_content)
    
    runner = CliRunner()
    
    try:
        result = runner.invoke(main, [
            '--file', script_path,
            '--input', 'test_input',
            '--expected', 'anything',
            '--timeout', '1'
        ])
        
        assert result.exit_code == 1  # Should exit with error code
        assert "timed out" in result.output
    finally:
        os.unlink(script_path)


def test_main_with_output_file():
    """Test the main CLI with output file saving."""
    script_content = 'print("Hello, World!")'
    script_path = create_temp_script(script_content)
    
    fd, output_path = tempfile.mkstemp(suffix=".txt")
    os.close(fd)  # Close the file descriptor
    
    runner = CliRunner()
    
    try:
        result = runner.invoke(main, [
            '--file', script_path,
            '--input', 'test_input',
            '--expected', 'Hello',
            '--output-file', output_path
        ])
        
        assert result.exit_code == 0
        assert "Report saved to" in result.output
        
        # Check that the file was created and contains the report
        with open(output_path, 'r') as f:
            report_content = f.read()
            assert "Grading Report for" in report_content
            assert "Found: \"Hello\"" in report_content
    finally:
        os.unlink(script_path)
        os.unlink(output_path) 