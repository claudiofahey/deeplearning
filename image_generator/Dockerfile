FROM continuumio/anaconda3

RUN apt-get -y update && \
    apt-get -y install libgl1-mesa-dev

RUN conda install -y -c conda-forge opencv

COPY image_generator.py /usr/local/bin/
