total_change = int(input())
def get_change(amount):
    if amount <= 0:
        print('No change')
        return

    coins = [(100, "Dollar"), (25, "Quarter"), (10, "Dime"), (5, "Nickel"), (1, "Penny")]

    for value, name in coins:
        count = amount // value
        if count > 0:
            print(f"{count} {name if count == 1 else name + 's'}")
            amount %= value

get_change(total_change)