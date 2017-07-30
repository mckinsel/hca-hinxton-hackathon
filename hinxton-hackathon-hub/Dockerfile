FROM ubuntu:zesty

RUN apt-get update \
 && apt-get install -y curl git python3-pip apt-transport-https ca-certificates software-properties-common \
 && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - \
 && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu zesty stable" \
 && apt-get update \
 && apt-get install -y docker-ce

RUN apt-get install -y npm nodejs-legacy \
 && npm install -g configurable-http-proxy \
 && pip3 install jupyterhub notebook jupyterhub-hashauthenticator

RUN git clone https://github.com/cassinyio/SwarmSpawner \
 && cd SwarmSpawner \
 && pip3 install -r requirements.txt \
 && python3 setup.py install

RUN sed -i -e 's/10)/600)/' /usr/local/lib/python3.5/dist-packages/jupyterhub/handlers/base.py
RUN mkdir -p /srv/jupyterhub

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyter_config.py"]
