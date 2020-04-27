SOURCE_PATH = .
CODESTYLE = pycodestyle
PYLINT = pylint
PYTEST = pytest
PYGOUNT = pygount
PYTHON = python
PIPENV = PIPENV_VERBOSITY=-1 pipenv
MANAGE = ./manage.py
ENV = $(shell pipenv --venv)
UWSGI = uwsgi
# APPS
APP_MAIN = yatube
APP_1 = posts
APP_2 = users

codequality: codestyle pylint tests

codestyle:
			$(CODESTYLE) --exclude=migrations --ignore=errors .

pylint:
			$(PYLINT) -j 0 $(APP_MAIN) $(APP_1) $(APP_2) --load-plugins pylint_django --output-format=parseable

tests:
			$(PYTEST)

requirements:
			$(PIPENV) lock -r > requirements.txt
			$(PIPENV) lock -r --dev > requirements_dev.txt

uwsgi:
			$(UWSGI) -H $(ENV) --ini uwsgi_dev.ini --die-on-term