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
            '''
            To carry over all tags from the volume use the code below:
            '''
            tag-snp = client.create_tags(
                Resources=[
                   snap-id,
                ],
                Tags=volume-tags
            )
            '''
            The code below only carries over specific tags and their values
            Uncomment and adjust to your scenario
            '''
            '''
            for tags in volume_tags:
                if tags["Key"] == 'Customer':
                    customer = tags["Value"]
                    print(customer)
                if tags["Key"] == 'Environment':
                    environment = tags["Value"]
                    print(environment)
                if tags["Key"] == 'Application':
                    application = tags["Value"]
                    print(application)
            tag_snp = ec2_client.create_tags(
                Resources=[
                    snap_id,
                ],
                Tags=[
                     {
                         'Key': 'Customer',
                         'Value': customer,
                     },
                     {
                         'Key': 'Environment',
                         'Value': environment,
                     },
                     {
                         'Key': 'Application',
                         'Value': application,
                     },
                     {
                         'Key': 'Taggedby',
                         'Value': 'snp-tagging',
                     },
                 ],
                )
            print(tag_snp)
            '''
