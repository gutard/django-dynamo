Django-Dynamo
=============
Dynamo let users and admins create and mantain their Django **DYNA** mic **MO** dels dynamically at runtime.
For details on setup and usage, please read the `documentation <http://django-dynamo.readthedocs.org/en/latest/>`_ on Readthedocs.

***********************************
Why would you need a dynamic model?
***********************************
Dynamic models are beneficial for applications that need data structures, which are only known at runtime, but not when the application is coded. Or when existing models need to be extended at runtime by additional fields. Typical use cases are:

#. *CMS:* In content management systems, users often need to maintain content that is unique for their specific website. The required data structures to store and maintain this content is therefore not known to the developers beforehand. 
#. *Web Shop:* The owner of a web shop has highly customized products, with very special product attributes. The shop developers want the web shop owner to define these attributes herself.
#. *Survey:* If you have an application to create and maintain online surveys, you do neither know the questions nor the possible answers at runtime, but let your users define these, as they implement their surveys.

Dynamo supports the three of these use cases - and many more!

*********************
How does Dynamo work?
*********************
Dynamo lets you define the meta data for your models their fields. This metadata definition is stored in "real" Django models. The defined model is then created at runtime. And of course, you can also modify the models later on, e.g. adding, renaming or deleting fields; or changing model attributes. It will also automatically manage your admin and app cache for the dynamic models. The meta data maintenance can be done via the Django Admin or via the provided API.

*********************
What else is there?
*********************
There are various approaches and implemenations available for Django developers:

* The most straight forward approach is to use the Django internals and its DB API to create and maintain models at runtime. Numerous authors have elaborated this option in the `Django Wiki <http://code.djangoproject.com/wiki/DynamicModels>`_ . Michael Hall has created an `app <https://bitbucket.org/mhall119/dynamo>`_ following this approach; he has also called in dynamo, I hope this does not cause too much confusion.
* `Entity-Attribute-Value <http://en.wikipedia.org/wiki/Entity-attribute-value_model>`_ / **EAV** Model is the traditioal computer science approach to tackle this kind of problem, and there are also django implementations for that available like `django-eav <https://github.com/mvpdev/django-eav>`_ or `eav-django <https://bitbucket.org/neithere/eav-django/>`_.
* Finally, Will Hardy has introduced a `South <http://south.aeracode.org/>`_ -based concept, that he has presented and discussed at the `DjangoCon Europe 2011 <http://2011.djangocon.eu/talks/22/>`_ . Following this concept, he has implemented `dynamic-models <https://github.com/willhardy/dynamic-models>`_ 

The South based approach seems to be the cleanest and clearly follows the DRY approach: all database handling, maintenance and transactions are left to the excellent South API.

*********************************
Who else gets credits for Dynamo?
*********************************
Dynamo is inspired by the excellent work of Will Hardy's `dynamic-models <https://github.com/willhardy/dynamic-models>`_ and this `Django Wiki Article <http://code.djangoproject.com/wiki/DynamicModels>`_. It also re-uses parts of their concepts and coding.
Furthermore, South is used to maintain the Dyanmo related database objects.

****************************************
Under which license is Dynamo available?
****************************************
Dynamo is available under the `BSD license <http://www.opensource.org/licenses/BSD-3-Clause>`_.

********************
How do I get suport?
********************
The online `documentation <http://django-dynamo.readthedocs.org/en/latest/>`_  on ReadtheDocs is a great place to start. If you have any further questions, issues or would like to contribute, please let us know at the `Dynamo Google Group <http://groups.google.com/group/django-dynamo>`_