add-apt-repository ppa:ubuntugis/ppa
apt-get update
apt-get -y install gdal-bin libgdal-dev

source antenv/bin/activate
python manage.py makemigrations
python manage.py makemigrations data
python manage.py migrate

gunicorn --bind=0.0.0.0 --timeout 600 data_appraisal.wsgi
