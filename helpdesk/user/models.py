from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
phone_re = RegexValidator(regex='^0[0-9]{2,}[0-9]{7,}$', message='شماره وارد شده صحیح نیست!')


class User(models.Model):
    """
    Register a user
    """
    name = models.CharField(max_length=30, blank=False, verbose_name='نام')
    last_name = models.CharField(max_length=30, blank=False, verbose_name='نام خانوادگی')
    email = models.EmailField(max_length=50, blank=False, verbose_name='ایمیل')
    phone = models.CharField(max_length=11, unique=True, validators=[phone_re], verbose_name='شماره موبایل')
    last_login = models.DateTimeField(auto_now=True, verbose_name='اخرین ورود')

    def __str__(self):
        """
        :return: define name
        """
        return self.name, self.last_name
