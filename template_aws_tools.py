import boto3
import boto3.session
import argparse
import yaml
import os


def new_aws_client(profile,client):
    session = boto3.session.Session(profile_name=profile)
    return session.client(client)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="AWS utility")
    parser.add_argument("--", dest='', default='', action='store', help="")
    parser.add_argument("--", dest='', action='store', help='')
    args = parser.parse_args()

    aws_profile = args.profile

    as_client = new_aws_client(aws_profile,'autoscaling')
    ec2_client = new_aws_client(aws_profile, 'ec2')
    as_groups = as_client.describe_auto_scaling_groups()
