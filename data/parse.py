#!/usr/bin/python3

import re

def producer(n):
    data = []
    with open('node-0_plot%d.log' % n) as f1, open('node-1_plot%d.log' % n) as f2, open('node-2_plot%d.log' % n) as f3:
        combined = zip(f1.readlines(), f2.readlines(), f3.readlines())
    try:
        while True:
            row = {}
            lines = next(combined)
            for line in lines:
                parts = line.split()
                for part in parts:
                    key, val = part.split('=')
                    row[key] = row.get(key, 0) + int(val)
            lines = next(combined)
            for line in lines:
                parts = line.split(',')
                tp = float(re.search('\(([0-9.]+) MB/sec\)', parts[1]).groups()[0])
                latency_95 = float(parts[5].split()[0])
                row['throughput'] = row.get('throughput', 0) + tp
                row['latency_95'] = row.get('latency_95', 0) + latency_95
            row['throughput'] *= 3
            row = {key: str(val//3) if type(val) is int else '%.3f' % (val/3) for key, val in row.items()}
            data.append(row)
    except StopIteration:
        pass
    with open('plot%d.data' % n, 'w') as f:
        keys = sorted(data[0].keys())
        f.write('#,' + ','.join(keys) + '\n')
        for row in data:
            f.write(','.join(row[key] for key in keys) + '\n')

def consumer(n):
    data = []
    with open('plot%d.log' % n) as f:
        lines = iter(f.readlines())
    try:
        while True:
            row = {}
            line = next(lines)
            parts = line.split()
            for part in parts:
                key, val = part.split('=')
                row[key] = int(val)
            line = next(lines)
            line = next(lines)
            tp = float(line.split(',')[3])
            row['throughput'] = tp
            data.append(row)
    except StopIteration:
        pass
    with open('plot%d.data' % n, 'w') as f:
        keys = sorted(data[0].keys())
        f.write('#,' + ','.join(keys) + '\n')
        for row in data:
            f.write(','.join(str(row[key]) if type(row[key]) is int else '%.3f' % row[key] for key in keys) + '\n')

if __name__ == '__main__':
    # plot 1
    producer(1)
    producer(2)
    consumer(3)
