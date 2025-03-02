#!/usr/bin/env python3
"""
Demo script showing how to use the Python Grader Tool with file-based expected patterns.

This script demonstrates the v0.2.0 feature of reading expected output patterns from a file.
"""

import os
import subprocess
import sys

# Get the absolute path to the project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the student script to grade
STUDENT_SCRIPT = os.path.join(PROJECT_ROOT, "examples", "student_script.py")

# Path to the expected output patterns file
EXPECTED_FILE = os.path.join(PROJECT_ROOT, "examples", "expected_outputs", "sample_patterns.txt")

# Path to the input file
INPUT_FILE = os.path.join(PROJECT_ROOT, "examples", "sample_input.txt")

# Direct input data (alternative to using a file)
DIRECT_INPUT = "Jane Smith"


def run_grader(input_source, use_file=False):
    """Run the grader with the specified input source."""
    # Ensure the student script exists
    if not os.path.exists(STUDENT_SCRIPT):
        print(f"Creating example student script at {STUDENT_SCRIPT}")
        with open(STUDENT_SCRIPT, "w") as f:
            f.write("""#!/usr/bin/env python3
name = input("Enter your name: ")
print(f"Hello, {name}!")
print("Result: 42")
print("Total: 99.99")
""")
    
    # Build the command
    cmd = [
        sys.executable,
        "-m",
        "grader.main",
        "--file", STUDENT_SCRIPT,
        "--input", input_source,
        "--expected-file", EXPECTED_FILE,
        "--timeout", "5"
    ]
    
    # Run the command
    print("\nRunning grader with the following command:")
    print(" ".join(cmd))
    
    if use_file:
        print(f"\nUsing input from file: {input_source}")
        with open(input_source, "r") as f:
            print(f"File contents: {f.read().strip()}")
    else:
        print(f"\nUsing direct input string: {input_source}")
    
    print("\n" + "="*50 + "\n")
    
    subprocess.run(cmd)


def main():
    """Run the grader with different input methods."""
    print("PYTHON GRADER TOOL DEMO")
    print("======================\n")
    print("This demo shows two ways to provide input to the grader:")
    print("1. Using a direct input string")
    print("2. Using a file containing the input")
    print("\nBoth examples use the same expected output patterns file.")
    
    # Demonstrate using direct input string
    print("\n\nMETHOD 1: USING DIRECT INPUT STRING")
    print("----------------------------------")
    run_grader(DIRECT_INPUT)
    
    # Demonstrate using input from file
    print("\n\nMETHOD 2: USING INPUT FROM FILE")
    print("------------------------------")
    run_grader(INPUT_FILE, use_file=True)


if __name__ == "__main__":
    main() 