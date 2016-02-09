#sudo apt-get update -y
#sudo apt-get upgrade -y
sudo apt-get install -y  python3 python-pip python3-mysql.connector
sudo apt-get install -y git
sudo apt-get install -y lilypond
sudo apt-get install -y nodejs npm
npm install -g bower
sudo apt-get install -y doxygen

sudo pip install -r requirements.txt

sudo python manage.py makemigrations
sudo python manage.py migrate
sudo python manage.py createcachetable
# sudo python manage.py createsuperuser --username=admin --email=admin@example.com
sudo python manage.py collectstatic

cd documentation 
sudo doxygen
cd ..

bower install

