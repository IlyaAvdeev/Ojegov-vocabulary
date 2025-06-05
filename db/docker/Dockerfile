FROM postgres:17-bookworm

RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

RUN mkdir /init_voc

ENV POSTGRES_DB words
ENV PGDATA /var/lib/postgresql/data