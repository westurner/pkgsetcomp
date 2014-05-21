.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"

clean: clean-build clean-pyc
	rm -fr htmlcov/

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	find . -name '__pycache__' -print0 | xargs -0 rm -rfv ;

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 pkgsetcomp tests

test:
	python setup.py test

test-all:
	tox

coverage:
	coverage run --source pkgsetcomp setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/pkgsetcomp.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ pkgsetcomp
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	#open docs/_build/html/index.html

release: clean
	#	 ver=v0.1.1
	## update HISTORY.txt
	#    release date
	#    release version
	#    summary
	## update version in setup.py
	#    sed "s/version='\(.*\)'/version='${ver}'/g"
	## update version in pkgsetcomp/__init__.py
	#    sed "s/__version__ = '\(.*\)'/__version__ = '${ver}'/g" 
	## add updated version to repository
	#    hg commit -m setup.py pkgsetcomp/__init__.py
	#    git commit -m setup.py pkgsetcomp/__init__.py
	## tag the release in the repository
	##   hg tag "v${ver}"
	#    git tag "v${ver}"
	## push the changes
	#    hg push
	#    git push
	## update http://github.com/westurner/pkgsetcomp/releases
	## with a new tagged release
	#	 browse to url, select version tag, click 'Edit release'
	#	 set the release name to "pkgsetcomp v${ver}"
	## register with pypi
	#    python setup.py build register
	## generate a source distribution and upload to pypi
	python setup.py sdist upload
	#python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

docs_rsync_to_local:
	rsync -avr ./docs/_build/html/ $(_DOCSHTML)/pkgsetcomp

docs_rebuild:
	$(MAKE) docs
	$(MAKE) docs_rsync_to_local
