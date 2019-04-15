start:
	docker-compose up -d neo4j
stop:
	docker stop neo4j && docker rm neo4j
