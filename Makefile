include .env

.PHONY: run
run:
	@echo "Starting server..."
	uvicorn main:app --reload --port ${PORT} --host ${HOST}