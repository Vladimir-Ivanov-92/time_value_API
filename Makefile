up:
	docker compose -f docker-compose.yml up -d

down:
	docker compose -f docker-compose.yml down

test:
	docker exec -it app bash -c "pytest . -v"