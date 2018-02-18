from subprocess import run

class FASTQC():
	def __init__(self):
		pass
	def install(self):
		command = 'conda install fastqc'
		run(command, shell=True)
	def run(self, fastq):
		command = 'fastqc {} -o output/'.format(fastq)
		run(command, shell=True)