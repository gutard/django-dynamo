Settings
========

The following settings are available to customize the Dynamo behavior.

* **DYNAMO_DELETE_COLUMNS**: Flag to define, whether database columns (including content) are deleted after the field has been deleted in the MetaField definition; default: True.

* **DYNAMO_DELETE_TABLES**: Flag to define, whether database tables (including content) are deleted after the model has been deleted in the MetaModel definition; default: True.

* **DYNAMO_DEFAULT_APP**: Default app to be used when model is generated; default: dynamo.

* **DYNAMO_DEFAULT_MODULE**: Default module to be used when model is generated; default: dynamo.models.

* **DYNAMO_FIELD_TYPES**: list of availabe Dynamo field types; default: all Django Field Types (as of Django 1.3). If you want to make any customized fields available, you would need to add them here!

* **STANDARD_FIELD_TYPES**: list of Dynamo standard field types; default: all Django Field Types (as of Django 1.3) except for relationship ones.

* **INTEGER_FIELD_TYPES**: list of integer field types, that control how the choices tuple is generated; default: all Django integer field types.

* **STRING_FIELD_TYPES**:  list of string field types, that define how the "require" field controls the blank and null option; default:all Django string field types.

* **RELATION_FIELD_TYPES**: list of field types that require an entry in related_model; default: all Django relation field types.
