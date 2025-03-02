"""Tests for the main module of the Python Grader Tool."""

import os
import tempfile

from click.testing import CliRunner

from grader.main import main


def create_temp_script(content: str) -> str:
    """Create a temporary Python script file for testing."""
    fd, path = tempfile.mkstemp(suffix=".py")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(content)
        return path
    except Exception:
        os.unlink(path)
        raise


def create_temp_input_file(content: str) -> str:
    """Create a temporary input file for testing."""
    fd, path = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(content)
        return path
    except Exception:
        os.unlink(path)
        raise


def create_temp_expected_file(patterns: list) -> str:
    """Create a temporary file with expected output patterns."""
    fd, path = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, "w") as f:
            for pattern in patterns:
                f.write(f"{pattern}\n")
        return path
    except Exception:
        os.unlink(path)
        raise


def test_main_with_valid_inputs():
    """Test the main CLI with valid inputs."""
    script_content = 'print("Hello, World!")'
    script_path = create_temp_script(script_content)

    expected_path = create_temp_expected_file(["Hello"])

    runner = CliRunner()

    try:
        result = runner.invoke(
            main,
            [
                "--file",
                script_path,
                "--input",
                "test_input",
                "--expected-file",
                expected_path,
            ],
        )

        assert result.exit_code == 0
        assert "Executing" in result.output
        assert "Grading Report" in result.output
        assert 'Found: "Hello"' in result.output
    finally:
        os.unlink(script_path)
        os.unlink(expected_path)


def test_main_with_input_file():
    """Test the main CLI using an input file."""
    script_content = 'name = input("Name: "); print(f"Hello, {name}!")'
    script_path = create_temp_script(script_content)

    input_content = "John Doe"
    input_path = create_temp_input_file(input_content)

    expected_path = create_temp_expected_file(["Hello, John Doe!"])

    runner = CliRunner()

    try:
        result = runner.invoke(
            main,
            [
                "--file",
                script_path,
                "--input",
                input_path,
                "--expected-file",
                expected_path,
            ],
        )

        assert result.exit_code == 0
        assert "Executing" in result.output
        assert 'Found: "Hello, John Doe!"' in result.output
    finally:
        os.unlink(script_path)
        os.unlink(input_path)
        os.unlink(expected_path)


def test_main_with_missing_expected_pattern():
    """Test the main CLI when an expected pattern is missing."""
    script_content = 'print("Hello, World!")'
    script_path = create_temp_script(script_content)

    expected_path = create_temp_expected_file(["Missing Pattern"])

    runner = CliRunner()

    try:
        result = runner.invoke(
            main,
            [
                "--file",
                script_path,
                "--input",
                "test_input",
                "--expected-file",
                expected_path,
            ],
        )

        assert (
            result.exit_code == 0
        )  # The script executes successfully, even though the pattern is missing
        assert "Executing" in result.output
        assert 'Missing: "Missing Pattern"' in result.output
        assert "Output Validation: 0/1 checks passed" in result.output
    finally:
        os.unlink(script_path)
        os.unlink(expected_path)


def test_main_with_multiple_expected_patterns():
    """Test the main CLI with multiple expected patterns."""
    script_content = 'print("First Line\\nSecond Line\\nThird Line")'
    script_path = create_temp_script(script_content)

    expected_path = create_temp_expected_file(["First", "Second", "Missing"])

    runner = CliRunner()

    try:
        result = runner.invoke(
            main,
            [
                "--file",
                script_path,
                "--input",
                "test_input",
                "--expected-file",
                expected_path,
            ],
        )

        assert result.exit_code == 0
        assert 'Found: "First"' in result.output
        assert 'Found: "Second"' in result.output
        assert 'Missing: "Missing"' in result.output
        assert "Output Validation: 2/3 checks passed" in result.output
    finally:
        os.unlink(script_path)
        os.unlink(expected_path)


def test_main_with_timeout():
    """Test the main CLI with a script that exceeds the timeout."""
    script_content = "import time; time.sleep(2)"
    script_path = create_temp_script(script_content)

    expected_path = create_temp_expected_file(["Some pattern"])

    runner = CliRunner()

    try:
        result = runner.invoke(
            main,
            [
                "--file",
                script_path,
                "--input",
                "test_input",
                "--expected-file",
                expected_path,
                "--timeout",
                "1",
            ],
        )

        assert result.exit_code != 0  # Non-zero exit code due to timeout
        assert "timed out" in result.output.lower()
    finally:
        os.unlink(script_path)
        os.unlink(expected_path)


def test_main_with_output_file():
    """Test the main CLI with output file saving."""
    script_content = 'print("Hello, World!")'
    script_path = create_temp_script(script_content)

    expected_path = create_temp_expected_file(["Hello"])
    output_path = tempfile.mktemp(suffix=".txt")

    runner = CliRunner()

    try:
        result = runner.invoke(
            main,
            [
                "--file",
                script_path,
                "--input",
                "test_input",
                "--expected-file",
                expected_path,
                "--output-file",
                output_path,
            ],
        )

        assert result.exit_code == 0
        assert "Report saved to" in result.output
        assert os.path.exists(output_path)

        with open(output_path, "r") as f:
            report_content = f.read()
            assert "Grading Report" in report_content
            assert 'Found: "Hello"' in report_content
    finally:
        os.unlink(script_path)
        os.unlink(expected_path)
        if os.path.exists(output_path):
            os.unlink(output_path)


def test_main_with_non_existent_file():
    """Test the main CLI with a non-existent Python file."""
    runner = CliRunner()

    expected_path = create_temp_expected_file(["Hello"])

    try:
        result = runner.invoke(
            main,
            [
                "--file",
                "non_existent_file.py",
                "--input",
                "test_input",
                "--expected-file",
                expected_path,
            ],
        )

        assert result.exit_code != 0
        assert "does not exist" in result.output
    finally:
        os.unlink(expected_path)


def test_main_with_non_existent_expected_file():
    """Test the main CLI with a non-existent expected output file."""
    script_content = 'print("Hello, World!")'
    script_path = create_temp_script(script_content)

    runner = CliRunner()

    try:
        result = runner.invoke(
            main,
            [
                "--file",
                script_path,
                "--input",
                "test_input",
                "--expected-file",
                "non_existent_file.txt",
            ],
        )

        assert result.exit_code != 0
        assert "file 'non_existent_file.txt' does not exist" in result.output.lower()
    finally:
        os.unlink(script_path)
