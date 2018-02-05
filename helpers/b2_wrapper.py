from subprocess import run
import os

class B2():
	def __init__():

	def main():
		print('main')

	def install():
		command = '''
		git clone https://github.com/Backblaze/B2_Command_Line_Tool.git
		cd B2_Command_Line_Tool
		python setup.py build
		python setup.py install
		b2 authorize-account
		'''
		run(command,shell=True)

	def upload(bucket, file):
		
		basename = os.path.basename(file)
		command = 'b2 upload-file mendelmd {} {}'.format(file, basename)
		run(command, shell=True)

		# {
		# "action": "upload",
		# "fileId": "4_z9c8c149aa77346e564160516_f109f885ab1209044_d20180131_m235956_c000_v0001058_t0036",
		# "fileName": "test",
		# "size": 0,
		# "uploadTimestamp": 1517443196000
		# }

	def download(bucket, file):

		basename = os.path.basename(file)
		command = 'b2 download-file-by-name mendelmd {} {}'.format(file, file)
		run(command, shell=True)