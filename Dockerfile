FROM python:3.6.4-alpine3.7
LABEL MAINTAINER = "s.abdulhakeem@hotmail.com"


ARG PIP_PKG_IDX_ARGS
ARG APP_CONF=pylons/conf/production.ini

ENV APP_CONF ${APP_CONF}
ENV DATABASE_URL ${DATABASE_URL}
ENV SESSION_KEY ${SESSION_KEY}
ENV JWT_PUBLIC_KEY ${JWT_PUBLIC_KEY}
ENV JWT_PRIVATE_KEY ${JWT_PRIVATE_KEY}
ENV SMTP_HOST ${SMTP_HOST}
ENV SMTP_PORT ${SMTP_PORT}
ENV SMTP_USERNAME ${SMTP_USERNAME}
ENV SMTP_PASSWORD ${SMTP_PASSWORD}

ENV APP_HOME /usr/lib/pylons/default
ENV APP_DATA /var/lib/pylons


# Install build deps, run `pip install` then remove unneeded build deps all in
# a single step.
RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
       gcc \
       make \
       pwgen \
       libc-dev \
       musl-dev \
       pcre-dev \
       libffi-dev \
       libxml2-dev \
       libxslt-dev \
       linux-headers \
       postgresql-dev \
    && pip install virtualenv

# setup virtual evn
RUN mkdir -p ${APP_HOME} ${APP_DATA} \
    && virtualenv ${APP_HOME} \
    && ln -s ${APP_HOME}/bin/pip /usr/local/bin/pylons-pip \
    && ln -s ${APP_HOME}/bin/paster /usr/local/bin/pylons-paster \
    && ln -s ${APP_HOME}/bin/pserve /usr/local/bin/pylons-pserve

# install private libs
RUN pylons-pip install --upgrade --use-wheel elixr2 ${PIP_PKG_IDX_ARGS}

# install other requirements
COPY ./requirements.txt /opt/pylons/
RUN pylons-pip install --use-wheel -r /opt/pylons/requirements.txt

# add shell scripts
ADD https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh /opt/pylons/wait-for-it.sh
COPY ./bin/create-admin-user.sh /opt/pylons/
COPY ./bin/pylons-entrypoint.sh /opt/pylons/
RUN chmod +x /opt/pylons/create-admin-user.sh \
             /opt/pylons/wait-for-it.sh \
             /opt/pylons/pylons-entrypoint.sh

# copy application code to image (ensure to create a .dockerignore file to
# exclude large files or directories)
COPY . ${APP_HOME}/src/pylons
ENTRYPOINT ["/opt/pylons/pylons-entrypoint.sh"]
EXPOSE 6543

WORKDIR ${APP_HOME}/src/pylons
CMD pylons-pserve --reload elx://${APP_CONF}
