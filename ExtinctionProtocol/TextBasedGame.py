# James Grant - Module Six Milestone

rooms = {
    'Server Room': {'East': 'Armory', 'South': 'Medical Bay'},
    'Armory': {'West': 'Server Room', 'East': 'Research Lab', 'South': 'Courtyard'},
    'Research Lab': {'West': 'Armory', 'East': 'Storage Closet', 'South': 'Hallway'},
    'Storage Closet': {'West': 'Research Lab'},
    'Medical Bay': {'North': 'Server Room', 'East': 'Courtyard'},
    'Courtyard': {'West': 'Medical Bay', 'East': 'Hallway', 'North': 'Armory', 'South': 'Security'},
    'Hallway': {'West': 'Courtyard', 'East': 'Elevator', 'North': 'Research Lab'},
    'Elevator': {'West': 'Hallway'},
    'Security': {'North': 'Courtyard', 'East': 'Command Hub', 'South': 'Core Access Hall'},
    'Command Hub': {'West': 'Security'},
    'Core Access Hall': {'North': 'Security', 'West': 'Engineering Bay', 'South': 'ECHELON Core'},
    'Engineering Bay': {'East': 'Core Access Hall'},
    'ECHELON Core': {'North': 'Core Access Hall'}
}

# Start the player in the Server Room
current_room = 'Server Room'

# Loop runs until the player types 'exit'
while current_room != 'exit':
    # Show the player where they are
    print("You are in the", current_room)

    # Ask the player what to do next
    move = input("Enter a direction (North, South, East, West) or type 'exit' to quit: ")

    # If the player wants to quit
    if move.lower() == 'exit':
        print("Thanks for playing!")
        current_room = 'exit'

    # Capitalize first letter so it matches keys in the dictionary
    elif move.capitalize() in rooms[current_room]:
        # Move to the new room
        current_room = rooms[current_room][move.capitalize()]

    # If the direction isn't valid from this room
    else:
        print("You can't go that way. Try a different direction.")


