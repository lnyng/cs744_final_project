#!/bin/bash
#export DLOG_HOME="$(pwd)"

#source $HOME/distlog-0.5.0/distributedlog-benchmark/bin/common.sh
export ZK='10.10.1.5:2181'
export STREAM_NAME_PREFIX=loadtest_
export BENCHMARK_DURATION=1 # minutes
export DL_NAMESPACE=distributedlog://$ZK/messaging/distributedlog/$1
export NUM_STREAMS=1
export INITIAL_RATE=200
distributedlog-benchmark/bin/dbench write
