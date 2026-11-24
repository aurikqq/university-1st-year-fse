import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
import matplotlib.pyplot as plt

# Часть 1

def load_users_data():
    try:
        users_tree = ET.parse('data/users.xml')
        users = []
        for user_elem in users_tree.getroot().findall('user'):
            user = {
                'user_id': int(user_elem.find('user_id').text),
                'name': user_elem.find('name').text,
                'age': int(user_elem.find('age').text),
                'weight': int(user_elem.find('weight').text),
                'fitness_level': user_elem.find('fitness_level').text,
                'workouts': []
            }
            users.append(user)
        return users
    except FileNotFoundError:
        print("Файл не найден")
        return []

def load_workouts_data():
    try:
        workouts_tree = ET.parse('data/workouts.xml')
        workouts = []
        for workout_elem in workouts_tree.getroot().findall('workout'):
            workout = {
                'workout_id': int(workout_elem.find('workout_id').text),
                'user_id': int(workout_elem.find('user_id').text),
                'date': workout_elem.find('date').text,
                'type': workout_elem.find('type').text,
                'duration': int(workout_elem.find('duration').text),
                'distance': float(workout_elem.find('distance').text),
                'calories': int(workout_elem.find('calories').text),
                'avg_heart_rate': int(workout_elem.find('avg_heart_rate').text),
                'intensity': workout_elem.find('intensity').text,
            }
            workouts.append(workout)
        return workouts
    except FileNotFoundError:
        print("Файл не найден")
        return []

def get_stats(users, workouts):
    total_workouts = len(workouts)
    total_users = len(users)
    total_calories = sum(workout['calories'] for workout in workouts)
    total_time = sum(workout['duration'] for workout in workouts)
    total_dist = sum(workout['distance'] for workout in workouts)

    print("ОБЩАЯ СТАТИСТИКА")
    print('=' * 20)
    print(f"Всего тренировок: {total_workouts}")
    print(f"Всего пользователей: {total_users}")
    print(f"Сожжено калорий: {total_calories}")
    print(f"Общее время: {(total_time / 60):.1f} часов")
    print(f"Пройдено дистанции: {total_dist} км")

# Часть 2

# не входило в задание, но реализовал функцию
# для более простого написания кода
def get_workout_data(workout_id, workouts):
    for workout in workouts:
        if workout['workout_id'] == workout_id:
            return workout
    return None


def analyze_user(user, workouts):
    user['workouts'] = []
    for workout in workouts:
        if workout['user_id'] == user['user_id']:
            user['workouts'].append(workout["workout_id"])

    user_workouts = [
        workout
        for workout_id in user["workouts"]
        if (workout := get_workout_data(workout_id, workouts)) is not None
    ]

    total_workouts = len(user_workouts)
    total_calories = sum(workout['calories'] for workout in user_workouts)
    total_time = sum(workout['duration'] for workout in user_workouts)
    total_dist = sum(workout['distance'] for workout in user_workouts)
    types = [workout['type'] for workout in user_workouts]
    favorite_type = Counter(types).most_common(1)[0][0] if types else "нет тренировок"

    print(f"ДЕТАЛЬНАЯ СТАТИСТИКА ДЛЯ ПОЛЬЗОВАТЕЛЯ: {user["name"]}")
    print('=' * 20)
    print(f"Возраст: {user["age"]} лет, вес: {user["weight"]} кг")
    print(f"Уровень: {user["fitness_level"]}")
    print(f"Тренировок: {total_workouts}")
    print(f"Сожжено калорий: {total_calories}")
    print(f"Общее время: {(total_time / 60):.1f} часов")
    print(f"Пройдено дистанции: {total_dist} км")
    average_calories = total_calories / total_workouts if total_workouts else 0
    print(f"Средние калории за тренировку: {average_calories:.1f}")
    print(f"Любимый тип тренировки: {favorite_type}\n")

def analyze_user_activity(users, workouts):
    users_top = []
    for user in users:
        total_calories = 0
        total_time = 0
        for workout_id in user["workouts"]:
            workout = get_workout_data(workout_id, workouts)
            if workout is not None:
                total_time += workout['duration']
                total_calories += workout['calories']
        users_top.append({
            "name": user["name"],
            "workouts_count": len(user["workouts"]),
            "calories": total_calories,
            "time": total_time,
            "level": user["fitness_level"]
        })

    users_top.sort(key=lambda user: user["workouts_count"], reverse=True)
    for i in range(min(3, len(users_top))):
        user = users_top[i]
        print(f"{i + 1}. {user["name"]} ({user["level"]}):\n",
        f"Тренировок: {user["workouts_count"]}\n",
        f"Калорий: {user["calories"]}\n",
        f"Время: {user["time"] / 60} часов\n")

    return users_top

def find_user_workouts(users, workouts, user_name):
    target_user = next(
        (user for user in users if user["name"] == user_name),
        None
    )
    if target_user is None:
        return []

    return [
        workout
        for workout_id in target_user["workouts"]
        if (workout := get_workout_data(workout_id, workouts)) is not None
    ]

