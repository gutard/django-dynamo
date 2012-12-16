
# django imports
from django.contrib import admin
from django import forms
from django.db import models

# dynamo imports
from dynamo.models import MetaModel, MetaField



class MetaFieldInlineAdmin(admin.StackedInline):
    model = MetaField
    fieldsets =(
        (None,{
            'fields':(('name','type','related_model'),
                      ('order','required','default','choices'),)
            }),
        ('Advanced Options',{
            'fields': (('verbose_name','description'),
                       ('unique','unique_together','help')),
            'classes': ('collapse',)
            })
        )
    extra=0


class MetaModelForm(forms.ModelForm):
    class Meta:
        model=MetaModel
    
class MetaModelAdmin(admin.ModelAdmin):
    model=MetaModel
    form=MetaModelForm
    inlines= [MetaFieldInlineAdmin]
    list_display =('name','verbose_name')
    list_display_links =('name','verbose_name')
    list_display_editable =('name','verbose_name')
    ordering=('name',)
    
    fieldsets = (
        (None, {
            'fields': (('name', 'verbose_name'),)
            }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (('app', 'admin'),)
            }),
        )
    def formfield_for_choice_field(self, db_field, request, **kwargs):
##        if db_field.name == "status":
##            kwargs['choices'] = (
##                ('accepted', 'Accepted'),
##                ('denied', 'Denied'),
##            )
##            if request.user.is_superuser:
##                kwargs['choices'] += (('ready', 'Ready for deployment'),)
        return super(MetaModelAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)        

admin.site.register(MetaModel, MetaModelAdmin)

