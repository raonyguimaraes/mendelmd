"""Family (trio) inheritance filters and cross-user isolation of filter helpers."""
from django.contrib.auth import get_user_model
from django.test import TestCase

from individuals.models import Individual
from individuals.populate import parse_line
from variants.models import Variant

CSQ = ["Allele", "Consequence", "IMPACT", "SYMBOL"]


def add(ind, chrom, pos, gt, gene, ref="A", alt="G"):
    line = "%s\t%s\t.\t%s\t%s\t50\tPASS\tCSQ=%s|missense_variant|MODERATE|%s\tGT:DP\t%s:30\n" % (
        chrom, pos, ref, alt, alt, gene, gt)
    Variant.objects.create(individual=ind, **parse_line(line, CSQ))


class TrioInheritanceTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("trio", "t@example.com", "pw-trio-123")
        mk = lambda n: Individual.objects.create(name=n, user=self.user)
        self.child, self.father, self.mother = mk("child"), mk("father"), mk("mother")
        # Recessive: both parents carriers, child homozygous.
        add(self.father, "1", 100, "0/1", "RECGENE"); add(self.mother, "1", 100, "0/1", "RECGENE")
        add(self.child, "1", 100, "1/1", "RECGENE")
        # Same genotype as a parent: not recessive, not de novo.
        add(self.father, "1", 200, "1/1", "SHARED"); add(self.child, "1", 200, "1/1", "SHARED")
        # De novo: absent from both parents.
        add(self.child, "1", 300, "0/1", "DENOVO")
        # Compound heterozygous: one hit from each parent in the same gene.
        add(self.father, "2", 400, "0/1", "COMPHET"); add(self.child, "2", 400, "0/1", "COMPHET")
        add(self.mother, "2", 410, "0/1", "COMPHET"); add(self.child, "2", 410, "0/1", "COMPHET")
        # Two hits from the father only: not compound heterozygous.
        add(self.father, "3", 500, "0/1", "FATHERONLY"); add(self.child, "3", 500, "0/1", "FATHERONLY")
        add(self.father, "3", 510, "0/1", "FATHERONLY"); add(self.child, "3", 510, "0/1", "FATHERONLY")
        self.client.force_login(self.user)

    def genes(self, option):
        r = self.client.get("/filter_analysis/family_analysis/", {
            "children": self.child.id, "father": self.father.id, "mother": self.mother.id,
            "inheritance_option": option})
        self.assertEqual(r.status_code, 200)
        return sorted({v.gene for v in r.context["variants"]})

    def test_recessive_keeps_child_genotypes_not_seen_in_parents(self):
        self.assertIn("RECGENE", self.genes("recessive"))
        self.assertNotIn("SHARED", self.genes("recessive"))

    def test_dominant_option_returns_de_novo_positions(self):
        self.assertEqual(self.genes("dominant"), ["DENOVO"])

    def test_compound_heterozygous(self):
        self.assertEqual(self.genes("compound heterozygous"), ["COMPHET"])


class FilterHelperIsolationTests(TestCase):
    """Excluding or grouping another user's samples must not change your results."""

    def setUp(self):
        User = get_user_model()
        self.alice = User.objects.create_user("alice", "a@example.com", "pw-alice-123")
        self.bob = User.objects.create_user("bob", "b@example.com", "pw-bob-123")
        self.alice_ind = Individual.objects.create(name="alice-s", user=self.alice)
        self.bob_ind = Individual.objects.create(name="bob-s", user=self.bob)
        add(self.alice_ind, "1", 100, "0/1", "PRIVATE")
        add(self.bob_ind, "1", 100, "0/1", "PRIVATE")
        add(self.bob_ind, "1", 900, "0/1", "OTHER")

    def bob_genes(self, **params):
        self.client.force_login(self.bob)
        r = self.client.get("/filter_analysis/", dict(params, individuals=self.bob_ind.id))
        return sorted(v.gene for v in r.context["variants"])

    def test_excluding_another_users_sample_is_ignored(self):
        self.assertEqual(self.bob_genes(), ["OTHER", "PRIVATE"])
        self.assertEqual(self.bob_genes(exclude_individuals=self.alice_ind.id), ["OTHER", "PRIVATE"])

    def test_genes_in_common_ignores_another_users_sample(self):
        self.client.force_login(self.bob)
        r = self.client.get("/filter_analysis/", {"individuals": [self.bob_ind.id, self.alice_ind.id],
                                                  "genes_in_common": "on"})
        self.assertEqual(sorted(v.gene for v in r.context["variants"]), [])
