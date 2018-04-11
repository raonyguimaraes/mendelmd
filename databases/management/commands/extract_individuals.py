from django.core.management.base import BaseCommand, CommandError
from individuals.models import Individual
import os

class Command(BaseCommand):
    help = 'Extract Individuals'

    def handle(self, *args, **options):
        self.stdout.write('Hello World')
        #get all individuals
        individuals = Individual.objects.all().order_by('id')
        for individual in individuals:
        	print(individual.id)
        	print(individual.variants_file)
        	#get user folder
        	filepath = str(individual.variants_file).split('/')
        	user = filepath[1]
        	print(user)
        	#now copy to destiny
        	orig_path = 'genomes/'
        	path = 'backup'
        	d = '%s/%s' % (path, user)
        	#create user dir
        	if not os.path.exists(d):
        		os.makedirs(d)
        	command = 'cp %s/%s %s/' % (orig_path, individual.variants_file, d)
        	os.system(command)
            