from individuals.tasks import _copy_first_vcf_from_tar

from django.test import TestCase

# Create your tests here.


class TarExtractionSafetyTest(TestCase):
    """A .tar.gz member must never be written to its own declared path.

    _copy_first_vcf_from_tar() copies the first regular *.vcf member through
    extractfile() rather than tar.extract(), so a member named "../evil.vcf"
    writes only to the target the caller chose. This test pins that.
    """

    def test_member_path_traversal_writes_only_to_target(self):
        import io
        import os
        import tarfile
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            tar_path = os.path.join(tmp, 'evil.tar.gz')
            payload = b'##fileformat=VCFv4.2\n'

            with tarfile.open(tar_path, 'w:gz') as tar:
                info = tarfile.TarInfo(name='../evil.vcf')
                info.size = len(payload)
                tar.addfile(info, io.BytesIO(payload))

            target_dir = os.path.join(tmp, 'out')
            os.makedirs(target_dir, exist_ok=True)
            target = os.path.join(target_dir, 'sample.vcf')

            found = _copy_first_vcf_from_tar(tar_path, target)

            self.assertTrue(found)
            with open(target, 'rb') as handle:
                self.assertEqual(handle.read(), payload)
            # The traversal path must not exist anywhere outside the target.
            self.assertFalse(os.path.exists(os.path.join(tmp, 'evil.vcf')))
            self.assertFalse(os.path.exists(os.path.join(os.path.dirname(tmp), 'evil.vcf')))
