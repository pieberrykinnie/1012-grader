# Python Grader Tool

A lightweight command-line tool designed to assist in grading Python programming assignments for COMP 1012: Computer Programming for Scientists and Engineers.

## Features

- **Script Execution**: Run student Python scripts with predefined inputs
- **Output Validation**: Check if the script's output contains expected strings or patterns read from a file
- **Code Analysis**: Analyze code for adherence to programming standards:
  - Count comments
  - Check for lines exceeding 100 words
  - Detect banned patterns (e.g., `break`, `continue`, `while True`)
  - Find functions with multiple return statements
- **Comprehensive Reporting**: Generate detailed reports on execution results, output validation, and code analysis

## Installation

### Prerequisites

- Python 3.6 or higher

### Using pip

```bash
# Clone the repository
git clone https://github.com/pieberrykinnie/1012-grader.git
cd 1012-grader

# Create and activate a virtual environment (optional but recommended)
python -m venv venv       # or python3, depending on your OS
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install the package
pip install -e .
```

## Usage

```bash
# Basic usage with expected output patterns file
python -m grader.main --file student_script.py --input "input_data" --expected-file patterns.txt

# Using an input file
python -m grader.main --file student_script.py --input input_file.txt --expected-file patterns.txt

# Specifying timeout and saving the report
python -m grader.main --file student_script.py --input "input_data" --expected-file patterns.txt --timeout 10 --output-file report.txt
```

### Command-line Options

- `--file`, `-f`: Path to the student's Python script (required)
- `--input`, `-i`: Input data for the script - either a string or a file path (required)
- `--expected-file`: Path to a file containing expected output patterns, one per line (required)
- `--timeout`, `-t`: Timeout in seconds for script execution (default: 5)
- `--output-file`, `-o`: Optional file path to save the grading report

### Expected Patterns File Format

The expected patterns file should contain one pattern per line. Empty lines and lines starting with `#` (comments) are ignored. For example:

```
# This is a comment and will be ignored
Hello, .+!

# Another comment
Your result is: \d+
```

## Example

### Student Script (student_script.py)

```python
name = input("Please enter your name: ")
print(f"Hello, {name}!")
print("Your result is: 42")
```

### Expected Patterns File (patterns.txt)

```
Hello, .+!
Your result is: \d+
```

### Grading Command

```bash
python -m grader.main --file student_script.py --input "John Doe" --expected-file patterns.txt
```

### Expected Output

```
Executing: student_script.py

Grading Report:
----------------------------------------
Execution:
[✓] Script executed successfully

Output Validation:
[✓] Found: "Hello, .+!"
[✓] Found: "Your result is: \d+"

Code Analysis:
[i] Comment count: 0

Summary:
- Output Validation: 2/2 checks passed
- Code Analysis: 0 issues found
```

## Changelog

### v0.2.0

- **Major Change**: Replaced multiple `--expected` command-line arguments with a single `--expected-file` option
- Now reads expected output patterns from a file with one pattern per line
- Empty lines and lines starting with `#` (comments) in the patterns file are ignored
- Improved user experience when working with multiple patterns
- Updated documentation and examples

### v0.1.0

- Initial release
- Basic functionality for script execution, output validation, and code analysis
- Command-line interface using multiple `--expected` options for patterns

## License

This project is licensed under the MIT License - see the LICENSE file for details. 