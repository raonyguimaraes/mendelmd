#!/usr/bin/python3
from subprocess import run,check_output
import os
apps = {}

def parse_apache_file(file):
    app={}
    apache_file=open(file,'r').readlines()
    for line in apache_file:
        # print(line)
        if 'DocumentRoot' in line:
            app['document_root']=line.strip().split()[1]

    for file in os.listdir(app['document_root']):
        # print(file)
        if file=='wp-config.php':
            app['app_type']='wordpress'
            app['source']='apache'
    return(app)

def parse_nginx_file(file):
    app={}
    nginx_file=open(file,'r').readlines()
    # print(nginx_file)
    for line in nginx_file:
        # print(line)
        if '\troot' in line:
            app['document_root']=line.strip().split()[1].replace(';','')
    if 'document_root' in app:
        for file in os.listdir(app['document_root']):
            # print(file)
            if 'jitsy' in file:
                app['app_type']='jitsy'
                app['source']='nginx'
    else:
        app['app_type'] = 'unknown'
        app['source']='nginx'
    return(app)

nginx_path='/etc/nginx/sites-available/'
if os.path.isdir(nginx_path):
    print('nginx')
    for file in os.listdir('/etc/nginx/sites-available/'):
        if ('ssl' not in file) and ('default' not in file):
            print(file)
            appname = file.replace('.conf', '')
            apps[appname] = parse_nginx_file(nginx_path + file)

apache_path='/etc/apache2/sites-available/'
if os.path.isdir(apache_path):
    # print('apache')
    for file in os.listdir(apache_path):
        # print(file)
        if ('ssl' not in file) and ('default' not in file):
            # print(file)
            appname=file.replace('.conf','')
            apps[appname]=parse_apache_file(apache_path+file)
print('now apps object')
print(apps)
# command = 'mkdir /mnt/hd'
# run(command,shell=True)

# command = 'mount /dev/sda1 /mnt/hd'
# run(command,shell=True)

# #check if file exists, if not create it
# #cat pub_key >> ~/.ssh/authorized_keys
# authorized_key = open('/root/.ssh/authorized_keys','r').readlines()[0]
# print(authorized_key)

# path='/mnt/hd/root/.ssh/authorized_keys'
# if os.path.isfile(path):
#     with open(path, "r+") as file:
#         for line in file:
#             if authorized_key in line:
#                break
#         else: # not found, we are at the eof
#             file.write(authorized_key) # append missing data
# else:
#     command = 'cp /root/.ssh/authorized_keys /mnt/hd/root/.ssh/authorized_keys'
#     run(command,shell=True)