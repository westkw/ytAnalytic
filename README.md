# Capstone

virtualenv -p python3 env

pip install -r requirements.txt

cd Portable/Web/django/mysite/

python3 manage.py migrate

python3 manage.py createcachetable

python3 manage.py runserver

On browser visit https://127.0.0.1:8000/

ctrl c to close server

