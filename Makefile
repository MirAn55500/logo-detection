# Название Docker образа
IMAGE:=logo-detection-app

# Общие команды
help:
	@echo "help - show this help"
	@echo "build - build docker image"
	@echo "test - run tests"
	@echo "lint - run linting"
	@echo "run - start application"
	@echo "dev - start application in dev mode with live reload"

# Команда для очистки Docker образа
clean:
	@docker rmi -f ${IMAGE}

# Команда для сборки Docker образа
build:
	@docker build -t ${IMAGE} . --network=host

# Команда для запуска приложения в режиме разработки с live reload
dev: build
	@echo 'Running dev server with live reload...'
	@docker run --rm \
		-v $(shell pwd)/weights:/app/weights \
		-v $(shell pwd)/data_folder:/app/data_folder \
		-p 8080:8080 \
		-it ${IMAGE} \
		adev runserver --livereload --host 0.0.0.0 --port 8080

# Команда для запуска приложения в обычном режиме
run: build
	@docker run --rm -it \
		-v $(shell pwd)/weights:/app/weights \
		-v $(shell pwd)/data_folder:/app/data_folder \
		-p 8080:8080 \
		${IMAGE}

# Команда для запуска тестов
test: build
	@echo 'Running tests...'
	@docker run --rm -v $(pwd):/app -i logo-detection-app \
		/bin/sh -c "PYTHONPATH=. pytest --disable-warnings -v tests/test_integration.py

# Команды для линтинга кода
flake8: build
	@echo 'Running flake8...'
	@docker run --rm \
		-v $(shell pwd)/weights:/app/weights \
		-v $(shell pwd)/data_folder:/app/data_folder \
		-it ${IMAGE} \
		python -m flake8 lib

pycodestyle: build
	@echo 'Running pycodestyle...'
	@docker run --rm \
		-v $(shell pwd)/weights:/app/weights \
		-v $(shell pwd)/data_folder:/app/data_folder \
		-it ${IMAGE} \
		python -m pycodestyle lib

pylint: build
	@echo 'Running pylint...'
	@docker run --rm \
		-v $(shell pwd)/weights:/app/weights \
		-v $(shell pwd)/data_folder:/app/data_folder \
		-it ${IMAGE} \
		python -m pylint lib

black: build
	@echo 'Running black...'
	@docker run --rm \
		-v $(shell pwd)/weights:/app/weights \
		-v $(shell pwd)/data_folder:/app/data_folder \
		-it ${IMAGE} \
		python -m black lib

# Команда для запуска всех линтеров
lint: black flake8 pycodestyle pylint
