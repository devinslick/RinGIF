FROM alpine:3.8
VOLUME ["/data"]
ENV email=emailaddress@notdefined.yet
ENV password=undefined
ENV doorbell=0
ENV fps=1
ENV archivePath=
RUN apk --update add --no-cache py-pip
RUN apk --update add --no-cache imagemagick
RUN apk --update add --no-cache ffmpeg
RUN apk --update add --no-cache libjpeg-turbo-utils
RUN apk --update add --no-cache tini
RUN pip install ring_doorbell
WORKDIR /
ENTRYPOINT ["/sbin/tini", "--"]
RUN wget https://raw.githubusercontent.com/devinslick/RinGIF/master/RinGIF.sh
RUN wget https://raw.githubusercontent.com/devinslick/RinGIF/master/check_last_recording.py
RUN chmod a+x *.sh
RUN echo '*  *  *  *  *    /RinGIF.sh' > /etc/crontabs/root
CMD ["/usr/sbin/crond", "-f"]
