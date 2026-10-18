from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from files.tasks import _parse_content_length, check_file


class ParseContentLengthTest(SimpleTestCase):
    """The header parsing that replaced 'grep Content-Length'."""

    def test_finds_header(self):
        headers = 'HTTP/1.1 200 OK\r\nContent-Length: 1234\r\n'
        self.assertEqual(_parse_content_length(headers), '1234')

    def test_is_case_insensitive(self):
        headers = 'HTTP/1.1 200 OK\r\ncontent-length: 42\r\n'
        self.assertEqual(_parse_content_length(headers), '42')

    def test_missing_header_returns_none(self):
        self.assertIsNone(_parse_content_length('HTTP/1.1 200 OK\r\n'))

    def test_empty_returns_none(self):
        self.assertIsNone(_parse_content_length(''))
        self.assertIsNone(_parse_content_length(None))


class CheckFileUsesArgvTest(SimpleTestCase):
    """check_file() must never build a shell string.

    File.location is an editable model field, so it is attacker-controlled
    data. These tests assert the argv shape and that no shell kwarg is used.
    """

    def _run(self, location, stdout=''):
        task = MagicMock()
        task.manifest = {'file': 2}
        file_obj = MagicMock()
        file_obj.location = location

        with patch('files.tasks.Task.objects.get', return_value=task), \
             patch('files.tasks.File.objects.get', return_value=file_obj), \
             patch('files.tasks.subprocess.run') as run:
            run.return_value = MagicMock(stdout=stdout, returncode=0)
            check_file(1)
        return file_obj, run

    def test_ftp_uses_argv_and_no_shell(self):
        location = 'ftp://example.org/pub/data.vcf'
        file_obj, run = self._run(
            location, 'HTTP/1.1 200 OK\r\nContent-Length: 99\r\n')

        self.assertEqual(run.call_args[0][0], ['curl', '-sI', location])
        self.assertNotIn('shell', run.call_args[1])
        self.assertEqual(file_obj.size, 99)

    def test_ftp_without_content_length_raises(self):
        with self.assertRaises(ValueError):
            self._run('ftp://example.org/pub/data.vcf', 'HTTP/1.1 200 OK\r\n')

    def test_local_path_uses_argv_and_no_shell(self):
        location = '/data/genomes/na12878/sample.vcf'
        _, run = self._run(location, '')

        called = [call[0][0] for call in run.call_args_list]
        self.assertIn(['ls', '-lah', '/data/genomes/na12878'], called)
        self.assertIn(['file', location], called)
        for call in run.call_args_list:
            self.assertNotIn('shell', call[1])

    def test_injection_payload_is_a_single_argv_element(self):
        # Would be command injection with shell=True; as argv it is just text.
        location = 'ftp://example.org/; touch /tmp/pwned; #'
        _, run = self._run(
            location, 'HTTP/1.1 200 OK\r\nContent-Length: 1\r\n')

        self.assertEqual(run.call_args[0][0], ['curl', '-sI', location])
        self.assertNotIn('shell', run.call_args[1])
