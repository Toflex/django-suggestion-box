from django.db import models


class Box(models.Manager):

    def get_unread(self, ip_address):
        result = Suggestion.objects.filter(ip_address=ip_address, read=False)
        if result:
            return result.get()
        else:
            return Suggestion(ip_address=ip_address)


class Suggestion(models.Model):
    message = models.TextField(null=False, blank=True, default='')
    ip_address = models.GenericIPAddressField(null=False, blank=False)
    read = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    objects = Box()

    def __unicode__(self):
        return '%s - %s' % (self.created, self.ip_address)

    def validate_unique(self, exclude=None):
        if self.deleted and not self.read:
            raise ValidationError(('Invalid finite state'), code='invalid')
        unique = super(Suggestion, self).validate_unique(exclude=exclude)
        if self.read is True:
            return unique
        if type(self).objects.exclude(id=self.id).filter(
                read=False, ip_address=self.ip_address).exists():
            raise ValidationError(('Duplicate IP Error'), code='invalid')
