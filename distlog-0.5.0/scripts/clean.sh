#!/bin/bash

bash scripts/stop-proxy.sh
bash scripts/delete.sh truncate -delete
SERVICE_PORT=3181 ./distributedlog-proxy-server/bin/dlog-daemon.sh stop bookie

rm -rf /data/bk/journal/*
rm -rf /data/bk/ledgers/*

#bash scripts/create-bookie.sh
#bash scripts/start-wp.sh
