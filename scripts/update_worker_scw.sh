pkill celery
pkill python

cd /projects
source venv/bin/activate

rm -rf mendelmd

git clone -b development https://github.com/raonyguimaraes/mendelmd
cd mendelmd

cp ~/local_settings.py mendelmd/

celery worker -l info -A mendelmd -c 1 -P solo