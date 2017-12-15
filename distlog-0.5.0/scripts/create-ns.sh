#!/bin/bash
NS=$1
ZK='10.10.1.5:2181'
distributedlog-proxy-server/bin/dlog admin bind \
	-dlzr $ZK \
	-dlzw $ZK \
	-s $ZK \
	-bkzr $ZK \
	-l /messaging/bookkeeper/ledgers \
	-i false \
	-r true \
	-c \
	distributedlog://$ZK/messaging/distributedlog/$NS
