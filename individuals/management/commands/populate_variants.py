from django.core.management.base import BaseCommand

from individuals.models import Individual
from individuals.tasks import PopulateVariants, annotated_vcf_path


class Command(BaseCommand):
    help = "Load annotated VCFs into the variants table (runs synchronously)."

    def add_arguments(self, parser):
        parser.add_argument("ids", nargs="*", type=int, help="Individual ids")
        parser.add_argument("--all-annotated", action="store_true",
                            help="Every individual with status 'annotated' or 'populated' that has an annotated VCF")
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, ids, all_annotated, dry_run, **options):
        qs = Individual.objects.order_by("id")
        if all_annotated:
            qs = qs.filter(status__in=["annotated", "populated"])
        elif ids:
            qs = qs.filter(id__in=ids)
        else:
            self.stderr.write("Give individual ids or --all-annotated")
            return
        for individual in qs:
            path = annotated_vcf_path(individual)
            if path is None:
                self.stdout.write("%s skipped: no annotated VCF" % individual.id)
                continue
            if dry_run:
                self.stdout.write("%s would load %s" % (individual.id, path))
                continue
            count = PopulateVariants(individual.id)
            self.stdout.write("%s loaded %s variants" % (individual.id, count))
