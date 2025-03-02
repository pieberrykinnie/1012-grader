# Sample student script for COMP 1012
# This script asks for the user's name and a number,
# then performs some calculations and displays the results.

def calculate_square(number):
    """Calculate the square of a number."""
    return number ** 2

def calculate_cube(number):
    """Calculate the cube of a number."""
    return number ** 3

def main():
    # Get user input
    name = input("Please enter your name: ")
    
    # Greet the user
    print(f"Hello, {name}!")
    
    try:
        # Get a number from the user
        number_str = input("Please enter a number: ")
        number = float(number_str)
        
        # Calculate and display results
        square = calculate_square(number)
        cube = calculate_cube(number)
        
        print(f"Number entered: {number}")
        print(f"Square: {square}")
        print(f"Cube: {cube}")
        
        # Use a banned pattern for testing
        i = 0
        while True:
            if i >= 5:
                break  # Another banned pattern
            print(f"Loop iteration: {i}")
            i += 1
            
    except ValueError:
        print("Error: Invalid number input.")
    
    print("Thank you for using this program!")

if __name__ == "__main__":
    main() 