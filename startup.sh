add-apt-repository ppa:ubuntugis/ppa
apt-get update
apt-get -y install gdal-bin libgdal-dev
echo "aaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
ls
gunicorn --bind=0.0.0.0 --timeout 600 data_appraisal.wsgi
