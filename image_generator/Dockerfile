FROM continuumio/anaconda3

RUN \
    apt-get -y install libgtk2.0 && \
    conda install -y -c menpo opencv3

COPY *.py /home/

WORKDIR /home
