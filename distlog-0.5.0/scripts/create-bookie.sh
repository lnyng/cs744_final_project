#!/bin/bash
export DL_HOME=/users/dennisz/distlog-0.5.0
export BOOKIE_CONF=${DL_HOME}/distributedlog-proxy-server/conf/bookie-1.conf
export SERVICE_PORT=3181
./distributedlog-proxy-server/bin/dlog bkshell bookieformat
./distributedlog-proxy-server/bin/dlog-daemon.sh start bookie \
	--conf ${DL_HOME}/distributedlog-proxy-server/conf/bookie-1.conf
