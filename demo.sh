#!/bin/bash

echo "Starting InfluxDb and Grafana... \n"

docker-compose  -f ./database/docker-compose.yaml up -d

echo "Starting Server... \n"

python ./src/streaming_utils/net_gears_server_side.py &


echo "Starting Client... \n"

python ./src/streaming_utils/net_gears_client_side.py --delay_prob 0.0 &

