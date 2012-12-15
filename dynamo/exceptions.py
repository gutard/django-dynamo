
# MetaField and MetaModel Exceptions

class DuplicateFieldName(Exception):
    '''
    A field is assigned to a MetaModel with a field name, that already
    exists for that MetaModel
    '''
    pass

class DuplicateFieldOrder(Exception):
    '''
    A field is assigned to a MetaModel with a field order, that already
    exists for that MetaModel
    '''
    pass


# API exceptions
class MetaModelAlreadyAssigned(Exception):
    '''
    The current instance of the API Model class has already been assigned a
    value to it. It can only have exactly 1 model assigned
    '''

class NoMetaModelAssigned(Exception):
    '''
    The current instance of the API Model class has not been assigned a
    value to it yet. Thus no operations can be performed yet.
    '''

class AssignedModelNotOfTypeMetaModel(Exception):
    '''
    The assigned model to the API Model class must be an instance of MetaModel
    '''
