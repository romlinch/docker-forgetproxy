FROM debian:jessie
RUN apt-get -q update && apt-get -qy install iptables
ADD run /tmp/run
CMD ["/tmp/run"]
