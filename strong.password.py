word = input()

replacements = {
     'i': '!',
     'a': '@',
     'm': 'M',
     'B': '8',
     'o': '.'
}
strong_password = ''

for char in word:

    if char in replacements:

        strong_password += replacements[char]

    else:
        strong_password += char

strong_password += 'q*s'

print(strong_password)
