PYTHON = python
CHECKSCRIPT = plyer/tools/pep8checker/pep8kivy.py
PLYER_DIR = plyer/

build:
	$(PYTHON) setup.py build

force:
	$(PYTHON) setup.py build -f

debug:
	$(PYTHON) setup.py build -f -g

pdf:
	$(MAKE) -C docs latex && make -C docs/build/latex all-pdf

html:
	env USE_EMBEDSIGNATURE=1 $(MAKE) force
	$(MAKE) -C docs html

style:
	$(PYTHON) $(CHECKSCRIPT) .

stylereport:
	$(PYTHON) $(CHECKSCRIPT) -html $(PLYER_DIR)

hook:
	# Install pre-commit git hook to check your changes for styleguide
	# consistency.
	cp plyer/tools/pep8checker/pre-commit.githook .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

install:
	python setup.py install

clean:
	-rm -rf docs/build
	-rm -rf build
	-find plyer -iname '*.so' -exec rm {} \;
	-find plyer -iname '*.pyc' -exec rm {} \;
	-find plyer -iname '*.pyo' -exec rm {} \;

distclean: clean
	-git clean -dxf -e debian
