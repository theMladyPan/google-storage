# docker run latest image
start:	
	docker compose -f 'docker-compose.yaml' up -d --build 

# docker stop and remove container
stop:
	docker compose -f 'docker-compose.yaml' down


restart:
	make stop
	make start