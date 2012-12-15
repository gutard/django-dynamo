# this complete code is just experimental and does not work yet at all
# TODO: please fix me


# dynamo imports
from dynamo.models import MetaModel, MetaField
from dynamo.exceptions MetaModelAlreadyAssigned, NoMetaModelAssigned, AssignedModelNotOfTypeMetaModel

class Field(object):
    pass


class Model(object):
    '''
    Model is a proxy class, which instances refer to exactly 1 MetaModel
    instance.
    '''
    def __init__(self,*args,**kwargs):
        '''
        A MetaModel instance can either be provided as first argument or with
        the keyword model
        '''
        self._model=args.get(0,None) or kwargs.get('model',None)
        if not isinstance(self._model,MetaModel):
            raise AssignedModelNotOfTypeMetaModel
        super(Dynamo,self).__init__()

    def get(self,key):
        '''
        Returns the MetaModel attribute key.
        '''
        try:
            return getattr(self._model,key)
        except:
            raise
            

    def set(self,key,value=None):
        '''
        Sets MetaModel attribute key to the specified value and saves it.
        or
        Accepts MetaModel and assigns it to the current instance.
        '''
        if not value and isinstance(key,MetaModel):
            if self._model:
                raise MetaModelAlreadyAssigned
            else:
                self._model=key
        try:
            setattr(self._model,key,value)
            self._model.save()
        except:
            raise

    def create(self,name,**kwargs):
        '''
        Creates a MetaModel with the given kwargs and saves it.
        '''
        if self._model:
            raise MetaModelAlreadyAssigned
        else:
            try:
                kwargs['name']=name
                self._model=MetaModel(**kwargs)
                self._model.save()
            except:
                raise

    def add_field(self,name,**kwargs):
        '''
        Creates a field with the given kwargs, adds it to the
        MetaModel, and saves both
        '''
        try:
            kwargs['name']=name
            kwargs['meta_model']=self._model
            field=MetaField(**kwargs)
            field.save()
        except:
            raise

    def remove_field(self,name):
        '''
        Deletes the field with the specified name from the MetaModel and saves
        it.
        '''
    def introspect(self):
        '''
        Introspects the MetaModel and its attached field and returns the informtions as a dict
        '''
        pass
    
        
