# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Rockbio (formerly MendelMD) is a Django web platform for analyzing NGS (Next-Generation Sequencing) data to identify disease-causing variants in patients with Mendelian disorders. It processes VCF files, annotates variants using multiple databases (dbSNP, ClinVar, OMIM, HGMD, etc.), and supports filtering/analysis workflows.

## Development Commands

```bash
# Local development (SQLite by default)
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py populate     # load genes/diseases reference data (run once)
python3 manage.py runserver

# Celery worker (required for background tasks - in a separate terminal)
source venv/bin/activate
python3 manage.py celery

# Docker (recommended for full stack with PostgreSQL + RabbitMQ)
docker-compose up

# Run tests
python3 manage.py test
python3 manage.py test individuals   # single app

# Database migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Collect static files
python3 manage.py collectstatic --noinput
```

## Configuration

Settings live in `rockbio/settings.py`. Local overrides go in `rockbio/local_settings.py` (gitignored). For Docker, `rockbio/local_settings_docker.py` is loaded when `USE_DOCKER=yes` is set. See `rockbio/local_settings.sample.py` for the override template.

Default development DB is SQLite (`rockbio.db`). Production uses PostgreSQL — configure via `local_settings.py`.

Stripe keys and webhook secrets are read from environment variables (`STRIPE_TEST_PUBLIC_KEY`, `STRIPE_TEST_SECRET_KEY`, `DJSTRIPE_WEBHOOK_SECRET`); test values are hardcoded as fallbacks in settings — never use these in production.

## Architecture

**Django project root:** `rockbio/` (settings, urls, celery, wsgi)

**Core data flow:**
1. User uploads a VCF file via `upload/` or `files/`
2. `individuals/` stores the patient (`Individual` model) and triggers annotation
3. `variants/` stores every annotated variant row (one `Variant` per VCF row, ~200 annotation fields)
4. `filter_analysis/` lets users build and save filter queries against variants
5. `cases/` groups individuals into family pedigrees (proband + mother/father/controls)
6. `analyses/` orchestrates multi-sample pipeline runs; `tasks/` tracks each unit of work; `workers/` manages cloud VMs (Hetzner via hcloud) that execute jobs

**Background tasks (Celery + RabbitMQ):**
- Broker: RabbitMQ (started via `service rabbitmq-server start` in Docker)
- Result backend: Django DB (`CELERY_RESULT_BACKEND = 'django-db'`)
- Task modules: `analyses/tasks.py`, `tasks/tasks.py`, `workers/tasks.py`, `individuals/tasks.py`
- Beat schedule: `workers.tasks.check_queue` runs every 30 seconds to poll for pending work

**Authentication:** django-allauth with Google OAuth social login. Login redirects to `dashboard`. Email is required; username+email login is supported.

**Payments:** dj-stripe integration. `stripeproducts/` and `settings/` apps handle subscription management. Subscription UI is at `/subscribe/`.

**Reference data apps** (mostly read-only after `populate`): `genes/`, `diseases/`, `databases/`

**Infrastructure apps**: `servers/` (cloud server management), `keys/` (SSH key storage), `workers/` (cloud worker VMs), `vms/`

**Variant annotation** is done by the external `pynnotator` library. Its settings file is copied from `configs/settings.py` at container startup.

**URL structure** mirrors app names: `/individuals/`, `/variants/`, `/cases/`, `/filter_analysis/`, `/pathway_analysis/`, `/statistics/`, `/projects/`, `/files/`, `/samples/`, `/settings/`, `/tasks/`, `/workers/`, `/analyses/`, `/keys/`, `/servers/`, `/apps/`

**Templates** are in the top-level `templates/` directory (not per-app). Base template is `templates/base.html`; dashboard layout uses `templates/base_large.html`. Auth templates are under `templates/account/` (allauth).

**Static files** are served from `static/` (source) and collected to `staticfiles/`. The app uses Bootstrap 3 + jQuery + Select2.
