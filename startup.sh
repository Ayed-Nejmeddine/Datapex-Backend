add-apt-repository ppa:ubuntugis/ppa
apt-get update
apt-get -y install gdal-bin libgdal-dev
gunicorn --bind=0.0.0.0 --timeout 600 data_appraisal.wsgi
echo "aaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
ls
