TARGET=tspapi
VERSION=0.3.1
PACKAGE=tspapi
TAR_FILE=dist/$(PACKAGE)-$(VERSION).tar.gz

install: build
	pip install $(TAR_FILE)

build: doc
	python setup.py sdist

doc:
	pandoc -f markdown -t plain README.md > README.txt

rebuild: clean install

upload:
	python setup.py sdist upload
	
clean:
	/bin/rm -rf build dist site MANIFEST
	pip freeze | grep "$(PACKAGE)==$(VERSION)" && pip uninstall -y $(TARGET)
