cd /d %~dp0
python get_host_ip.py
copy hosts C:\Windows\System32\drivers\etc\hosts /Y
ipconfig /flushdns
pause