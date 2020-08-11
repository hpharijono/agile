# Screening Task

Sample project that exposes the 4 values and 12 principles of Agile Software Development (https://agilemanifesto.org/).

## Setup

### Cloning the repository

```
git clone https://github.com/RemiBesnard/django-screening.git
```

### Install packages

```
pipenv install --dev
```

### Load dumped data

```
pipenv run python manage.py loaddata agile/fixtures/fixtures.json
```

A default admin user has been created:

- **Username**: admin
- **Password**: admin

### Running the server

```
pipenv run python manage.py runserver
```

### Test everything

```
bash format_and_check.sh
```
