#!/bin/bash
export ZK='10.10.1.5:2181'
export WP_NAMESPACE=distributedlog://$ZK/messaging/distributedlog/ns-1
LWP_SHARD_ID=1
LWP_SERVICE_PORT=4181
LWP_STATS_PORT=20001

for i in $(seq 1 $1); do
    echo "$LWP_SHARD_ID $LWP_SERVICE_PORT $LWP_STATS_PORT"
    export WP_SHARD_ID=$LWP_SHARD_ID
    export WP_SERVICE_PORT=$LWP_SERVICE_PORT
    export WP_STATS_PORT=$LWP_STATS_PORT
    ./distributedlog-proxy-server/bin/dlog-daemon.sh start writeproxy
    let LWP_SHARD_ID+=3
    let LWP_SERVICE_PORT+=1
    let LWP_STATS_PORT+=1
done
