# TODO possibly start using visudo so we don't have to type in password during
# run of fabric. Although it's not a huge deal right now.

from fabric.api import abort
from fabric.api import env
from fabric.api import execute
from fabric.api import get
from fabric.api import local
from fabric.api import put
from fabric.api import run
from fabric.api import settings
from fabric.api import sudo
from fabric.colors import green
from fabric.colors import red
from fabric.context_managers import cd, lcd
from fabric.contrib.console import confirm
from fabric.decorators import parallel
from fabric.decorators import runs_once
from fabric.decorators import task

@task
def setup_machine():
    """
    Main task that will run all other installation and setup tasks
    """
    #TODO setup selections for certain packages (e.g. node installation)
    execute('install_development_deps')
    execute('install_db_stuff')
    execute('install_java_stuff')
    execute('install_node_stuff')
    execute('install_python_stuff')
    execute('install_ruby_stuff')
    execute('install_xps13de_stuff')
    execute('install_personal_stuff')

@task
def install_personal_stuff():
    """
    Installs/Sets up all non-development packages
    """
    execute('install_chrome')
    execute('install_gnome_tweak_tool')
    execute('install_gimp')
    execute('install_flux')
    execute('remove_depricated_bluetooth_package')
    execute('install_spotify')
    execute('install_lynx')
    execute('install_image_magick')

@task
def install_chrome():
    """
    Downloads chrome from google, and installs it via dpkg
    """
    # TODO try to figure out how to install extensions.
    # It looks as though there is a preferences file where you can specify
    # this. see: https://developer.chrome.com/extensions/external_extensions#preferences
    with lcd('/tmp'):
        local('wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb')
        local('sudo dpkg -i google-chrome-stable_current_amd64.deb')

@task
def install_gnome_tweak_tool():
    """
    Install gnome-tweak-tool via apt-get
    """
    local('sudo apt-get -y install gnome-tweak-tool')

@task
def install_gimp():
    """
    Install gimp via apt-get
    """
    local('sudo apt-get -y install gimp')

@task
def install_flux():
    """
    Download flux tarball, untar, then put in /usr/local/bin
    """
    with cd('/tmp'):
        local('wget https://justgetflux.com/linux/xflux64.tgz')
        local('tar xzvf xflux64.tgz')
        local('cp xflux /usr/local/bin/xflux')

@task
def remove_depricated_bluetooth_package():
    """
    Uninstalls deprecated bluetooth package.

    NOTE This should only be run when this package is not used.
    """
    local('sudo apt-get -y purge oem-wireless-bluetooth-intel-7260-dkms')

@task
def install_spotify():
    """
    installs deps, adds apt source, and install spotify
    """

    # install libgcrypt
    with lcd('/tmp'):
        local('wget -O libcrypt.deb https://launchpad.net/ubuntu/+archive/primary/+files/libgcrypt11_1.5.3-2ubuntu4.2_amd64.deb')
        local('sudo dpkg -i libcrypt.deb')

    # setup spotify apt source
    local('sudo echo "deb http://repository.spotify.com stable non-free" >> /etc/apt/sources.list')
    local('sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 94558F59')
    local('sudo apt-get -y update')

    # install spotify
    local('sudo apt-get -y install spotify-client')

@task
def install_lynx():
    """
    Install cli web browser
    """
    local('sudo apt-get -y install lynx')

@task
def install_image_magick():
    """
    Installs imagemagick
    """
    local('sudo apt-get -y install imagemagick')

@task
def install_development_deps():
    """
    Installs all development dependencies
    """

    # deps via apt-get
    deps = ' '.join([
        'build-essentials',
        'bzr',
        'libc++1',
        'git',
        'python-dev',
        'python-pip',
        'vim'
    ])
    local('sudo apt-get -y install %s' % deps)

    # install heroku-tookbelt
    local('wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh')

    # install/setup vim stuff
    local('mkdirk ~/.vim')
    with lcd('~/.vim'):
        local('mkdir autoload bundle colors')

        with lcd('./autoload'):
            local('wget https://tpo.pe/pathogen.vim')

        with lcd('./bundle'):
            local('git clone git@github.com:kien/ctrlp.vim.git')
            local('git clone git@github.com:digitaltoad/vim-jade.git')
            local('git clone git@github.com:plasticboy/vim-markdown.git')

        with lcd('./colors'):
            local('wget https://raw.githubusercontent.com/nanotech/jellybeans.vim/master/colors/jellybeans.vim')

