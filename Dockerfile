FROM nats:latest
COPY nats-server.conf /nats-server.conf
CMD ["nats-server", "-c", "/nats-server.conf"]
