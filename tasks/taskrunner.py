import datetime
import subprocess
import sys, os
from subprocess import check_output
from threading import Thread

# sys.path.append('/home/raony/dev/rockbio')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings

from tasks.models import Task
class TaskRunner(object):
    def __init__(self,task_id):
        self.task_id=task_id

    def run(self):
        print('Run Task')
        task_id = self.task_id

        tstart = datetime.datetime.now()
        print(tstart)#

        print(task_id)
        task=Task.objects.get(id=2)
        print(task)
        #ok, now transfer it!
        print('ok, now transfer it!')
        transfer = Thread(target=self.transfer(task_id))
        transfer.daemon = True
        transfer.start()
        print('Return Safely')


    def transfer(self,task_id):
        print('transfer it now!')
        # command = 'bash '
        task = Task.objects.get(pk=task_id)
        task.status='running'
        task.save()

        data=task.manifest
        if data['task_type']=='transfer_nf-tower_local':
            print('transfer_nf-tower_lxd')
            ip_origin=data['server_ip']
            ip_dest = data['server_destination']
            command = 'bash scripts/transfer_nf-tower_to_lxd.sh {} {} > work_dir/out.{}.log 2>&1'.format(ip_origin,ip_dest,task_id)#
            try:
                output = check_output(command, shell=True, stderr=subprocess.STDOUT).decode()
                print(output)
            except subprocess.CalledProcessError as e:
                print(e)
                print(e.stdout.decode())
                # output=e.stdout
                output = str(e.stdout.decode())
            #transfer dns
            print('transfer dns afterwards!')

            # run_local_command(command)

