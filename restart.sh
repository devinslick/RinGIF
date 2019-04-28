pythonRunning=$(ps -ef | grep python | grep -v grep | wc -l)
if [[ $pythonRunning == "0" ]]; then
  python /main.py
fi
