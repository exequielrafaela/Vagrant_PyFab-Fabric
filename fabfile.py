from fabric.api import run, sudo, settings, hide
from fabric.context_managers import cd
from fabric.contrib.files import exists
from termcolor import colored

def server_ubuntu():
    with settings(warn_only=True):
        print colored('##########################', 'blue')
        print colored('######### SERVER #########', 'blue')
        print colored('##########################', 'blue')

        print colored('###########################', 'blue')
        print colored('## JUMPHOST PROVISIONING ##', 'blue')
        print colored('###########################', 'blue')
        sudo('apt-get update')
        sudo('apt-get -y upgrade')
        sudo('apt-get install -y git python-minimal python2.7 python2.7-dev')

        print colored('===================================================================', 'blue')
        print colored('DEPENDENCIES PROVISIONING                          ', 'blue', attrs=['bold'])
        print colored('===================================================================', 'blue')
        sudo('apt-get install -y build-essential checkinstall')
        sudo('apt-get install -y  libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev '
             'tk-dev libgdbm-dev libc6-dev libbz2-dev')

        with cd('/usr/src'):
            sudo('wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz')
            sudo('tar xzf Python-2.7.13.tgz')
            with cd('/Python-2.7.13'):
                sudo('./configure')
                sudo('make altinstall')

        python_ver = run('python2.7 -V')
        if python_ver == "Python 2.7.13":
            print colored('==========================', 'blue')
            print colored('Python SUCCESFULLY UPDATED', 'blue', attrs=['bold'])
            print colored('==========================', 'blue')
        else:
            print colored('================================', 'blue')
            print colored('Python NOT UPDATED, please check', 'blue', attrs=['bold'])
            print colored('================================', 'blue')

        with cd('/usr/bin'):
            sudo('ls -ltra | grep python')
            sudo('rm python')
            sudo('ln -s /usr/src/Python-2.7.13/python python')
            sudo('ls -ltra | grep python')

        pip_status = str(run('pip | grep "pip <command>"'))
        pip_status = pip_status.strip()
        if pip_status != "pip <command> [options]":
            with cd('/usr/src'):
                sudo('wget https://bootstrap.pypa.io/get-pip.py')
                sudo('python get-pip.py')
                sudo('pip install --upgrade pip')

        with cd('/home/vagrant'):
            if exists('/home/vagrant/proton', use_sudo=True):
                with cd('/home/vagrant/proton'):
                    sudo('git checkout dev-test')
                    sudo('fab -R local inst_ubu_14_fab.install_upgrade_python_27_13:vagrant')
                    sudo('fab -R local inst_ubu_14_fab.install_jenkins:vagrant')
                    sudo('fab -R local inst_ubu_14_fab.install_docker:vagrant')
            else:
                run('git clone https://github.com/exequielrafaela/proton.git')
                with cd('/home/vagrant/proton'):
                    sudo('git checkout dev-test')
                    sudo('fab -R local inst_ubu_14_fab.install_upgrade_python_27_13:vagrant')
                    sudo('fab -R local inst_ubu_14_fab.install_jenkins:vagrant')
                    sudo('fab -R local inst_ubu_14_fab.install_docker:vagrant')

        print colored('######################################', 'blue')
        print colored('FIREWALL - NAT TABLE STATUS:      ', 'blue')
        print colored('######################################', 'blue')
        with hide('output'):
            fw = sudo('iptables -t nat -L')
        print colored(fw, 'red')

        print colored('######################################', 'blue')
        print colored('FIREWALL - FILTER TABLE STATUS:   ', 'blue')
        print colored('######################################', 'blue')
        with hide('output'):
            fw = sudo('iptables -L')
        print colored(fw, 'red')

        print colored('##########################', 'blue')
        print colored('## NETWORK CONFIGURATION #', 'blue')
        print colored('##########################', 'blue')
        with hide('output'):
            netconf = sudo('ip addr show')
        print colored(netconf, 'yellow')

