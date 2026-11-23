import re

text = input("\nВведите текст, который нужно разделить на предложения:\n")
sentences = re.split(r"(?<=[.?!]) ", text)

print("\nПредложения в тексте:")
for sentence in sentences: print(sentence)

print(f"\nПредложений в тексте: {len(sentences)}")