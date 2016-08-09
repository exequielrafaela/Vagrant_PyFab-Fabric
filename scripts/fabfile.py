# Fabfile to:
#    - check the credentials for a certain user.
#    - to invoke: fab -f file func()
#    - $ fab -R local gen_key
#    - $ fab -R dev push_key
#    - $ fab -R dev test_key
# NOTE: http://docs.fabfile.org/en/1.12/usage/env.html#roles

# Import Fabric's API module#
#from fabric.api import *
from fabric.api import hosts, sudo, settings, hide, env, execute, prompt, run, local
from termcolor import colored
import os
import logging

# As a good practice we can log the state of each phase in our script.
#  https://docs.python.org/2.7/howto/logging.html
logging.basicConfig(filename='check_ssh.log', level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

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

#vagrant@nagios-server:/vagrant/scripts$ fab -R local gen_key
def gen_key():
    with settings(warn_only=True):
        username = prompt("Which USERNAME you like to GEN KEYS?")
        print colored('#######################################################', 'blue')
        print colored('Consider that we generate user: username pass: username', 'blue')
        print colored('#######################################################', 'blue')

        sudo('useradd -m -d /home/'+username+' -U '+username)
        sudo('echo "'+username+':'+username+'" | chpasswd')
        sudo("ssh-keygen -t rsa -f /home/" + username + "/.ssh/id_rsa -N ''", user=username)
        #http://unix.stackexchange.com/questions/36540/why-am-i-still-getting-a-password-prompt-with-ssh-with-public-key-authentication
        sudo('chmod 755 /home/'+username)
        sudo('chmod 755 /home/'+username+'/.ssh')
        sudo('chmod 600 /home/'+username+'/.ssh/id_rsa')

def push_key():
    with settings(warn_only=True):
        username = prompt("Which USERNAME you like to CREATE & PUSH KEYS?")
        sudo('useradd -m -d /home/' +username +' -U '+username)
        sudo('echo "'+username+':'+username+'" | chpasswd')
        local('ssh-copy-id -i /home/'+username+'/.ssh/id_rsa.pub '+username+'@'+env.host_string)
        sudo('chmod 700 /home/'+username+'/.ssh/authorized_keys')

def test_key():
    username = prompt("Which USERNAME you like to TEST KEYS?")
    hostvm = sudo('hostname')
    if (os.path.exists('/home/'+username+'/.ssh/')):
        ssh_test = local('ssh -i /home/'+username+'/.ssh/id_rsa -q '+username+'@'+env.host_string+' exit')
        if (ssh_test.succeeded):
            print colored('###############################################', 'blue')
            print colored(username+' WORKED! in:'+hostvm+' IP:'+env.host_string, 'blue')
            print colored('###############################################', 'blue')
    else:
        print colored('##############################################', 'red')
        print colored(username +' FAIL! in:'+hostvm+'- IP:'+env.host_string, 'red')
        print colored('##############################################', 'red')