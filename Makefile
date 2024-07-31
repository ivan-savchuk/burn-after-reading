include src/.env

.PHONY: run
run:
	@echo "Starting server..."
	cd src; \
	uvicorn main:app --reload --port ${PORT} --host ${HOST};