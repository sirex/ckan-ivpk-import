IVPK duomenų bazės importavimo įrankis
======================================

Nuorodos
--------

- http://opendata.gov.lt/

- http://atviriduomenys.lt/data/ivpk/


Diegimas
--------

::

  pip3 install -r requirements.txt -e .


Programavimo aplinka
--------------------

::

  pip3 install -r requirements.txt -r requirements-dev.txt -e .


Automatiniai testai
-------------------

::

  py.test --cov-report=term-missing --cov=ivpkimport.py tests.py
