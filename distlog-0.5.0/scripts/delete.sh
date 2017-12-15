#!/bin/bash
export ZK='10.10.1.5:2181'
export DL_URI=distributedlog://$ZK/messaging/distributedlog/ns-1
CMD=$1
shift
distributedlog-core/bin/dlog tool $CMD -u $DL_URI $@
