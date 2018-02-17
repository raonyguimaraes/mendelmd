pkill celery
pkill python

cd /projects
source venv/bin/activate

rm -rf mendelmd

git clone -b development https://github.com/raonyguimaraes/mendelmd
cd mendelmd

cp ~/local_settings.py mendelmd/

./manage.py celery