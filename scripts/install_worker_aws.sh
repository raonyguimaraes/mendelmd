pkill celery
pkill python

sudo apt update
sudo DEBIAN_FRONTEND=noninteractive apt -y upgrade
sudo apt -y install git python3-pip python3-venv postgresql-client htop

sudo mkfs -t ext4 /dev/nvme0n1
sudo mkdir -p /projects
sudo mount /dev/nvme0n1 /projects
sudo chown ubuntu:ubuntu /projects -R
cd /projects

python3 -m venv venv
source venv/bin/activate

rm -rf mendelmd
git clone -b development https://github.com/raonyguimaraes/mendelmd
cd mendelmd
pip install wheel
pip install -r requirements.txt

bash scripts/install_conda.sh

cp ~/local_settings.py mendelmd/

./manage.py celery