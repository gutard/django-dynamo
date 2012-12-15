Signals
=======

Dynamo provides numerous Django signals to let developers hook into the process.

* **pre_model_creation**: triggers before a model is created; providing_args=['new_model']

* **post_model_creation**: triggers after a model is created: providing_args=['new_model']

* **pre_model_update**: triggers before a model is updated; providing_args= ['old_model','new_model']

* **post_model_update**: triggers after a model has been updated; providing_args=['old_model','new_model']

* **pre_model_delete**: triggers before a model is deleted; providing_args=['old_model']

* **post_model_delete**: triggers after a model has been deleted; providing_args=['old_model']

* **pre_field_creation** triggers before a field is created; providing_args=['new_field']

* **post_field_creation**: triggers after a field has been created; providing_args=['new_field']

* **pre_field_update**: triggers before a field is updated; providing_args=['old_field','new_field']

* **post_field_update**: triggers after a field has been updated; providing_args=['old_field','new_field']

* **pre_field_delete**: triggers before a field is deleted; providing_args=['old_field']

* **post_field_delete**: triggers after a field has been deleted; providing_args=['old_field']

