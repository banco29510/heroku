#sudo apt-get update -y
#sudo apt-get upgrade -y
sudo apt-get install -y  python3 python-pip python3-mysql.connector
sudo apt-get install -y git
sudo apt-get install -y lilypond
sudo apt-get install -y nodejs npm
npm install -g bower
sudo apt-get install -y doxygen


sudo apt-get install -y mysql-server
sudo service mysql start

sudo pip install -r requirements.txt

sudo git clone https://banco29510:antoine29510@bitbucket.org/banco29510/score_c9.git
cd score_c9

sudo python manage.py makemigrations
sudo python manage.py migrate
sudo python manage.py createcachetable
sudo python manage.py createsuperuser --username=admin --email=admin@example.com
sudo python manage.py collectstatic


sudo doxygen

bower install

