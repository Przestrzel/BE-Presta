#!/bin/bash

CONTAINER="admin-mysql_db.1.jhmt04hxq732lvnr76m7ikzlv"

docker cp ./*.sql $CONTAINER:/tmp/be_172588.sql
docker cp ./db_create.sh $CONTAINER:/tmp/db_create.sh
docker exec -it $CONTAINER  chmod 777 /tmp/db_create.sh
docker exec -it $CONTAINER /bin/sh /tmp/db_create.sh
docker exec -it $CONTAINER  rm /tmp/be_172588.sql
docker exec -it $CONTAINER  rm /tmp/db_create.sh