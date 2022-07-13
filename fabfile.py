'''
Fabric script for fasia server setup
'''
from __future__ import with_statement
from fabric.api import run, env, task, cd, sudo, settings, hide, prompt, put
from fabric.tasks import execute
from fabric.utils import warn
import fasiafabfile as fasia

def apt_update():
	sudo('apt-get update')

def apt_get_install(*packages):
	sudo('apt-get -y --no-upgrade install %s' % ' '.join(packages), shell=False)

def dependencies():
	apt_update()
	apt_get_install(
        	'build-essential',
	        'autoconf',
        	'libtool',
	        'pkg-config',
	        'rsync',
        	'libffi-dev',
	        'libssl-dev',
        	'libmysqlclient-dev',
	        'python-virtualenv',
        	'python-dev',
	        'binutils',
	        'libproj-dev',
	        'gdal-bin',
	        'libreadline-dev',
	        'libncurses5-dev',
	        'libpcre3-dev',
	        'perl',
	        'make',
	        'libgeoip-dev'
	)

@task
def newsetup():
	execute(dependencies)

@task
def fasiaenv():
    print('Creating fasiaenv')
    with cd('/home/northfacing'):
        run('virtualenv fasiaenv')

@task
def change_permissions():
	'''
	Used to change the deployed code to nfgroup
	'''
	run('sudo chown -R %s:%s /home/fasiaamerica/fasia' %(env.user,env.user))

@task
def restore_fasiaamerica_owner():
	'''
	Used to change the ownership to fasiaamerica
	'''
	run('sudo chown -R fasiaamerica:fasiaamerica /home/fasiaamerica/fasia')