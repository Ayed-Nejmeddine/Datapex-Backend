add-apt-repository ppa:ubuntugis/ppa
apt-get update
apt-get install gdal-bin libgdal-dev
export GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
