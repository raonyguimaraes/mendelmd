#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='mendelmd',
      version='1.2.4',
      packages=find_packages(),
      scripts=['bin/mendelmd'],
      include_package_data=True,
      install_requires=[
          'wheel',
          'django',
          'pysam',
          'cython',
          'wheel',
          'Django',
          'psycopg2-binary',
          'django-allauth',
          'django-debug-toolbar',
          'django-crispy-forms',
          'SOAPpy',
          'Sphinx',
          'Fabric3',
          'pysam',
          'pynnotator',
          'pyvcf',
          'celery',
          # 'django-celery',
          'django-celery-results',
          'docutils<0.15',
          'django-appconf',
          'gunicorn',
          'boto3',
          'django-formtools',
          'dj-database-url',
          'django-gravatar2',
          'pandas',
      ],
      package_data = {
            'templates': ['*']
        }
      # entry_points={  # Optional
      #         'console_scripts': [
      #             'mendelmd=mendelmd.main:main',
      #         ],
      # },
      )
