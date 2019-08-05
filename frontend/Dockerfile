FROM node

ADD . /

RUN npm install
RUN npm run build


RUN npm install http-server 

WORKDIR dist/

EXPOSE 8080

CMD ["node", "../node_modules/http-server/bin/http-server", "-d", "False"]