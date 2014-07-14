#/bin/bash
function start {
  python server.py &
}
function stop {
  local pid=`cat tm_gateway.pid`
  kill $pid
  rm tm_gateway.pid
}

if [ $# -eq 1 ]; then
  if [ "$1" = "start" ]; then
    start
  elif [ "$1" = "stop" ]; then
    stop
  elif [ "$1" = "restart" ]; then
    start
    stop
  else
    echo "error , usage ./run.sh start|stop|restart"
  fi
else
  echo "error , usage ./run.sh start|stop|restart"
fi
 
