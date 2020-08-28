#! /bin/bash

sudo apt update -y 
sudo apt upgrade -y

if [ $(which python3) ];
then
    echo 'Python 3 is already installed'
else 
   sudo apt install python3 python3-pip
   sudo apt install --fix-broken
   echo 'Python 3 and pip have been installed'
fi

if [ $(which selenium) ];
then
    echo 'Selenium is already installed'
else 
    echo 'Installing Selenium'
    python -m pip install selenium
    echo 'Selenium has been installed'
fi

if [ $(which geckodriver) ];
then 
    echo 'Geckodriver is already installed'
else 
    echo 'Installing Gecko driver'
    wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
    tar -xvzf geckodriver*
    chmod +x geckodriver
    sudo mv geckodriver /usr/local/bin/
    echo 'Gecko driver is installed'
fi 
