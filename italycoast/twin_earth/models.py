from django.utils.translation import gettext_lazy as _
from django.db import models

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

    source = models.TextField(null=True)
    layer_name = models.CharField(max_length=256, null=True)
    readable_name = models.CharField(max_length=256, default="")
    description = models.TextField(default="")
    keywords = models.TextField(default="") # Comma separated keywords
    type = models.CharField(max_length=256, choices=LayerType.choices)
    parameters = models.TextField(default="", blank=True) # Comma separated parameters of the layer
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT, related_name="layers")
    frequency = models.CharField(max_length=256, blank=True, null=True, default="") #monthly, daily, hourly

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