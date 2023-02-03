# cyber-fyp
# The important thing you need to do:
1. clone the repository
2. switch to dev branch
3. take a pull request from dev branch
4. create your own branch in this format [name]_dev
5. checkout to your new branch 
6. take a pull from dev branch 
7. then use your branch for changes 

# To Run project Do the following steps:
 1. pip install virtualenv
 2. virtualenv env
 3. source env/Scripts/activate
 4. pip install requirements.txt
 5. Setup your db and then change the credentails in settings.py
 DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': [name of your db],
    'USER': [user of your db],
    'PASSWORD': [password of your db],
    'HOST': 'localhost',
    
    'PORT': ['port on which your db is running'],
  }
}
6. python manage.py migrate
7. python manage.py createsuperuser
5. python manage.py runserver
