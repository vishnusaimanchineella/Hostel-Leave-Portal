import datetime
from student.utility import code_format
from django.db import models
from student.wardens import Studentmanager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from leave.models import Leave




# Create your models here.


class Department(models.Model):


    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125,null=True,blank=True)

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)


    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['name','created']
    
    def __str__(self):
        return self.name



class Student(models.Model):

    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    NOT_KNOWN = 'Not Known'

    GENDER = (
    (MALE,'Male'),
    (FEMALE,'Female'),
    (OTHER,'Other'),
    (NOT_KNOWN,'Not Known'),
    )


    
    
    # PERSONAL DATA
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    
    image = models.FileField(_('Profile Image'),upload_to='profiles',default='default.png',blank=True,null=True,help_text='upload image size less than 2.0MB')#work on path username-date/image
    firstname = models.CharField(_('Firstname'),max_length=125,null=False,blank=False)
    lastname = models.CharField(_('Lastname'),max_length=125,null=False,blank=False)
    othername = models.CharField(_('Othername (optional)'),max_length=125,null=True,blank=True)
    birthday = models.DateField(_('Birthday'),blank=False,null=False)
   
 
    department =  models.ForeignKey(Department,verbose_name =_('Department'),on_delete=models.SET_NULL,null=True,default=None)
    studentid = models.CharField(_('Student ID Number'),max_length=10,null=True,blank=True)

    # app related
    is_blocked = models.BooleanField(_('Is Blocked'),help_text='button to toggle employee block and unblock',default=False)
    is_deleted = models.BooleanField(_('Is Deleted'),help_text='button to toggle employee deleted and undelete',default=False)
 
    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)


    #PLUG MANAGERS
    objects = Studentmanager()

    
    
    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
        ordering = ['-created']



    def __str__(self):
        return self.get_full_name

    

    @property
    def get_full_name(self):
        fullname = ''
        firstname = self.firstname
        lastname = self.lastname
        othername = self.othername

        if (firstname and lastname) or othername is None:
            fullname = firstname +' '+ lastname
            return fullname
        elif othername:
            fullname = firstname + ' '+ lastname +' '+othername
            return fullname
        return


    @property
    def get_age(self):
        current_year = datetime.date.today().year
        dateofbirth_year = self.birthday.year
        if dateofbirth_year:
            return current_year - dateofbirth_year
        return



    @property
    def can_apply_leave(self):
        pass





   

    





    def save(self,*args,**kwargs):
        '''
        overriding the save method - for every instance that calls the save method 
        perform this action on its employee_id
        added : March, 03 2019 - 11:08 PM

        '''
        get_id = self.studentid #grab employee_id number from submitted form field
        data = code_format(get_id)
        self.studentid = data #pass the new code to the employee_id as its orifinal or actual code
        super().save(*args,**kwargs) # call the parent save method
        # print(self.employeeid)









