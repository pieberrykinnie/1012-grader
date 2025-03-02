# Python Grader Tool

A lightweight command-line tool designed to assist in grading Python programming assignments for COMP 1012: Computer Programming for Scientists and Engineers.

## Features

- **Script Execution**: Run student Python scripts with predefined inputs
- **Output Validation**: Check if the script's output contains expected strings or matches regex patterns
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
# Basic usage
python -m grader.main --file student_script.py --input "input_data" --expected "Expected output"

# Using an input file
python -m grader.main --file student_script.py --input input_file.txt --expected "Expected output"

# Multiple expected outputs
python -m grader.main --file student_script.py --input "input_data" --expected "Pattern 1" --expected "Pattern 2"

# Specifying timeout and saving the report
python -m grader.main --file student_script.py --input "input_data" --expected "Expected output" --timeout 10 --output-file report.txt
```

### Command-line Options

- `--file`, `-f`: Path to the student's Python script (required)
- `--input`, `-i`: Input data for the script - either a string or a file path (required)
- `--expected`, `-e`: Expected output snippets or regex patterns (required, can be specified multiple times)
- `--timeout`, `-t`: Timeout in seconds for script execution (default: 5)
- `--output-file`, `-o`: Optional file path to save the grading report

## Example

### Student Script (student_script.py)

```python
name = input("Please enter your name: ")
print(f"Hello, {name}!")
print("Your result is: 42")
```

### Grading Command

```bash
python -m grader.main --file student_script.py --input "John Doe" --expected "Hello, John Doe!" --expected "Your result is: \d+"
```

### Expected Output

```
Executing: student_script.py

Grading Report:
----------------------------------------
Execution:
[✓] Script executed successfully

Output Validation:
[✓] Found: "Hello, John Doe!"
[✓] Found: "Your result is: \d+"

Code Analysis:
[i] Comment count: 0

Summary:
- Output Validation: 2/2 checks passed
- Code Analysis: 0 issues found
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 