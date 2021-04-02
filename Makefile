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
	py.test --cov=admin_anchors tests

.PHONY: tox
tox:
	tox

.PHONY: release
release:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
