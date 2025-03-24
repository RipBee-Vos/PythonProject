def count_characters(text: str) -> int:
    excluded_characters = {',', '.', ' '}
    return sum(1 for c in text if c not in excluded_characters)

user_text = input('Enter line of text: ')
print(count_characters(user_text))
