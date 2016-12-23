.PHONY: test
test:
	py.test --cov-report=term-missing --cov=ivpkimport.py tests.py

.PHONY: ckan
ckan:
	ansible-playbook --ask-become-pass -c local -i ckan, -e path=$(PWD) ckan.yml

.PHONY: reset
reset:
	sudo -u postgres dropdb ckan_default
	ansible-playbook --ask-become-pass -c local -i ckan, -e path=$(PWD) -t create_ckan_db ckan.yml
