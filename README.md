# Glasshouse
Regulary scraping the property listings from https://www.century21global.com/.
Data then displayed in tables and allows more filters than original website.

## Description

Displays the quick summary of listed houses with additional filters.
Keeps the history of sold houses to help identify the best value for money.
Track price history of each property to assist with price negotiation.

TODO: Send notification when new house with matching criterias was listed.
TODO: Compare housing prices from other agency in the same area.

## Getting Started

### Dependencies

* Docker, Docker-compose, Python 3.8, Django 4.0.5

### Installation
In Docker containers (Recommended):
* Clone the repo
* Run "docker-compose built -d"

Note: Docker-compose mounts .glasshouse as bind mount. So any changes made to container are updated inside the source code as well

In VM:
* Clone the repo
* Install the requirements.txt

* Start celery worker
```
celery -A glasshouse worker --loglevel=DEBUG -EB
```

* Start celery beat. Add schedules in django/admin to Celery beat DB
```
 celery -A glasshouse beat -l info --scheduler
```

* TODO: add Redis manual setup steps 

### Executing program

* Total 4 containers should be running
* docker ps
* Creating celery scheduled task with Django Admin
TODO: Step-by-step bullets with output sample
```
code blocks for commands
```

## Troubleshooting

1. Container failed to start
2. Django URL doesn't load
3. Celery to Redis connection

TODO: terminal output sample
```
command to run if program contains helper info
```

## Authors


## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License
TODO: add LICENCE.md 

## Acknowledgments
To Internet
