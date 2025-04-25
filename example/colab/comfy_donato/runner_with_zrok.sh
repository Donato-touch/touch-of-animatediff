#!/bin/bash

ZROK_TOKEN=$1
PORT=8188
INPUT_DIR=$2
OUTPUT_DIR=$3

curl -sSf https://get.openziti.io/install.bash | sudo bash -s zrok

zrok disable
zrok enable $ZROK_TOKEN
zrok status

echo "==zrok ready!=="

python3 main.py --dont-print-server --input-directory $INPUT_DIR --output-directory $OUTPUT_DIR &
SERVER_PID=$!

cleanup() {
    echo "Stopping server..."
    kill $SERVER_PID 2>/dev/null
    wait $SERVER_PID 2>/dev/null
    echo "Cleanup done."
}
trap cleanup SIGINT SIGTERM

echo "Waiting for port $PORT to open..."
while ! nc -z localhost $PORT; do
    sleep 3
done
echo "Port $PORT is open."
sleep 3

zrok share public $PORT

cleanup

