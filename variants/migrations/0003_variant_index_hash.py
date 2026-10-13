"""Index `index` with a hash index instead of a btree.

`index` is "chr-pos-allele-allele" (e.g. 1-2387623-G-T). For a long indel the
alleles are the full sequences, so the value can run to thousands of bytes. A
btree entry must fit in 1/3 of a page, so loading a genome with a long indel
aborted the whole insert:

    OperationalError: index row size 3592 exceeds btree version 4 maximum 2704
    for index "variants_variant_index_5e0eba2e"

That truncated HG002 at 1,549,999 of 4,048,342 variants on 2026-06-15. The dev
database was patched by hand at the time with a btree on md5(index), but that
was never recorded here, so a fresh deploy still crashes.

A hash index is used rather than md5(index) because the family filters query
this column with `index__in` (filter_analysis/views.py, filter_options.py). A
functional index on md5(index) cannot serve `index IN (...)`, which would turn
the trio filters into a sequential scan over every variant. A hash index stores
only the hash, so it has no row-size limit and still serves the equality
lookups these filters issue.

The DDL is idempotent and the state change is kept separate: on the hand-patched
database the plain btree is already gone, and AlterField would introspect for an
index to drop, find none, and fail.
"""

from django.db import migrations, models

# Drop any btree index on variants_variant(index) whatever its generated name
# (the hash suffix differs between installs), including the _like companion and
# the hand-made md5 one, then add the hash index.
FORWARD_SQL = """
DO $$
DECLARE idx record;
BEGIN
    FOR idx IN
        SELECT indexname FROM pg_indexes
        WHERE tablename = 'variants_variant'
          AND (indexdef ~ 'USING btree \\(index( text_pattern_ops)?\\)'
               OR indexdef ~ 'USING btree \\(md5\\(index\\)\\)')
    LOOP
        EXECUTE format('DROP INDEX IF EXISTS %I', idx.indexname);
    END LOOP;
END $$;

CREATE INDEX IF NOT EXISTS variants_variant_index_hash
    ON variants_variant USING hash (index);
"""

REVERSE_SQL = """
DROP INDEX IF EXISTS variants_variant_index_hash;
CREATE INDEX IF NOT EXISTS variants_variant_index_5e0eba2e
    ON variants_variant USING btree (index);
"""


class Migration(migrations.Migration):

    dependencies = [
        ('variants', '0002_slim_variant_indexes'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                # Django has no hash-index field option, so the column carries
                # no db_index and migration 0003 owns the index instead.
                migrations.AlterField(
                    model_name='variant',
                    name='index',
                    field=models.TextField(),
                ),
            ],
            database_operations=[
                migrations.RunSQL(FORWARD_SQL, REVERSE_SQL),
            ],
        ),
    ]
