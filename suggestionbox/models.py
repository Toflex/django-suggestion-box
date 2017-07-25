from django.db import models


class Suggestion(models.Model):
    message = models.TextField(null=False, blank=True, default='')
    ip_address = models.GenericIPAddressField(null=False, blank=False)
    read = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s - %s' % (self.created, self.class_name)

    def validate_unique(self, exclude=None):
        unique = super(Suggestion, self).validate_unique(exclude=exclude)
        if self.read is True:
            return unique
        if type(self).objects.exclude(id=self.id).filter(
                read=False, ip_address=self.ip_address).exists():
            raise ValidationError(('Duplicate IP Error'), code='invalid')
