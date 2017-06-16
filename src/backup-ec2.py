import os
import time
import boto3


def run_handler(event, context):
    ec2 = boto3.client('ec2')
    instance_id = os.environ['instance_id']
    instance_name = os.environ['instance_name']
    instance_description = os.environ['instance_description']
    time_stamp = time.strftime("%c")
    name_of_backup = 'Backup_' + instance_name + \
        '_' + time.strftime("%d_%m_%y_%H_%M")
    description = instance_description
    response_create_image = ec2.create_image(
        InstanceId=instance_id, Name=name_of_backup, Description=description + time_stamp)
    # Get AMI Id
    image_id = response_create_image['ImageId']
    # From AMI Id get Snapshots Ids
    response_images = ec2.describe_images(ImageIds=[image_id])
    print("New AMI Id: " + image_id + " Details: ")
    print(response_images['Images'][0])
    # Tag AMI
    response_tag_image = ec2.create_tags(Resources=[image_id], Tags=[{'Key': 'Origin', 'Value': 'aws-lambda'}, {'Key': 'Name', 'Value': name_of_backup}, {'Key': 'Environment', 'Value': 'dev'}, {
        'Key': 'backup:instance_id', 'Value': instance_id}, {'Key': 'backup:timestamp', 'Value': time_stamp}, ])
    print(response_tag_image)
