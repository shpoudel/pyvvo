Building the PyVVO Documentation
================================

This section discusses what is required to build PyVVO's documentation.
TL;DR (though please read): ``python build_docs.py --checkout``

.. _venv:

Prerequisites
-------------

This may not be comprehensive, but I'll try.

-   Python >= 3.5 (Brandon only tested with 3.7)
-   LaTex (Brandon installed via MikTex)
-   LaTex packages (see ``latex/packages.tex``, MikTex automagically
    installs packages)
-   dvisvgm (Brandon didn't have to install this, so maybe it comes with
    MikTex?)

Virtual Environment
-------------------

To keep things simple, Brandon builds the documentation via a Python
interpreter within a local virtual environment, rather than using
a Docker-based interpreter. The `Python docs
<https://docs.python.org/3/tutorial/venv.html>`__ provide a nice
tutorial for building and using virtual environments. TL;DR:

.. code:: bash

    cd ~/git/pyvvo
    python3 -m venv venv
    source venv/bin/activate

After activating the virtual environment, install ``sphinx`` and
``numpy``. The original goal was to *only* require installing ``sphinx``
in the virtual environment, but ``zip.py`` has quite a few constants
that depend on ``numpy``, so `mocking
<https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autodoc_mock_imports>`__
the ``numpy`` import simply isn't practical. Install like so:

.. code:: bash

    python -m pip install sphinx numpy

Initial Setup
-------------

The files ``conf.py``, ``index.rst``, ``make.bat``, and ``Makefile``
were originally created using the `sphinx-quickstart
<https://www.sphinx-doc.org/en/master/usage/quickstart.html>`__ tool.
All these files have since been modified.

Building the Documentation
--------------------------

Building the documentation is wicked simple. After activating your
virtual environment (see :ref:`venv`), and assuming your shell's
current working directory is ``pyvvo/docs``, simply:

.. code:: bash

    python build_docs.py --checkout

**NOTE**: Be careful when using the ``--checkout`` flag. You should
ensure that your Git workspace in ``docs/rst_latex`` is **clean** before
running ``build_docs.py`` with the --checkout command. Really, you
should ensure you have a clean workspace before running
``build_docs.py`` at all, because it does some find+replace in the
``rst_latex`` directory.

For details on the available flags/arguments, run:

.. code:: bash

    python build_docs.py --help

Note that all tools (``latex``, ``dvisvgm``, ``sphinx-build``) have
their outputs "quieted." Thus, if you get any output besides the
obvious output from the Python script itself, that's cause for concern.
For reference, with no warnings, clean output from ``build_docs.py``
should look like:

    INFO:root:Running tex2svg for flow_conventions...
    INFO:root:Done.
    INFO:root:Running tex2svg for main_loop...
    INFO:root:Done.
    INFO:root:Building the documentation...
    INFO:root:Done.
    INFO:root:Checking out files in rst_latex...
    INFO:root:Done.

``build_docs.py`` will emit a warning like so if any of the ``\ref{}``
references in the ``rst_latex`` files don't match up with the ``.tex``
files:

    WARNING:root:Some reference(s) did not get updated in main_loop.rst, and are thus not defined in main_loop.tex: ['\\ref{flow:update-glm-manager}']

For an unknown reason, Brandon had troubles where the docs would not
always get completely updated after building. There's a simple fix:
delete the `doctrees` and `html` directories and build again.

Viewing the Built Documentation
-------------------------------

Simply open ``~/git/pyvvo/docs/html/index.html`` in your web browser.
