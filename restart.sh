caddyRunning=$(ps -ef | grep caddy | grep -v grep | wc -l)
if [[ $caddyRunning == "0" ]]; then
  cd /data
  caddy -quic -cpu 50 -quiet -port 8735 browse &
fi
                     
pythonRunning=$(ps -ef | grep python | grep -v grep | wc -l)
if [[ $pythonRunning == "0" ]]; then
  python3 /main.py
fi

