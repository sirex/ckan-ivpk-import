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

First of all you need to export data from opendata.gov.lt website, for this you
can use following script:

https://github.com/sirex/databot-bots/blob/master/bots/ivpk/opendata-gov-lt.py

You can find already exported data here (``datasets.jsonl`` file):

http://atviriduomenys.lt/data/ivpk/opendata-gov-lt/

You can download already exported opendata.gov.lt data using this command::

  wget http://atviriduomenys.lt/data/ivpk/opendata-gov-lt/datasets.jsonl -O data/ivpk.jsonl

For all commands below to to work, make sure, that you installed
``ckan-ivpk-import`` as described in `How to install`_ section.

Then you need to export target CKAN data, in order to keep existing data
updated if some datasets are already described in both places. To export data,
you can use this command::

  ckanapi dump datasets --all -O data/opendata.jsonl -r http://opendata.lt/

Once you have exported data from both, opendata.gov.lt and your CKAN website,
for example opendata.lt, then you can create new CKAN dump, by combining data
from both sources::

  ivpkimport data/opendata.jsonl data/ivpk.jsonl data/both.jsonl


Finally you can update CKAN website with new data. In order to update CKAN you
have to run ``ckanapi load datasets`` command from server where CKAN is
deployed::

  ckanapi load datasets --input=data/both.jsonl -c production.ini


.. _Python package management: What you need to know before starting
