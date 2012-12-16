
# django imports
from django.conf import settings


# Delete database column after field has been deleted
DYNAMO_DELETE_COLUMNS = getattr(settings,'DYNAMO_DELETE_COLUMNS',True)

# Delete database table after model has been deleted
DYNAMO_DELETE_TABLES  = getattr(settings,'DYNAMO_DELETE_TABLES',True)

# Default app to be used when model is generated
DYNAMO_DEFAULT_APP = getattr(settings,'DYNAMO_DEFAULT_APP','dynamo')

# Default module to be used when model is generated
DYNAMO_DEFAULT_MODULE = getattr(settings,'DYNAMO_DEFAULT_MODULE','dynamo.models')

# Available standard Field Types (as of Django 1.3)
from django.db import models
FIELD_TYPES = [('AutoField', models.AutoField),
               ('BooleanField', models.BooleanField),
               ('CharField', models.CharField),
               ('CommaSeparatedIntegerField', models.CommaSeparatedIntegerField),
               ('DateField', models.DateField),
               ('DateTimeField', models.DateTimeField),
               ('DecimalField', models.DecimalField),
               ('EmailField', models.EmailField),
               ('FileField', models.FileField),
               ('FloatField', models.FloatField),
               ('ImageField', models.ImageField),
               ('NullBooleanField', models.NullBooleanField),
               ('SlugField', models.SlugField),
               ('TimeField', models.TimeField),
               ('URLField', models.URLField),
               ('BigIntegerField', models.BigIntegerField),
               ('IntegerField', models.IntegerField),
               ('PositiveIntegerField', models.PositiveIntegerField),
               ('PositiveSmallIntegerField', models.PositiveSmallIntegerField),
               ('SmallIntegerField', models.SmallIntegerField),
               ('ForeignKey', models.ForeignKey),
               ('OneToOneField', models.OneToOneField),
               ('ManyToManyField', models.ManyToManyField)
               ]

DYNAMO_FIELD_TYPES = getattr(settings,'DYNAMO_FIELD_TYPES',FIELD_TYPES)

STANDARD_FIELD_TYPES = ['AutoField',
                        'BooleanField',
                        'CharField',
                        'CommaSeparatedIntegerField',
                        'DateField',
                        'DateTimeField',
                        'DecimalField',
                        'EmailField',
                        'FileField',
                        'FloatField',
                        'ImageField',
                        'NullBooleanField',
                        'SlugField',
                        'TimeField',
                        'URLField',
                        'BigIntegerField',
                        'IntegerField',
                        'PositiveIntegerField',
                        'PositiveSmallIntegerField',
                        'SmallIntegerField'                        
                        ]
DYNAMO_STANDARD_FIELD_TYPES = getattr(settings, 'DYNAMO_STANDARD_FIELD_TYPES', STANDARD_FIELD_TYPES)

INTEGER_FIELD_TYPES =   ['BigIntegerField',
                         'IntegerField',
                         'PositiveIntegerField',
                         'PositiveSmallIntegerField',
                         'SmallIntegerField'
                         ]
DYNAMO_INTEGER_FIELD_TYPES = getattr(settings, 'DYNAMO_INTEGER_FIELD_TYPES',INTEGER_FIELD_TYPES)


STRING_FIELD_TYPES =    ['CommaSeparatedIntegerField',
                        'EmailField',
                        'FileField',
                        'ImageField',
                        'SlugField',
                        'URLField',
                        ]
DYNAMO_STRING_FIELD_TYPES = getattr(settings, 'DYNAMO_STRING_FIELD_TYPES',STRING_FIELD_TYPES)

# Available relationship Field Types (as of Django 1.3)
RELATION_FIELD_TYPES =['ForeignKey','OneToOneField','ManyToManyField']
DYNAMO_RELATION_FIELD_TYPES = getattr(settings, 'DYNAMO_RELATION_FIELD_TYPES',RELATION_FIELD_TYPES)


