import sys
import math

try:
    file_name = sys.argv[1]
except IndexError:
    print("Укажите входной файл в команде (например, python B2.py 1.WCData.txt)")
    sys.exit()
output_file_name = f"{file_name[0]}.WindChillReport.txt"
out_lines = []
chilled_temp_sum = 0

with open(file_name) as file:
    strs = file.readlines()

strs.pop(0)
strs.pop(0)
# убираем бесполезные первые 2 строки

for string in strs:
    string = string.split(" ")
    string[:] = [x for x in string if x != '']   # убираем все пустые элементы из массива
    string[-1].replace("\n", "")                 # и перенос строки из последнего элемента

    temp = int(string[1])
    # string[0] - время, string[2] - скорость ветра;
    # temp введена, чтобы не повторять одну и ту же операцию int() несколько раз

    chilled_temp = 35.74 + 0.6125 * temp + (0.4275 * temp - 35.75) * int(string[2]) ** 0.16
    chilled_temp_sum += chilled_temp
    chilled_temp = round(chilled_temp, 1)

    out_lines.append(f"{string[0]:<8}{chilled_temp:>16}{round(chilled_temp - temp, 1):>16}\n")

avg_chilled_temp = round(chilled_temp_sum / len(out_lines), 1)

with open(output_file_name, 'w') as output:
    output.write(f"{'Time':<8}{'WC temp':>16}{'WC Effect':>16}\n")
    output.write("-" * 40 + "\n")

    output.writelines(out_lines)
    output.write("-" * 40 + "\n")

    output.write(f"\nThe average adjusted temperature, based on {len(out_lines)} observations, " + 
        f"was {avg_chilled_temp}")

print(f"Отчёт для данных из файла {file_name} сохранён в {output_file_name}")