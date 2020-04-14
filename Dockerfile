FROM python:3.6-slim
LABEL maintainer "Sebastian Weiss <wpai@3ele.de>"
RUN  apt-get update  &&\
        ACCEPT_EULA=Y  apt-get install -y \
        python3-pip  -y \
        python3-setuptools -y \
        python-dev \
        && rm -rf /var/lib/apt/lists/*  

COPY app /home/app
RUN pip3 install  -r home/app/requirements.txt
ARG PASSWORD
ARG USER




WORKDIR /home/app
#ENTRYPOINT [ "python3" ]
#CMD ["app.py"]
RUN chmod +x ./start.sh
RUN chown -R www-data:www-data ./wp
CMD ["./start.sh"]
EXPOSE 5000
