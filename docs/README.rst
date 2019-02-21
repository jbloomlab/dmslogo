===========================
Documentation
===========================

This subdirectory contains the `reStructuredText`_ documentation that can be built with `sphinx`_.

Building the documentation
-----------------------------

To build the documentation, you need to install:

    * `sphinx`_ 
    
    * `nb2plots`_

Then simply type::

    make html

and the HTML documentation will be built in ``./_build/html/``.

Notes on configuration
------------------------

Note that the configuration automatically created by ``sphinx-quickstart`` has been modified in the following ways:

    * ``conf.py`` has been modified to:
    
        - read the version and package information from ``../dmslogo/__init__.py``

        - specify `numfig = True` to enable figure numbering

    * ``Makefile`` has been modified to automatically run `sphinx-apidoc`_.

Notes on nb2plots
-------------------
`nb2plots`_ was used to generate `examples.rst <examples.rst>`_ from a Jupyter notebook.

.. _`reStructuredText`: http://docutils.sourceforge.net/docs/user/rst/quickref.html
.. _`sphinx`: http://sphinx-doc.org/
.. _`sphinx-apidoc`: http://www.sphinx-doc.org/en/stable/man/sphinx-apidoc.html
.. _`nb2plots`: https://matthew-brett.github.io/nb2plots/
