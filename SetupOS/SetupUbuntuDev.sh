echo ""
echo "Setting up the OS"
echo "-----------------"
echo "Logfile: /var/log/setupOS.log"
echo ""

# Configuration
# -------------

# Using apache2 as web server
# This setting changes which packages are installed.
# E.g. for PHP
using_apache2=true

# Basic tools
install_basic_tools=true
    # Web server
    install_apache2=true
    # Version control
    install_git=true

# PHP
install_php=true
    # PHP 8.1
    install_php8_1=true

# Developer tools
install_dev_tools=true
    # Color picker
    install_gpick=true
    # MySQL client
    install_heidiSQL=true
    # Text editor
    install_vscode=true

if $install_basic_tools ; then
    echo "Installing basic tools ..."

    if $install_apache2 ; then
        echo "    Installing Apache2"
        echo "----------------------------------" >> /var/log/setupOS.log
        echo "Installing Apache2 ..." >> /var/log/setupOS.log

        echo "> sudo apt-get -y install apache2" >> /var/log/setupOS.log
        sudo apt-get -y install apache2 >> /var/log/setupOS.log
    fi

    if $install_git ; then
        echo "    Installing Git ..."
        echo "----------------------------------" >> /var/log/setupOS.log
        echo "Installing Git ..." >> /var/log/setupOS.log
        
        echo "> sudo apt-get -y install git" >> /var/log/setupOS.log
        sudo apt-get -y install git >> /var/log/setupOS.log
    fi

    echo ""
fi

if $install_php ; then
    # Source: https://de.linuxcapable.com/how-to-install-php-8-1-on-ubuntu-20-04/
    echo "Installing PHP ..."
    echo "----------------------------------" >> /var/log/setupOS.log
    echo "Installing PHP ..." >> /var/log/setupOS.log
    
    echo "Install dependencies ..." >> /var/log/setupOS.log
        
    echo "> sudo apt-get -y install software-properties-common" >> /var/log/setupOS.log
    sudo apt-get -y install software-properties-common >> /var/log/setupOS.log

    echo "> sudo add-apt-repository ppa:ondrej/php -y" >> /var/log/setupOS.log
    sudo add-apt-repository ppa:ondrej/php -y >> /var/log/setupOS.log

    if $install_php8_1 ; then
        # Source : https://de.linuxcapable.com/how-to-install-php-8-1-on-ubuntu-20-04/
        echo "    Installing PHP 8.1"
        echo "----------------------------------" >> /var/log/setupOS.log
        echo "Installing PHP 8.1 ..." >> /var/log/setupOS.log

        echo "> sudo apt-get -y install php8.1" >> /var/log/setupOS.log
        sudo apt-get -y install php8.1 >> /var/log/setupOS.log

        if $using_apache2 ; then
            echo "> sudo apt-get -y install libapache2-mod-php8.1" >> /var/log/setupOS.log
            sudo apt-get -y install libapache2-mod-php8.1 >> /var/log/setupOS.log

            echo "> sudo systemctl restart apache2" >> /var/log/setupOS.log
            sudo systemctl restart apache2 >> /var/log/setupOS.log
        fi
    fi

    echo ""
fi
install_php=true
    # PHP 8.1
    install_php8_1=true

if $install_dev_tools ; then
    echo "Installing developer tools ..."

    if $install_gpick ; then
        # Source: https://zoomadmin.com/HowToInstall/UbuntuPackage/gpick
        echo "    Installing Gpick"
        echo "----------------------------------" >> /var/log/setupOS.log
        echo "Installing Gpick ..." >> /var/log/setupOS.log
        
        echo "> sudo apt-get -y install gpick" >> /var/log/setupOS.log
        sudo apt-get -y install gpick >> /var/log/setupOS.log
    fi

    if $install_heidiSQL ; then
        # Source: https://snapcraft.io/install/heidisql-wine/ubuntu
        echo "    Installing HeidiSQL ..."
        echo "----------------------------------" >> /var/log/setupOS.log
        echo "Installing HeidiSQL ..." >> /var/log/setupOS.log

        echo "> sudo snap install heidisql-wine --beta" >> /var/log/setupOS.log
        sudo snap install heidisql-wine --beta >> /var/log/setupOS.log
    fi

    if $install_vscode ; then
        # Source: https://linuxize.com/post/how-to-install-visual-studio-code-on-debian-10/
        echo "    Installing Visual Studio Code ..."
        echo "----------------------------------" >> /var/log/setupOS.log
        echo "Installing Visual Studio Code ..." >> /var/log/setupOS.log
        
        echo "Install dependencies ..." >> /var/log/setupOS.log
        
        echo "> sudo apt-get -y install software-properties-common" >> /var/log/setupOS.log
        sudo apt-get -y install software-properties-common >> /var/log/setupOS.log
        
        echo "> sudo apt-get -y install apt-transport-https" >> /var/log/setupOS.log
        sudo apt-get -y install apt-transport-https >> /var/log/setupOS.log
        
        echo "> sudo apt-get -y install curl" >> /var/log/setupOS.log
        sudo apt-get -y install curl >> /var/log/setupOS.log
        
        echo "Add GPG key for MSFT repo ..." >> /var/log/setupOS.log
        curl -sSL https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
        
        echo "> sudo add-apt-repository --yes \"deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main\"" >> /var/log/setupOS.log
        sudo add-apt-repository --yes "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" >> /var/log/setupOS.log
        
        echo "> sudo apt-get -y install code" >> /var/log/setupOS.log
        sudo apt-get -y install code >> /var/log/setupOS.log
    fi
    
    echo ""
fi