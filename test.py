import boto3

client = boto3.client('eks', region_name="eu-north-1")
cluster_names = client.list_clusters()['clusters']

for cluster_name in cluster_names:
    response = client.describe_cluster(
        name=cluster_name
    )
    cluster_info = response['cluster']
    cluster_status = cluster_info['status']
    cluster_endpoint = cluster_info['endpoint']
    cluster_version = cluster_info['version']

    print(f"Cluster {cluster_name} status is {cluster_status}")
    print(f"Cluster endpoint: {cluster_endpoint}")
    print(f"Cluster version: {cluster_version}")
    print("==========")