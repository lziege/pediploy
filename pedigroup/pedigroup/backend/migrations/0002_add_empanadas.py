# Generated by Django 5.0.3 on 2024-04-04 18:32

from django.db import migrations


def crear_objetos(apps, schema_editor):
    Empanada = apps.get_model("backend", "Empanada")
    Empanada.clean()
    empanada1 = Empanada(type="Pollo", restaurant="Eden")
    empanada1.save()
    empanada2 = Empanada(type="Verdura", restaurant="Eden")
    empanada2.save()

class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_objetos),
    ]
