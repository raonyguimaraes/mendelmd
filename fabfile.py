from fabric.api import *
from fabric.api import run
#comment
env.user  = 'raony'
env.hosts = ['mendel']

def install():
    # local('pip install cython')
    # local('pip install pynnotator')
    local('pip install -r requirements.txt')
    # local('pynnotator install')
    # local('python manage.py migrate auth')#bug with version 1.8
    # local('python manage.py migrate')

def backup_users():
    local('python3 manage.py dumpdata --indent=4 --format=json auth account allauth > fixtures/users.json')
    local('python3 manage.py dumpdata --indent=4 --format=json individuals > fixtures/individuals.json')
    local('python3 manage.py dumpdata --indent=4 --format=json individuals.usergroup > fixtures/usergroups.json')
    # local('python manage.py dumpdata users allauth > initial_data.json')

def reset_migrations():

    models = ['cases', 'projects', 'individuals', 'databases', 'variants', 
    'diseases', 'genes', 'files', 'filter_analysis', 'samples', 'analyses', 
    'tasks', 'workers', 'upload', 'settings', 'projects', 'mapps', 'pathway_analysis', 'mapps', 'analyses']
    for model in models:
        local('rm -rf %s/migrations' % (model))
    for model in models:
        local('python manage.py makemigrations %s' % (model))

    local('python manage.py migrate')

def resetdb():
    # local('rm db.sqlite3')
    # local('psql -d template1 -c "DROP DATABASE rockbio_prod;"')
    # local('psql -d template1 -c "CREATE DATABASE rockbio_prod;"')
    # local('python manage.py syncdb')
    local('dropdb rockbio')
    local('createdb rockbio')
    local('./manage.py migrate')
    # local('python manage.py loaddata fixtures/users.json')
    # local('python manage.py loaddata fixtures/usergroups.json')
    #load genes, diseases, pathways


    # local('python manage.py createsuperuser')
    #local('python manage.py runserver mendel.medicina.ufmg.br:8001')

def import_samples():
    local('./manage.py import_files')
    local('python ../scripts/import_samples.py')
    local('python ../scripts/update_sample_files.py')


def make_doc():
    with lcd('../docs'):
        local('make html')
        local('cp -rf _build/html/* /var/www/rockbio_static/docs/')

#def backup():
#    run(' mysqldump -u root -p rockbio14 | gzip > db_backup/rockbio151012.sql.gz ')
def create_sample_data():
    #backup all users
#    with cd('/projects/www/rockbio14'):
#
#        run('mysqldump -u root -p rockbio14 auth_user account_account profiles_profile | gzip > db_backup/users.sql.gz')
#        #get sample from individuals
#        run('mysqldump -u root -p --where="individual_id < 16" rockbio14 individuals_variant | gzip > db_backup/individual_variants_sample.sql.gz')
#        run('mysqldump -u root -p --where="id < 16" rockbio14 individuals_individual | gzip > db_backup/individuals_sample.sql.gz')


    get('/projects/www/rockbio14/db_backup/users.sql.gz', '/home/raony/sites/rockbio14/db_backup/')
    get('/projects/www/rockbio14/db_backup/individual_variants_sample.sql.gz', '/home/raony/sites/rockbio14/db_backup/')
    get('/projects/www/rockbio14/db_backup/individuals_sample.sql.gz', '/home/raony/sites/rockbio14/db_backup/')

def copy_sample_from_server():
    local('scp 150.164.199.43:/projects/www/rockbio14/db_backup/rockbio040113_withoutvariants.zip .')

def make_sample_data():
    # local('pg_dump -U raony rockbio -T individuals_variant > db_sample/rockbio_sample_variants.sql')
    # local('zip db_sample/samples.sql.zip db_sample/rockbio_sample_variants.sql')
    # local('rm db_sample/rockbio_sample_variants.sql')
    local('python manage.py makefixture --format=json --indent=4 rockbio.individuals.variant[1:101] > fixtures/individuals_variant.json')

def load_sample_data():
    local('psql -U raony -d rockbio < db_sample/rockbio210313_sample.sql')
    local('psql -U raony -d rockbio -f db_sample/restore_db.sql')


def loaddata():
    #Load user and sample from individuals
    local('gunzip < db_backup/users.sql.gz | mysql -u root -p rockbio')
    local('gunzip < db_backup/individual_variants_sample.sql.gz | mysql -u root -p rockbio ')
    local('gunzip < db_backup/individuals_sample.sql.gz | mysql -u root -p rockbio ')


#    run(' gunzip < db_backup/rockbio151012.sql.gz | mysql -u root -p rockbio14 ')
#    local("""python manage.py loaddata db_backup/all_without_individuals.json.gz""")

def local_reset():
	#delete database

    # local("sudo su - postgres")
    # local("""psql -c 'DROP DATABASE rockbio_dev;'""")
    # local("""psql -c 'CREATE DATABASE rockbio_dev;'""")

    #sync and migrate
    local('python manage.py sqlclear individuals | python manage.py dbshell')

    local('python manage.py syncdb --migrate')

    local('python manage.py createsuperuser')
    local('python manage.py runserver mendel.medicina.ufmg.br:8002')

    #load user data
    # local('python manage.py loaddata user_data.json')
    #ready to go!

    #backup db?
    #python manage.py dumpdata -v 2 --format=json users auth account > user_data.json
#
#    local('python manage.py flush --noinput')

    #local('python manage.py syncdb --noinput')
#    local('python manage.py runserver')

def requirements():
    local('pip install -r requirements.txt')
    #local('python filetransfers/setup.py install')
    #local('python wikitools-1.1.1/setup.py install')
    #local('easy_install fisher')



def backup_diseases():
    local('python manage.py dumpdata ')
def run_local():
#    local('pkill python')
    local('python manage.py celeryd &')
    local('python manage.py runserver mendel.medicina.ufmg.br:8002')
#    local('pkill python')

def deploy(message="changes (fabric)"):
    local('git add .; git commit -m "%s";git push' % (message))
    with cd('/projects/www/rockbio'):
#        run('git reset --hard HEAD')
        run('git pull')
#        run('source virtualenvwrapper.sh && workon genome_research && python manage.py syncdb --noinput')

        run('sudo /etc/init.d/apache2 restart')

def clean_individuals():

    local('python manage.py  sqlclear individuals | python manage.py dbshell')

def clean_variants():
    local('python manage.py  sqlclear variants | python manage.py dbshell')
    local('python manage.py  migrate')

def docs():
    with lcd('../docs'):
        local('make html')
        local('cp -r _build/html/* ../static/docs/')
