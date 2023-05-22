#!/bin/bash

last_time=0
if [[ -f last_time.txt ]]; then
    last_time=$(cat last_time.txt)
fi

current_time=$(date +%s)
((delta_time=$current_time-$last_time))
## 预计多少天运行一次
((goal=3600*24*85))

((delta_day=$delta_time/86400))
echo "Delta day: $delta_day"

if [[ $delta_time -gt $goal ]]; then
    echo "$current_time" > last_time.txt
    echo "Need to update..."
    exit 0
fi

echo "No need to update, exit"
exit 1


