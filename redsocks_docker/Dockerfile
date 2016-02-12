FROM debian:wheezy

ENTRYPOINT ["/usr/sbin/redsocks", "-c", "/etc/redsocks.conf"]
RUN apt-get -q update
RUN apt-get -qy install \
    procps \
    psmisc \
    redsocks
ADD redsocks.conf /etc/redsocks.conf
