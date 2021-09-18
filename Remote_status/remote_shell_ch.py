import paramiko
import time
import os
from rich.console import Console
from rich.text import Text
from rich.prompt import Prompt

os.system('banner System Health')
console = Console()

def yprint(string):
	console.print(Text(string,style="bold yellow"))

def bprint(string): 
	console.print(Text(string,style="bold blue"))

def rprint(string): 
	console.print(Text(string,style="bold red"))
	
def gprint(string): 
	console.print(Text(string,style="bold green"))

def connect(hostname, port, username, password):
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	bprint("Connecting.............")
	ssh_client.connect(hostname=hostname, port=port,username=username, password=password)
	return ssh_client

def get_shell(ssh_client):
	shell = ssh_client.invoke_shell()
	return shell

def send_cmd(shell,cmd):
	print(f"Sending...{cmd}")
	shell.send(cmd+"\n")
	time.sleep(1)

def show(shell):
	output = shell.recv(10000)
	return output.decode()

def close(ssh_client):
	if ssh_client.get_transport().is_active() == True:
		bprint("Disconnecting.............")
	ssh_client.close()

def menu():
	print("1. Display available RAM")
	print("2. Display uptime")
	print("3. Display Load avearge")
	print("4. Routing Table")
	print("5.Exit")
if __name__ == "__main__":
	client=connect("127.0.0.1",22,"superuser","root")
	shell=get_shell(client)
	while True:
		menu()
		ch = Prompt.ask("Enter your option:	", choices=["1", "2", "3","4","5"])
		if ch == "1":
			send_cmd(shell,"free -m")
			output1 = show(shell)
			gprint(output1)
		elif ch == "2":
			send_cmd(shell,"uptime")
			output2 = show(shell)
			yprint(output2)
		elif ch == "3":
			send_cmd(shell,"cat /proc/loadavg")
			output3 = show(shell)
			bprint(output3)
		elif ch == "4":
			send_cmd(shell,"ip route list")
			output4 = show(shell)
			gprint(output4)
		elif ch == "5":
			break
	close(shell)
