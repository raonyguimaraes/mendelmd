from django.core.management.base import BaseCommand, CommandError
from files.models import File
import os
from django.conf import settings
import time
from django.core.exceptions import ObjectDoesNotExist
import glob
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import datetime

class Command(BaseCommand):
    help = 'Import Files'

    def handle(self, *args, **options):
        print('Hello World Import Files')
        File.objects.all().delete()
        start_time = time.time()
        file_objs=[]
        #files = [x for x in os.walk('/projects/mendelmd/genomes/')]


        #prepare user dict
        users = User.objects.all()
        user_dict = {}
        for user in users:
            user_dict[slugify(user.username)] = user
        # print(sorted(user_dict.keys()))
        
        path = '/projects/mendelmd/genomes/'
        for root, directories, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(root,filename)
                # print(file_path)
                username = file_path.split('/')[4]
                user = ''
                if username in user_dict:
                    user=user_dict[username]
                elif username == 'public':
                    user=None
                else:
                    # print('cannot find username!')
                    # print(username)
                    #this user didn't exists in the production account, must have been created under another username
                    if username == 'korziner':
                        user=user_dict['k']
                        # print(user_dict['k'])

                if user != '':
                    basename = os.path.basename(file_path)
                    file_size = os.stat(file_path)
                    # print(file_size)
                    filename, file_extension = os.path.splitext(file_path)
                    if file_size.st_size >0:
                        file_obj = File(
                            name=basename,
                            user=user,
                            size=file_size.st_size,
                            #    last_modified=datetime.datetime.strptime(str(file_size.st_mtime), "%a %b %d %H:%M:%S %Y"),
                            #    creation_date=datetime.datetime.strptime(str(file_size.st_ctime), "%a %b %d %H:%M:%S %Y"),
                            extension=file_extension,
                            location=file_path
                        )
                        file_objs.append(file_obj)
                else:
                    print('cannot find user', username)
        print(len(file_objs))


        #import files from ufmg
        path = '/projects/backup/genomes_ufmg'
        for root, directories, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(root,filename)
                # print(file_path)
                username = file_path.split('/')[4]
                username = slugify(username)
                user = ''
                if username in user_dict:
                    user=user_dict[username]
                elif username == 'public':
                    user=None
                else:
                    print('cannot find username!', username)
                    print(username)
                    #this user didn't exists in the production account, must have been
                    # if username == 'Débora':
                    #     user=user_dict['debora']
                    # if username == 'andrey.leonardo':
                    #     user=user_dict['andreyleonardo']

                    #     # print(user_dict['k'])

                if user != '':
                    basename = os.path.basename(file_path)
                    file_size = os.stat(file_path)
                    # print(file_size)
                    filename, file_extension = os.path.splitext(file_path)
                    if file_size.st_size >0:
                        file_obj = File(
                            name=basename,
                            user=user,
                            size=file_size.st_size,
                            #    last_modified=datetime.datetime.strptime(str(file_size.st_mtime), "%a %b %d %H:%M:%S %Y"),
                            #    creation_date=datetime.datetime.strptime(str(file_size.st_ctime), "%a %b %d %H:%M:%S %Y"),
                            extension=file_extension,
                            location=file_path
                        )
                        file_objs.append(file_obj)
                else:
                    print('cannot find user', username)
        print(len(file_objs))
        File.objects.bulk_create(file_objs)

        elapsed_time = time.time() - start_time
        print('Importing Files Took {}'.format(elapsed_time))
