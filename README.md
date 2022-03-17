# Inflation Rate Tracker

Statistical tool to track Jamaica's monthly inflation rate dating back 10 years

## Installation

Create virtual python environment and install dependencies located in pip file

```bash
$ pipenv shell
$ pipenv install
```

Copy environment variables through .env.example and configure them

```bash
$ cp .env.example .env
```
Setting Flask app

```bash
$ export FLASK_APP=run.py
$ export FLASK_DEBUG=true # Enable debugging
```

Running Flask app

```bash
$ flask run
```

## Task Scheduling with Celery

On the 1st of every month the IRT will scrape data regarding inflation from [Bank Of Jamaica's Official Website](https://boj.org.jm/statistics/real-sector/inflation/)

Test Scheduler

```bash
$ celery -A api.worker:celery worker -l info -P gevent -E -Q default -n default
```

Using celery beat
```bash
$ celery -A api.worker.celery beat -l info
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

