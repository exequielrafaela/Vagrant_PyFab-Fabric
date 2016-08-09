from fabric.api import run, sudo, settings, hide, put
from termcolor import colored


def server():
    with settings(warn_only=True):
        print colored('##########################', 'blue')
        print colored('######### SERVER #########', 'blue')
        print colored('##########################', 'blue')

        sudo('apt-get -y update')
        sudo('apt-get -y install python-pip')
        sudo('pip install fabric')
        # Alternatively, you can also use *pip*:
        # sudo aptitude install fabric

        #https: // www.digitalocean.com / community / tutorials / how - to - use - fabric - to - automate - administration - tasks - and -deployments
        #### USEFUL - SUDO a specific USER. ####
        #sudo("mkdir /var/www/web-app-one", user="web-admin")

        #### USEFUL - GET to replace SCP. ####
        # Download some logs
        #get(remote_path="/tmp/log_extracts.tar.gz", local_path="/logs/new_log.tar.gz")

        # Download a database back-up
        #get("/backup/db.gz", "./db.gz")

        #### USEFUL - PUT to replace SCP. ####
        # Upload a tar archive of an application
        #put("/local/path/to/app.tar.gz", "/tmp/trunk/app.tar.gz")

        # Use the context manager `cd` instead of "remote_path" arg.
        # This will upload app.tar.gz to /tmp/trunk/
        #with cd("/tmp"):
        #    put("local/path/to/app.tar.gz", "trunk")

        # Upload a file and set the exact mode desired
        #upload = put("requirements.txt", "requirements.txt", mode=664)

        # Verify the upload
        #upload.succeeded

        #### USEFUL Prompt the user - For example PORT to use ####
        #port_number = prompt("Which port would you like to use?")

        # Prompt the user with defaults and validation
        #port_number = prompt("Which port?", default=42, validate=int)

        #### USEFUL - The *cd* context manager makes enwrapped command's
        # execution relative to the stated path (i.e. "/tmp/trunk")
        #with cd("/tmp/trunk"):
        #    items = sudo("ls -l")

        # It is possible to "chain" context managers
        # The run commands gets executed, therefore at "/tmp/trunk"
        #with cd("/tmp"):
        #    with cd("/trunk"):
        #        run("ls")

        #### USEFUL - The lcd context manager (local cd) works very similarly to one above (cd); ####
        # however, it only affects the local system's state.
        #Usage examples:

        # Change the local working directory to project's
        # and upload a tar archive
        #with lcd("~/projects/my_project"):
            #print "Uploading the project archive"
            #put("app.tar.gz", "/tmp/trunk/app.tar.gz")

        #### USEFUL - temporarily (i.e. for a certain command chain),
        # you can use the settings statement (i.e. override env values).
        #Perform actions using a different *user*
        #with settings(user="user1"):
        #    sudo("cmd")

        #### USEFUL - PREFIX with prefix("cmd arg."):
        #run("./start")
            # cmd arg. && ./start

        #http://stackoverflow.com/questions/12330712/cant-connect-to-remote-server-with-fabric-and-ssh-using-key-file
        #fab command -i /path/to/key.pem [-H [user@]host[:port]]

        #put("/home/e.barrirero/grey_repo/personal_scripts/out_users.txt", "/home/vagrant/scripts/")

        print colored('######################################', 'blue')
        print colored('SERVER BASIC PROVISIONING:      ', 'blue')
        print colored('######################################', 'blue')
        #sudo('cp /vagrant/fabric/fabfile.py /home/vagrant/fabfile.py')

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

        sudo('apt-get -y update')
        #sudo('apt-get -y install tcpdump nmap vim')
        #sudo('apt-get -y install python-pip')
        #sudo('pip install fabric')

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

        sudo('apt-get -y update')
        #sudo('apt-get -y install tcpdump nmap lynx-cur vim')
        sudo('apt-get -y install apache2')
        #sudo('pip install fabric')

        sudo('if ! [ -L /var/www ]; then'
             'rm -rf /var/www'
             'ln -fs /vagrant/ /var/www'
             'fi')

        print colored('##########################', 'blue')
        print colored('#### APACHE2 WEB_SERV ####', 'blue')
        print colored('##########################', 'blue')
        #sudo('wget -P /var/www/ -E -H -k -K -p http://www.binbash.com.ar')
        #sudo('cp -r /var/www/www.binbash.com.ar/* /var/www/')
        #sudo('echo "ServerName localhost" >> /etc/apache2/apache2.conf')
        #sudo('cp /vagrant/Apache2/ports.conf /etc/apache2/ports.conf')
        #sudo('sudo cp /vagrant/Apache2/default /etc/apache2/sites-available/default')
        sudo('service apache2 restart')

        print colored('##########################', 'blue')
        print colored('## NETWORK CONFIGURATION #', 'blue')
        print colored('##########################', 'blue')
        with hide('output'):
            netconf = sudo('ip addr show')
        print colored(netconf, 'yellow')

        #############################################################################
        #############################################################################
