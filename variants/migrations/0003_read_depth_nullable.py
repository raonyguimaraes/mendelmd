from django.db import migrations, models


class Migration(migrations.Migration):
    """Array genotypes have no DP or QUAL; store NULL instead of 0 so the
    depth and QUAL filters can keep them instead of dropping every row."""

    dependencies = [
        ('variants', '0002_slim_variant_indexes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variant',
            name='read_depth',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='qual',
            field=models.FloatField(blank=True, null=True),
        ),
        # Rows loaded without a DP field (GT-only array data) were stored as 0/0.0.
        migrations.RunSQL(
            "UPDATE variants_variant SET read_depth = NULL, qual = NULL "
            "WHERE read_depth = 0 AND qual = 0 AND (format IS NULL OR format NOT LIKE '%%DP%%')",
            migrations.RunSQL.noop,
        ),
    ]
