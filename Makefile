up:

	docker compose -f docker-compose.yml up -d --build

down:
	docker compose -f docker-compose.yml down

test:
	docker exec -it app bash -c "pytest . -v"

run_stored_pocedure:
	docker exec -it app bash -c "python3 run_stored_procedure.py"