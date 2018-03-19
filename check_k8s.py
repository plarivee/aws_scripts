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
    parser.add_argument("--profile", dest='profile', default='', action='store', help="Use this profile for aws")
    parser.add_argument("--context", dest='context', action='store', help='filter which cluster to show')
    args = parser.parse_args()

    aws_profile = args.profile
    if args.context:
        k8s_context= args.context

    # get list of k8s AutoScaling groups
    as_client = new_aws_client(aws_profile,'autoscaling')
    ec2_client = new_aws_client(aws_profile, 'ec2')
    as_groups = as_client.describe_auto_scaling_groups()
    as_group_servers = {}
    k8s_group_servers = []
    error = False
    kube_ctl_servers = os.popen('kubectl get nodes --context %s | grep -v NAME | awk {\'print $1\'} | sort -u' % k8s_context).read()
    for server in kube_ctl_servers.splitlines():
        k8s_group_servers.append(server)

    for group in as_groups['AutoScalingGroups']:
        if k8s_context in group['AutoScalingGroupName']:
            as_group_name = (group['AutoScalingGroupName'])
            for instance in group['Instances']:
                i_id=instance['InstanceId']
                ec2_info = ec2_client.describe_instances(InstanceIds=[instance['InstanceId']])
                for i in ec2_info['Reservations']:
                    if i['Instances'][0]['PrivateDnsName'] not in k8s_group_servers:
                        print("%s \t %s is missing in k8s" %(i_id,i['Instances'][0]['PrivateDnsName']))
                        error = True
    if not error:
        print("All servers in AS Group found in k8s context")
        print(yaml.dump(k8s_group_servers, default_flow_style=False))

    
#https://github.com/kubernetes-client/python-base/pull/48
#    config.load_kube_config(context='k8s.dev.cloud')
#    v1 = client.CoreV1Api()
#    #print("Listing pods with their IPs:")
#    ret = v1.list_node()
#     print(ret)   