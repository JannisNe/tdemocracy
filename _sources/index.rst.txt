``tdemocracy``
==============

Listen to nuclear alerts from the Vera Rubin Observatory for the TDEmocracy project.

Prerequisites
-------------

You need an account at the `SCIMMA Hopskotch service`_. Please contact the TDEmocracy lead to have your account added to the Ampel-TDEmocracy group. You can store your username and password in your environment variables ``TDEMOCRACY_USERNAME`` and ``TDEMOCRACY_PASSWORD`` or in a ``.env`` file in the root of the repository.

.. _SCIMMA Hopskotch service: https://scimma.org/hopskotch

Installation
------------

Clone the repository::


   git clone https://github.com/JannisNe/tdemocracy.git

Create a new python environment with your favourite environment manager (``python >=3.11``). You can then install the package and all dependencies using `poetry`_::

   cd tdemocracy
   poetry install

.. _poetry: https://python-poetry.org/


In the future, you will be able to install the package via ``pip``::

   pip install tdemocracy


Getting started
---------------


.. toctree::
   listen
   selection
   model
   settings
   :maxdepth: 1
