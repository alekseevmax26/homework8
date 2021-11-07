import subprocess
from datetime import datetime
from collections import defaultdict


def get_process_data():
    process = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE, universal_newlines=True).stdout.readlines()
    nfields = len(process[0].split()) - 1
    retval = []
    for row in process[1:]:
        retval.append(row.split(None, nfields))
    return retval


def get_count_of_process(lines):
    return len(lines)


def get_users_from_process(lines):
    users = []
    for line in lines:
        if line[0] not in users:
            users.append(line[0])

    return users


def user_process_count(lines):
    process_by_user = defaultdict(int)
    for line in lines:
        user_item = line[0]
        process_by_user[user_item] += 1
    return process_by_user


def calculate_memory_and_cpu_usage(lines):
    memory_result = 0
    cpu_result = 0
    for line in lines:
        memory_number = float(line[3])
        cpu_number = float(line[2])
        memory_result += memory_number
        cpu_result += cpu_number

    return round(memory_result, 2), round(cpu_result, 2)


def process_who_eat_memory(lines):
    highest_memory = 0
    highest_memory_name = ""
    for line in lines:
        if float(line[3]) > highest_memory:
            highest_memory = float(line[3])
            highest_memory_name = line[10][:20]
        elif float(line[3]) == highest_memory:
            highest_memory = float(line[3])
            highest_memory_name = line[10][:20].rstrip()

    return highest_memory_name


def process_who_eat_cpu(lines):
    highest_cpu_load = 0
    highest_cpu_load_name = ""
    for line in lines:
        if float(line[2]) > highest_cpu_load:
            highest_cpu_load = float(line[2])
            highest_cpu_load_name = line[10][:20]
        elif float(line[2]) == highest_cpu_load:
            highest_cpu_load = float(line[2])
            highest_cpu_load_name = line[10][:20].rstrip()

    return highest_cpu_load_name


data = get_process_data()
cpu_and_memory = calculate_memory_and_cpu_usage(data)
process_count = get_count_of_process(data)
users = get_users_from_process(data)
user_processes_count = user_process_count(data)
name_of_highest_cpu = process_who_eat_cpu(data)
name_of_highest_memory = process_who_eat_memory(data)

report = [
    f"Пользователи системы: {users}\n",
    f"Процессов запущено: {process_count}\n",
    f"Пользовательских процессов: {dict(user_processes_count)}\n",
    f"Всего памяти используется: {cpu_and_memory[0]}\n",
    f"Всего CPU используется: {cpu_and_memory[1]}\n",
    f"Больше всего памяти использует: {name_of_highest_memory}\n",
    f"Больше всего CPU использует: {name_of_highest_cpu}",

]

with open(f"{datetime.today():%d-%m-%Y-%H:%M}-scan.txt", 'w') as fp:
    fp.writelines(report)

print(f"Пользователи системы: {users}")
print(f"Процессов запущено: {process_count}")
print(f"Пользовательских процессов: {dict(user_processes_count)}")
print(f"Всего памяти используется: {cpu_and_memory[0]}")
print(f"Всего CPU используется: {cpu_and_memory[1]}")
print(f"Больше всего памяти использует: {name_of_highest_memory}")
print(f"Больше всего CPU использует: {name_of_highest_cpu}")
