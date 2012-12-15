The Basics
==========
To create a dynamic model at runtime, the meta information needs to be defined. This meta information is stored in two models: MetaModel and MetaField. Both of these models are available in the Dynamo Admin section. As soon as any instance of these is saved, numerous background activities are triggered to ensure that a Django model and its underlying database table(s) exists.

****************
Creating a Model
****************

The following fields are available in the MetaModel model:

* *name*: the name of your dynamic model; this field is required.
* *description*: an optional description of your dynamic model (this is only for information, but not used for model creation)
* *app*: the application /application label that is used for the creation of the model; default: as specified in settings.
* *admin*: a flag to indicate whether the admin page should be created and maintained as well for the specified model; default as specified in settings.

****************
Creating a Field
****************
For each model, you can define as many fields as you like to in the MetaFields model. The following fields are available in the MetaField model, all of which are described in more detail in the `Django Docs <https://docs.djangoproject.com/en/1.3/ref/models/fields/#field-options>`_

* name
* verbose_name
* meta_model
* type
* related_model
* description 
* order
* unique_together
* unique
* help
* choices
* default
* required

Please be aware of the following.

* *type*: type describes the field type as defined in the 'Django Docs <https://docs.djangoproject.com/en/1.3/ref/models/fields/#field-types>`_
* *related_model*: this field can and should only be populated, when type is a `relationship field <https://docs.djangoproject.com/en/1.3/ref/models/fields/#module-django.db.models.fields.related>`_
* *unique_together*: is a flag that represents the `Meta Unique_Together Option <https://docs.djangoproject.com/en/1.3/ref/models/options/#unique-together>`_
* *required*: is a flag that indicates, whether this field can be left empty; reflects the blank and null option of the Django fields.


********************
Background Processes
********************
With each "Save" or "Delete" of a MetaModel instance or MetaField instance, the following chain of activities is performed with regard to the underlying dynamic model:

#. Check if relevant attributes have changed that would change the Dynamic Model (via a hash value). If no change is detected, the process stops here.
#. (Re-)generate Dynamic Model based on the new information.
#. Update the database based to the latest changes of the Dynamic Model (e.g. add another table column).
#. Update Model Cache with the regenerated Dynamic Model.
#. Update Admin page ofr the regenerated Dynamic Model.
#. Trigger `Dynamo Signals <abc>`_ .
