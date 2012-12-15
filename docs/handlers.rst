Signal Handlers
===============
Dynamo has attached numerous handlers to the Django model signals. If you are sure that you know what you are doing, you can disconnect these and connect your own.

#. **when_classes_prepared**: Runs the given function as soon as the model dependencies are available. This is used to build dyanmic models classes on startup, that are already existent in the database. 

#. **field_pre_save**: A signal handler to run any MetaField pre save activities and trigger the built-in pre_save signals
    1. Detect renamed fields and store the old field name for migration
    2. Detect if the field is just created and store this information.
    3. Detect if the field is just updated and store this information
    4. Trigger the pre creation signal
    5. Trigger the pre update signal


#. **field_post_save**: A signal handler to run any MetaField post save activities and trigger the built-in post_save signals:
    1. Detect renamed fields and run migration
    2. Create new fields, if necessary
    3. Trigger post creation signal
    4. Trigger post update signal

#. **field_pre_delete**: A signal handler to run any MetaField pre delete activities and trigger the built-in pre delete signals:
    1. Trigger the pre delete signal
 

#. **field_post_delete**: A signal handler to run any MetaField pre save activities and trigger the built-in pre_save signals:
    1. Update the database with regard to the deleted field
    2. Trigger the post delete signal


#. **model_pre_save**: A signal handler to run any MetaModel pre save activities and trigger the built-in pre save signals:
    1. Detect if the model is just created and store this information.
    2. Detect if the model is just updated and store this information
    3. Trigger the pre creation signal
    4. Trigger the pre update signal


#. **model_post_save**: A signal handler to run any MetaModel pre save activities and trigger the built-in pre save signals:
    1. Detect if the model has been changed and appy these changes to the db
    2. Trigger the pre creation signal
    3. Trigger the pre update signal


#. **model_pre_delete**: A signal handler to run any MetaModel pre delete activities and trigger the built-in pre delete signals
    1. Delete the table in db, if settings require us to do so
    2. Trigger the pre delete signal


#. **model_post_delete**: A signal handler to run any MetaModel post delete activities and trigger the built-in pre delete signals
    1. Trigger the post delete signal

