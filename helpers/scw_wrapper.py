from subprocess import run, check_output
import subprocess
from time import sleep


class SCW():

	def __init__(self):
		pass

	def main(self):
		print('main')

	def install():
		command = '''
		sudo apt-get update
		sudo apt-get -y upgrade
		wget https://storage.googleapis.com/golang/go1.9.2.linux-amd64.tar.gz
		sudo tar -xvf go1.9.2.linux-amd64.tar.gz
		sudo mv go /usr/local
		export GOROOT=/usr/local/go

		export GOPATH=$HOME/go

		export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
		'''
		# command = 'GO15VENDOREXPERIMENT=1 go get -u github.com/scaleway/scaleway-cli/cmd/scw'
		run(command,shell=True)

	def launch(self, worker_type=None):
		# Create a new server but do not start it.
		result = {}
		# Options:

		command = 'scw --region=ams1 create --name="mendelmd_worker" ubuntu-xenial'#--volume=150GB --commercial-type=X64-15GB 
		output = run(command,shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()


		short_id = output.split('-')[0]
		
		result['id'] = short_id

		command = 'scw --region=ams1 start {}'.format(short_id)
		output = run(command,shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

		flag = True
		while(flag):
			command = 'scw --region=ams1 ps -a'
			output = run(command,shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()			
			for line in output:
				# print(line)
				row = line.split()
				# print(row)
				if row[0] == short_id:
					if row[5] == 'running':
						ip = row[6]
						result['ip'] = ip
						flag = False
					else:
						print('Waiting {} to start'.format(short_id))
						sleep(30)

		command = 'ssh-keygen -f ~/.ssh/known_hosts -R {}'.format(ip)
		print(command)

		output = run(command,shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
		print(output)
		return(result)

	def terminate(self, id):
		command = 'scw --region=ams1 stop -t {}'.format(id)
		output = run(command,shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()


		# scw ps
		# scw create ubuntu
		# scw start 5cf8058e
		# scw exec test01 echo "Hello world!"
		# scw help



# 1  FROM scaleway/ubuntu:lastest
# 2  MAINTAINER
# 3  
# 4  # Prepare rootfs for image-builder.
# 5  # This script prevent aptitude to run services when installed
# 6  RUN /usr/local/sbin/builder-enter
# 7  
# 8   # Your app
# 9  
# 10 # Install packages
# 11 RUN apt-get -q update && \
# 12  apt-get -y -qq upgrade && \
# 13  apt-get install -y -qq cowsay
# 14 
# 15 # Add local files from the patches directory
# 16 COPY ./patches/ /
# 17 
# 18 # End
# 19 
# 20 # Clean rootfs from image-builder.
# 21 # Revert the builder-enter script
# 22 RUN /usr/local/sbin/builder-leave		