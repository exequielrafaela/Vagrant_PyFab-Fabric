# Fabfile to:
#    - check the credentials for a certain user.
#    - to invoke: fab -f file func()
#    - $ fab -R local gen_key
#    - $ fab -R dev push_key
#    - $ fab -R dev test_key:username
# NOTE: http://docs.fabfile.org/en/1.12/usage/env.html#roles

# Import Fabric's API module#
#from fabric.api import *
from fabric.api import hosts, sudo, settings, hide, env, execute, prompt, run, local
from termcolor import colored
import os
import logging
#import apt
import yum

# As a good practice we can log the state of each phase in our script.
#  https://docs.python.org/2.7/howto/logging.html
logging.basicConfig(filename='check_ssh.log', level=logging.DEBUG)
logging.info('LOG STARTS')
#logging.debug('This message should go to the log file')
#logging.warning('And this, too')

# Open the server list file and split the IP o each server.
# http://www.tutorialspoint.com/python/string_split.htm
# with open("./out_users_test.txt", "r") as f:
#    ServerList = [line.split()[0] for line in f]
with open("./out_users_test.txt", "r") as f:
    ServerList = [line.split()[0] for line in f]
    print(ServerList)

# In env.roledefs we define the remote servers. It can be IP Addrs or domain names.
env.roledefs = {
    'local': ['localhost'],
    'dev': ServerList,
    'staging': ['user@staging.example.com'],
    'production': ['user@production.example.com']
}

# Fabrci user and pass.
env.user = "vagrant"
env.password = "vagrant"

def apt_package(action,package):
    with settings(warn_only=False):
        hostvm = sudo('hostname')
        if (action =="install"  ):
            aptcache = apt.Cache()
            if aptcache[package].is_installed:
                print colored('###############################################################################', 'yellow')
                print colored(package + ' ALREADY INSTALLED in:' + hostvm + '- IP:' + env.host_string, 'yellow')
                print colored('###############################################################################', 'yellow')
            else:
                print colored('###############################################################################', 'blue')
                print colored(package + ' WILL BE INSTALLED in:' + hostvm + '- IP:' + env.host_string, 'blue')
                print colored('###############################################################################', 'blue')
                sudo('apt-get update')
                sudo('apt-get install '+package)
                aptcachenew = apt.Cache()
                if aptcachenew[package].is_installed:
                    print colored('##################################################################################', 'green')
                    print colored(package + 'SUCCESFULLY INSTALLED in:' + hostvm + '- IP:' + env.host_string, 'green')
                    print colored('##################################################################################', 'green')
                else:
                    print colored('#################################################################################', 'red')
                    print colored(package + 'INSTALLATION PROBLEM in:' + hostvm + '- IP:' + env.host_string, 'red')
                    print colored('#################################################################################', 'red')

        elif (action =="upgrade"  ):
            aptcache = apt.Cache()
            if aptcache[package].is_installed:
                print colored('############################################################################', 'yellow')
                print colored(package + ' TO BE UPGRADED in:' + hostvm + '- IP:' + env.host_string, 'yellow')
                print colored('############################################################################', 'yellow')
                sudo('apt-get update')
                sudo('apt-get install --only-upgrade '+package)
            else:
                print colored('###########################################################################', 'red')
                print colored(package + ' NOT INSTALLED in:' + hostvm + '- IP:' + env.host_string, 'red')
                print colored('###########################################################################', 'red')

        else:
            print colored('############################################################################', 'yellow')
            print colored('Usage eg1: $ fab -R dev apt_package:install,cron', 'red')
            print colored('Usage eg2: $ fab -R dev apt_package:upgrade,gcc', 'red')
            print colored('############################################################################', 'blue')

