
# django imports
from django.test import TestCase

# dynamo imports
from dynamo.models import *
from dynamo.exceptions import DuplicateFieldName
from dynamo_app.models import TestModel

        
class TestDynamicModel(TestCase):
    def setUp(self):

        # Create meta model 1
        self.meta1=MetaModel(name='meta1',description='meta1')
        self.meta1.save()

        # Create meta model 2
        self.meta2=MetaModel(name='meta2',description='meta2')
        self.meta2.save()

        # Get DynamicModel 2 from meta model 2
        #self.DynamicModel2=self.meta2.get_model()

        # Add a normal TextField to meta model 1
        self.field1=MetaField(meta_model=self.meta1,name='field1',description='field1',type='TextField',order=1)
        self.field1.save()

        # Add another TextField to meta model 1
        self.field2=MetaField(meta_model=self.meta1,name='field2',description='field2',type='TextField',order=2)
        self.field2.save()

        
        # Add a normal IntegerField to meta model 1
        self.field3=MetaField(meta_model=self.meta1,name='field3',description='field3',type='IntegerField',order=3)
        self.field3.save()


        # Add a relationship field to meta model 2, refering to TestModel
        self.field4=MetaField(meta_model=self.meta1,name='field4',description='field2',
                              type='ForeignKey', related_model='dynamo_app.TestModel', order=4)
        self.field4.save()  

        # Add a relationship field to meta model 2, refering to DynamicModel 
        self.field5=MetaField(meta_model=self.meta1,name='field5',description='field2',
                              type='ForeignKey', related_model='dynamo.%s'%self.meta2.model_name, order=5)
        self.field5.save()     


    def test_MetaModelAdmin(self):
        # TODO: check existence or non existence of Admin based on MetaModel admin field
        pass

    def test_MetaModelApp(self):
        # TODO: check the app and the app in admin based on the MetaModel app field
        pass


    def test_MetaModelDelete(self):
        # TODO: check if the underlying table is deleted or not based on settings
        pass

    def test_FieldSaveWithoutDuplicates(self):
        '''
        Test the creation and saving of fields
        ==> should raise no error
        '''
        field6=MetaField(meta_model=self.meta1,name='field6',description='field6',type='TextField',order=6)
        field6.save()
        field7=MetaField(meta_model=self.meta1,name='field7',description='field7',type='TextField',order=7)
        field7.save()    
        
    def test_FieldSaveWithDuplicatesAcrossMeta(self):
        '''
        Test the creation and saving of fields with identical names, but different meta_model
        ==> should raise no error
        '''
        field6=MetaField(meta_model=self.meta1,name='field6',description='field6',type='TextField',order=6)
        field6.save()
        field6=MetaField(meta_model=self.meta2,name='field7',description='field7',type='TextField',order=7)
        field6.save()  

    def test_FieldSaveWithDuplicatesWithinMeta(self):
        '''
        Test the creation and saving of fields with identical names and identical meta_model
        ==> should raise an error
        '''
        field6=MetaField(meta_model=self.meta1,name='field6',description='field6',type='TextField',order=6)
        field6.save()
        field6=MetaField(meta_model=self.meta1,name='field6',description='field7',type='TextField',order=7)
        self.assertRaises(DuplicateFieldName,field6.save)

    def test_FieldUnique(self):
        # TODO
        pass

    def testFieldUniqueTogether(self):
        # TODO
        pass
    
    def test_FieldChoicesInt(self):
        # TODO
        pass

    def test_FieldChoicesChar(self):
        # TODO
        pass

    def test_FieldDefault(self):
        # TODO
        pass

    def test_FieldVerboseName(self):
        # TODO
        pass

    def test_FieldOrder(self):
        # TODO
        pass
    
        
    def test_FieldUpdateName(self):
        # TODO
        pass
    def test_FieldUpdateDescription(self):
        # TODO
        pass
    def test_FieldUpdateOptions(self):
        # TODO
        pass
    def test_FieldDelete(self):
        # TODO
        pass
    def test_FieldDeleteRel(self):
        # TODO
        pass         

    def test_ModelGeneration(self):
        '''
        Test the generation of the model via model cache
        '''

        # Get the dynamic model
        DynamicModel=self.meta1.get_model()
        options=DynamicModel._meta
        # Check the module name of the model
        self.assertEqual(options.db_table,'dynamo_%s_%s' %(str(self.meta1.id),self.meta1.name))
        
        #Check the name of db table in meta
        self.assertEqual(options.db_table,'dynamo_%s_%s' %(str(self.meta1.id),self.meta1.name))

        # Check the name of the fields in meta
        self.assertEqual(options.get_field('field1').name,'field1')
        self.assertEqual(options.get_field('field2').name,'field2')

        # Ensure that the generated model is identical to the model cache
        from django.db.models import get_model
        installed_model= get_model('dynamo',self.meta1.model_name)
        self.assertIs(installed_model,DynamicModel)

    def test_DynamicModelBasic(self):

        # Get the dynamic model
        DynamicModel=self.meta1.get_model()

        # Create an instance of the dynamic model
        instance=DynamicModel(field1='content field 1', field3=2 )
        self.assertEqual(instance.id,None)
        instance.save()
        self.assertEqual(instance.field1,'content field 1')
        self.assertEqual(instance.field3,2)
        self.assertNotEqual(instance.id,None)

    def test_ForeignKeyField2ExternalModel(self):

        # Get the dynamic model
        DynamicModel1=self.meta1.get_model()

        # Create an instance of the TestModel
        instance_test=TestModel(test_field=1)
        instance_test.save()   

        # Create an instance of the dynamic model with a relationship to TestModel
        instance1=DynamicModel1(field1='content field 1', field4=instance_test )
        self.assertEqual(instance1.id,None)
        instance1.save()
        self.assertEqual(instance1.field1,'content field 1')
        self.assertEqual(instance1.field4,instance_test)
        self.assertNotEqual(instance1.id,None)


        # Check whether the related field has been created on the TestModel class
        self.assertEqual(instance_test.field4s.all()[0].field1,'content field 1')

        # Check whether the relationship field has access to the TestModel class and instances
        self.assertEqual(instance1.field4,instance_test)
        
    def test_ForeignKeyField2DynamicModel(self):

        # Get the dynamic models
        DynamicModel1=self.meta1.get_model()
        DynamicModel2=self.meta2.get_model()

        # Creante a normal instance of dynamic model 2 and create an instance
        # of the dynamic model 1 with a relationship to DynamicModel2
        instance2=DynamicModel2()
        instance2.save()
        instance1=DynamicModel1(field1='content field 1', field5=instance2 )
        self.assertEqual(instance1.field1,'content field 1')
        self.assertEqual(instance1.field5,instance2)
        self.assertEqual(instance1.id,None)
        instance1.save()

        # Check whether the related field has been created on the TestModel class
        self.assertEqual(instance2.field5s.all()[0].field1,'content field 1')

        # Check whether the relationship field has access to the TestModel class and instances
        self.assertEqual(instance1.field5,instance2)        
    


class TestDynamicModelSignals(TestCase):
    pass
                 

