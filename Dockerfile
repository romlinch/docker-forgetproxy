FROM debian:jessie

RUN apt-get -q update
RUN apt-get -qy install \
    procps \
    psmisc \
    redsocks \
    iptables \
    python squid3
CMD ["/tmp/run"]

# Redsocks
ADD redsocks.conf /etc/redsocks.conf

# Squid
RUN sed -i "s/^#acl localnet/acl localnet/" /etc/squid3/squid.conf
RUN sed -i "s/^#http_access allow localnet/http_access allow localnet/" /etc/squid3/squid.conf
RUN sed -i "s/^http_access deny !Safe_ports/#http_access deny !Safe_ports/" /etc/squid3/squid.conf
RUN sed -i "s/^http_access deny CONNECT !SSL_ports/#http_access deny CONNECT !SSL_ports/" /etc/squid3/squid.conf
RUN	echo "forwarded_for delete" >> /etc/squid3/squid.conf
RUN mkdir -p /var/cache/squid3
RUN chown -R proxy:proxy /var/cache/squid3
ADD deploy_squid.py /tmp/deploy_squid.py
ADD run /tmp/run
