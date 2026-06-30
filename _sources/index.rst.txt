``tdemocracy``
==============

Listen to nuclear alerts from the Vera Rubin Observatory for the TDEmocracy project.

Prerequisites
-------------

You need an account at the `SCIMMA Hopskotch service`_. Please contact the TDEmocracy lead to have your account added to the Ampel-TDEmocracy group. You can store your username and password in your environment variables ``TDEMOCRACY_USERNAME`` and ``TDEMOCRACY_PASSWORD`` or in a ``.env`` file in the root of the repository.

.. _SCIMMA Hopskotch service: https://scimma.org/hopskotch

Installation
------------

Pull the repository and install the dependencies with `poetry`_::



   git clone https://github.com/JannisNe/tdemocracy.git
   cd tdemocracy
   poetry install

.. _poetry: https://python-poetry.org/

In the future, you will be able to install the package via ``pip``::

   pip install tdemocracy


Usage
-----


********
CONTENTS
********

.. toctree::
   selection
   listen
   model
   settings
   :maxdepth: 1
