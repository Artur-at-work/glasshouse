# Glasshouse

Regulary scraping the property listings from https://www.century21global.com/ 
Data then displayed in tables and allows more filters than original website.

## Description

Displays the quick summary of listed houses with additional filters.
Keeps the history of sold houses to help identify the best value for money.
Track price history of each property to assist with price negotiation.

TODO: Send notification when new house with matching criterias was listed.
TODO: Compare housing prices from other agency in the same area.

## Getting Started

### Installation in Containers (Recommended):
* Clone the repo
```
sudo git clone https://github.com/Artur-at-work/glasshouse.git
```
* Build and start the containers
```
sudo docker-compose build
sudo docker-compose up
```
Note:
1. celery-beat container may fail to start since the schedule is empty. We’re going to address this problem in later steps
2. Docker-compose mounts .glasshouse as bind mount. So any changes made to container are updated inside the source code as well

* Create Admin user for database
- Connect to glasshouse_web container to create Django administrative user
```
docker exec -it $YOUR_CONTAINER_ID bash

root@16d5445a8026:/usr/src/app# python manage.py createsuperuser
Username (leave blank to use 'root'): admin
Email address: 
Password:
```
- Login to http://localhost:8000/admin with newly created admin user

* Create Periodic Task for Celery-beat

- "PERIODIC TASKS – Periodic Tasks – Add"
- Restart containers. This time celery-beat container must start
```
docker-compose down
docker-compose up
```
- Verify your shcedule task is executed in logs
```
celery-beat_1  | [2022-09-20 18:01:00,021: INFO/MainProcess] Scheduler: Sending due task hourly scrape price test (scrape.tasks.archive_prices)
```

* Manual scraping
During first time installation (or debugging) it’s recommended to verify scraping manually before creating the automated celery-beat task.

- Go to http://localhost:8000/scrape and press "Scrape Houses"
It must start scraping the website and may take around 15 min.

- Press “Generate Cities and Districts”
It will extract distinct City and District names from the scraped houses table and store into separate table. Those records are used to populate the drop-down menu

- Go to http://localhost:8000 to see the scraped results (or refresh the page)
## Installation In VM:

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
```
code blocks for commands
```

## Troubleshooting

1. Container failed to start
2. Django URL doesn't load
3. Celery to Redis connection

TODO: terminal output sample
```
command
```

## Version History

* 0.1
    * Initial Release

<!-- ## License

This project is licensed under the MIT License -->
