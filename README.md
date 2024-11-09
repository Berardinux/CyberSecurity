You can use iptables with a command like this to stop SYN attacks like these.

$(sudo iptables -A INPUT -p tcp --syn -m connlimit --connlimit-above 10 -j REJECT)
