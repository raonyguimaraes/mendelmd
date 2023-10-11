#!/usr/bin/python3
from subprocess import run,check_output
import os
import json
#apps = {
#   'wordpress':{'app_folder':'grazyna'},
#   'wordpress':{'app_folder':'raony'}
#}
def main():
    apps = []
    #parse apache
    apache_path='/etc/apache2/sites-available/'
    if os.path.isdir(apache_path):
        # print('apache')
        for file in os.listdir(apache_path):
            # print(file)
            if ('ssl' not in file) and ('default' not in file):
                # print(file)
                appname = file.replace('.conf', '')
                app = {
                    'name': appname,
                    'source': 'apache2',
                    'apache_document_root': []
                }

                apache_file=open(apache_path+file,'r').readlines()
                for line in apache_file:
                    # print(line)
                    if 'DocumentRoot' in line:
                        app['apache_document_root'].append(line.strip().split()[1])
                apps.append(app)
    #nginx
    nginx_path='/etc/nginx/sites-available/'
    if os.path.isdir(nginx_path):
        # print('nginx')
        for file in os.listdir('/etc/nginx/sites-available/'):
            if ('ssl' not in file) and ('default' not in file):
                print(file)
                appname = file.replace('.conf', '')
                app = {
                    'name': appname,
                    'source': 'nginx',
                    'nginx_document_root': [],
                    'nginx_server_name': [],
                    'nginx_proxy_pass': []
                }

                # apps[appname] = parse_nginx_file(nginx_path + file)
                nginx_file=open(nginx_path+file,'r').readlines()
                # print(nginx_file)
                for line in nginx_file:
                    # print(line)
                    if 'root' in line and '#root' not in line:
                        docroot=line.strip().split()[1].replace(';','')
                        if docroot not in app['nginx_document_root']:
                            app['nginx_document_root'].append(docroot)
                    if 'server_name' in line:
                        server_name=line.strip().split()[1].replace(';','')
                        if server_name not in app['nginx_server_name']:
                            app['nginx_server_name'].append(server_name)
                    if 'proxy_pass' in line:
                        proxy_pass=line.strip().split()[1].replace(';','')
                        if proxy_pass not in app['nginx_proxy_pass']:
                            app['nginx_proxy_pass'].append(proxy_pass)
                # if 'document_root' in app:
                #     for file in os.listdir(app['document_root']):
                #         # print(file)
                #         if 'jitsy' in file:
                #             app['app_type']='jitsy'
                # else:
                #     app['app_type'] = 'unknown'
                apps.append(app)
    # #check nf-tower
    nftower_path='/root/nf-tower'
    if os.path.isdir(nftower_path):
        app = {
            'name': 'nftower',
            'app_folder':nftower_path
        }
        apps.append(app)


    galaxy_path='/root/galaxy'
    if os.path.isdir(galaxy_path):
        app = {
            'name': 'galaxy',
            'app_folder': galaxy_path
        }
        apps.append(app)
    #
    discourse_path='/var/discourse'
    if os.path.isdir(discourse_path):
        app = {
            'name': 'discourse',
            'app_folder': discourse_path
        }
        apps.append(app)

    #now check apps for credentials
    # print('now check apps')
    for idx, app in enumerate(apps):
        if 'apache_document_root' in app:
            # print('apache2')
            for docroot in app['apache_document_root']:
                wordpress_file_path=docroot+'/wp-config.php'
                # print(wordpress_file_path)
                if os.path.isfile(wordpress_file_path):
                    # print('wordpress_file_path exists!')
                    apps[idx]['app_type']='wordpress'
                    wordpress_file = open(wordpress_file_path,'r').readlines()
                    for line in wordpress_file:
                        # define('DB_NAME', 'xxx');
                        # define('DB_USER', 'xxx');
                        # define('DB_PASSWORD', 'xxx');
                        if line.startswith("define('DB_NAME'"):
                            dbname=line.split(' ')[1][1:-3]
                            apps[idx]['db_name'] = dbname
                        if line.startswith("define('DB_USER'"):
                            db_user=line.split(' ')[1][1:-3]
                            apps[idx]['db_user'] = db_user
                        if line.startswith("define('DB_PASSWORD'"):
                            db_pass=line.split(' ')[1][1:-3]
                            apps[idx]['db_pass'] = db_pass
                        # print(line)
        if 'nginx_proxy_pass' in app:
            for nginx_proxy_pass in app['nginx_proxy_pass']:
                proxy_path=nginx_proxy_pass
                print('nginx_proxy_pass', proxy_path)
                proxy_port=proxy_path.split(':')[-1].replace('/','')
                print(proxy_port,'proxy_port')


    # print(apps)
    with open('apps.json', 'w') as fp:
        json.dump(apps, fp)



if __name__ == '__main__':
    main()

# def parse_nginx_file(file):
#     app={}
#     nginx_file=open(file,'r').readlines()
#     # print(nginx_file)
#     for line in nginx_file:
#         # print(line)
#         if '\troot' in line:
#             if 'document_root' not in app:
#                 app['document_root']=[]
#             docroot=line.strip().split()[1].replace(';','')
#             app['document_root'].append(docroot)
#     if 'document_root' in app:
#         for file in os.listdir(app['document_root']):
#             # print(file)
#             if 'jitsy' in file:
#                 app['app_type']='jitsy'
#     else:
#         app['app_type'] = 'unknown'
#     return(app)
#
# nginx_path='/etc/nginx/sites-available/'
# if os.path.isdir(nginx_path):
#     print('nginx')
#     for file in os.listdir('/etc/nginx/sites-available/'):
#         if ('ssl' not in file) and ('default' not in file):
#             print(file)
#             appname = file.replace('.conf', '')
#             apps[appname] = parse_nginx_file(nginx_path + file)
#
# apache_path='/etc/apache2/sites-available/'
# if os.path.isdir(apache_path):
#     # print('apache')
#     for file in os.listdir(apache_path):
#         # print(file)
#         if ('ssl' not in file) and ('default' not in file):
#             # print(file)
#             appname=file.replace('.conf','')
#             print(appname)
#             apps[appname]=parse_apache_file(apache_path+file)
#
# #check nf-tower
# nftower_path='/root/nf-tower'
# if os.path.isdir(nftower_path):
#     apps['nftower'] = {}
#     apps['nftower']['app_folder']=nftower_path
#
# galaxy_path='/root/galaxy'
# if os.path.isdir(galaxy_path):
#     apps['galaxy'] = {}
#     apps['galaxy']['app_folder']=galaxy_path
#
# discourse_path='/var/discourse'
# if os.path.isdir(discourse_path):
#     apps['discourse'] = {}
#     apps['discourse']['app_folder']=discourse_path
#
# print('now apps object')
# print(apps)
# # command = 'mkdir /mnt/hd'
# # run(command,shell=True)
#
# # command = 'mount /dev/sda1 /mnt/hd'
# # run(command,shell=True)
#
# # #check if file exists, if not create it
# # #cat pub_key >> ~/.ssh/authorized_keys
# # authorized_key = open('/root/.ssh/authorized_keys','r').readlines()[0]
# # print(authorized_key)
#
# # path='/mnt/hd/root/.ssh/authorized_keys'
# # if os.path.isfile(path):
# #     with open(path, "r+") as file:
# #         for line in file:
# #             if authorized_key in line:
# #                break
# #         else: # not found, we are at the eof
# #             file.write(authorized_key) # append missing data
# # else:
# #     command = 'cp /root/.ssh/authorized_keys /mnt/hd/root/.ssh/authorized_keys'
# #     run(command,shell=True)