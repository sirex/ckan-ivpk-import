BUILDOUT = bin/buildout -N


.PHONY: all
all: \
    bin/buildout \
    bin/ivpkimport

bin/buildout:
	python bootstrap.py --version=1.7.0 --distribute

bin/ivpkimport: buildout.cfg setup.py versions.cfg
	bin/buildout -N
	touch bin/ivpkimport -c


.PHONY: tags
tags: all
	bin/ctags -v
