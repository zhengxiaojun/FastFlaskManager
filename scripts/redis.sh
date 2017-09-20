#!/bin/sh

#current_dir=`dirname "$0"`
#dir=`cd $current_dir;pwd`
current_dir="/Users/jack/redis/redis-2.8.17"

start() {
    ${current_dir}/src/redis-server ${current_dir}/redis.conf
    echo $! > $current_dir/redis.pid
    PID=`cat ${current_dir}/redis.pid`
    if [ -n "$PID" ];then
        echo "Server started, PID : $PID"
    fi
}

stop() {
    PID=`cat ${current_dir}/redis.pid`
    if [ -n "$PID" ];then
        echo "Stoping server, PID : $PID"
            for p_pid in `ps -ef |grep $PID |grep 'redis' |awk '{print $2}'`
	    do
    		kill -9 $p_pid
	    done
    fi
}

case "$1" in
    start)
            start
            ;;
    stop)
            stop
            ;;
    restart)
            stop
            start $@
            ;;
    *)
            echo "Usage: $0 {start|stop|restart}"
            exit 1
esac