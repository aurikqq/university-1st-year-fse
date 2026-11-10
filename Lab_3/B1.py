import sys
import math


try:
    file_name = sys.argv[1]
except IndexError:
    print("Укажите входной файл в команде (например, python B1.py 1.ChaseData.txt)")
    sys.exit()

with open(file_name) as file:
    strs = file.readlines()

size = list(map(lambda x: int(x.replace('\n', '')), strs[0].strip().split("   ")))
m_pos = [0, 0]
c_pos = [0, 0]
m_dist = 0 
c_dist = 0
is_caught = False


def mouse_turn():
    global m_dist, m_pos

    if m_pos != [0, 0]:
        m_dist += abs(int(string[1])) + abs(int(string[2]))

    m_pos[0] += int(string[1])
    m_pos[1] += int(string[2])

    while m_pos[0] < 1:
        m_pos[0] = size[0] - abs(m_pos[0])

    while m_pos[0] > size[0]:
        m_pos[0] -= size[0]

    while m_pos[1] < 1:
        m_pos[1] = size[1] - abs(m_pos[1])

    while m_pos[1] > size[1]:
        m_pos[1] -= size[1]

def cat_turn():
    global c_dist, c_pos

    if c_pos != [0, 0]:
        c_dist += abs(int(string[1])) + abs(int(string[2]))

    c_pos[0] += int(string[1])
    c_pos[1] += int(string[2])

    while c_pos[0] < 1:
        c_pos[0] = size[0] - abs(c_pos[0])

    while c_pos[0] > size[0]:
        c_pos[0] -= size[0]

    while c_pos[1] < 1:
        c_pos[1] = size[1] - abs(c_pos[1])

    while c_pos[1] > size[1]:
        c_pos[1] -= size[1]

def fmt_pos(pos):
    x = f"{pos[0]:>2}" if pos[0] != 0 else " ?"
    y = f"{pos[1]:>2}" if pos[1] != 0 else " ?"
    return f"({x},{y})"


print("\ngitCat and Mouse\n")
print(f"{'Cat':^10}{'Mouse':^10}{'Distance':^10}")
print("-" * 30)

for string in strs:
    string = string.split()
    string[-1].replace('\n', '')
    
    match string[0]:
        case "M":
            mouse_turn()
        case "C":
            cat_turn()
        case "P":
            cat_str = fmt_pos(c_pos)
            mouse_str = fmt_pos(m_pos)

            if c_pos != (0, 0):  # или другое условие "кот уже знает позицию"
                dist = abs(m_pos[0] - c_pos[0]) + abs(m_pos[1] - c_pos[1])
                dist_str = str(dist)
            else:
                dist_str = ""

            print(f"{cat_str:<12}{mouse_str:<12}{dist_str}")
    
    if m_pos == c_pos and m_pos != [0, 0]:
        is_caught = True
        break

print("-" * 30)
print()
print(f"{'Distance':<10}{'Mouse':^10}{'Cat':^10}")
print(f"{'':<10}{m_dist:^10}{c_dist:^10}\n")
print("Mouse escaped Cat" if is_caught else "Mouse evaded Cat")