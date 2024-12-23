## MySQL setup

```
docker run --name my-mysql-container \
  -e MYSQL_ROOT_PASSWORD=**** \
  -e MYSQL_DATABASE=**** \
  -e MYSQL_USER=**** \
  -e MYSQL_PASSWORD=**** \
  -p 3307:3306 \
  -d mysql/mysql-server:latest
```