def server_centos():
    with settings(warn_only=True):
        print colored('##########################', 'blue')
        print colored('######### SERVER #########', 'blue')
        print colored('##########################', 'blue')

        print colored('###########################', 'blue')
        print colored('## JUMPHOST PROVISIONING ##', 'blue')
        print colored('###########################', 'blue')
        sudo('yum clean all')
        sudo('yum install -y gcc glibc glibc-common gd gd-devel wget net-tools git rsync')
        sudo('yum install -y python-devel vim net-tools sudo openssh-server openssh-clients')
        sudo('yum install -y epel-release ')

        print colored('#########################################', 'blue')
        print colored('####### INSTALLING PYTHON FABRIC ########', 'blue')
        print colored('#########################################', 'blue')
        sudo('yum install -y python-pip')
        sudo('pip install --upgrade pip')
        sudo('pip install fabric')
        sudo('pip install termcolor')
        sudo('pip install iptools')
        sudo('pip install passlib')

        print colored('######################################', 'blue')
        print colored('FIREWALL - NAT TABLE STATUS:      ', 'blue')
        print colored('######################################', 'blue')
        with hide('output'):
            fw = sudo('iptables -t nat -L')
        print colored(fw, 'red')

        print colored('######################################', 'blue')
        print colored('FIREWALL - FILTER TABLE STATUS:   ', 'blue')
        print colored('######################################', 'blue')
        with hide('output'):
            fw = sudo('iptables -L')
        print colored(fw, 'red')

        print colored('##########################', 'blue')
        print colored('## NETWORK CONFIGURATION #', 'blue')
        print colored('##########################', 'blue')
        with hide('output'):
            netconf = sudo('ip addr show')
        print colored(netconf, 'yellow')


#############################################################################
#############################################################################

def client1():
    with settings(warn_only=True):
        print colored('##########################', 'blue')
        print colored('######## CLIENT 1 ########', 'blue')
        print colored('##########################', 'blue')
        sudo('yum clean all')
        sudo('yum install -y python-devel vim net-tools sudo openssh-server openssh-clients wget')
        sudo('yum install -y epel-release rsync')

        print colored('######################################', 'blue')
        print colored('END FIREWALL - NAT TABLE STATUS:      ', 'blue')
        print colored('######################################', 'blue')
        with hide('output'):
            fw = sudo('iptables -t nat -L')
        print colored(fw, 'red')

        print colored('######################################', 'blue')
        print colored('END FIREWALL - FILTER TABLE STATUS:   ', 'blue')
        print colored('######################################', 'blue')
        with hide('output'):
            fw = sudo('iptables -L')
        print colored(fw, 'red')

        print colored('##########################', 'blue')
        print colored('## NETWORK CONFIGURATION #', 'blue')
        print colored('##########################', 'blue')
        with hide('output'):
            netconf = sudo('ip addr show')
        print colored(netconf, 'yellow')


#############################################################################
#############################################################################

def client2():
    with settings(warn_only=True):
        print colored('##########################', 'blue')
        print colored('######## CLIENT 2 ########', 'blue')
        print colored('##########################', 'blue')
        sudo('yum clean all')
        sudo('yum install -y python-devel vim net-tools sudo openssh-server openssh-clients wget')
        sudo('yum install -y epel-release')
        sudo('yum install -y epel-release rsync')

        print colored('######################################', 'blue')
        print colored('END FIREWALL - NAT TABLE STATUS:      ', 'blue')
        print colored('######################################', 'blue')
        with hide('output'):
            fw = sudo('iptables -t nat -L')
        print colored(fw, 'red')

        print colored('######################################', 'blue')
        print colored('END FIREWALL - FILTER TABLE STATUS:   ', 'blue')
        print colored('######################################', 'blue')
        with hide('output'):
            fw = sudo('iptables -L')
        print colored(fw, 'red')

        print colored('##########################', 'blue')
        print colored('## NETWORK CONFIGURATION #', 'blue')
        print colored('##########################', 'blue')
        with hide('output'):
            netconf = sudo('ip addr show')
        print colored(netconf, 'yellow')

#############################################################################
#############################################################################
