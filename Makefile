
ifneq (,$(wildcard .env))
    include .env
    export
endif

export PROJECT_ROOT := $(shell pwd)
export AIRFLOW_UID := $(shell id -u)

COMPOSE := docker compose -f $(PROJECT_ROOT)/.docker/docker-compose.yaml

.PHONY: build
build:
	mkdir -p $(PROJECT_ROOT)/data/logs $(PROJECT_ROOT)/data/plugins $(PROJECT_ROOT)/data/config
	$(COMPOSE) build --pull

.PHONY: up
up:
	AIRFLOW_USER=$(AIRFLOW_USER) AIRFLOW_PASSWORD=$(AIRFLOW_PASSWORD) AIRFLOW_EMAIL=$(AIRFLOW_EMAIL) $(COMPOSE) up -d

.PHONY: down
down:
	$(COMPOSE) down

.PHONY: sync
sync:
	uv sync --no-install-project --all-groups
	uv run -- python -m playwright install chromium

.PHONY: clean
clean:
	$(COMPOSE) down -v --remove-orphans --rmi all
	rm -rf $(PROJECT_ROOT)/data
