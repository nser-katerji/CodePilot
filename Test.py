def find_multiples_in_range(number, start, end):
    """Finds all multiples of 'number' in a given range [start, end]."""
    return [i for i in range(start, end + 1) if i % number == 0]

# Example usage: find multiples of 5 between 10 and 30
num = int(input("Enter a number: "))
start = int(input("Enter start of range: "))
end = int(input("Enter end of range: "))
print(f"Multiples of {num} between {start} and {end}: {find_multiples_in_range(num, start, end)}")