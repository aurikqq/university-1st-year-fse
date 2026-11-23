words = input("\nВведите текст: ").split()
abbreviation = ""

for word in words:
    if len(word) >= 3:
        abbreviation += word[0].upper()

print(f"\nАббревиатура из текста: {abbreviation}")