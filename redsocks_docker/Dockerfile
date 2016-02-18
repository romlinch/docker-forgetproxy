FROM debian:jessie

RUN apt-get -q update
RUN apt-get -qy install \
    procps \
    psmisc \
    redsocks \
    iptables
CMD ["/tmp/run"]
ADD redsocks.conf /etc/redsocks.conf
ADD run /tmp/run
