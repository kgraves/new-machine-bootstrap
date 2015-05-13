# import fabric
from fabric.api import abort
from fabric.api import cd
from fabric.api import env
from fabric.api import execute
from fabric.api import get
# from fabric.api import lcd
from fabric.api import local
from fabric.api import put
from fabric.api import run
from fabric.api import settings
from fabric.api import sudo
from fabric.api import task
from fabric.colors import green
from fabric.colors import red
# from fabric.context_managers import hide
# from fabric.context_managers import settings
# from fabric.context_managers import show
from fabric.contrib.console import confirm
# from fabric.contrib import files
from fabric.decorators import parallel
from fabric.decorators import runs_once
from fabric.decorators import with_settings
from fabric.decorators import wraps
# from fabric.contrib.project import rsync_project
import fabric.api
import fabric.state
import fabric.utils

@task
def install_chrome():
    """
    Downloads chrome from google, and installs it via dpkg

    TODO try to figure out how to install extensions
    """
    get('wget -O /tmp/chrome_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb')
    local('sudo dpkg -i /tmp/chrome_amd64.deb')

@task
def install_vim():
    """
    Install vim via apt-get
    """
    local('sudo apt-get install vim')

@task
def install_gnome_tweak_tool():
    """
    Install gnome-tweak-tool via apt-get
    """
    local('sudo apt-get install gnome-tweak-tool')

@task
def install_gimp():
    """
    Install gimp via apt-get
    """
    local('sudo apt-get install gimp')

@task
def install_flux():
    """
    Download flux tarball, untar, then put in /usr/local/bin
    """
    with cd('/tmp'):
        get('wget https://justgetflux.com/linux/xflux64.tgz')
        local('tar xzvf xflux64.tgz')
        local('cp xflux /usr/local/bin/xflux')

@task
def remove_depricated_bluetooth_package():
    """
    Uninstalls deprecated bluetooth package.

    NOTE This should only be run when this package is not used.
    """
    local('sudo apt-get-purge oem-wireless-bluetooth-intel-7260-dkms')

