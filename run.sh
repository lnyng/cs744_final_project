#!/bin/bash

echo "compiling ProducerPerformance.java"
pdsh -b -R exec -f 5 -w ^/worker_machines ssh %h \
    "sudo sh -c 'cd /root/benchmarking && . ./setup.sh && javac ProducerPerformance.java'"

echo "removing old logs"
pdsh -b -R exec -f 5 -w ^/worker_machines ssh %h \
    "sudo sh -c 'cd /root/benchmarking/ && rm producer.log consumer.log'"

for record_size in 128 256 512; do
    for batch_size in 4096 16384 65536 131072; do
        echo "creating topic"
        python3.6 benchmark.py create partitions=9 || exit 1

        echo "running producer test"
        pdsh -b -R exec -f 5 -w ^/worker_machines ssh %h \
            "sudo sh -c ""'""cd /root/benchmarking && python3.6 benchmark.py producer acks=-1 num_producers=8 record_size=$record_size batch_size=$batch_size >> producer.log""'" || exit 1
        #python3.6 benchmark.py producer num_producers=5 record_size=$record_size batch_size=$batch_size
        echo "running consumer test"
        pdsh -b -R exec -f 5 -w ^/worker_machines ssh %h \
            "sudo sh -c ""'""cd /root/benchmarking && python3.6 benchmark.py consumer record_size=$record_size batch_size=$batch_size >> consumer.log""'" || exit 1
        #python3.6 benchmark.py consumer record_size=$record_size batch_size=$batch_size
    done
done

echo "removing old logs"
pdsh -b -R exec -f 5 -w ^/worker_machines ssh %h \
    "sudo sh -c 'cd /root/benchmarking/ && rm producer.1.log producer.2.log consumer.1.log consumer.2.log'"

record_size=512
batch_size=131072
for partitions in 24; do
    echo "creating replicated topic"
    python3.6 benchmark.py create partitions=$partitions || exit 1

    echo "running producer test"
    pdsh -b -R exec -f 5 -w ^/worker_machines ssh %h \
        "sudo sh -c ""'""cd /root/benchmarking && python3.6 benchmark.py producer record_size=$record_size batch_size=$batch_size partitions=$partitions >> producer.1.log""'" || exit 1

    echo "running consumer test"
    python3.6 benchmark.py consumer record_size=$record_size batch_size=$batch_size partitions=$partitions threads=$partitions >> consumer.1.log
    #pdsh -b -R exec -f 5 -w ^/worker_machines ssh %h \
    #    "sudo sh -c ""'""cd /root/benchmarking && python3.6 benchmark.py consumer record_size=$record_size batch_size=$batch_size partitions=$partitions >> consumer.1.log""'" || exit 1

    echo "creating non-replicated topic"
    python3.6 benchmark.py create partitions=$partitions replica=1 || exit 1

    echo "running producer test"
    pdsh -b -R exec -f 5 -w ^/worker_machines ssh %h \
        "sudo sh -c ""'""cd /root/benchmarking && python3.6 benchmark.py producer replica=1 acks=1 record_size=$record_size batch_size=$batch_size partitions=$partitions >> producer.2.log""'" || exit 1

    echo "running consumer test"
    python3.6 benchmark.py consumer replica=1 record_size=$record_size batch_size=$batch_size partitions=$partitions threads=$partitions >> consumer.2.log
    #pdsh -b -R exec -f 5 -w ^/worker_machines ssh %h \
    #    "sudo sh -c ""'""cd /root/benchmarking && python3.6 benchmark.py consumer replica=1 record_size=$record_size batch_size=$batch_size partitions=$partitions >> consumer.2.log""'" || exit 1
done

record_size=512
batch_size=131072
buffer_memory=33554432

echo "removing old logs"
pdsh -b -R exec -f 5 -w ^/worker_machines ssh %h \
    "sudo sh -c 'cd /root/benchmarking/ && rm producer.3.log'"
for partitions in 1 6 12 18 24; do
    echo "creating async replicated topic"
    python3.6 benchmark.py create partitions=$partitions || exit 1

    echo "running producer test"
    pdsh -b -R exec -f 5 -w ^/worker_machines ssh %h \
        "sudo sh -c ""'""cd /root/benchmarking && python3.6 benchmark.py producer replica=1 acks=1 record_size=$record_size batch_size=$batch_size partitions=$partitions buffer_memory=$buffer_memory >> producer.3.log""'" || exit 1
done
