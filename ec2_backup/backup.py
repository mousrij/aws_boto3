import boto3
import json
import schedule
import time

ec2 = boto3.client('ec2')

def create_snapshot():
    volumes = ec2.describe_volumes(
        Filters=[
            {
                'Name':'tag:Environment',
                'Values': ['Production']

            }
        ]
    )

    for volume in volumes.get('Volumes'):
        print(volume['VolumeId'])
        new_snapshot = ec2.create_snapshot(
            VolumeId = volume['VolumeId']
        )
        print(f"{new_snapshot.get('StartTime')}: Created a new snapshot of volume {new_snapshot.get('VolumeId')}.")


schedule.every().minute.do(create_snapshot)


while True:
    schedule.run_pending()
    time.sleep(1)
    


