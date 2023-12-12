sudo apt update
sudo DEBIAN_FRONTEND=noninteractive apt -y upgrade
sudo apt -y install git python3-pip python3-venv postgresql-client

mkfs -t ext4 /dev/vdb
mkdir -p /projects
mount /dev/vdb /projects
cd /projects

python3 -m venv venv
source venv/bin/activate

git clone -b development https://github.com/raonyguimaraes/rockbio
cd rockbio
pip install wheel
pip install -r requirements.txt

bash scripts/install_conda.sh

cp ~/local_settings.py rockbio/

celery worker -l info -A rockbio -c 1 -P solo