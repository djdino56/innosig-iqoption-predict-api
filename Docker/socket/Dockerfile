FROM python:3.7-buster

RUN apt-get update -y

# TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
  tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --prefix=/usr && \
  make && \
  make install

RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz

RUN mkdir /app
COPY src/requirements.txt /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY src /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD [ "python", "-u", "sockets/process.py" ]