from django.db import models
# Create your models here.
from django.utils.text import slugify
# from simple_history.models import HistoricalRecords
from simple_history.models import HistoricalRecords

from ticket import enums


class Query(models.Model):
    """
    Create query ticket
    """
    subject = models.CharField(max_length=30, blank=False, verbose_name='موضوع تیکت')
    message = models.CharField(max_length=500, blank=False, verbose_name='متن تیکت')
    status = models.CharField(max_length=20, choices=enums.TicketStatuses.choices,
                              default=enums.TicketStatuses.CREATED, verbose_name='وضعیت تیکت')
    is_active = models.BooleanField(default=True, verbose_name='فعال است؟')
    create_info = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    slug = models.SlugField(max_length=50, unique=True, editable=False)
    # ForeignKey
    user_related = models.ForeignKey('auth.User', on_delete=models.PROTECT, verbose_name='رابطه با کاربران', null=True,
                                     blank=True)
    category_related = models.ForeignKey('ticket.Category', on_delete=models.PROTECT, verbose_name='رابطه با کتگوری',
                                         null=True,
                                         blank=True)
    operator_related = models.CharField(max_length=20, default=0, verbose_name='ادمین این تیکت')
    history = HistoricalRecords()

    def __str__(self):
        """
        :return: define name
        """
        return self.subject

    def save(self, *args, **kwargs):
        """
        auto add slug
        """
        if not self.id:
            self.slug = slugify(self.subject, allow_unicode=True)
        super().save(*args, **kwargs)

    def close_query(self):
        if self.is_active:
            self.is_active = False
            self.status=enums.TicketStatuses.CANCELED
            return True
        else:
            return False


class Replay(models.Model):
    """
    Create replay ticket
    """
    replay_message = models.CharField(max_length=500, blank=False, verbose_name='پاسخ تیکت')
    create_info = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    query_related = models.ForeignKey('ticket.Query', on_delete=models.CASCADE, verbose_name='کلید جواب برای سوال',
                                      null=True,
                                      blank=True)
    operator_related = models.ForeignKey('auth.User', on_delete=models.PROTECT, verbose_name='کلید شخص برای سوال',
                                         null=True,
                                         blank=True)
    history = HistoricalRecords()

    def __str__(self):
        """
        :return: define name
        """
        return self.replay_message


class Category(models.Model):
    """
    Create category for tickets and operators
    """
    category_name = models.CharField(max_length=100, blank=False, unique=True, verbose_name='دسته بندی تیکت')
    slug = models.SlugField(max_length=50, unique=True, editable=False)
    history = HistoricalRecords()

    # query_related = models.ForeignKey('ticket.Query', on_delete=models.PROTECT, verbose_name='رابطه با پرسش')

    def __str__(self):
        """
        :return: define name
        """
        return self.category_name

    def save(self, *args, **kwargs):
        """
        auto add slug
        """
        if not self.id:
            self.slug = slugify(self.category_name, allow_unicode=True)
        super().save(*args, **kwargs)
