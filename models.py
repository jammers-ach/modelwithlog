from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


def make_list_of_changes(form):
    '''Takes the changed fields in a form and tells you the proper name'''
    updated_fields = []
    for field_name, field in form.fields.items():
        if field_name in form.changed_data:
            updated_fields.append(field.label)

    print updated_fields
    return ",".join(updated_fields)

class ModelStamp(models.Model):

    STAMP_TYPES=((1,'Addition'),
                 (2,'Change'),
                 (3,'Deletion'))


    #User information
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True)
    user_objid = models.PositiveIntegerField() #this can be blank, the other can't)

    #Can't use foreignkeys to link to objects, so use an integer id and a content type id
    target_content_type = models.ForeignKey(ContentType)
    target_object_id = models.PositiveIntegerField()
    target_object = generic.GenericForeignKey(
        'target_content_type', 'target_object_id'
    )

    #Change messages
    timestamp = models.DateTimeField(auto_now_add=True)
    stamp_type = models.IntegerField(choices=STAMP_TYPES)
    change_message = models.TextField()

    #Changed fields (if there was any)


    class Meta:
        ordering=['-timestamp']

    @classmethod
    def create(klass,stamp_type,user,log_message,obj):

        stamp = klass()
        stamp.user = user
        stamp.user_objid = user.pk if user != None else -1
        stamp.stamp_type = stamp_type
        stamp.target_object = obj
        stamp.change_message = log_message
        stamp.save()



# Create your models here.
#
class ModelWithLog(models.Model):
    '''model but using the editlog from jdjangoextentions
    '''


    class Meta:
        abstract = True

    def log_change(self,user,log_message,form=None):
        '''logs that a change has taken place to this object'''

        if(form == None):
            self.log_stamp(user,log_message,2)
        else:
            self.log_stamp(user,log_message + ':' + make_list_of_changes(form) ,2)

    def log_creation(self,user,log_message):
        '''Lots that this object was created'''
        self.log_stamp(user,log_message,1)

    def log_deletion(self,user,log_message):
        '''Logs that this object was deleted'''
        self.log_stamp(user,log_message,3)

    def _get_content_type(self):
        return ContentType.objects.get_for_model(self)

    def get_stamps(self):
        return ModelStamp.objects.filter(target_content_type=self._get_content_type(),target_object_id=self.id,)


    def log_stamp(self,user,log_message,stamp_type):
        ModelStamp.create(stamp_type,user,log_message,self)
