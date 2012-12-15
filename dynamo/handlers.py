
# The follwong code was heavily inspired by and partly copied from 
# https://github.com/willhardy/dynamic-models/blob/master/surveymaker/signals.py

# django imports
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.loading import cache as app_cache
from django.db.models.signals import class_prepared
from django.db import  DatabaseError

# south imports
from south.db import db

# dynamo imports
from dynamo import utils
from dynamo.settings import DYNAMO_DELETE_COLUMNS, DYNAMO_DELETE_TABLES
from dynamo import (pre_model_creation, post_model_creation, pre_model_update,  post_model_update, pre_model_delete, post_model_delete,
                    pre_field_creation, post_field_creation, pre_field_update, post_field_update, pre_field_delete, post_field_delete)



# TODO: this is not working yet, dynamic model admins not available after start
# of runserver
def when_classes_prepared(*args):
    """ Runs the given function as soon as the model dependencies are available.
        You can use this to build dyanmic model classes on startup instead of
        runtime. 

        app_name       the name of the relevant app
        dependencies   a list of model names that need to have already been 
                       prepared before the dynamic classes can be built.
        fn             this will be called as soon as the all required models 
                       have been prepared

        NB: The fn will be called as soon as the last required
            model has been prepared. This can happen in the middle of reading
            your models.py file, before potentially referenced functions have
            been loaded. Becaue this function must be called before any 
            relevant model is defined, the only workaround is currently to 
            move the required functions before the dependencies are declared.

        TODO: Allow dependencies from other apps?
    """
    args=list(args)
    fn=args.pop(-1)
    dependencies = []
    for app in args:
        app_list=app.split('.')
        dependencies.append(app_list[0].lower()+'.'+app_list[1].lower())

    def _class_prepared_handler(sender, **kwargs):
        """ Signal handler for class_prepared. 
            This will be run for every model, looking for the moment when all
            dependent models are prepared for the first time. It will then run
            the given function, only once.
        """

        sender_app=sender._meta.app_label.lower()+'.'+sender._meta.object_name
        already_prepared=set([sender_app])
        for app,models in app_cache.app_models.items():
            for model_name,model in models.items():
                already_prepared.add(app.lower()+'.'+model_name)
                
        if all([x in already_prepared for x in dependencies]):
            db.start_transaction()
            try:
                # We need to disconnect, otherwise each new dynamo model generation
                # will trigger it and cause a "maximim recursion error"
                class_prepared.disconnect(_class_prepared_handler,weak=False)                
                fn()
            except DatabaseError, message:
                # If tables are  missing altogether, not much we can do
                # until syncdb/migrate is run. "The code must go on" in this 
                # case, without running our function completely. At least
                # database operations will be rolled back.
                db.rollback_transaction()
                # Better connect again
                if message<>'no such table: dynamo_metamodel':
                    class_prepared.connect(_class_prepared_handler, weak=False)
                else:
                    raise
            else:
                db.commit_transaction()
    
    # Connect the above handler to the class_prepared signal
    # NB: Although this signal is officially documented, the documentation
    # notes the following:
    #     "Django uses this signal internally; it's not generally used in 
    #      third-party applications."
    class_prepared.connect(_class_prepared_handler, weak=False)


def field_pre_save(sender, **kwargs):
    '''
    A signal handler to run any pre_save activities and trigger the built-in
    pre_save signals
    1. Detect renamed fields and store the old field name for migration
    2. Detect if the field is just created and store this information.
    3. Detect if the field is just updated and store this information
    4. Trigger the pre creation signal
    5. Trigger the pre update signal
    '''
    MetaField=sender
    meta_field=kwargs['instance']
    
    try:
        # Try to detect if a model's field has been given a new name(which would
        # require a column rename)
        if meta_field.pk:
            meta_field._old_name = MetaField.objects.filter(pk=meta_field.pk).exclude(name=meta_field.name).get().name

        # Try to detect if a model's field is now just created, or if it is updated
        # to trigger the right signals and to handover the right information to
        # subsequent post_save handlers
        if not meta_field.pk:
            pre_field_creation.send(sender=meta_field.meta_model.get_model(),new_field=meta_field)
            meta_field._creation=True
        elif meta_field._old_name:
            pre_field_update.send(sender=meta_field.meta_model.get_model(),field=meta_field)
            meta_field._update=meta_field
    # Fixture loading will not have a related survey object, so we can't use it
    # This won't be a problem because we're only looking for renamed slugs
    except ObjectDoesNotExist:
        pass


