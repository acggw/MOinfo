#!bin/bash

sudo cp apache_config.conf /etc/apache2/sites-available/moinfo.conf

sudo chmod o+x /home/$USER
sudo chmod -R o+rx /home/$USER/MOinfo/Flask

sudo a2ensite moinfo.conf
sudo systemctl reload apache2

