
# The follwong code was heavily inspired by and partly copied from 
# https://github.com/willhardy/dynamic-models/blob/master/surveymaker/models.py
# and http://code.djangoproject.com/wiki/DynamicModels 

# Django imports
from django.core.validators import ValidationError
from django.db import models, transaction, IntegrityError
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.db.models.loading import cache as app_cache
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
from django.utils.hashcompat import md5_constructor

# Dynamo imports
from dynamo.settings import DYNAMO_DEFAULT_MODULE, DYNAMO_DEFAULT_APP, \
     DYNAMO_STANDARD_FIELD_TYPES, DYNAMO_RELATION_FIELD_TYPES,DYNAMO_STRING_FIELD_TYPES, \
     DYNAMO_INTEGER_FIELD_TYPES
from dynamo.utils import remove_from_model_cache, build_existing_dynamic_models
from dynamo import handlers
from dynamo.exceptions import DuplicateFieldName
from dynamo.handlers import when_classes_prepared


# Build all existing dynamic models as soon as possible
# This is optional, but is nice as it avoids building the model when the
# first relevant view is loaded.
handlers.when_classes_prepared('dynamo.MetaModel','dynamo.MetaField', build_existing_dynamic_models)
    
  
class MetaModel(models.Model):
    name = models.SlugField(verbose_name=_('Name'), max_length=50, unique=True)
    verbose_name = models.CharField(verbose_name=_('Verbose name'), max_length=255, blank=True)
    app = models.CharField(verbose_name=_('Application'), max_length=50,blank=True,
                                   choices=tuple([(app.__name__.split('.')[-2],_(app.__name__.split('.')[-2])) for app in app_cache.get_apps()]))
    admin = models.BooleanField(verbose_name=_('Admin'), default=True)
    

    def get_model(self,*args,**kwargs):
        '''
        Returns a functional Django model based on current data
        Attention: this method does not take are of the model cache, admin, DB etc,
        this needs to be done separately.
        '''
        #if hasattr(self,'_model'):
        #    return self._model
        
        # Get all associated fields into a list ready for dict()
        #fields = [(f.name, f.get_django_field()) for f in self._fields.all()]

        # Use the create_model function defined above
        #self._model= model_factory(self)

        # Do not return anything, if model is not saved yet
        if not self.id:
            return None

        _app_label = getattr(self,'app',None).lower() or DYNAMO_DEFAULT_APP.lower()
        _model_name = self.name.encode('ascii')
        
        try:
            # try to get the model from the model cache
            m=app_cache.app_models[_app_label][_model_name]
        except KeyError:
            # Model has never been created before, just continue with the process
            pass
        except:
            # Any other error should be raised
            raise
        else:
            # if model was found, check the hash to identify changes
            if m.hash==self.get_hash():
                # return cached model, since nothing has changed
                return m
            else:
                # we need to clear the model cache here, otherwise
                # the metaclass ModelBase will not generate it, but get
                # the old one from the cache, when we run the type(...) statement
                remove_from_model_cache(_app_label,_model_name)

        # Create the model from sratch
        
        class Meta:
            app_label = _app_label
            verbose_name = self.verbose_name
            unique_together=self.unique_together
        attrs=self.django_fields
        attrs.update({
            'Meta': Meta,
            '__module__': getattr(self,'module',DYNAMO_DEFAULT_MODULE),
            '__unicode__': lambda s: '%s' % self.name,
            'hash': self.get_hash(),
            'admin': self.admin
            })
        return type(_model_name, (models.Model,), attrs)

    @property
    def unique_together(self):
        '''
        Returns the unique fields
        '''
        return [field.field_name for field in self.fields.filter(unique_together=True)]

    @property
    def django_fields(self):
        '''
        Returns a dictionary of the field names and field objects
        '''
        fields={}
        for field in self.fields.order_by('order').all():
            args,kwargs= field.django_field_attrs

            fields[field.field_name] = field.django_field(*args,**kwargs)
        return fields


    def get_hash(self):
        """
        Returns a hash based on a string to describe that parts of the model
        that are relevant to the generated dynamic model
        """
        # Only use the fields that are relevant
        model_list= [self.name] 
        fields_list = [field.hash_list for field in self.fields.all()]
        return md5_constructor(simplejson.dumps(model_list+fields_list)).hexdigest()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name    


