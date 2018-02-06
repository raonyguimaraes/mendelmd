from subprocess import run

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

		# Options:

		#   --bootscript=""           Assign a bootscript
		#   --commercial-type=X64-2GB Create a server with specific commercial-type C1, C2[S|M|L], X64-[2|4|8|15|30|60|120]GB, ARM64-[2|4|8]GB
		#   -e, --env=""              Provide metadata tags passed to initrd (i.e., boot=rescue INITRD_DEBUG=1)
		#   -h, --help=false          Print usage
		#   --ip-address=dynamic      Assign a reserved public IP, a 'dynamic' one or 'none'
		#   --name=""                 Assign a name
		#   --tmp-ssh-key=false       Access your server without uploading your SSH key to your account
		#   -v, --volume=""           Attach additional volume (i.e., 50G)

		# Examples:

		#     $ scw create docker
		#     $ scw create 10GB
		#     $ scw create --bootscript=3.2.34 --env="boot=live rescue_image=http://j.mp/scaleway-ubuntu-trusty-tarball" 50GB
		#     $ scw inspect $(scw create 1GB --bootscript=rescue --volume=50GB)
		#     $ scw create $(scw tag my-snapshot my-image)
		#     $ scw create --tmp-ssh-key 10GB

		command = 'scw create --region=ams1 ubuntu 150GB'
		run(command,shell=True)
		

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