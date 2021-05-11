install:
	poetry install

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

run:
	poetry run python manage.py runserver 0.0.0.0:8000

lint:
	poetry run flake8 .

makemessages:
	django-admin makemessages -l ru

compilemessages:
	django-admin compilemessages

test:
	poetry run python manage.py test

test-coverage:
	poetry run coverage run --source='.' manage.py test task_manager
	coverage html
	coverage report
