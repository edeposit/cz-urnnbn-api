CZ URN\:NBN API
===============

Python API for czech `URN:NBN resolver <https://resolver.nkp.cz/>`_ (`documentation <https://code.google.com/p/urnnbn-resolver-v2/>`_).

What is URN\:NBN
----------------
URN\:NBN is system for registration and assigning of special codes for electronic publications (it may look like this: ``urn:nbn:cz:edep-00000s``). The codes can be then used to resolve (translate) the code to metadata information about publication and/or to get pointer to actual digital instance of the publication (=file).

The system works like `magnet`_ used by the popular torrent programs and websites. Once you have the URN, you can query independent resolvers (torrent trackers), which then points you to libraries (users), who store copy of the document (file).

.. _magnet: https://en.wikipedia.org/wiki/Magnet_URI_scheme

cz-urnnbn-api
-------------

``cz-urnnbn-api`` is Python package used to work with czech URN\:NBN resolver. It allows you to register documents, add new digital instances and resolve strings back to URL of systems, where the document is stored.

Warning:
    The package is not 100% complete, because complex nature of the API and because it was created for E-deposit_ project, which doesn't require 100% functionality. Package is opensource, and pull requests are welcomed.

.. _E-deposit: http://edeposit.nkp.cz/

Package structure
-----------------

The package itself is split into multiple files.

File relations
++++++++++++++

Import relations of files:

.. image:: /_static/relations.png
    :width: 400px

Class relations
+++++++++++++++

Relations of the classes:

.. image:: /_static/class_relations.png
    :width: 400px

API
---

:doc:`/api/urn_nbn_api`:

.. toctree::
    :maxdepth: 1

    /api/api.rst
    /api/xml_composer.rst
    /api/xml_convertor.rst
    /api/settings.rst


:doc:`/api/api_structures/api_structures`:

.. toctree::
    :maxdepth: 1

    /api/api_structures/catalog.rst
    /api/api_structures/digital_instance.rst
    /api/api_structures/digital_library.rst
    /api/api_structures/modes.rst
    /api/api_structures/registrar.rst
    /api/api_structures/urn_nbn.rst

.. toctree::
    :maxdepth: 1

    /api/api_structures/tools.rst

Usage example
-------------

.. toctree::
    :maxdepth: 2

    /example/example

Installation
------------
Module is hosted at `PYPI <https://pypi.python.org/pypi/cz-urnnbn-api>`_,
and can be easily installed using `PIP`_::

    sudo pip install cz-urnnbn-api

.. _PIP: http://en.wikipedia.org/wiki/Pip_%28package_manager%29


Source code
+++++++++++
Project is released under MIT license. Source code can be found at GitHub:

- https://github.com/edeposit/cz-urnnbn-api

Unittests
+++++++++
Almost every feature of the project is tested by unittests. You can run those
tests using provided ``run_tests.sh`` script, which can be found in the root
of the project.

The ``run_tests.sh`` script can be used to run unittests (``-u`` switch), which doesn't activelly work with online API, and integration tests (``-i`` switch), which works only with online API. Both tests can be run using ``-a`` switch.

If you have any trouble, just add ``--pdb`` switch at the end of your ``run_tests.sh`` command like this: ``./run_tests.sh -a --pdb``. This will drop you to `PDB`_ shell.

.. _PDB: https://docs.python.org/2/library/pdb.html

Requirements
^^^^^^^^^^^^
This script expects that packages pytest_ and fake-factory_ is installed. In case you don't have it yet, it can be easily installed using following command::

    pip install --user pytest fake-factory

or for all users::

    sudo pip install pytest fake-factory

.. _pytest: http://pytest.org/
.. _fake-factory: https://github.com/joke2k/faker

Example
^^^^^^^
::

    $ ./run_tests.sh -a
    ============================= test session starts ==============================
    platform linux2 -- Python 2.7.6 -- py-1.4.26 -- pytest-2.6.4
    plugins: cov
    collected 29 items 

    tests/integration/test_api.py ....
    tests/unit/test_rest.py ....
    tests/unit/test_xml_composer.py .........
    tests/unit/test_xml_convertor.py ..
    tests/unit/api_structures/test_digital_instance.py .....
    tests/unit/api_structures/test_modes.py ...
    tests/unit/api_structures/test_tools.py ..

    ========================== 29 passed in 0.75 seconds ===========================


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
