from datetime import date

name = input("What is your name?: ")
age = int(input("How old are you?: "))
current_yr = date.today().year

print(f"Hello {name}! You were born in {current_yr-age}.")



