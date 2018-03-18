.. _contributing-guide:

Contributing
==================

There are plenty of ways to contribute to this project. If you think you've found
a bug please submit an issue. If there is a feature you'd like to see then please
open an ticket proposal for it. If you've come up with some helpful examples then
you can add to our example project.


Getting the Source
--------------------------------------

The source code is hosted on `Github <https://github.com/mlavin/django-selectable>`_.
You can download the full source by cloning the git repo::

    git clone git://github.com/mlavin/django-selectable.git

Feel free to fork the project and make your own changes. If you think that it would
be helpful for other then please submit a pull request to have it merged in.


Submit an Issue
--------------------------------------

The issues are also managed on `Github issue page <https://github.com/mlavin/django-selectable/issues>`_.
If you think you've found a bug it's helpful if you indicate the version of django-selectable
you are using the ticket version flag. If you think your bug is javascript related it is
also helpful to know the version of jQuery, jQuery UI, and the browser you are using.

Issues are also used to track new features. If you have a feature you would like to see
you can submit a proposal ticket. You can also see features which are planned here.


Submit a Translation
--------------------------------------

We are working towards translating django-selectable into different languages. There
are not many strings to be translated so it is a reasonably easy task and a great way
to be involved with the project. The translations are managed through
`Transifex <https://www.transifex.com/projects/p/django-selectable/>`_.

Running the Test Suite
--------------------------------------

There are a number of tests in place to test the server side code for this
project. To run the tests you need Django and `mock <http://www.voidspace.org.uk/python/mock/>`_
installed and run::

    python runtests.py

`tox <http://tox.readthedocs.org/en/latest/index.html>`_ is used to test django-selectable
against multiple versions of Django/Python. With tox installed you can run::

    tox

to run all the version combinations. You can also run tox against a subset of supported
environments::

    tox -e py27-django15

For more information on running/installing tox please see the
tox documentation: http://tox.readthedocs.org/en/latest/index.html

Client side tests are written using `QUnit <http://docs.jquery.com/QUnit>`_. They
can be found in ``selectable/tests/qunit/index.html``. The test suite also uses
`PhantomJS <http://phantomjs.org/>`_ to
run the tests. You can install PhantomJS from NPM::

    # Install requirements
    npm install -g phantomjs jshint
    make test-js


Building the Documentation
--------------------------------------

The documentation is built using `Sphinx <http://sphinx.pocoo.org/>`_
and available on `Read the Docs <http://django-selectable.readthedocs.io/>`_. With
Sphinx installed you can build the documentation by running::

    make html

inside the docs directory. Documentation fixes and improvements are always welcome.

