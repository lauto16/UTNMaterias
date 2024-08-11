# Generated by Django 5.0.6 on 2024-08-11 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainTree', '0007_utnsubjectcivil_utnsubjectelectrica_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utnsubjectcivil',
            name='approval_children',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectcivil',
            name='approval_fathers',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectcivil',
            name='regular_children',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectcivil',
            name='regular_fathers',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectelectrica',
            name='approval_children',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectelectrica',
            name='approval_fathers',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectelectrica',
            name='regular_children',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectelectrica',
            name='regular_fathers',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectelectronica',
            name='approval_children',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectelectronica',
            name='approval_fathers',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectelectronica',
            name='regular_children',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectelectronica',
            name='regular_fathers',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectindustrial',
            name='approval_children',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectindustrial',
            name='approval_fathers',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectindustrial',
            name='regular_children',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectindustrial',
            name='regular_fathers',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectmecanica',
            name='approval_children',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectmecanica',
            name='approval_fathers',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectmecanica',
            name='regular_children',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectmecanica',
            name='regular_fathers',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectmetalurgica',
            name='approval_children',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectmetalurgica',
            name='approval_fathers',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectmetalurgica',
            name='regular_children',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectmetalurgica',
            name='regular_fathers',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectquimica',
            name='approval_children',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectquimica',
            name='approval_fathers',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectquimica',
            name='regular_children',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectquimica',
            name='regular_fathers',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectsistemas',
            name='approval_children',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectsistemas',
            name='approval_fathers',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectsistemas',
            name='regular_children',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='utnsubjectsistemas',
            name='regular_fathers',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
