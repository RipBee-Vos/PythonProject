def generate_passwords():
    # Get user input
    favorite_color = input().strip()
    pet_name = input().strip()
    number = input().strip()

    # Output entered values
    print(f"You entered: {favorite_color} {pet_name} {number}")

    # Generate passwords
    first_password = f"{favorite_color}_{pet_name}"
    second_password = f"{number}{favorite_color}{number}"

    # Output passwords
    print(f"\nFirst password: {first_password}")
    print(f"Second password: {second_password}")

    # Output password lengths
    print(f"\nNumber of characters in {first_password}: {len(first_password)}")
    print(f"Number of characters in {second_password}: {len(second_password)}")


# Run the function
generate_passwords()
