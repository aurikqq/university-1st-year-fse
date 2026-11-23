text = input("\nВведите текст со скобками: ")

while ('(' in text and ')' in text):
    left = text.find('(') - 1 # убирает лишний пробел
    right = text.find(')') + 1
    text = text.replace(text[left:right], '')

while ('(' in text):
    text = text.replace('(', '')

while (')' in text):
    text = text.replace(')', '')

print('\nТекст без скобок:' + text)