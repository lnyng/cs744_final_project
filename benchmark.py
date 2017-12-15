#!/usr/bin/env python3

import os, sys, subprocess as sp
import time

HOST = '10.10.1.4'

def create(partitions=24, replica=1, name='test'):
    while True:
        try:
            sp.check_call((f'kafka-topics.sh --zookeeper {HOST}:2181 --delete --if-exists --topic {name}').split())
            time.sleep(10)
            cmd = f'kafka-topics.sh --zookeeper {HOST}:2181 --create --topic {name} --partitions {partitions} --replication-factor {replica}'
            sp.check_call(cmd.split())
            sp.check_call(['/drop_caches.sh'])
            break
        except:
            time.sleep(10)

def producer(num_producers=8, acks=-1, record_size=4096, topic='test', batch_size=16384, num_records=50000000, partitions=9, replica=1, buffer_memory=33554432):
    print(f'num_producers={num_producers} acks={acks} record_size={record_size} batch_size={batch_size} ' +
            f'num_records={num_records} partitions={partitions} replica={replica} buffer_memory={buffer_memory}')
    sys.stdout.flush()

    cmd = f'java ProducerPerformance --topic {topic} --num-producers {num_producers} --num-records {num_records} --throughput -1 ' + \
            f'--record-size {record_size} --producer-props acks={acks} bootstrap.servers={HOST}:9092 batch.size={batch_size} buffer.memory={buffer_memory}'
    sp.check_call(cmd.split(), stdout=sys.stdout)

def consumer(record_size, batch_size, partitions=9, threads=8, num_records=5000000, replica=1):
    print(f'partitions={partitions} threads={threads} record_size={record_size} batch_size={batch_size} replica={replica}')
    sys.stdout.flush()

    cmd = f'java kafka.tools.ConsumerPerformance --zookeeper {HOST}:2181 ' + \
        f'--messages {num_records} --topic test --threads {threads} --num-fetch-threads {threads}'
    sp.check_call(cmd.split(), stdout=sys.stdout)

if __name__ == '__main__':
    os.environ['PATH'] = '/root/kafka_2.11-1.0.0/bin:' + os.environ.get('PATH', '')
    os.environ['CLASSPATH'] = '/root/benchmarking:/root/kafka_2.11-1.0.0/libs/*:' + os.environ.get('CLASSPATH', '')
    argv = {arg.split('=')[0]: arg.split('=')[1] for arg in sys.argv[2:]}
    if sys.argv[1] == 'create':
        create(**argv)
    elif sys.argv[1] == 'producer':
        producer(**argv)
    elif sys.argv[1] == 'consumer':
        consumer(**argv)
    """

    for record_size in (128, 256, 512):
        for batch_size in (4096, 16384, 65536, 262144):
            producer(record_size=record_size, batch_size=batch_size)
            consumer(record_size=record_size, batch_size=batch_size)

    pairs = ((128, 16384), (128, 65536), (256, 65536), (512, 262144))
    producer_log.close()
    consumer_log.close()

    for pair in pairs:
        for partitions in (1, 3, 6, 9, 12):
            producer(partitions=partitions, record_size=pair[0], batch_size=pair[1])
            consumer(partitions=partitions, threads=16, record_size=pair[0], batch_size=pair[1])

    for pair in pairs:
        for threads in (1, 4, 8, 12, 16):
            producer(partitions=9, num_producers=threads, record_size=pair[0], batch_size=pair[1])
            consumer(partitions=9, threads=threads, record_size=pair[0], batch_size=pair[1])
    """
