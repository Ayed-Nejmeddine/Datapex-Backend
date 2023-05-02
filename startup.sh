add-apt-repository ppa:ubuntugis/ppa
apt-get update
apt-get -y install gdal-bin libgdal-dev
export GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
gunicorn --bind=0.0.0.0 --timeout 60000 data_appraisal.wsgi
