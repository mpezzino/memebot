#!/bin/sh

# scp memebot_credentials.properties onto instance first

wget http://pypi.python.org/packages/source/p/pip/pip-1.1.tar.gz#md5=62a9f08dd5dc69d76734568a6c040508
tar -xvf pip*.gz
cd pip*
sudo python setup.py install
sudo pip uninstall requests

sudo mkdir /var/lib/memebot
sudo chmod 777 /var/lib/memebot

cd
sudo python setup.py install
sudo pip install -U nltk
python -c 'import nltk; nltk.download("stopwords"); nltk.download("punkt")'

sudo yum install tmux