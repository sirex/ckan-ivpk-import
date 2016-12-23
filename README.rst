A too for importing IVPK opendata.gov.lt data into CKAN
=======================================================

Links
-----

- http://opendata.gov.lt/

- http://atviriduomenys.lt/data/ivpk/

- https://github.com/sirex/databot-bots/blob/master/bots/ivpk/opendata-gov-lt.py


What you need to know before starting
-------------------------------------

You should have basic understanding about `Python package management`_.


How to install
--------------

::

  pip3 install -r requirements.txt -e .


How to set up development environment
-------------------------------------

::

  pip3 install -r requirements.txt -r requirements-dev.txt -e .


Running automated tests
-----------------------

::

  py.test --cov-report=term-missing --cov=ivpkimport.py tests.py


How to use this tool
--------------------

Command bellow::

  ivpkimport data/ http://opendata.lt/

Will produce ``data/orgs-new.jsonl`` and ``data/datasets-new.jsonl`` files. You
can use these file to import data to CKAN::

  ckanapi load organizations --input=data/orgs-new.jsonl -c production.ini
  ckanapi load datasets --input=data/datasets-new.jsonl -c production.ini

``ivpkimport`` script will only generate missing or updated entries.

How to test data import locally
-------------------------------

In order to test data import locally you can use ``ckan.yml`` Ansible_ script.
Whole CKAN stack will be installed into your machine with this single command
(only tested on Ubuntu 16.04)::

  ansible-playbook --ask-become-pass -c local -i ckan, -e path=$PWD ckan.yml

When CKAN is installed, you can run it like this::

  venv/bin/paster serve development.ini

Then to test the import, run following command::

  venv/bin/pip install ckanapi
  venv/bin/ckanapi load datasets --input=data/both.jsonl -c development.ini


Canonical list of organizations
-------------------------------

Canonical list of organization names was borrowed from e-tar.lt_, using this
JavaScript snippet from JavaScript console:

.. code-block:: javascript

    for (let x of $x('//div[@id="contentForm:searchParamPane:j_id_2j:tree"]//span[contains(@class, "ui-treenode-label")]/span/text()')) {
        console.log(x.data);
    }


.. _Ansible: http://docs.ansible.com/ansible/intro_installation.html
.. _Python package management: What you need to know before starting
.. _e-tar.lt: https://www.e-tar.lt/portal/lt/legalActSearch
