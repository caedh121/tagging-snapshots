import boto3

session = boto3.Session(profile_name="default")
regions = ['us-east-1', 'ap-southeast-1']
for region in regions:
    ec2_resource = boto3.resource('ec2', region_name=region)
    ec2_client = boto3.client('ec2', region_name=region)
    all_snapshots = ec2_client.describe_snapshots(OwnerIds=['self'])['Snapshots']
    all_volumes = volumes = ec2_resource.volumes.all()
    volume_ids = []

    for volume in all_volumes:
        volume_ids.append(volume.id)

    for snap in all_snapshots:
        snap_id = snap['SnapshotId']
        volume_id = snap['VolumeId']
        print(snap_id, volume_id)
        if volume_id in volume_ids:
            volume_info = ec2_client.describe_volumes(VolumeIds=[volume_id])
            volume_tags = volume_info['Volumes'][0]['Tags']
            print(volume_tags)
             tag_snp = ec2_client.create_tags(
                Resources=[
                    snap_id,
                ],
                Tags=volume_tags
             )
             print(tag_snp)
