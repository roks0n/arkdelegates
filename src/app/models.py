from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.utils.text import slugify

from app.constants import PIN_LENGTH

MAINNET = 'mainnet'
DEVNET = 'devnet'
NETWORK_CHOICES = (
    (MAINNET, 'mainnet'),
    (DEVNET, 'devnet'),
)


class Delegate(models.Model):
    user = models.OneToOneField(get_user_model(), blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    address = models.CharField(max_length=34, db_index=True)
    public_key = models.CharField(max_length=66, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True, auto_now=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    proposal = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Delegate "{}">'.format(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class History(models.Model):
    delegate = models.ManyToManyField('Delegate', related_name='history')
    voters = models.IntegerField(null=True, blank=True)
    uptime = models.FloatField(null=True, blank=True)
    approval = models.FloatField(null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True, db_index=True)
    forged = models.FloatField(null=True, blank=True)
    missed = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    voting_power = models.CharField(max_length=20, null=True, blank=True)
    payload = JSONField(default=dict)


class Node(models.Model):
    delegate = models.ForeignKey('Delegate', related_name='nodes', on_delete=models.CASCADE)
    network = models.CharField(max_length=10, default=MAINNET, choices=NETWORK_CHOICES)
    cpu = models.CharField(max_length=256, null=True, blank=True)
    memory = models.CharField(max_length=256, null=True, blank=True)
    is_dedicated = models.BooleanField(default=False)
    is_backup = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    has_arkstats = models.BooleanField(default=False)


class Contribution(models.Model):
    delegate = models.ForeignKey('Delegate', related_name='contributions', on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)


class ClaimAccointPin(models.Model):
    delegate = models.ForeignKey('Delegate', related_name='claim_account', on_delete=models.CASCADE)
    pin = models.CharField(max_length=PIN_LENGTH)
    generated_at = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<ClaimAccointPin "{}">'.format(self.delegate.name)