def field_post_save(sender, **kwargs):
    '''
    A signal handler to run any post_save activities and trigger the built-in
    post_save signals
    1. Detect renamed fields and run migration
    2. Create new fields, if necessary
    2. Trigger post creation signal
    3. Trigger post update signal
    '''
    MetaField=sender
    meta_field=kwargs['instance']

    try:
        # Regenerate our MetaModel, which may have changed
        DynamicModel = meta_field.meta_model.get_model()

        # If we previously identified a renamed field name, then rename the column
        if hasattr(meta_field, '_old_name'):
            utils.rename_db_column(DynamicModel, meta_field._old_name, meta_field.name)
            del meta_field._old_name

        # If necessary, add any new columns
        utils.add_necessary_db_columns(DynamicModel)

        # Check if the field has just been created
        if hasattr(meta_field, '_creation'):
            post_field_creation.send(sender=DynamicModel,new_field=meta_field)
            del meta_field._creation
            
        # Check if the field has just been updated
        if hasattr(meta_field, '_update'):
            post_field_update.send(sender=DynamicModel,old_field=meta_field._update,new_field=meta_field)
            del meta_field._update        

    except ObjectDoesNotExist:
        return


def field_pre_delete(sender, **kwargs):
    '''
    A signal handler to run any pre delete activities and trigger the built-in
    pre delete signals
    1. Trigger the pre delete signal
    '''
    MetaField=sender
    meta_field=kwargs['instance']
    pre_field_delete.send(sender=meta_field.meta_model.get_model(),field=meta_field)
 

def field_post_delete(sender, **kwargs):
    '''
    A signal handler to run any pre_save activities and trigger the built-in
    pre_save signals
    1. Update the database with regard to the deleted field
    2. Trigger the post delete signal
    '''

    MetaField=sender
    meta_field=kwargs['instance']
    try:
        # Regenerate our MetaModel, which may have changed
        DynamicModel = meta_field.meta_model.get_model(regenerate=True, notify_changes=True)
        utils.unregister_in_admin(admin_site, DynamicModel)
        utils.remove_from_model_cache(DynamicModel._meta.app_label, DynamicModel.__name__)

        # Delete field in the database
        if DYNAMO_DELETE_FIELDS:
            # TODO: no delete field function available yet
            pass

        post_field_update.send(sender=Dynamic_model,field=meta_field)
    except:
        pass

def model_pre_save(sender, **kwargs):
    '''
    A signal handler to run any model presave activities and trigger the built-in
    pre save signals
    2. Detect if the model is just created and store this information.
    3. Detect if the model is just updated and store this information
    4. Trigger the pre creation signal
    5. Trigger the pre update signal
    '''
    

    MetaModel=sender
    meta_model=kwargs['instance']
    NewDynamicModel=meta_model.get_model()

    if not meta_model.id:
        pre_model_creation.send(sender=MetaModel,new_model=NewDynamicModel)
        meta_model._creation=True
    else:
        OldDynamicModel=MetaModel.objects.get(pk=meta_model.pk).get_model()
        if OldDynamicModel.hash <> NewDynamicModel:
            meta_model._update=OldDynamicModel
            pre_model_update.send(sender=MetaModel,old_model=OldDynamicModel,new_model=NewDynamicModel)       

def model_post_save(sender,**kwargs):
    '''
    A signal handler to run any model presave activities and trigger the built-in
    pre save signals
    1. Detect if the model has been changed and appy these changes to the db
    2. Trigger the pre creation signal
    3. Trigger the pre update signal
    '''    

    MetaModel=sender
    meta_model=kwargs['instance']
    update=hasattr(meta_model,'_update')
    creation=hasattr(meta_model,'_creation')

    if update or creation:
        DynamicModel = meta_model.get_model()
        # Create a new table if it's missing
        utils.create_db_table(DynamicModel)
        
    if creation:
        post_model_creation.send(sender=MetaModel,new_model=DynamicModel)
        del meta_model._creation

    if update:
        post_model_update.send(sender=MetaModel,old_model=meta_model._update,new_model=DynamicModel)
        del meta_model._update

def model_pre_delete(sender, **kwargs):
    '''
    A signal handler to run any model pre delete activities and trigger the built-in
    pre delete signals
    1. Delete the table in db, if settings require us to do so
    2. Trigger the pre delete signal
    '''
    
    MetaModel=sender
    meta_model=kwargs['instance']
    DynamicModel = meta_model.get_model()

    if DYNAMO_DELETE_TABLES:
        utils.delete_db_table(DynamicModel)


    # trigger pre field delete signal
    pre_field_delete.send(sender=MetaModel,old_model=DynamicModel)
    meta_model._delete=DynamicModel

def model_post_delete(sender, **kwargs):
    '''
    A signal handler to run any model post delete activities and trigger the built-in
    pre delete signals
    1. Trigger the post delete signal
    '''    
    MetaModel=sender
    meta_model=kwargs['instance']
    
    post_field_delete.send(sender=MetaModel,old_model=meta_model._delete)

