import os
import sys


def decode(sequence):
    result = ""
    count = ""
    for symbol in sequence:
        if symbol.isdigit():
            count += symbol
        elif count:
            result += symbol * int(count)
            count = ""
        else:
            result += symbol

    if count:
        raise ValueError("После числа в RLE-последовательности должна быть буква")
    return result


try:
    commands_file = sys.argv[1]
    sequences_file = sys.argv[2]
except IndexError:
    print("Укажите входные файлы в команде "
          "(например, python A4.py data/commands.0.txt data/sequences.0.txt)")
    sys.exit()

folder = os.path.dirname(os.path.realpath(__file__))

proteins = []
by_name = {}
with open(os.path.join(folder, sequences_file), encoding="utf-8-sig") as file:
    for line in file:
        if not line.strip():
            continue

        name, organism, sequence = line.rstrip("\n").split("\t")
        sequence = decode(sequence)
        proteins.append((name, organism, sequence))
        by_name[name] = sequence

separator = "-" * 74
out_lines = ["Artyom Astahov", "Genetic Searching", separator]
number = 0

with open(os.path.join(folder, commands_file), encoding="utf-8-sig") as file:
    for line in file:
        if not line.strip():
            continue

        command = line.rstrip("\n").split("\t")
        operation = command[0]
        number += 1

        if operation == "search":
            command[1] = decode(command[1])

        out_lines.append(f"{number:03d}   " + "   ".join(command))

        if operation == "search":
            out_lines.append("organism                 protein")
            found = False

            for name, organism, sequence in proteins:
                if command[1] in sequence:
                    out_lines.append(f"{organism}     {name}")
                    found = True

            if not found:
                out_lines.append("NOT FOUND")

        elif operation == "diff":
            out_lines.append("amino-acids difference:")
            first_name = command[1]
            second_name = command[2]
            missing = []

            for name in (first_name, second_name):
                if name not in by_name:
                    missing.append(name)

            if missing:
                out_lines.append("MISSING: " + ", ".join(missing))
            else:
                first = by_name[first_name]
                second = by_name[second_name]

                # Лишние буквы в конце длинной цепочки тоже считаем различиями.
                differences = abs(len(first) - len(second))
                for i in range(min(len(first), len(second))):
                    if first[i] != second[i]:
                        differences += 1
                out_lines.append(str(differences))

        elif operation == "mode":
            out_lines.append("amino-acid occurs:")
            name = command[1]

            if name not in by_name:
                out_lines.append("MISSING: " + name)
            else:
                counts = {}
                for symbol in by_name[name]:
                    if symbol not in counts:
                        counts[symbol] = 0
                    counts[symbol] += 1

                best = ""
                best_count = 0
                for symbol in counts:
                    count = counts[symbol]
                    if count > best_count or (count == best_count and symbol < best):
                        best = symbol
                        best_count = count

                out_lines.append(f"{best}          {best_count}")

        else:
            raise ValueError(f"Неизвестная операция: {operation}")

        out_lines.append(separator)

with open(os.path.join(folder, "data", f"genedata.{number}.txt"), "w", encoding="utf-8") as file:
    file.write("\n".join(out_lines) + "\n")

print(f"Результат записан в genedata.{number}.txt")
