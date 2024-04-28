import subprocess
import time
import random
import csv
import sys

def generate_random_number(lower_bound, upper_bound):
    return random.randint(lower_bound, upper_bound)

def get_random_time(lower_bound, upper_bound, multiple):
    random_time = generate_random_number(lower_bound, upper_bound)
    while random_time % multiple != 0:
        random_time = generate_random_number(lower_bound, upper_bound)
    return random_time

def calculate_expected_data_transfer(data_size, period, random_time):
    return data_size * (random_time // period)

def main():
    if len(args) != 2:
        print("Необходимо указать два аргумента: период и количество данных")
        return
        
    set_ip = subprocess.Popen(['python3', 'check_ip.py'])
    set_ip.wait()
    
    period_main = get_random_time(2, 10, 2)
    main_process = subprocess.Popen(['python3', 'main.py', str(period_main), 'test.csv'])
    time.sleep(period_main)

    args = sys.argv[1:]

    period = int(args[0])
    data_size = int(args[1])

    server_process = subprocess.Popen(['python3', 'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    client_process = subprocess.Popen(['python3', 'client.py', str(period), str(data_size)])
    
    all_time = get_random_time(10, 20, 2)
    time.sleep(all_time)

    client_process.terminate()
    time.sleep(10)
    main_process.terminate()
    server_process.terminate()
    
    subprocess.run(['fuser', '-k', '2345/tcp'], stdout=subprocess.PIPE)
   
    total_sent_bytes = 0
    with open('test.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            total_sent_bytes += int(row[1])

    expected_data_transfer = calculate_expected_data_transfer(data_size, period, all_time)
    if total_sent_bytes == expected_data_transfer:
        print("OK")
        print("Результат в файле test.csv")
    else:
        print(f"FALSE: Ожидалось {expected_data_transfer}, отправлено {total_sent_bytes}")

if __name__ == '__main__':
    main()
