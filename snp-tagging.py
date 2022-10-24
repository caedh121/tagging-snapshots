"""
Created by Adrian Estrada
"""
import boto3
'''
Credentials 
Use the code below to inherit aws credentials from ~/.aws/credentials:
session = boto3.Session(profile_name="default")

Use the code below to inherit aws credentials from attached instance role:
from boto3.session import Session

To run as an AWS Lambda function there is no need to use credentials,
as they are provided by Lambda
'''

session = boto3.Session(profile_name="default")
regions = [ 'ap-southeast-1','sa-east-1','us-east-1','eu-west-1','eu-west-2']
orphan_snp = []
orphan_snp_total_size = []
non_orphan_snp = []
all_snp = []
all_snp_total_size = []

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
        vol_size = snap['VolumeSize']
        all_snp.append(snap_id)
        all_snp_total_size.append(vol_size)
        print(snap_id, volume_id)
        if volume_id in volume_ids:
            volume_info = ec2_client.describe_volumes(VolumeIds=[volume_id])
            volume_tags = volume_info['Volumes'][0]['Tags']
            non_orphan_snp.append(snap_id)
            print(volume_tags)
            '''
            To carry over all tags from the volume use the code below:
            '''
            '''
            tag-snp = client.create_tags(
                Resources=[
                   snap-id,
                ],
                Tags=volume-tags
            )
            '''
            '''
            The code below only carries over specific tags and their values
            Uncomment and adjust to your scenario
            #'''
            for tags in volume_tags:
                if tags["Key"] == 'Customer':
                    customer = tags["Value"]
                    print(customer)
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
                                'Key': 'Taggedby',
                                'Value': 'snp-tagging',
                            },
                             ])
                if tags["Key"] == 'Environment':
                    environment = tags["Value"]
                    print(environment)
                    tag_snp = ec2_client.create_tags(
                        Resources=[
                            snap_id,
                        ],
                        Tags=[
                            {
                                'Key': 'Environment',
                                'Value': environment,
                            }, ])
                if tags["Key"] == 'Application':
                    application = tags["Value"]
                    print(application)
                    tag_snp = ec2_client.create_tags(
                        Resources=[
                            snap_id,
                        ],
                        Tags=[
                            {
                                'Key': 'Application',
                                'Value': application,
                            }, ])

        else:
            orphan_snp.append(snap_id)
            orphan_vol_size = snap['VolumeSize']
            orphan_snp_total_size.append(orphan_vol_size)
            if volume_id not in volume_ids:
                tag_snp = ec2_client.create_tags(
                    Resources=[
                        snap_id,
                    ],
                    Tags=[
                        {
                            'Key': 'isVolumeOrphan',
                            'Value': 'yes',
                        },
                        {
                            'Key': 'Taggedby',
                            'Value': 'snp-tagging',
                        },
                    ])
print('Orphans: ',len(orphan_snp))
print('Non Orphans: ',len(non_orphan_snp))
print('All: ',len(all_snp))
orphan_snp_sum = sum(orphan_snp_total_size)
all_snp_sum = sum(all_snp_total_size)
print('Orphans total size ',(orphan_snp_sum),'GiB')
print('All total size ',(all_snp_sum),'GiB')
