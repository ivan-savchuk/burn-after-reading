include src/.env

.PHONY: run
run:
	@echo "Starting server..."
	cd src; \
	uvicorn main:app --reload --port ${PORT} --host ${HOST};

.PHONY: up
up:
	@echo "Starting server..."
	docker-compose -f build/docker-compose.yaml build --build-arg PORT=${PORT} --build-arg HOST=${HOST}
	docker-compose -f build/docker-compose.yaml up -d

.PHONY: down
down:
	@echo "Stopping server..."
	docker-compose -f build/docker-compose.yaml down

.PHONY: clean
clean:
	@echo "Cleaning..."
	docker rmi -f fastapi-app:latest