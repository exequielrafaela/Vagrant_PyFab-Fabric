VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.network "private_network", type: "dhcp"
  config.hostmanager.enabled = true
  config.hostmanager.ip_resolver = proc do |vm, resolving_vm|
	  if vm.id
		    `VBoxManage guestproperty get #{vm.id} "/VirtualBox/GuestInfo/Net/1/V4/IP"`.split()[1]
	  end
  end

  config.vm.define :server do |srv|
    #srv.ssh.insert_key=false
    #srv.vm.box = "centos/7"
    srv.vm.box = "geerlingguy/centos7"
    #srv.vm.box = "geerlingguy/centos6"
    #srv.vm.box = "scalefactory/centos6"
    srv.vm.provider "virtualbox" do |vb|
      vb.memory = 512
      vb.cpus = 1
    end
    srv.vm.hostname = "server"
    #srv.vm.synced_folder "/home/e.barrirero/vagrant_projects/Vagrant_PyFab-Fabric", "/vagrant", type: "sshfs"
    srv.vm.provision :fabric do |fabric|
      fabric.fabfile_path = "./fabfile.py"
      fabric.tasks = ["server", ]
    end
  end

  config.vm.define :client1 do |cl1|
    #cl1.ssh.insert_key=false
    #cl1.vm.box = "centos/7"
    cl1.vm.box = "geerlingguy/centos7"
    #cl1.vm.box = "geerlingguy/centos6"
    #cl1.vm.box = "scalefactory/centos6"
    cl1.vm.provider "virtualbox" do |vb|
      vb.memory = 512
      vb.cpus = 1
    end
    cl1.vm.hostname = "centos-client1"
    #cl1.vm.synced_folder "/home/e.barrirero/vagrant_projects/Vagrant_PyFab-Fabric", "/vagrant", type: "sshfs"
    cl1.vm.provision :fabric do |fabric|
      fabric.fabfile_path = "./fabfile.py"
      fabric.tasks = ["client1", ]
    end
  end

  config.vm.define :client2 do |cl2|
    #cl2.ssh.insert_key=false
    #cl2.vm.box = "centos/7"
    cl2.vm.box = "geerlingguy/centos7"
    #cl2.vm.box = "geerlingguy/centos6"
    #cl2.vm.box = "scalefactory/centos6"
    cl2.vm.provider "virtualbox" do |vb|
      vb.memory = 512
      vb.cpus = 1
    end
    cl2.vm.hostname = "centos-client2"
    #cl1.vm.synced_folder "/home/e.barrirero/vagrant_projects/Vagrant_PyFab-Fabric", "/vagrant", type: "sshfs"
    cl2.vm.provision :fabric do |fabric|
      fabric.fabfile_path = "./fabfile.py"
      fabric.tasks = ["client2", ]
    end
  end
#  config.vm.define :client2 do |cl2|
#    #cl2.ssh.insert_key=false
#    cl2.vm.box = "centos/7"
#    cl2.vm.provider "virtualbox" do |vb|
#      vb.memory = 512
#      vb.cpus = 1
#    end
#    cl2.vm.hostname = "centos-client2"
#    cl2.vm.provision :fabric do |fabric|
#      fabric.fabfile_path = "./fabfile.py"
#      fabric.tasks = ["client2", ]
#    end
#  end
end
