from fabric.api import *
from fabric.contrib.files import exists
import os
from time import strftime

repo = 'git@github:username/mysite.git'
path = '/var/www/mysite'
env.use_ssh_config = True
env.sudo_user = 'www-data'

env.hosts = ['grace', 'gospel']
# check read-access to the keys, to be server-independent
keys = ['~/.ssh/id_rsa']
env.key_filename = [key for key in keys if os.access(key, os.R_OK)]

# this tags the sha deploy
def tag_prod():
    tag = "prod/%s" % strftime("%Y/%m-%d-%H-%M-%S")
    local('git tag -a %s -m "Prod"' % tag)
    local('git push --tags')

def install():
    sudo('mkdir -p ' + path)
    with cd(path):
        sudo('git clone ' + repo + ' .')
        sudo('composer install --dev')
        sudo('php app/console doctrine:database:create')
        sudo('php app/console doctrine:migrations:migrate --no-interaction')

def update():
    with cd(path):
        sudo('git remote update')
        sudo('git pull')
        sudo('composer install --dev')
        sudo('php app/console doctrine:migrations:migrate --no-interaction')
#        tag = run('git tag -l prod/* | sort | tail -n1')
#        run('git checkout ' + tag)

def deploy():
    if not exists(path):
        install()

#    tag_prod()
    update()

#def rollback(num_revs=1):
#    with cd(path):
#        run('git fetch')
#        tag = run('git tag -l prod/* | sort | tail -n' + str(1 + int(num_revs)) + ' | head -n1')
#        run('git checkout ' + tag)

