FROM nginx:1.17.4

COPY default.conf /etc/nginx/conf.d/default.conf

RUN rm -r /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]