# Mendel,MD

[![BSD License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Django](https://img.shields.io/badge/Django-powered-092E20.svg)](https://www.djangoproject.com)

Mendel,MD is an open-source web tool for annotating, filtering and diagnosing patients with Mendelian disorders from whole-exome (WES) and whole-genome (WGS) sequencing data. It is built for clinicians, researchers and bioinformaticians who need to go from a VCF to a short list of candidate variants without writing code.

Live instance: **https://mendelmd.org**

Annotation is handled by [Pynnotator](https://github.com/raonyguimaraes/pynnotator), the VEP-centric annotation framework developed alongside Mendel,MD.

## Features

- Upload VCFs from exomes or genomes and annotate them automatically
- Filter variants by frequency, predicted impact, inheritance model, gene lists and clinical databases
- Family and cohort analyses across multiple individuals
- Gene, disease and pathway views for candidate prioritisation
- Background processing with Celery so large genomes do not block the UI

## Quick start with Docker

```bash
git clone https://github.com/raonyguimaraes/mendelmd
cd mendelmd
docker-compose up
```

## Development setup

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
./manage.py migrate
./manage.py runserver
```

In a second terminal, start the background worker:

```bash
source venv/bin/activate
./manage.py celery
```

## Deployment

A deployment script for Ubuntu 22.04 LTS is included:

```bash
wget https://raw.githubusercontent.com/raonyguimaraes/mendelmd/master/scripts/deployment_ubuntu_22.04_LTS.sh
bash deployment_ubuntu_22.04_LTS.sh
```

Scripts for other distributions live in [`scripts/`](scripts/).

## History

Mendel,MD was developed during a PhD at UFMG (Brazil) and first published in 2015. Between 2017 and 2024 the codebase was extended under the name Rockbio ([rockbio/rockbio](https://github.com/rockbio/rockbio)); in 2026 it was rebranded back to Mendel,MD, which is the actively maintained version in this repository.

## Citing

- Cardenas RGCCL, Linhares ND, Ferreira RL, Pena SDJ. *Mendel,MD: A user-friendly open-source web tool for analyzing WES and WGS in the diagnosis of patients with Mendelian disorders.* PLOS Computational Biology, 2017. https://doi.org/10.1371/journal.pcbi.1005520
- Guimarães R, et al. *Mendel,MD: a user-friendly online program for clinical exome analysis.* BMC Bioinformatics, 2015. https://doi.org/10.1186/1471-2105-16-S8-A2
- Coverage in [GenomeWeb](https://www.genomeweb.com/informatics/software-tool-aims-easy-quick-mendelian-disease-diagnoses-genome-data), January 2017.

## License

BSD 3-Clause. See [LICENSE](LICENSE).
