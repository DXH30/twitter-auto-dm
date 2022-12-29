# Introduction
This is a simple api implementing tweeter api

# How to run
Run using docker-compose
```
docker-compose up -d
```

# How to generate certificate
Using mkcert
```
mkcert example.com
```
move PEM certifcate to docker/nginx/certs/cert.pem, and PEM key to docker/nginx/certs/cert.key
```
mv *example.com*key* docker/nginx/certs/cert.key
```
```
mv *example.com*pem* docker/nginx/certs/cert.pem
```
