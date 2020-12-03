def runlenght(input):
    prev_b = 2  # Will store the previous byte of message. Equal 2 to always be different as first byte
    output = []  # Will store the final output
    count = 0  # Count the consecutive bytes

    for b in input:
        if b != prev_b:                 # When byte does not coincide with previous one (include the first)
            if count:                   # Omit the step if we re at the first byte
                output.append(count)    # Write how many zeros or ones
                output.append(prev_b)   # Write if it is a zero or one
            prev_b = b                  # Set the new previous byte to be compared
            count = 1                   # Reset counter
        elif b == prev_b:               # When byte coincide with previous one
            count += 1                  # Increase one the counter
    output.append(count)                # Since the loop reaches the last byte we need to repeat
    output.append(prev_b)               # the  write steps for the last set
    return output


def main():
    while True:
        data = input("Input a sequence of bytes separated by space: ").split()  # store the user input
        print(runlenght(data))  # Print output function


main()
