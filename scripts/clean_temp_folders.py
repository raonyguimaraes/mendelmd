genomes_path = '../genomes'

#walk in path getting the name fo the folder
import os
import shutil

# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk(genomes_path):
    
    path = root.split('/')
    
    if path[-1] == 'ann_sample':
    	# print path
    	shutil.rmtree("/".join(path))
    	# os.rmdir(path)
#    print (len(path) - 1) *'---' , os.path.basename(root)       
#    for file in files:
#        print len(path)*'---', file

#remove folder
