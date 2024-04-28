#!/usr/bin/python3

import socket
import time
import csv
import subprocess
import re
import threading
import sys

max_received = 0
max_sent = 0

def get_received_stats(port):
    global max_received
    while True:
        result = subprocess.run(['ss', '-tin', 'sport', f':{port}'], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        matches = re.findall(r'bytes_received:(\d+)', output)
        received = sum(int(match) for match in matches)
        max_received = max(max_received, received)
        time.sleep(0.2)

def get_sent_stats(port):
    global max_sent
    while True:
        result = subprocess.run(['ss', '-tin', 'dport', f':{port}'], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        matches = re.findall(r'bytes_sent:(\d+)', output)
        sent = sum(int(match) for match in matches)
        max_sent = max(max_sent, sent)

def read_tcp_connections():
    connections = 0
    with open('/proc/net/tcp', 'r') as f:
        for line in f.readlines()[1:]:
            parts = line.strip().split()
            local_address, local_port = parts[1].split(':')
            remote_address, remote_port = parts[2].split(':')
            if int(local_port, 16) == 2345:
                connections += 1

    return connections

def write_to_file(data, output_file):
    with open(output_file, 'w') as f:
        for row in data:
            f.write(','.join(str(item) for item in row) + '\n')

def main():
    # period = int(input('Введите период сбора метрик: '))
    # output_file = input('Введите путь к выходному файлу: ')
    global max_sent
    if len(sys.argv) != 3:
        with open('config.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                parts = line.split("=")
                if len(parts) == 2:
                    key, value = parts[0], parts[1]
                    if key == "file_path":
                        output_file = value
                    elif key == "period":
                        period = int(value)
    else:
        period = int(sys.argv[1])
        output_file = sys.argv[2]

    data = []
    received_thread = threading.Thread(target=get_received_stats, args=(2345,))
    sent_thread = threading.Thread(target=get_sent_stats, args=(2345,))
    received_thread.start()
    sent_thread.start()

    prev_received = max_received
    prev_sent = max_sent

    while True:
        connection_count_before = read_tcp_connections()
        
        time.sleep(period)

        current_timestamp = time.time()
        received = max_received
        sent = max_sent
        connection_count_after = read_tcp_connections()

        data.append([
            int(current_timestamp),
            received - prev_received,
            sent - prev_sent,
            max(connection_count_before,connection_count_after)  - 1
        ])
        
        write_to_file(data, output_file)
        prev_received = received
        prev_sent = sent

if __name__ == '__main__':
    main()
