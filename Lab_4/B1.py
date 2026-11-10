import math
import sys

MONTH_DAYS = {
    "January": 31, "February": 28, "March": 31, "April": 30,
    "May": 31, "June": 30, "July": 31, "August": 31,
    "September": 30, "October": 31, "November": 30, "December": 31,
}


def days_in_month(month, year):
    if month == "February" and year % 4 == 0:
        return 29
    return MONTH_DAYS[month]


if len(sys.argv) == 3:
    in_filename, out_filename = sys.argv[1], sys.argv[2]
elif len(sys.argv) == 1:
    in_filename, out_filename = "Precip.txt", "Report.txt"
else:
    print("Использование: python B1.py [Precip.txt Report.txt]")
    sys.exit(1)

with open(in_filename) as f:
    data = [line.strip() for line in f.readlines()]

station = data[1]
month, year_str = data[2].split(', ')
year = int(year_str)
total_days = days_in_month(month, year)

entries = data[3:]

precip = {}
errors = []
line_no = 4   # нумерация строк файла начинается с 4-й (данные)

for entry in entries:
    values = entry.split()
    day_str = values[0]
    day = int(day_str)
    amount = float(values[1])

    if day < 1 or day > total_days:
        errors.append(("Invalid", day_str, line_no))
    elif day_str in precip:
        errors.append(("Repeated", day_str, line_no))
    else:
        precip[day_str] = amount

    line_no += 1

with open(out_filename, 'w') as report:
    report.write("Programmer: Artyom Astahov\n")
    report.write("CS 1044 Project 5 Fall 2008\n")
    report.write("\n")
    report.write(f"Precipitation report for {station} during {month}, {year}\n")
    report.write("\n")

    report.write(f"{'Error':<14}{'Day':>3}{'Line':>11}\n")
    for err_type, day_str, line in errors:
        report.write(f"{err_type:<14}{day_str:>3}{line:>11}\n")
    report.write("\n")

    report.write("Day Amount Graph\n")
    for day in range(1, total_days + 1):
        day_str = str(day)
        if day_str not in precip:
            report.write(f"{day:>3}{'NA':>7}\n")
        else:
            amount = precip[day_str]
            stars = '*' * math.ceil(amount / 0.25)
            report.write(f"{day:>3}{amount:>7.2f} {stars}\n")
    report.write("\n")
    
    report.write(f"{'Minimum':<12}{'Maximum':<12}{'Average'}\n")
    if precip:
        minimum = min(precip.values())
        maximum = max(precip.values())
        average = sum(precip.values()) / total_days
        report.write(f"{minimum:>7.2f}{maximum:>12.2f}{average:>12.2f}\n")
    else:
        report.write(f"{'NA':>7}{'NA':>12}{'NA':>12}\n")