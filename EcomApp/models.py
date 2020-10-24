from django.db import models
from django.forms import ModelForm, TextInput, EmailInput, Textarea

# Create your models here.


class Setting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False')
    )
    title = models.CharField(max_length=200, blank=True)
    keyword = models.CharField(max_length=200)
    description = models.TextField()
    phone = models.IntegerField()
    fax = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    smtpserver = models.CharField(max_length=100, blank=True, null=True)
    smtpemail = models.EmailField(max_length=50, blank=True, null=True)
    smtppassword = models.CharField(blank=True, max_length=50)
    smtpport = models.CharField(blank=True, max_length=100)
    icon = models.ImageField(blank=True, null=True, upload_to='icon/')
    facebook = models.CharField(blank=True, null=True, max_length=100)
    instagram = models.CharField(blank=True, null=True, max_length=100)
    twitter = models.CharField(blank=True, null=True, max_length=100)
    linkedin = models.CharField(blank=True, null=True, max_length=100)
    pinterest = models.CharField(blank=True, null=True, max_length=100)
    youtube = models.CharField(blank=True, null=True, max_length=100)
    rss = models.CharField(blank=True, null=True, max_length=100)
    address = models.TextField()
    contact = models.TextField()
    reference = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed')
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=1000)
    status = models.CharField(max_length=40, default='New')
    ip = models.CharField(max_length=100, blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ContactMessageForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name', 'required': 'required'}),


            'email': EmailInput(attrs={'type': 'email', 'class': 'form-control', 'placeholder': 'Your Email', 'required': 'required'}),

            'subject': TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject', 'required': 'required'}),

            'message': Textarea(attrs={'class': 'form-control', 'placeholder': 'Message', 'rows': '5', 'required': 'required'}),
        }
        labels = {
            'name': '',
            'email': '',
            'subject': '',
            'message': '',
        }
