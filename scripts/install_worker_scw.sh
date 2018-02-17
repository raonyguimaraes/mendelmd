sudo apt update
sudo apt -y upgrade
sudo apt install git

mkfs -t ext4 /dev/vdb
mkdir -p /projects
mount /dev/vdb /projects
cd /projects

git clone -b development git@github.com:raonyguimaraes/mendelmd.git