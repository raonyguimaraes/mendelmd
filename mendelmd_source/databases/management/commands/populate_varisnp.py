from django.core.management.base import BaseCommand, CommandError
from databases.models import VariSNP
import os

class Command(BaseCommand):
    help = 'Populate VariSNP'

    def handle(self, *args, **options):
        self.stdout.write('Populate VariSNP')
        file = open('data/neutral_snv_2014-06-24.csv', 'r')
        header = file.readline()

        for line in file:
            variant = line.split('\t')
            snpid = 'rs'+variant[0]
            snp = VariSNP(dbsnp_id=snpid)
            snp.save()
        print("Finished Inserting Data")


            
            
        #get all individuals
        # individuals = Individual.objects.all().order_by('id')
        # for individual in individuals:
        # 	print individual.id
        # 	print individual.variants_file
        # 	#get user folder
        # 	filepath = str(individual.variants_file).split('/')
        # 	user = filepath[1]
        # 	print user
        # 	#now copy to destiny
        # 	orig_path = 'genomes/'
        # 	path = 'backup'
        # 	d = '%s/%s' % (path, user)
        # 	#create user dir
        # 	if not os.path.exists(d):
        # 		os.makedirs(d)
        # 	command = 'cp %s/%s %s/' % (orig_path, individual.variants_file, d)
        # 	os.system(command)


