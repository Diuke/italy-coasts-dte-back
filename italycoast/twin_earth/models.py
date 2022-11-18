from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=256)
    #parent_layer_group = models.ForeignKey("self", blank=True, null=True, on_delete=models.PROTECT, default=None, related_name="children_layer_groups")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Layer(models.Model):

    class LayerType(models.TextChoices):
        WFS = 'WFS', _('WFS')
        WMS = 'WMS', _('WMS')
        WMST = 'WMST', _('WMST')
        ARCGIS_ImageServer = 'ARCGIS_IS', _('ArcGIS ImageServer')
        ARCGIS_MapServer = 'ARCGIS_MS', _('ArcGIS MapServer')

    source = models.TextField(null=True)
    layer_name = models.CharField(max_length=256, null=True)
    readable_name = models.CharField(max_length=256, default="")
    description = models.TextField(default="")
    keywords = models.TextField(default="", blank=True, null=True) # Comma separated keywords
    type = models.CharField(max_length=256, choices=LayerType.choices)
    parameters = models.TextField(default="", blank=True) # Comma separated parameters of the layer
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT, related_name="layers")
    frequency = models.CharField(max_length=256, blank=True, null=True, default="") #monthly, daily, hourly
    units = models.CharField(max_length=100, blank=True, null=True, default="")

    enabled = models.BooleanField(default=True)

    service_url = models.TextField(null=True)
    metadata_url = models.TextField(null=True)
    legend_url = models.TextField(null=True) 
    more_data_url = models.TextField(null=True)
    copyright = models.TextField(null=True)

    initial_time_range = models.DateField(blank=True, null=True) #DD-MM-AAAA
    final_time_range = models.DateField(blank=True, null=True) #DD-MM-AAAA

    def __str__(self):
        return f'{self.readable_name} - {self.layer_name} - {self.frequency}'

    class Meta:
        db_table = "layer"
        verbose_name = "Layer"
        verbose_name_plural = "Layers"

class Scenario(models.Model):
    name = models.CharField(max_length=256)
    scenario_json = models.JSONField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="scenarios")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "scenario"
        verbose_name = "Scenario"
        verbose_name_plural = "Scenarios"