@task
def install_db_stuff():
    """
    Installs all dbs needed locally:
    - mongodb

    TODO figure out if there is a 'latest' release, so we do not have to settle
    for a particular release.
    """

    # install mongodb
    with lcd('/tmp'):
        # download tarball and untar
        local('wget -O mongo3.0.3.tgz https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1410-clang-3.0.3.tgz')
        local('tar xzvf mongo3.0.3.tgz')

        # copy all binaries to /usr/bin
        with lcd('./mongo3.0.3/bin'):
            local('sudo cp ./* /usr/bin/')

    # create mongo data direcotry
    # TODO figure out which user will be running mongod and change permissions
    # for that user/group
    local('sudo mkdir -p /data/db')
    local('sudo chmod 777 /data && sudo chmod 777 /data/db')

@task
def install_java_stuff():
    """
    """
    # TODO
    pass

@task
def install_node_stuff():
    """
    install a more current version of node than what ubuntu ppa has.

    I ran into an issue where I needed some sync functions in the fs package
    that only the newer versions of node had.
    """
    # TODO possibly merge some functionality with below node_stuff task into a
    # general node_stuff function/task

    with lcd('/tmp'):
        # download and untar node
        local('wget -O node-v0.12.2.tar.gz http://nodejs.org/dist/v0.12.2/node-v0.12.2-linux-x64.tar.gz')
        local('tar xzvf node-v0.12.2.tar.gz')

        # copy bin to /usr/bin
        with lcd('./node-v0.12.2/bin'):
            local('sudo cp ./node /usr/bin/node-v0.12.2')

        # add node alias to .bashrc
        local('echo "# add node alias" >> .bashrc')
        local('echo "alias node="/usr/bin/node-v0.12.2"" >> .bashrc')

    # globally install npm packages
    packages = ' '.join([
        'bower',
        'express-generator'
    ])
    local('npm install -g %s' % packages)

@task
def install_node_stuff_via_apt():
    """
    install node via apt-get

    NOTE This will install an older (not up to date) version of node. For a more
    recent version of node, see the above function.
    """

    # install node via apt-get
    local('sudo apt-get -y install node')

    # add npm/bin directory to path and add node alias
    with lcd('~/'):
        # just to ensure that .bashrc exists
        local('touch .bashrc')
        local('echo "# add npm bin directory to path" >> .bashrc')
        local('echo "export PATH="\$PATH:\$HOME/npm/bin"" >> .bashrc')
        local('echo "# add node alias" >> .bashrc')
        local('echo "alias node="/usr/bin/nodejs"" >> .bashrc')

    # set global npm directory to ~/npm, rather than /usr/local...
    # permissions issues :(
    local('npm config set prefix ~/npm')

    # globally install npm packages
    packages = ' '.join([
        'bower',
        'express-generator'
    ])
    local('npm install -g %s' % packages)

@task
def install_python_stuff():
    """
    Upgrade pip, install pip packages, and some virtualenv stuff.

    NOTE dependencies are installed with install_development_deps task.
    """
    local('sudo pip install --upgrade pip')
    local('sudo pip install virtualenv')

    # add virtualenv's activate alias
    with lcd('~/'):
        local('echo "alias aa="source ./env/bin/activate" >> .bashrc')

@task
def install_ruby_stuff():
    """
    Install dependencies, get gpg key for rvm, rvm/rbenv
    """
    local('sudo apt-get -y install libffi-dev libgdbm-dev libncurses5-dev')
    local('gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3')
    local('curl -L https://get.rvm.io | bash -s stable')

@task
def install_xps13de_stuff():
    """
    Installs Dell xps13 de specific stuff, and makes some rc changes
    """
    # TODO add change to /etc/rc.local
    # TODO install libsmbios
    pass
