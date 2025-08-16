import boto3 
import schedule
import time

ec2_client = boto3.resource('ec2', 'eu-north-1')


instances = ec2_client.instances.all()


def check_status():
    for instance in instances:
        print(f"ID: {instance.id} | State: {instance.state['Name']} | Type: {instance.instance_type}")
    print("===========")

schedule.every(5).seconds.do(check_status)

while True:
    schedule.run_pending()
    time.sleep(1)
