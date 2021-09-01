FROM python:3
USER root

WORKDIR /root

RUN wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
RUN xz -dc ffmpeg-release-amd64-static.tar.xz | tar xfv -
RUN rm ffmpeg-release-amd64-static.tar.xz
RUN mv ffmpeg-* bin
ENV PATH /root/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE 1
RUN pip install pillow clint requests

WORKDIR /veddy
ENTRYPOINT ["/usr/local/bin/python3","-u","main.py"]