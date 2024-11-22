from django.db import models

# Create your models here.
class Taxonomy(models.Model):
    kingdom = models.CharField(max_length=255, verbose_name="界", blank=True, null=True)
    phylum = models.CharField(max_length=255, verbose_name="门", blank=True, null=True)
    class_name = models.CharField(max_length=255, verbose_name="纲", blank=True, null=True)
    subclass_name = models.CharField(max_length=255, verbose_name="亚纲", blank=True, null=True)
    order = models.CharField(max_length=255, verbose_name="目", blank=True, null=True)
    family = models.CharField(max_length=255, verbose_name="科", blank=True, null=True)
    genus = models.CharField(max_length=255, verbose_name="属", blank=True, null=True)
    species = models.CharField(max_length=255, verbose_name="种", blank=True, null=True)
    subspecies = models.CharField(max_length=255, verbose_name="亚种", blank=True, null=True)

    class Meta:
        db_table = 'taxonomy'
        verbose_name = "物种信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.kingdom} {self.phylum} {self.class_name} {self.subclass_name} {self.order} {self.family} {self.genus} {self.species} {self.subspecies}"


class Insect(models.Model):
    chinese_name = models.CharField(max_length=255, verbose_name="中文学名")
    latin_name = models.CharField(max_length=255, unique=True, verbose_name="拉丁文")
    common_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="俗名")
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.CASCADE, verbose_name="物种信息")
    aliases = models.TextField(blank=True, null=True, verbose_name="别名")
    appearance = models.TextField(blank=True, null=True, verbose_name="外貌形态")
    habits = models.TextField(blank=True, null=True, verbose_name="习性")
    distribution = models.TextField(blank=True, null=True, verbose_name="分布")
    relatives = models.TextField(blank=True, null=True, verbose_name="近亲")

    class Meta:
        db_table = "insect"
        verbose_name = "昆虫"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.latin_name


