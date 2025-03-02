# Python Grader Tool - User Instructions

The Python Grader Tool is designed to help grade Python programming assignments for COMP 1012: Computer Programming for Scientists and Engineers. This document provides instructions on how to use the tool effectively.

## Installation

Before using the tool, you need to install it on your system.

### Prerequisites

- Python 3.6 or higher

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/pieberrykinnie/1012-grader.git
   cd 1012-grader
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv       # or python3, depending on your OS
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the package:
   ```bash
   pip install -e .
   ```

## Basic Usage

The tool provides a command-line interface to grade Python scripts. Here's the basic syntax:

```bash
1012-grader --file SCRIPT_PATH --input INPUT_DATA_OR_FILE --expected-file PATTERNS_FILE
```

Or alternatively:

```bash
python -m grader.main --file SCRIPT_PATH --input INPUT_DATA_OR_FILE --expected-file PATTERNS_FILE
```

### Required Arguments

- `--file` or `-f`: Path to the student's Python script.
- `--input` or `-i`: Input data for the script. This can be:
  - A direct string (e.g., `--input "John Doe"`)
  - A path to a file containing input data (the tool will detect if the path exists)
- `--expected-file`: Path to a file containing expected output patterns, with one pattern per line.

### Optional Arguments

- `--timeout` or `-t`: Timeout in seconds for script execution (default: 5).
- `--output-file` or `-o`: Path to save the grading report as a file.

## Expected Patterns File Format

The expected patterns file should contain one pattern per line. Empty lines and lines starting with `#` (comments) are ignored. For example:

```
# This is a comment
Hello, .+!
Result: \d+

# Another comment
Total: \d+\.\d{2}
```

Each non-comment line is treated as a separate pattern to search for in the script's output.

## Examples

### Example 1: Basic Usage

Create a file `patterns.txt` with the following content:
```
Hello, John Doe!
Result: [0-9]+
```

Then run:
```bash
1012-grader --file student_script.py --input "John Doe" --expected-file patterns.txt
```

This runs `student_script.py` with the input "John Doe" and checks if the output contains:
1. The exact string "Hello, John Doe!"
2. A pattern matching "Result:" followed by one or more digits.

### Example 2: Using an Input File

Create a file `input.txt` with one or more lines of input:
```
John Doe
42
```

Create a file `patterns.txt` with the patterns:
```
Hello, John Doe!
Result: 42
```

Then run:
```bash
1012-grader --file student_script.py --input input.txt --expected-file patterns.txt
```

### Example 3: Saving the Report

```bash
1012-grader --file student_script.py --input "John Doe" --expected-file patterns.txt --output-file report.txt
```

This runs the grader and saves the report to `report.txt`.

## Understanding the Report

The grading report includes several sections:

### Execution

Shows whether the script executed successfully or encountered errors.

### Output Validation

Lists each expected pattern and whether it was found or missing in the output.

### Code Analysis

Provides information about the code, including:
- Comment count
- Lines exceeding 100 words
- Banned patterns such as "break", "continue", "while True"
- Functions with multiple return statements

### Summary

A concise summary of the output validation and code analysis results.

## Tips for Effective Grading

1. **Regex Patterns**: Use regex patterns to allow for flexibility in output checking. For example, `"Result: [0-9]+"` matches "Result: " followed by any number.

2. **Multi-line Input**: When using a file for input, each line in the file corresponds to one input() call in the student's script.

3. **Timing Out**: Set appropriate timeouts based on the expected runtime of the script. Complex calculations might need a longer timeout.

4. **Saving Reports**: Save reports to files for record-keeping and to share feedback with students.

5. **Using Comments**: Add comments in your patterns file to document what each pattern is checking for, making the file more maintainable.

## Troubleshooting

If you encounter any issues with the tool, try the following:

1. Ensure your Python version is 3.6 or higher.
2. Check that the student's script exists and is readable.
3. Verify that input files and expected pattern files are correctly formatted.
4. For regex pattern issues, test your patterns separately with a tool like regex101.com.
5. Make sure your patterns file contains at least one non-empty, non-comment line. 