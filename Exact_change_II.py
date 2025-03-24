ef exact_change(user_total):
    dollars = user_total // 100
    user_total %= 100

    quarters = user_total // 25
    user_total %= 25

    dimes = user_total // 10
    user_total %= 10

    nickels = user_total // 5
    user_total %= 5

    pennies = user_total

    return dollars, quarters, dimes, nickels, pennies

if __name__ == '__main__':
    total_change = int(input())
    dollars, quarters, dimes, nickels, pennies = exact_change(total_change)

    if total_change == 0:
        print('no change')
    else:
        if dollars > 0:
            print(f"{dollars} dollar" + ("s" if dollars > 1 else ""))
        if quarters > 0:
            print(f"{quarters} quarter" + ("s" if quarters > 1 else ""))
        if dimes > 0:
            print(f"{dimes} dime" + ("s" if dimes > 1 else ""))
        if nickels > 0:
            print(f"{nickels} nickel" + ("s" if nickels > 1 else ""))
        if pennies > 0:
            print(f"{pennies} penny" + ("ies" if pennies > 1 else ""))
