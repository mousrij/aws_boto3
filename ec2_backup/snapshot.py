import boto3
from operator import itemgetter

ec2 = boto3.client('ec2', region_name='eu-north-1')

volume_id = ec2.describe_volumes(
    Filters=[
        {
            'Name':'tag:Environment',
            'Values': ['Production']
        }
    ]
)['Volumes'][0]['VolumeId']


snap = ec2.describe_snapshots(
    OwnerIds=['self'],
    Filters=[
        {
            'Name':'volume-id',
            'Values': [volume_id]
        }
    ]
)['Snapshots']

sort = sorted(snap, key=itemgetter('StartTime'))
sort_lambda = sorted(snap, key= lambda x: x['StartTime'], reverse=True)


#deleting snapshot from EBS

# for snap in sort_lambda:
#     response = ec2.delete_snapshot(
#             SnapshotId=snap.get('SnapshotId')
#         )
#     print(f"HTTP status code of delete-snapshot response: {response.get('ResponseMetadata').get('HTTPStatusCode')}")

snapshot_id_0 = sort_lambda[0]


#Create new volume with snapshot attached to it

new_volume = ec2.create_volume(
    SnapshotId=snapshot_id_0,
    AvailabilityZone='eu-norht-1a',
    TagSpecifications=[
    {
        'ResourceType': 'volume',
        'Tags': [
            {
                'Key': 'Environment',
                'Value': 'Production'
            }
        ]
    }
)['VolumeId']

ec2_resource = boto.resource('ec2', region_name='eu-north-1')

while True:
    print("====")
    new_vol = ec2_resource.Volume(new_volume)
    print(new_volume.state)
     