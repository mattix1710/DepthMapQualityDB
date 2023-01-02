# Generated by Django 4.1.4 on 2023-01-02 17:20

import depthQualifier.models
import depthQualifier.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MethodProposal',
            fields=[
                ('method_id', models.AutoField(primary_key=True, serialize=False)),
                ('method_name', models.CharField(max_length=30, unique=True, validators=[depthQualifier.models.validate_method_name_exist, depthQualifier.models.validate_method_name_correct])),
                ('desc', models.TextField()),
                ('upload_date', models.DateField(auto_now=True)),
                ('src', models.FileField(upload_to=depthQualifier.models.method_location, validators=[depthQualifier.validators.validate_archive_method])),
            ],
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('seq_id', models.AutoField(primary_key=True, serialize=False)),
                ('seq_name', models.CharField(max_length=30, unique=True, validators=[depthQualifier.models.validate_sequence_name_exist, depthQualifier.models.validate_sequence_name_correct])),
                ('seq_src', models.FileField(upload_to=depthQualifier.models.sequence_location, validators=[depthQualifier.validators.validate_archive_sequence])),
            ],
        ),
        migrations.CreateModel(
            name='SeqDepthResults',
            fields=[
                ('result_id', models.AutoField(primary_key=True, serialize=False)),
                ('synth_PSNR_1018', models.FloatField(null=True)),
                ('synth_bitrate_1018', models.FloatField(null=True)),
                ('synth_PSNR_3042', models.FloatField(null=True)),
                ('synth_bitrate_3042', models.FloatField(null=True)),
                ('synth_PSNR_none', models.FloatField(null=True)),
                ('synth_bitrate_none', models.FloatField(null=True)),
                ('method_id', models.ForeignKey(db_column='method_id', on_delete=django.db.models.deletion.CASCADE, to='depthQualifier.methodproposal')),
                ('seq_id', models.ForeignKey(db_column='seq_id', on_delete=django.db.models.deletion.PROTECT, to='depthQualifier.sequence')),
            ],
        ),
    ]
