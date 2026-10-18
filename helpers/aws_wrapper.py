import os
import boto3
from time import sleep
from subprocess import run
from django.conf import settings

class AWS:

    def __init__(self):
        pass

    def main(self):
        pass

    def launch(self, config):
        print('Launch Worker')

        worker = {}

        session = boto3.Session(profile_name=config['profile_name'])

        ec2 = session.resource('ec2', region_name=config['region_name'])
        print('Create instance')
        client = session.client('ec2', region_name=config['region_name'])

        response = client.request_spot_instances(
            DryRun=False,
            SpotPrice=config['spot_price'],
            InstanceCount=1,
            Type='one-time',
            LaunchSpecification={
                'ImageId': config['image_id'],
                'KeyName': config['KeyName'],
                'SubnetId': config['SubnetId'],
                'InstanceType': config['instance_type'],
                'Placement': {
                    'AvailabilityZone': config['AvailabilityZone'],
                },
                'EbsOptimized': True,
                'SecurityGroupIds': [
                    config['SecurityGroupIds'],
                ],
                #'IamInstanceProfile': {
                #    'Name': config['IamInstanceProfile'],
                #}
            }
        )

        print(response)
        # this works!
        sir_id = response['SpotInstanceRequests'][0]['SpotInstanceRequestId']
        print(sir_id)

        fulfilled = False
        while not fulfilled:
            try:
                response = client.describe_spot_instance_requests(
                    DryRun=False,
                    SpotInstanceRequestIds=[
                        sir_id,
                    ]
                )
                # print(response)
                instance_id = response['SpotInstanceRequests'][0]['InstanceId']
                fulfilled = True
            except KeyError:
                print('Sleep 30...')
                sleep(30)
                pass

        print(instance_id)

        instance = ec2.Instance(instance_id)
        tag = instance.create_tags(
            Tags=[
                {
                    'Key': 'Name',
                    'Value': 'rockbio Worker'
                }
            ]
        )

        instance.wait_until_running()
        print(instance.private_ip_address)
        worker = {
            'id': instance_id,
            'ip': instance.private_ip_address,
        }
        return(worker)

    def terminate(self, instance_id):
        print('Terminate Worker')
        ec2 = boto3.resource('ec2', region_name='eu-west-1')
        print('Create instance')
        client = boto3.client('ec2', region_name='eu-west-1')
        response = client.terminate_instances(
            InstanceIds=[instance_id,],
            DryRun=False
        )
        return(response)

    def install(self, ip):

        print('Install Worker')

        # local '~' is expanded with expanduser (the shell did this before);
        # the remote '~/' stays literal and is resolved by scp/sshd on the target.
        opts = ['-o', 'StrictHostKeyChecking=no']
        target = 'ubuntu@%s' % (ip)

        run(['scp', '-r'] + opts + [os.path.expanduser('~/.aws'), target + ':~/'])

        run(['scp'] + opts + [os.path.expanduser('~/.ssh/id_rsa'), target + ':~/.ssh'])

        run(['scp'] + opts + [os.path.expanduser('~/.ssh/id_rsa.pub'), target + ':~/.ssh'])

        run(['scp'] + opts + [os.path.expanduser('~/.ssh/config'), target + ':~/.ssh'])

        run(['scp'] + opts + ['scripts/install_worker_aws.sh', target + ':~/'])

        run(['scp'] + opts + ['/projects/scripts/local_settings.py', target + ':~/'])

        # '>' redirection, '&' backgrounding and ';'-style chaining are intentionally
        # still interpreted, but by the REMOTE shell: ssh receives this as one argument.
        remote_command = """nohup bash install_worker_aws.sh >nohup.out 2>&1 & sleep 2"""

        run(['ssh'] + opts + ['-t', target, remote_command])

    def update(self,ip):

        opts = ['-o', 'StrictHostKeyChecking=no']
        target = 'ubuntu@%s' % (ip)

        run(['scp'] + opts + ['scripts/update_worker_aws.sh', target + ':~/'])

        # Executed by the remote shell (redirection/background/chaining), see install().
        remote_command = """nohup bash update_worker_aws.sh >nohup.out 2>&1 & sleep 5"""

        print(['ssh'] + opts + ['-t', target, remote_command])

        run(['ssh'] + opts + ['-t', target, remote_command])

    def upload(source,dest):

        dest = '{}{}'.format(settings.UPLOAD_FOLDER, dest)

        run(['aws', 's3', 'sync', '--profile', str(settings.UPLOAD_FOLDER_PROFILE), source, dest])




if __name__ == '__main__':
    worker = AWS().main()