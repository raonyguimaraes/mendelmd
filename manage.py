#!/usr/bin/env python
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "apps"))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mendelmd.settings")

    # Add the apps directoriy to Python's path. In production it will
    # be necessary to add the apps directory to the path, too.
    # from os.path import abspath, dirname, join
    # PROJECT_ROOT = abspath(dirname(__file__))
    # sys.path.append(join(PROJECT_ROOT, "apps"))
    

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