def analyze_workout_types(workouts):
    workouts_by_type = defaultdict(list)
    for workout in workouts:
        workouts_by_type[workout["type"]].append(workout)
    types_distribution = {}

    total_workouts = len(workouts)
    print("РАСПРЕДЕЛЕНИЕ ПО ТИПАМ ТРЕНИРОВОК:")
    for workout_type, type_workouts in workouts_by_type.items():
        count = len(type_workouts)
        percentage = count / total_workouts * 100
        types_distribution[workout_type] = percentage
        average_duration = sum(
            workout["duration"] for workout in type_workouts
        ) / count
        average_calories = sum(
            workout["calories"] for workout in type_workouts
        ) / count

        print(
            f"{workout_type.capitalize()}: {count} тренировок "
            f"({percentage:.1f}%)"
        )
        print(f"Средняя длительность: {average_duration:.0f} мин")
        print(f"Средние калории: {average_calories:.0f} ккал")

    return types_distribution

# Часть 3

def types_percentage_diagram(types_distribution):
    sizes = []
    labels = []
    for workout_type, percentage in types_distribution.items():
        labels.append(workout_type)
        sizes.append(percentage)

    plt.figure(figsize=(10, 4))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%")
    plt.axis("equal")
    plt.title("Распределение типов тренировок", fontweight="bold")

def activity_diagram(users):
    sizes = []
    names = []
    for user in users:
        names.append(user["name"])
        sizes.append(user["workouts_count"])

    plt.figure(figsize=(6, 4))
    plt.bar(names, sizes, color = "skyblue", edgecolor = "black")
    plt.title("Активность пользователей (количество тренировок)", fontweight="bold")
    plt.ylabel("Количество тренировок")
    plt.xlabel("Пользователи")

def get_efficiency(workouts):
    totals = defaultdict(lambda: {"calories": 0, "duration": 0})

    for workout in workouts:
        workout_type = workout["type"]
        totals[workout_type]["calories"] += workout["calories"]
        totals[workout_type]["duration"] += workout["duration"]

    efficiency_stats = []
    for workout_type, total in totals.items():
        duration = total["duration"]
        if duration > 0:
            efficiency = total["calories"] / duration
            efficiency_stats.append((workout_type, efficiency))

    return sorted(efficiency_stats, key=lambda item: item[1], reverse=True)

def efficiency_diagram(workouts):
    efficiency_stats = get_efficiency(workouts)
    names = [workout_type for workout_type, _ in efficiency_stats]
    efficiency = [value for _, value in efficiency_stats]

    plt.figure(figsize=(6, 4))
    plt.bar(names, efficiency, color="skyblue", edgecolor="black")
    plt.title("Эффективность тренировок (калории/минуту)", fontweight="bold")
    plt.ylabel("Калории в минуту")
    plt.xlabel("Тип тренировки")

def comparsion_diagram(users):
    level_colors = {
        "продвинутый": "#FF4C4C",
        "средний": "#FFBF4C",
        "начальный": "#4CA64C",
    }
    level_labels = {
        "продвинутый": "Продвинутый",
        "средний": "Средний",
        "начальный": "Начальный",
    }

    if isinstance(users, dict):
        user_stats = []
        for name, value in users.items():
            if isinstance(value, dict):
                stat = dict(value)
                stat["name"] = stat.get("name", name)
                stat["calories"] = stat.get("calories", 0)
            else:
                stat = {"name": name, "calories": value}
            user_stats.append(stat)
    else:
        user_stats = list(users)

    user_stats = sorted(user_stats, key=lambda user: user["calories"], reverse = True)
    names = [user["name"] for user in user_stats]
    sizes = [user["calories"] for user in user_stats]

    bar_colors = []
    shown_levels = set()
    for user in user_stats:
        level = str(
            user.get("fitness_level", user.get("level", ""))
        ).lower()
        color = level_colors.get(level, "#808080")
        bar_colors.append(color)
        if level in level_colors:
            shown_levels.add(level)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(names, sizes, color=bar_colors, edgecolor="black")

    handles = [
        plt.Rectangle((0, 0), 1, 1, color=level_colors[level])
        for level in ("продвинутый", "средний", "начальный")
        if level in shown_levels
    ]
    handle_labels = [
        level_labels[level]
        for level in ("продвинутый", "средний", "начальный")
        if level in shown_levels
    ]
    if handles:
        ax.legend(handles, handle_labels)

    plt.title("Сравнение пользователей по общим затраченным калориям", fontweight="bold")
    plt.ylabel("Общие калории")
    plt.xlabel("Пользователи")

    plt.show()


def main():

    # Часть 1

    users = load_users_data()
    workouts = load_workouts_data()
    print("\n")
    get_stats(users, workouts)
    print("\n")

    # Часть 2

    for user in users:
        analyze_user(user, workouts)
    print("")
    top_users = analyze_user_activity(users, workouts)
    find_user_workouts(users, workouts, users[0]["name"])
    print("")

    # Часть 3

    types_distribution = analyze_workout_types(workouts)
    types_percentage_diagram(types_distribution)
    activity_diagram(top_users)
    efficiency_diagram(workouts)
    comparsion_diagram(top_users)

if __name__ == "__main__":
    main()