STANDARD_FIELD_TYPE_CHOICES = [ (field,_(field)) for field in DYNAMO_STANDARD_FIELD_TYPES]
RELATION_FIELD_TYPE_CHOICES = [ (field,_(field)) for field in DYNAMO_RELATION_FIELD_TYPES]
FIELD_TYPE_CHOICES = STANDARD_FIELD_TYPE_CHOICES +RELATION_FIELD_TYPE_CHOICES

       
class MetaField(models.Model):
    name = models.SlugField(verbose_name=_('Field Name'), max_length=50)
    verbose_name = models.CharField(verbose_name=_('Verbose Name'),max_length=50,null=True,blank=True)
    meta_model = models.ForeignKey(MetaModel,verbose_name=_('Parent Model'), related_name='fields')    
    type = models.CharField(verbose_name=_('Field Type'),max_length=255,choices=FIELD_TYPE_CHOICES)
    related_model = models.CharField(verbose_name=_('Related Model'),max_length=50,null=True,blank=True) #models.ForeignKey('contenttypes.ContentType',null=True,blank=True)    
    order = models.IntegerField(verbose_name=_('Field Position'))
    unique_together=models.BooleanField(verbose_name=_('Unique Together'))
    unique=models.BooleanField(verbose_name=_('Unique'))    
    help_text = models.CharField(verbose_name=_('Help Text'), max_length=150, blank=True, null=True)
    choices = models.CharField(verbose_name=_('Choices'),max_length=200, blank=True,null=True)
    default  = models.CharField(verbose_name=_('Default Value'), max_length=50, blank=True)
    required = models.BooleanField(verbose_name=_('Required'), default=False)

    @property
    def django_choices(self):
        if self.choices:
            if self.type in DYNAMO_INTEGER_FIELD_TYPES:
                return tuple([(i,_(choice)) for i, choice in enumerate(self.choices.split(','))])
            else:
                return tuple([(choice,_(choice)) for choice in self.choices.split(',')])
        else:
            return None

    @property
    def django_field(self):
        '''Returns the correct django field class, not instantiated yet'''
        return getattr(models, self.type)

    @property
    def django_field_attrs(self):
        args,kwargs=[], {}

        # Field Choices
        choices=self.django_choices
        if choices:
            kwargs['choices']=choices

        # Relation ship attributes
        if self.type in DYNAMO_RELATION_FIELD_TYPES:
            app,model=self.related_model.split('.')
            args=args+[app_cache.app_models[app.lower()][model.lower()]]
            kwargs['related_name']='%ss' %self.name

        # Default
        if self.default:
            kwargs['default']=self.default

        # Verbose Name
        if self.verbose_name:
            kwargs['verbose_name']=self.verbose_name

        # Helptext
        if self.help_text:
            kwargs['help_text']=self.help_text

        # Required ==> Blank, Null
        if self.required:
           kwargs['blank']=False
           kwargs['null']=False
        else:
           kwargs['blank']=True
           if self.type in DYNAMO_STRING_FIELD_TYPES:
               kwargs['null']=False
           else:
               kwargs['null']=True
        if self.unique:
            kwargs['unique']=True

        # Max Lenght
        # TODO: add params
        kwargs['max_length']=50
            
        return args,kwargs

    @property
    def slug(self):
        return filter(str.isalnum,self.name.replace('-','_').replace(' ','_').encode('ascii', 'ignore'))
    @property
    def hash_list(self):
        return [self.name,self.verbose_name,self.type, self.related_model, self.order, self.unique, self.help_text, self.choices, self.default, self.required]

    @property
    def field_name(self):
        return self.slug

    def save(self,*args,**kwargs):
        try:
            return super(MetaField,self).save(*args,**kwargs)
        # TODO: fix that it only handles IntegrityErrors that refer to duplicate field names
        # TODO: check the relationship between relation ship field type and related model before saving
        except IntegrityError:
            raise DuplicateFieldName('You have defined 2 fields for model %s with the identical name %s' %(self.meta_model.name,self.name))

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name= 'Field'
        unique_together = (('meta_model', 'name'),('meta_model', 'order'),)



    
# Connect signals
pre_save.connect(handlers.field_pre_save, sender=MetaField)
post_save.connect(handlers.field_post_save, sender=MetaField )
post_delete.connect(handlers.field_post_delete, sender=MetaField)
pre_save.connect(handlers.model_pre_save, sender=MetaModel)
post_save.connect(handlers.model_post_save, sender=MetaModel)
pre_delete.connect(handlers.model_pre_delete, sender=MetaModel)


