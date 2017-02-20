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
        sudo('apt-get install -y git')

        print colored('===================================================================', 'blue')
        print colored('DEPENDENCIES PROVISIONING                          ', 'blue', attrs=['bold'])
        print colored('===================================================================', 'blue')

        with cd('/home/vagrant'):
            if exists('/home/vagrant/proton', use_sudo=True):
                with cd('/home/vagrant/proton'):
                    sudo('git checkout dev-test')
                    sudo('git pull')
                    sudo('./requirements.sh')
                    run('fab -i /vagrant/.vagrant/machines/server/virtualbox/private_key'
                        ' -R local inst_ubu_14_fab.install_upgrade_python_27_13')
                    run('fab -i /vagrant/.vagrant/machines/server/virtualbox/private_key'
                        ' -R local inst_ubu_14_fab.install_jenkins')
                    run('fab -i /vagrant/.vagrant/machines/server/virtualbox/private_key'
                        ' -R local inst_ubu_14_fab.install_docker:vagrant')
            else:
                run('git clone https://github.com/exequielrafaela/proton.git')
                with cd('/home/vagrant/proton'):
                    sudo('git checkout dev-test')
                    sudo('./requirements.sh')
                    run('fab -i /vagrant/.vagrant/machines/server/virtualbox/private_key'
                        ' -R local inst_ubu_14_fab.install_upgrade_python_27_13')
                    run('fab -i /vagrant/.vagrant/machines/server/virtualbox/private_key'
                        ' -R local inst_ubu_14_fab.install_jenkins')
                    run('fab -i /vagrant/.vagrant/machines/server/virtualbox/private_key'
                        ' -R local inst_ubu_14_fab.install_docker:vagrant')

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
        sudo('yum install -y git python-devel vim net-tools sudo openssh-server openssh-clients wget')
        sudo('yum install -y epel-release rsync')

        with cd('/home/vagrant'):
            if exists('/home/vagrant/proton', use_sudo=True):
                with cd('/home/vagrant/proton'):
                    sudo('git checkout dev-test')
                    sudo('git pull')
                    sudo('./requirements.sh')
                    run('fab -i /vagrant/.vagrant/machines/client1/virtualbox/private_key'
                        ' -R local inst_centos_7_fab.install_lamp')

            else:
                run('git clone https://github.com/exequielrafaela/proton.git')
                with cd('/home/vagrant/proton'):
                    sudo('git checkout dev-test')
                    sudo('./requirements.sh')
                    run('fab -i /vagrant/.vagrant/machines/client1/virtualbox/private_key'
                        ' -R local inst_centos_7_fab.install_lamp')

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
        sudo('yum install -y epel-release rsync')

        with cd('/home/vagrant'):
            if exists('/home/vagrant/proton', use_sudo=True):
                with cd('/home/vagrant/proton'):
                    sudo('git checkout dev-test')
                    sudo('git pull')
                    sudo('./requirements.sh')
                    run('fab -i /vagrant/.vagrant/machines/client2/virtualbox/private_key'
                        ' -R local inst_centos_7_fab.install_lamp')

            else:
                run('git clone https://github.com/exequielrafaela/proton.git')
                with cd('/home/vagrant/proton'):
                    sudo('git checkout dev-test')
                    sudo('./requirements.sh')
                    run('fab -i /vagrant/.vagrant/machines/client2/virtualbox/private_key'
                        ' -R local inst_centos_7_fab.install_lamp')

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
