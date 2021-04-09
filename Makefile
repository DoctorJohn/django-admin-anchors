.PHONY: setup
setup:
	pip install -e ".[dev]"

.PHONY: hook
hook:
	pre-commit install

.PHONY: format
format:
	black admin_anchors tests setup.py

.PHONY: lint
lint:
	flake8 admin_anchors tests setup.py

.PHONY: test
test:
	py.test --cov-report term-missing --cov=admin_anchors tests

.PHONY: tox-format
tox-format:
	TOXENV=black tox

.PHONY: tox-lint
tox-lint:
	TOXENV=flake8 tox

.PHONY: tox-test
tox-test:
	tox

.PHONY: release
release:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
