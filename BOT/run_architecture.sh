docker-compose -f docker-compose.yml up -d --build rabbitmq

docker-compose -f docker-compose.yml up -d --build pokedex_database

DATABASE_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' pokedex_database) 

echo $DATABASE_IP

DATABASE_IP=$DATABASE_IP docker-compose -f docker-compose.yml up -d --build pokedex_manager

docker-compose -f docker-compose.yml up -d --build discord_listener