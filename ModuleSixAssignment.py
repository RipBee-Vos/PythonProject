#James Grant

rooms = {
    'Elevator': {'West': 'Hallway'},
    'Hallway': {'West': 'Courtyard', 'East': 'Elevator', 'North': 'Research Lab'},
    'Courtyard': {'West': 'Medical Bay', 'East': 'Hallway', 'North': 'Armory', 'South': 'Security'},
    'Medical Bay': {'North': 'Server Room', 'East': 'Courtyard'},
    'Server Room': {'East': 'Armory', 'South': 'Medical Bay'},
    'Armory': {'West': 'Server Room', 'East': 'Research Lab', 'South': 'Courtyard'},
    'Research Lab': {'West': 'Armory', 'East': 'Storage Closet', 'South': 'Hallway'},
    'Storage Closet': {'West': 'Research Lab'},
    'Security': {'North': 'Courtyard', 'East': 'Command Hub', 'South': 'Core Access Hall'},
    'Command Hub': {'West': 'Security'},
    'Core Access Hall': {'North': 'Security', 'West': 'Engineering Bay', 'South': 'ECHELON Core'},
    'Engineering Bay': {'East': 'Core Access Hall'},
    'ECHELON Core': {'North': 'Core Access Hall'}
}

current_room = 'Elevator'

while current_room != 'exit':
    print("You are in the", current_room)

    move = input("Enter a direction (North, South, East, West) or type 'exit' to quit: ")

    if move.lower() == 'exit':
        print("Simulation Terminated")
        current_room = 'exit'

    else:
        print("You can't go that way. Try a different direction.")

