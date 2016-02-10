# README.md #

### La maison des partitions ###

### Pré requis ###

- Python 3.5
- Wamp 
- Compte gitlab [Gitlab](https://gitlab.com/) ou compte GIT
- Compte reCaptcha [reCaptcha](https://www.google.com/recaptcha/intro/index.html)
- Compte Raven [Raven/sentry](https://getsentry.com/welcome/)
- Doxygen [Doxygen](http://www.stack.nl/~dimitri/doxygen/)
- RabbitMQ [RabbitMQ](https://www.rabbitmq.com/) ou cloud rabbitmq
- Compte CI sur sémaphore (cf : installation automatisé)

### Installation ###

1 Dépendances :

    pip install -r requirements.txt
    
2 Piwik :

Installtion de piwik : [Piwik](http://fr.piwik.org/telechargement/)

3 Configuration de la base de données :

Créer base score en UTF8

Modifier le settings.py

4 Django :

    manage.py makemigrations
    manage.py migrate

Commande suivante à chaque lancement :

    manage.py runserver
    
Dans le dossier score du projet

    celery -A score worker -l info
    
### Installation automatisé ###

sudo sh setup.sh


### CONTACT ###

contact : banco29510@gmail.com