def yum_package(action, package):
    with settings(warn_only=False):
        hostvm = sudo('hostname')
        if(action =="install"):
            yumcache = yum.YumBase()
            if yumcache.rpmdb.searchNevra(name=package):
                print colored('###############################################################################', 'yellow')
                print colored(package + ' ALREADY INSTALLED in:' + hostvm + '- IP:' + env.host_string, 'yellow')
                print colored('###############################################################################', 'yellow')
            else:
                print colored('###############################################################################', 'blue')
                print colored(package + ' WILL BE INSTALLED in:' + hostvm + '- IP:' + env.host_string, 'blue')
                print colored('###############################################################################', 'blue')
                sudo('yum install -y '+package)
                yumcache = yum.YumBase()
                if yumcache.rpmdb.searchNevra(name=package):
                    print colored('##################################################################################', 'green')
                    print colored(package + ' SUCCESFULLY INSTALLED in:' + hostvm + '- IP:' + env.host_string, 'green')
                    print colored('##################################################################################', 'green')
                else:
                    print colored('#################################################################################', 'red')
                    print colored(package + ' INSTALLATION PROBLEM in:' + hostvm + '- IP:' + env.host_string, 'red')
                    print colored('#################################################################################', 'red')

        elif (action =="upgrade"  ):
            yumcache = yum.YumBase()
            if yumcache.rpmdb.searchNevra(name=package):
                print colored('############################################################################', 'yellow')
                print colored(package + ' TO BE UPGRADED in:' + hostvm + '- IP:' + env.host_string, 'yellow')
                print colored('############################################################################', 'yellow')
                sudo('yum update -y '+package)
            else:
                print colored('###########################################################################', 'red')
                print colored(package + ' NOT INSTALLED in:' + hostvm + '- IP:' + env.host_string, 'red')
                print colored('###########################################################################', 'red')

        else:
            print colored('############################################################################', 'yellow')
            print colored('Usage eg1: $ fab -R dev yum_package:install,cron', 'red')
            print colored('Usage eg2: $ fab -R dev yum_package:upgrade,gcc', 'red')
            print colored('############################################################################', 'blue')

def gen_key():
    with settings(warn_only=False):
        usernameg = prompt("Which USERNAME you like to GEN KEYS?")
        print colored('#######################################################', 'blue')
        print colored('Consider that we generate user: username pass: username', 'blue')
        print colored('#######################################################', 'blue')

        sudo('useradd -m -d /home/'+usernameg+' -U '+usernameg)
        sudo('echo "'+usernameg+':'+usernameg+'" | chpasswd')
        sudo("ssh-keygen -t rsa -f /home/" + usernameg+ "/.ssh/id_rsa -N ''", user=usernameg)
        #http://unix.stackexchange.com/questions/36540/why-am-i-still-getting-a-password-prompt-with-ssh-with-public-key-authentication
        #sudo('chmod 700 /home/' + usernameg)
        sudo('chmod 755 /home/'+usernameg)
        sudo('chmod 755 /home/'+usernameg+'/.ssh')
        sudo('chmod 600 /home/'+usernameg+'/.ssh/id_rsa')

def push_key():
    with settings(warn_only=False):
        usernamep = prompt("Which USERNAME you like to CREATE & PUSH KEYS?")
        sudo('useradd -m -d /home/' +usernamep +' -U '+usernamep)
        sudo('echo "'+usernamep+':'+usernamep+'" | chpasswd')
        # Remember that the usernamep is not in the remote server
        # Then you are gona be ask the pass of this user.
        # To avoid this you must use a user that it's already created
        # in the local and remote host with the proper permissions.
        local('ssh-copy-id -i /home/'+usernamep+'/.ssh/id_rsa.pub '+usernamep+'@'+env.host_string)
        sudo('chmod 700 /home/'+usernamep+'/.ssh/authorized_keys')

def test_key(usernamet):
    with settings(warn_only=False):
        hostvm = sudo('hostname')
        if (os.path.exists('/home/'+usernamet+'/.ssh/')):
            ssh_test = local('ssh -i /home/'+usernamet+'/.ssh/id_rsa -o "StrictHostKeyChecking no" -q '+usernamet+'@'+env.host_string+' exit')
            if (ssh_test.succeeded):
                print colored('###################################################', 'blue')
                print colored(usernamet+' WORKED! in:'+hostvm+' IP:'+env.host_string, 'blue')
                print colored('###################################################', 'blue')
        else:
            print colored('###################################################', 'red')
            print colored(usernamet+' FAIL! in:'+hostvm+'- IP:'+env.host_string, 'red')
            print colored('###################################################', 'red')