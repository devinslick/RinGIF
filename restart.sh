pythonRunning=$(ps -ef | grep python | grep -v grep | wc -l)
if [[ $pythonRunning == "0" ]]; then
  python /main.py
fi

caddyRunning=$(ps -ef | grep caddy | grep -v grep | wc -l)
if [[ $caddyRunning == "0" ]]; then
  caddy -quiet -root /scripts -http-port 8123 -quic -cpu 50 &
fi
