from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.core.exceptions import ValidationError
from django.db import models


class Box(models.Manager):

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.model)
        return urlresolvers.reverse("admin:%s_%s_changelist" % (
            content_type.app_label, content_type.model))

    def get_unread(self, ip_address):
        result = Suggestion.objects.filter(ip_address=ip_address, read=False)
        if result.exists():
            return result.get()
        else:
            return Suggestion(ip_address=ip_address)


class Suggestion(models.Model):
    message = models.TextField(null=False, blank=True, default='')
    ip_address = models.GenericIPAddressField(null=False, blank=False)
    read = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    objects = Box()

    def __unicode__(self):
        return '%s - %s' % (self.created, self.ip_address)

    @property
    def message_start(self):
        return self.message[:80]

    def clean(self):
        clean = super(Suggestion, self).clean()
        if self.blocked:
            self.read = False
        if self.read is True:
            return clean
        if type(self).objects.exclude(id=self.id).filter(
                read=False, ip_address=self.ip_address).exists():
            raise ValidationError(('Duplicate IP Error'), code='invalid')

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (
            content_type.app_label, content_type.model), args=(self.id,))
