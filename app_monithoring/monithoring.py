# 1st things :
# make a query with module request from the ec2 server that host a docker engine 
# query for the ec2 address to interrogate nginx home page from the container

import requests
import time
import paramiko 
import boto3

response = requests.get("http://51.20.122.112:8080")

# print(response.text)

# 2nd thing :
# establish an ssh connection with paramiko 
# pip install paramiko 

# now we do need the 
def send_notification(msg=None):
    if msg is None:
        print("Notification!!")
    else:
        print(f"Notification !! \n >> {msg}")


def restart_container():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect(hostname='51.20.122.112', username='ec2-user', key_filename='.\\key.ppk')
    stdin, stdout, stderr = client.exec_command('docker ps')

    print(stdout.readlines())
    print("======")
    

    stdin, stdout, stderr = client.exec_command("docker ps -a | grep nginx | awk 'split($0, a); print(a[1])'")
    containerId = stdout.readlines()
    
    print("======")
    stdin, stdout, stderr = client.exec_command(f"docker stop {containerId}")
    print(stdout.readlines())
    time.sleep(30)

    print("======")
    #start the container again 
    stdin, stdout, stderr = client.exec_command(f"docker start {containerId}")
    print(stdout.readlines())
    client.close()

# Now we have the objective to monitor the container i.e nginx server
# what is the nginx server is down 
# we need to restart the container > docker restart c-id
# take the first program with request 



# 3rd thing :
# we need to make a restart_server_and_container if the application level not responding

def restart_server_and_container():
    client = boto3.client('ec2', region_name='eu-north-1')
    status = client.describe_instances(
        Filters=[
            {
                'Name': 'instance-id',
                'Values': ['i-05e4199f22f5a32b6']  # Your Docker instance ID
            }
        ]
    )['Reservations'][0]['Instances'][0]['State']['Name']
    
    
    
    

    time.sleep(300)

    while True:
        if status in ('pending', 'running'):
            time.sleep(30)
            if status == 'running':
                restart_container()
                break
        
        restart_response = client.reboot_instances(
            InstancesIds = [
                'i-05e4199f22f5a32b6'
            ]
        )
    

    












if response.status_code == 200:
    print("Application is running successfully !!")
    print("nginx is up!") 
    

else:
    try:

        # but before we need to grep the nginx id container :
        print('Application Down. Fix it!')
        msg = f"Application returned {response.status_code}"
        send_notification(msg)
        restart_container()  # <---
    except Exception as e:
        print(f"Connection error happened: {e}")
        msg = 'Application not accessible at all'
        send_notification(msg)
        restart_server_and_container()



