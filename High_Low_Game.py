import random

# 1. Get Player Name and Display Welcome Message
player_name = input("Enter your name: ")
print(f"Welcome to the higher/lower game, {player_name}!")

# 2. Generate Random Number between 1 and 100
secret_number = random.randint(1, 100)

# 3. Start Guessing Loop
while True:
    try:
        player_number = int(input("Enter a Number Between 1 and 100: "))

        if player_number < secret_number:
            print("Too low! Try again.")
        elif player_number > secret_number:
            print("Too high! Try again.")
        else:
            print(f"You got it, {player_name}! The secret number was {secret_number}.")
            break

    except ValueError:
        print("Invalid input. Please enter a whole number.")