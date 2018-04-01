#installing Ring Doorbell python package
#shoutout to the creator: https://github.com/tchellomello/python-ring-doorbell
yum -y install python-pip wget
pip install --upgrade pip
pip install ring_doorbell

#installing jpegtran for jpeg optimization
yum -y install libjpeg-turbo-utils

#Downloading and compiling Graphics Magick tools
gmInstalled=$(gm | wc -l)
if [ "$gmInstalled" -lt "2" ]; then
  echo Graphics Magick tools are already installed.
  exit
else
  echo Downloading and compiling Graphics Magick tools...
  cd /tmp
  wget ftp://ftp.graphicsmagick.org/pub/GraphicsMagick/GraphicsMagick-LATEST.tar.gz
  tar -xzvf GraphicsMagick-LATEST.tar.gz
  cd GraphicsMagick*
  yum -y install libpng libjpeg libpng-devel libjpeg-devel ghostscript libtiff libtiff-devel freetype freetype-devel jasper jasper-devel
  ./configure
  make install
  gm version
  ./configure --disable-openmp
  make install
  gm version
  ./configure --disable-openmp --bindir=/usr/bin --sbindir=/usr/sbin
  make install
  gm version
  make uninstall
fi
