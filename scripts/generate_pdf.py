

import os

extensions = ['py', 'txt', 'rst', 'js', 'css', 'html']
for ext in extensions:
    command = 'find /home/raony/development/rockbio_master/ -name "*.%s" > %s_files.txt' % (ext,ext)
    os.system(command)
    file_list = open('%s_files.txt'% (ext), 'r')
    file_counter = 0
    for file in file_list:
	#generate a pdf
        #print file
	#die()
	command = 'enscript -E -q -Z -p - -f Courier10 %s | ps2pdf - output/%s.%s.pdf' % (file.strip(), ext, file_counter)
	#print command
	
	os.system(command)
	file_counter += 1 
	#file_content = open('%s'% (file.strip()), 'r')
	 #for line in file_content:
	#		print line
    #now integrate all pdf
    command = 'convert output/%s.*.pdf integration_%s.pdf' % (ext, ext)
    os.system(command)
