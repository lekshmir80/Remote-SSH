import paramiko
import time
import datetime
from rich.console import Console
from rich.text import Text

console = Console()
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
timestamp = str(datetime.datetime.now().timestamp()).split(".")[0]

def yprint(string):
	console.print(Text(string,style="bold yellow"))	
def gprint(string): 
	console.print(Text(string,style="bold green"))
	
gprint("Connecting........")
ssh_client.connect(hostname="127.0.0.1", port=22,
                   username="superuser", password="root")
                   
gprint("Compressing..........")
stdin, stdout, stderr = ssh_client.exec_command("tar -cvf backup_projects_1_"+timestamp+".bz2 /home/superuser/Python_Training_UST/projects_1/\n")
yprint(stdout.read().decode())
time.sleep(2)

gprint("Copying..........")
ftp_client = ssh_client.open_sftp() 
ftp_client.get(remotepath="/home/superuser/backup_projects_1_"+timestamp+".bz2",localpath="/home/superuser/Python_Training_UST/backup_projects_1_"+timestamp+".bz2") 

ftp_client.close()

if ssh_client.get_transport().is_active() == True:
    gprint("Disconnecting.............")
    ssh_client.close()

