Installation and Setup
======================



************
Dependencies
************
   * `south <http://south.aeracode.org/>`_

Developers might also need `Sphinx <http://sphinx.pocoo.org>`_ to maintain and update the docs.

************
Installation
************
Install into your python path using pip or easy_install::

   pip install django-dynamo

If you are feeling adventurous you can get the lates code from `Bitbucket <https://bitbucket.org/schacki/django-dynamo>`_


************
Configuration
************
Now, you just need to add 'dynamo' to your installed apps::

	INSTALLED_APPS=(
      	 # other apps
		"dynamo",
	)

And you are all set and ready to go!

**************
Sample Project
**************
Dynamo also comes with a built-in working sample project, that you can easily use to play around.
To setup this project, download the source from `Bitbucket <https://bitbucket.org/schacki/django-dynamo>`_ into your target directory and run::

	bootstrap.py

This will create a virtualenv, install all dependencies, and create a customized manage script in your root (**Attention**: this manage script is just a helper that calls the "normal" manage.py command).
So to start the project, just do::

	manage syncdb

to create and sync the database.
And then run::

	manage runserver

to start the server. Now you can open the browser, log into the admin and create your MetaModels and MetaFields.
