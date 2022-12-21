# Generated by Django 4.1.1 on 2022-11-22 12:58

import depthQualifier.models
import depthQualifier.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('depthQualifier', '0003_sequencemodel_quality'),
    ]

    operations = [
        migrations.CreateModel(
            name='MethodProposal',
            fields=[
                ('method_id', models.AutoField(primary_key=True, serialize=False)),
                ('method_name', models.CharField(max_length=30, unique=True, validators=[depthQualifier.models.validate_method_name_exist, depthQualifier.models.validate_method_name_correct])),
                ('desc', models.TextField()),
                ('upload_date', models.DateField()),
                ('src', models.FileField(upload_to=depthQualifier.models.method_location, validators=[depthQualifier.validators.validate_archive_extension])),
            ],
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('seq_id', models.AutoField(primary_key=True, serialize=False)),
                ('seq_name', models.CharField(max_length=30, unique=True, validators=[depthQualifier.models.validate_sequence_name_exist, depthQualifier.models.validate_sequence_name_correct])),
                ('seq_src', models.FileField(upload_to=depthQualifier.models.seq1_location, validators=[depthQualifier.validators.validate_archive_extension])),
            ],
        ),
        migrations.CreateModel(
            name='SeqDepthResults',
            fields=[
                ('depth_id', models.AutoField(primary_key=True, serialize=False)),
                ('synth_PSNR_1018', models.FloatField(null=True)),
                ('synth_bitrate_1018', models.FloatField(null=True)),
                ('synth_PSNR_3042', models.FloatField(null=True)),
                ('synth_bitrate_3042', models.FloatField(null=True)),
                ('synth_PSNR_none', models.FloatField(null=True)),
                ('synth_bitrate_none', models.FloatField(null=True)),
                ('method_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depthQualifier.methodproposal')),
                ('seq_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='depthQualifier.sequence')),
            ],
        ),
    ]