import sys
from decimal import Decimal, ROUND_HALF_UP

try:
    input_file = sys.argv[1]
except IndexError:
    print("Укажите входной файл в команде (например, python B1.py inmap0.dat)")
    sys.exit()

with open(input_file) as file:
        strs = file.readlines()
        vals = list(map(float, strs[0].replace("\n", "").split("  "))) # vals[0] - количество мест, [1] - масштаб
        scale = Decimal(vals[1]).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total = 0

print("Artyom Astahov\n" +
    "Simple Map Distance Computations\n\n" +
    f"Map Scale Factor:    {scale} miles per inch\n\n" +
    "       Map         Mileage\n" +
    "       Measure     Distance")
print("=" * 50)

for i in range(1, int(vals[0]) + 1):
    dist = strs[i].replace("\n", "")
    dist_f = (Decimal(dist) * scale).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    total += dist_f
    print(f"#  {i}     {dist}        {dist_f}")
    
print("=" * 50 + "\n" +
    f"Total Distance:    {total} miles")
