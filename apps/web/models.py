from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

class Category(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(default='', editable=False, max_length=550)
    keterangan = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Options(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(default='', editable=False, max_length=550)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='option/', blank=True)
    keterangan = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Option"
        verbose_name_plural = "Options"


class Regions(models.Model):
    name = models.CharField(max_length=75)
    slug = models.SlugField(default='', editable=False, max_length=100, blank=True, null=True)
    area_code = models.PositiveIntegerField()
    category = models.ForeignKey('Options', limit_choices_to={'category': 1}, on_delete=models.CASCADE)
    parents = models.ForeignKey('self', null=True, blank=True, related_name='sub_provinces', on_delete=models.CASCADE )
    keterangan = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def top_level_province(self):
        region = self
        while region.parents:
            region = region.parents
        return region

    class Meta:
        verbose_name = 'Provinisi/Kabupaten/Kota'
        verbose_name_plural = "Provinisi/Kabupaten/Kota"

class Incidents(models.Model):
    incident_id = models.CharField(max_length=10)
    incident_date = models.DateField()
    location = models.ForeignKey('Regions', null=True, blank=True, related_name='incident_loc', on_delete=models.CASCADE)
    coder = models.ForeignKey(User, null=True, blank=True, related_name='incidents_coded', on_delete=models.SET_NULL)
    verificator = models.ForeignKey(User, null=True, blank=True, related_name='incidents_verified',
                                    on_delete=models.SET_NULL)
    image = models.ImageField(upload_to="incidents/")
    link = models.URLField(blank=True, null=True)
    category = models.ManyToManyField('Options', limit_choices_to={'category': 2}, related_name='Violence_category')
    incident_relation = models.ForeignKey('self', null=True, blank=True, related_name='incident_relations', on_delete=models.CASCADE)
    description = models.TextField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)


    def __str__(self):
        return f"Incident {self.incident_id} on {self.incident_date}"

    def save(self, *args, **kwargs):
        if not self.coder and hasattr(settings, 'CURRENT_USER'):
            self.coder = settings.CURRENT_USER
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Incidents"
        verbose_name_plural = "Incident"

class Actor(models.Model):
    incident = models.ForeignKey('Incidents', related_name='Incident_id', on_delete=models.CASCADE)
    actor = models.ForeignKey('Options', related_name='incident_actor', limit_choices_to={'category': 3}, on_delete=models.CASCADE)
    actor_atribute = models.ForeignKey('Options', limit_choices_to={'category': 4}, related_name='attribute_actor', on_delete=models.CASCADE)
    minorities = models.BooleanField(default=False)
    total_actor = models.IntegerField(default='-99')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.incident)

    class Meta:
        verbose_name = "Actors"
        verbose_name_plural = "Actor"

class Violence(models.Model):
    incident = models.ForeignKey('Incidents', related_name='Incident_violence', on_delete=models.CASCADE)
    violence_form = models.ForeignKey('Options', limit_choices_to={'category': 5}, related_name='form_violence', on_delete=models.CASCADE)
    weapon_type = models.ForeignKey('Options', limit_choices_to={'category': 6}, related_name='weapon_type_violence', on_delete=models.CASCADE)
    issue_type = models.ForeignKey('Options', limit_choices_to={'category': 2}, related_name='issue_type_violence', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Incident {self.incident}"

    class Meta:
        verbose_name = "Violences"
        verbose_name_plural = "Violence"

class Casualities(models.Model):
    incident = models.ForeignKey('Incidents', related_name='Incident_casualities', on_delete=models.CASCADE)
    num_death = models.PositiveIntegerField(default='0')
    num_injured = models.PositiveIntegerField(default='0')
    death_injured = models.PositiveIntegerField(default='0')
    female_death = models.PositiveIntegerField(default='0')
    female_injured = models.PositiveIntegerField(default='0')
    female_total = models.PositiveIntegerField(default='0')
    child_death = models.PositiveIntegerField(default='0')
    child_injured = models.PositiveIntegerField(default='0')
    child_total = models.PositiveIntegerField(default='0')
    infra_damage = models.PositiveIntegerField(default='0')
    infra_destroyed = models.PositiveIntegerField(default='0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Incident {self.incident}"

    class Meta:
        verbose_name = "Casualities"
        verbose_name_plural = "Casuality"

class Intervene(models.Model):
    incident = models.ForeignKey('Incidents', related_name='Incident_intervene', on_delete=models.CASCADE)
    intervene_actor = models.ForeignKey('Options', limit_choices_to={'category': 7}, on_delete=models.CASCADE)
    intervene_actor_type = models.ForeignKey('Options', on_delete=models.CASCADE, limit_choices_to={'category': 4}, related_name='intervene_type')
    result = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Incident {self.incident}"

    class Meta:
        verbose_name = "Intervene"
        verbose_name_plural = "Intervene"

class DataName(models.Model):
    name = models.CharField(max_length=225)
    slug = models.SlugField(default='', editable=False, max_length=550)
    category = models.ForeignKey('Options', related_name='Statistics', limit_choices_to={'category': 9}, on_delete=models.CASCADE)
    satuan = models.ForeignKey('Options', related_name='Statistics_satuan', limit_choices_to={'category': 8}, on_delete=models.CASCADE)
    sumber = models.TextField(blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Data Name"
        verbose_name_plural = "Data Name"

class DataValue(models.Model):
    name = models.ForeignKey('DataName', on_delete=models.CASCADE)
    region = models.ForeignKey('Regions', on_delete=models.CASCADE)
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} area {self.region}"

    class Meta:
        verbose_name = "Data Value"
        verbose_name_plural = "Data Value"

