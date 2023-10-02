pkill celery
pkill python

cd /projects
source venv/bin/activate

rm -rf rockbio

git clone -b development https://github.com/raonyguimaraes/rockbio
cd rockbio

cp ~/local_settings.py rockbio/

celery worker -l info -A rockbio -c 1 -P solo