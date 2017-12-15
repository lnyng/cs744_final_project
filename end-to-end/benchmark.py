#!/usr/bin/env python3

import os, sys, subprocess as sp
import time

HOST = '10.10.1.1'
producer_log = None#open('producer.log', 'w')
consumer_log = None#open('consumer.log', 'w')

def create_topic(partitions=9, replica=1, flush_ms=9223372036854775807, flush_messages=9223372036854775807):
    sp.check_call((f'kafka-topics.sh --zookeeper {HOST}:2181 --delete --if-exists --topic test').split())
    time.sleep(10)
    cmd = f'kafka-topics.sh --zookeeper {HOST}:2181 --create --topic test --partitions {partitions} --replication-factor {replica}'
    if flush_ms is not None:
        cmd += f' --config flush.ms={flush_ms}'
    if flush_messages is not None:
        cmd += f' --config flush.messages={flush_messages}'
    sp.check_call(cmd.split())
    sp.check_call(['/drop_caches.sh'])

def producer(partitions=9, replica=1, num_producers=16, acks=1, record_size=256, batch_size=16384,
        linger=0, num_records=50000000, flush_ms=9223372036854775807, flush_messages=9223372036854775807, logging=True):
    if logging:
        producer_log.write(f'partition={partitions} replica={replica} num_producers={num_producers} acks={acks} record_size={record_size} batch_size={batch_size} ' +
                f'linger={linger} num_records={num_records} flush_ms={flush_ms} flush_messages={flush_messages}\n')
        producer_log.flush()

    cmd = f'java MyProducerPerformance --topic test --num-producers {num_producers} --num-records {num_records} --throughput -1 ' + \
            f'--record-size {record_size} --producer-props acks={acks} bootstrap.servers={HOST}:9092'
    sp.check_call(cmd.split(), stdout=producer_log if logging else None)

def consumer(partitions=9, threads=16, record_size=0, batch_size=0, num_records=50000000):
    consumer_log.write(f'partitions={partitions} threads={threads} record_size={record_size}\n')
    consumer_log.flush()

    cmd = f'java MyConsumerPerformance --zookeeper {HOST}:2181 ' + \
        f'--messages {num_records} --topic test --threads {threads} --num-fetch-threads {threads}'
    sp.check_call(cmd.split(), stdout=consumer_log)

if __name__ == '__main__':
    os.environ['PATH'] = '/root/kafka_2.12-1.0.0/bin:' + os.environ.get('PATH', '')
    os.environ['CLASSPATH'] = '.:/root/kafka_2.12-1.0.0/libs/*:' + os.environ.get('CLASSPATH', '')

    if sys.argv[1] == 'consumer':
        consumer_log = open('consumer.log', 'w')
        sp.check_call('scalac MyConsumerPerformance.scala'.split())
        consumer(1, 1)
    elif sys.argv[1] == 'producer':
        producer_log = open('producer.log', 'w')
        sp.check_call('javac MyProducerPerformance.java'.split())
        producer(partitions=1, num_producers=1, record_size=256)
    elif sys.argv[1] == 'create':
        create_topic(9)
