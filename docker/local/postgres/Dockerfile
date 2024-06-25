FROM postgres:15-bullseye


COPY ./docker/local/postgres/maintenace /usr/local/bin/maintenace

RUN chmod +x /usr/local/bin/maintenace/*

RUN mv /usr/local/bin/maintenace/* /usr/local/bin/ \
    && rmdir /usr/local/bin/maintenace