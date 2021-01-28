.PHONY: build docs test

BUILDDIR := $(PWD)
CHECKDIRS := examples notebooks scripts src tests utils setup.py
DOCDIR := docs
TARGET := ""  # directory/file/function to target with pytest

# run checks on all files for the repo
quality:
	@echo "Running python quality checks";
	black --check $(CHECKDIRS);
	isort --check-only $(CHECKDIRS);
	flake8 $(CHECKDIRS);

# style the code according to accepted standards for the repo
style:
	@echo "Running python styling";
	black $(CHECKDIRS);
	isort $(CHECKDIRS);

# run tests for the repo
test:
	@echo "Running python tests";
	@pytest $(TARGET);

# create docs
docs:
	sphinx-apidoc -o "$(DOCDIR)/source/" src/sparseml;
	cd $(DOCDIR) && $(MAKE) html;

# creates wheel file
build:
	python3 setup.py sdist bdist_wheel

# clean package
clean:
	rm -fr .pytest_cache;
	rm -fr docs/_build docs/build;
	find $(CHECKDIRS) | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -fr;
	find $(DOCDIR) | grep .rst | xargs rm -fr;