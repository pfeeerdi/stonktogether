FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev

COPY requirements.txt ./app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app
CMD ["/bin/echo", "Running Python script now"]
ENTRYPOINT [ "python3" ]

CMD [ "server.py" ]



# docker build -t registry.gitlab.com/femu/jwt-auth/api . -->dockerfile needs to be there
# docker login registry.gitlab.com -u #username -p #token
# docker push registry.gitlab.com/femu/jwt-auth/api