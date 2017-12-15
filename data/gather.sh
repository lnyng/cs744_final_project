#!/bin/bash

for i in 0 1 2; do
    scp node-${i}:/root/benchmarking/producer.log node-${i}_plot1.log
    scp node-${i}:/root/benchmarking/producer.1.log node-${i}_plot2.log
    scp node-${i}:/root/benchmarking/producer.2.log node-${i}_plot2_norep.log
    scp node-${i}:/root/benchmarking/producer.3.log node-${i}_plot2_async.log
    cat node-${i}_plot2_norep.log >> node-${i}_plot2.log
    cat node-${i}_plot2_async.log >> node-${i}_plot2.log
done
cp /root/benchmarking/consumer.1.log plot3.log
cat /root/benchmarking/consumer.2.log >> plot3.log
rm *norep*
rm *async*
