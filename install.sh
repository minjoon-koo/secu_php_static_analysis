#django install
pip install django
pip install python-dotenv
pip install xmltodict


#jira 
pip install jira



#ubuntu
sudo apt install software-properties-common
sudo add-apt-repository ppa:ondrej/php


apt install php-curl php-json php-mbstring php-mysql php-xml php-zip
curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/bin/ 
sudo ln -s /usr/bin/composer.phar /usr/bin/composer

#WORKDIR = ./app/Storage
composer require --dev vimeo/psalm
composer require --dev psalm/plugin-laravel
./vendor/bin/psalm --init
./vendor/bin/psalm-plugin enable psalm/plugin-laravel
composer require --dev roave/psalm-html-output