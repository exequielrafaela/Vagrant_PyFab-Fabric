VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = 512
    vb.cpus = 1
  end

  config.vm.network "private_network", type: "dhcp"

  config.hostmanager.enabled = true
  config.hostmanager.ip_resolver = proc do |vm, resolving_vm|
	  if vm.id
		    `VBoxManage guestproperty get #{vm.id} "/VirtualBox/GuestInfo/Net/1/V4/IP"`.split()[1]
	  end
  end

  config.vm.define :server do |srv|
    srv.vm.hostname = "server"
    #srv.vm.synced_folder "server/", "/usr/local/nagios/etc", create: true
    #srv.vm.network "forwarded_port", guest: 80, host: 8080
    #srv.vm.provision "shell", path: "server-provision"
    srv.vm.provision :fabric do |fabric|
      fabric.fabfile_path = "./fabfile.py"
      fabric.tasks = ["server", ]
    end
  end

  config.vm.define :client1 do |cl1|
    cl1.vm.hostname = "client1"
    #cl1.vm.synced_folder "client/", "/usr/local/nagios/etc", create: true
    #cl1.vm.provision "shell", path: "client-provision"
    cl1.vm.provision :fabric do |fabric|
      fabric.fabfile_path = "./fabfile.py"
      fabric.tasks = ["client1", ]
    end
  end
  config.vm.define :client2 do |cl2|
    cl2.vm.hostname = "client2"
    #cl2.vm.synced_folder "client/", "/usr/local/nagios/etc", creaete: true
    #cl2.vm.provision "shell", path: "client-provision"
    cl2.vm.provision :fabric do |fabric|
      fabric.fabfile_path = "./fabfile.py"
      fabric.tasks = ["client2", ]
    end
  end
end
