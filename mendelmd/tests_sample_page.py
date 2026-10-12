"""The sample page pages through the parquet file without loading it all."""
import os
import shutil
import tempfile

import pandas as pd
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from individuals.models import Individual


class SamplePageTests(TestCase):
    def setUp(self):
        self.base = tempfile.mkdtemp()
        self.user = get_user_model().objects.create_user("sp", "sp@example.com", "pw-sp-123")
        self.ind = Individual.objects.create(name="big", user=self.user)
        folder = os.path.join(self.base, "genomes", "sp", str(self.ind.id), "ann_sample")
        os.makedirs(folder)
        n = 12000
        pd.DataFrame({
            "CHROM": ["chr1" if i < 7000 else "chr2" for i in range(n)],
            "POS": list(range(n)),
            "ID": ["." if i % 4 == 0 else "rs%d" % i for i in range(n)],
            "REF": ["A"] * n, "ALT": ["G"] * n, "QUAL": ["50"] * n, "FILTER": ["PASS"] * n,
            "VARTYPE": ["SNP"] * n, "SYMBOL": ["G%d" % i for i in range(n)], "HET": ["1"] * n,
        }).to_parquet(os.path.join(folder, "annotation.final.parquet"))
        self.client.force_login(self.user)

    def tearDown(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def get(self, page):
        with override_settings(BASE_DIR=self.base):
            return self.client.get("/individuals/view/%s/" % self.ind.id, {"page": page})

    def test_counts_and_pages(self):
        r = self.get(1)
        self.assertEqual(r.status_code, 200)
        ind = r.context["individual"]
        self.assertEqual(ind.n_variants, 12000)
        self.assertEqual(ind.novel_variants, 3000)
        self.assertEqual(ind.chromossome, [{"chr": "chr1", "total": 7000}, {"chr": "chr2", "total": 5000}])
        page = r.context["variants"]
        self.assertEqual(page.paginator.num_pages, 240)
        self.assertEqual([row["POS"] for row in page][:2], [0, 1])
        self.assertNotIn("HET", r.context["parquet_columns"])
        # Page 100 spans rows 4950-4999 (inside the first 5000-row batch); page 101 crosses into the second.
        self.assertEqual([row["POS"] for row in self.get(100).context["variants"]], list(range(4950, 5000)))
        self.assertEqual([row["POS"] for row in self.get(101).context["variants"]], list(range(5000, 5050)))
        last = self.get(240).context["variants"]
        self.assertEqual([row["POS"] for row in last][-1], 11999)
