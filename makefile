install:
	poetry install
	poetry run playwright install chromium


run-docker:
	docker run --rm -v $(PWD):/app -w /app python:3.11-slim \
		bash -c "pip install poetry && poetry install && poetry run pytest test_suite"
# 如果只是純 .py 改 code，掛 volume ，就可以在 docker 用最新的 code ，不用重新 run


#docker compose -f docker-compose-dev.yml down
# docker compose -f docker-compose-dev.yml up --build
# docker exec -it app bash
# pytest --env=test -s -v
