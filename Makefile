.PHONY: test release flake8 coverage clean coveralls
project_name=domains

test:
	python setup.py develop
	python setup.py test
	python setup.py develop --uninstall


release:
	python setup.py sdist --format=zip,bztar,gztar register upload
	python setup.py bdist_wheel register upload

flake8:
	flake8 --max-complexity 12 ${project_name} setup.py tests.py


coverage:
	coverage run --rcfile=coverage.rc --include=${project_name}/* setup.py test
	coverage html

clean:
	python setup.py develop --uninstall
	rm -rf *.egg-info *.egg
	rm -rf htmlcov
	rm -f .coverage
	rm -rf build dist
	find . -name "*.pyc" -exec rm -rf {} \;

coveralls:
	coveralls --rcfile=coverage.rc
