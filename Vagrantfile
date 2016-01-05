# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/trusty32"
  config.ssh.forward_agent = true
  config.ssh.forward_x11 = true
  locale = "fr_FR.UTF.8"


  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
   config.vm.provider "virtualbox" do |vb|
     # Display the VirtualBox GUI when booting the machine
     vb.gui = true
  
     # Customize the amount of memory on the VM:
     vb.memory = "2048"
   end
  #
  # View the documentation for the provider you are using for more
  # information on available options.



  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
   config.vm.provision "shell", inline: <<-SHELL
	 sudo add-apt-repository ppa:chris-lea/node.js
     sudo apt-get update
     sudo apt-get install -y apache2
	 sudo apt-get install -y python3
	 sudo apt-get install -y python-dev
	 sudo apt-get install -y python-pip
	 sudo apt-get install -y python3-pip
	 sudo apt-get install -y libffi-dev
	 sudo apt-get install -y php5 php5-cli libapache2-mod-php5
	 sudo apt-get install -y docker
	 sudo apt-get install -y docker.io
	 sudo apt-get intall -y proftpd proftpd
	 sudo apt-get install -y erlang
	 sudo apt-get install -y rabbitmq-server
	 sudo apt-get install -y git
	 sudo apt-get install -y postgressql
	 sudo apt-get install -y pgadmin3
	 sudo apt-get install -y python-software-properties python g++ make
	 sudo apt-get install -y nodejs	 
	 sudo apt-get install -y lilypond
	 sudo apt-get install -y cmake
	 sudo apt-get install -y xorg
	 sudo apt-get install -y xinit
	 sudo docker pull mysql
	 sudo docker pull django
	 sudo docker pull marvambass/piwik
	 sudo docker pull redmine
	 sudo docker pull alunduil/roundcube
	 sudo docker pull rabbitmq
	 sudo pip install django
	 # install gitlab
	 #sudo apt-get install -y curl openssh-server ca-certificates postfix
	 #curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash
	 #sudo apt-get install -y gitlab-ce
	 #sudo gitlab-ctl reconfigure
	 # install libgit
	 pip install cffi
	 sudo wget https://github.com/libgit2/libgit2/archive/v0.23.4.tar.gz
	 tar xzf v0.23.4.tar.gz
	 cd libgit2-0.23.4/
	 cmake .
	 make
	 sudo make install
	 sudo apt-get install libgit2-dev
	 pip install pygit2
	 sudo ldconfig

   SHELL
end
