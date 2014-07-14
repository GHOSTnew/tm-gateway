#rsa:2048
openssl req -x509 -nodes -days 365 -newkey rsa:8192 -keyout my.key -out my.crt
#openssl req -x509 -nodes -days 365 -newkey rsa:50000 -keyout my.key -out my.crt
