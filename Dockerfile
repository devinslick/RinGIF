FROM alpine:3.8
VOLUME ["/data"]
ENV email=emailaddress@notdefined.yet
ENV password=undefined
ENV fps=1
ENV resolution=192x108
ENV timezone=America/Chicago
RUN apk --update add --no-cache py-pip
RUN apk --update add --no-cache imagemagick
RUN apk --update add --no-cache ffmpeg
RUN apk --update add --no-cache libjpeg-turbo-utils
RUN apk --update add --no-cache tini
RUN apk --update add --no-cache jpegoptim
RUN apk --update add --no-cache tzdata
RUN apk --update add --no-cache caddy
RUN ln -sf /usr/share/zoneinfo/$timezone /etc/localtime
RUN pip install ring_doorbell
RUN pip install wget
RUN pip install ffmpeg-python
EXPOSE 8123
WORKDIR /
ENTRYPOINT ["/sbin/tini", "--"]
ADD . /
RUN chmod a+x *.sh
RUN echo '* * * * * /restart.sh' > /etc/crontabs/root
CMD ["/usr/sbin/crond", "-f"]
