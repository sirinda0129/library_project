### --- Final small image --- ###
FROM python:3.7-alpine as build
LABEL maintainer="Alexandr Khmelevsky <a.khmelevsky.255@gmail.com>"

ENV PYTHONUNBUFFERED 1
ENV WORKDIR /opt/app
ENV WHEELDIR /opt/packages

WORKDIR $WORKDIR
COPY requirements.txt $WORKDIR

RUN apk add --no-cache --virtual .build-dependencies gcc libc-dev linux-headers

RUN pip install --upgrade pip \
  && pip wheel --wheel-dir=${WHEELDIR} -r requirements.txt \
  && rm -rf .cache/pip \
  && apk del .build-dependencies

### --- Final small image --- ###
FROM python:3.7-alpine

ENV WORKDIR /opt/app
ENV WHEELDIR /opt/packages

WORKDIR $WORKDIR
COPY requirements.txt $WORKDIR
COPY --from=build ${WHEELDIR} ${WHEELDIR}

RUN apk --no-cache add util-linux \
  && pip install --upgrade pip \
  && pip install -r requirements.txt --find-links=${WHEELDIR} \
  && rm -rf .cache/pip \
  && rm -rf ${WHEELDIR} \
  && rm requirements.txt

COPY . $WORKDIR

EXPOSE 8000

CMD ["/bin/sh", "docker-entrypoint.sh"]