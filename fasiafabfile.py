'''
Fabric script for fasia application setup
'''
import os

from fabric.api import cd, env, put, run, sudo, task, warn_only, local
from fabric.tasks import execute
from fabric.contrib.files import sed
from fabric.contrib.project import rsync_project
from ConfigParser import SafeConfigParser

#GLOBAL VARIABLES
repo_folder = os.path.dirname(os.path.abspath(__file__))
database = repo_folder + "/database"
host_name = ""
domain_name = "" 

if len(env.hosts) > 0:
    host_name = env.hosts[0].split('@')[-1]
    domain_name = host_name

if 'domain_name' in env:
    domain_name = env.domain_name
    host_name = domain_name


@task
def check_domain():
    print ("your domain_name is %s" %(domain_name))


@task
def set_config_web():
    '''
    set config values
    '''
    if host_name == 'dev1.fasiaamerica.org':
        CONFIG_FILE='WEBSERVICES_SETTINGS=/home/fasiaamerica/fasia/web_services/config/config_dev.py'
    elif host_name == 'test.fasiaamerica.org':
        CONFIG_FILE='WEBSERVICES_SETTINGS=/home/fasiaamerica/fasia/web_services/config/config_test.py'
    elif host_name == "fasiaamerica.org":
        CONFIG_FILE='WEBSERVICES_SETTINGS=/home/fasiaamerica/fasia/web_services/config/config_prod.py'
    parser = SafeConfigParser()
    path = repo_folder+"/web_services/fasiamain-uwsgi.ini"
    parser.read(path)
    parser.set('uwsgi', 'env', CONFIG_FILE)
    with open(path, 'wb') as configfile:
        parser.write(configfile)
    rsync_project(remote_dir='/home/fasiaamerica/fasia/web_services', local_dir='web_services/fasiamain-uwsgi.ini', exclude=['.git','*.pyc','android','ios','*.patch'])
    local('git checkout web_services/fasiamain-uwsgi.ini')


@task
def set_config_admin():
    '''
    set config Admin
    '''
    if host_name == 'dev1.fasiaamerica.org':
        CONFIG_FILE='ADMIN_SETTINGS=/home/fasiaamerica/fasia/services/fasia-admin/config/config_dev.py'
    elif host_name == 'test.fasiaamerica.org':
        CONFIG_FILE='ADMIN_SETTINGS=/home/fasiaamerica/fasia/services/fasia-admin/config/config_test.py'
    elif host_name == "fasiaamerica.org":
        CONFIG_FILE='ADMIN_SETTINGS=/home/fasiaamerica/fasia/services/fasia-admin/config/config_prod.py'
    parser = SafeConfigParser()
    path = repo_folder+"/services/fasia-admin/fasiaadmin-uwsgi.ini"
    parser.read(path)
    parser.set('uwsgi', 'env', CONFIG_FILE)
    with open(path, 'wb') as configfile:
        parser.write(configfile)
    rsync_project(remote_dir='/home/fasiaamerica/fasia/services/fasia-admin/', local_dir='services/fasia-admin/fasiaadmin-uwsgi.ini', exclude=['.git','*.pyc','android','ios','*.patch'])
    local('git checkout services/fasia-admin/fasiaadmin-uwsgi.ini')


@task
def set_config_advice():
    '''
    set config Advice
    '''
    if host_name == 'dev1.fasiaamerica.org':
        CONFIG_FILE = 'ADVISE_SETTINGS=/home/fasiaamerica/fasia/services/advise-forum/config/config_dev.py'
    elif host_name == 'test.fasiaamerica.org':
        CONFIG_FILE = 'ADVISE_SETTINGS=/home/fasiaamerica/fasia/services/advise-forum/config/config_test.py'
    elif host_name == "fasiaamerica.org":
        CONFIG_FILE = 'ADVISE_SETTINGS=/home/fasiaamerica/fasia/services/advise-forum/config/config_prod.py'
    parser = SafeConfigParser()
    path = repo_folder + "/services/advise-forum/fasiaadvise-uwsgi.ini"
    parser.read(path)
    parser.set('uwsgi', 'env', CONFIG_FILE)

    with open(path, 'wb') as configfile:
        parser.write(configfile)

    rsync_project(
        remote_dir='/home/fasiaamerica/fasia/services/advise-forum/',
        local_dir='services/advise-forum/fasiaadvise-uwsgi.ini',
        exclude=['.git', '*.pyc', 'android', 'ios', '*.patch']
    )
    local('git checkout services/advise-forum/fasiaadvise-uwsgi.ini')


@task
def user_perm():
        '''
        Used to change the deployed code to nfgroup
        '''
        run('sudo chown -R %s:%s /home/fasiaamerica/fasia' %(env.user,env.user))


@task
def restore_owner():
    '''
    Used to change the ownership to fasiaamerica
    '''
    run('sudo chown -R fasiaamerica:fasiaamerica /home/fasiaamerica/fasia')


@task
def pip():
    run('/home/fasiaamerica/fasiaenv/bin/pip install -r /home/fasiaamerica/fasia/web_services/requirement.txt')


@task
def cp_server_details():
    execute(user_perm)
    print('Copying... fasia server details source')
    rsync_project(
        remote_dir='/home/fasiaamerica/fasia',
        local_dir='web_server',
        exclude=['.git','*.pyc','android','ios','*.patch']
    )
    execute(restore_owner)
    execute(restart)


@task
def cp_web_service():
    execute(user_perm)
    print('copying... fasia web serivce source')
    rsync_project(
        remote_dir='/home/fasiaamerica/fasia',
        local_dir='web_services',
        exclude=['.git','*.pyc','android','iOS','*.patch','*.ini', '*.log']
    )
    execute(set_config_web)
    execute(restore_owner)
    execute(restart_web_service_uwsgi)


@task
def cp_admin_service():
    execute(user_perm)
    print('Copying... fasia admin service source')
    rsync_project(
        remote_dir="/home/fasiaamerica/fasia/services",
        local_dir='services/fasia-admin',
        exclude=['.git','*.pyc','android','iOS','*.patch','*.ini','*.log']
    )
    execute(set_config_admin)
    execute(restore_owner)
    execute(restart_admin_uwsgi)
    

@task
def cp_advise_service():
    execute(user_perm)
    print('Copying... fasia get Advice serive source')
    rsync_project(
        remote_dir="/home/fasiaamerica/fasia",
        local_dir='services',
        exclude=['.git','*.pyc','android','iOS','*.patch','*.log','*.ini']
    )
    execute(set_config_advice)
    execute(restore_owner)
    execute(restart_advice_uwsgi)


@task
def restart_web_service_uwsgi():
    sudo('service fasiamain stop')
    sudo('service fasiamain start')


@task
def restart_admin_uwsgi():
    sudo('service fasiaadmin stop')
    sudo('service fasiaadmin start')


@task
def restart_advice_uwsgi():
    sudo('service fasiaadvise stop')
    sudo('service fasiaadvise start')


@task
def start_uwsgi():
    '''
     To start uwsgi
    '''
    sudo('service fasiamain start')
    sudo('service fasiaadmin start')
    sudo('service fasiaadvise start')


@task
def stop_uwsgi():
    '''
    To stop uwsgi
    '''
    sudo('service fasiamain stop')
    sudo('service fasiaadmin stop')
    sudo('service fasiaadvise stop')


@task
def restart():
    '''
     To restart uwsgi
    '''
    execute(stop_uwsgi)
    execute(start_uwsgi)


@task
def copy_all():
    '''
    To copy all service
    '''
    execute(cp_web_service)
    execute(cp_admin_service)
    execute(cp_advise_service)
