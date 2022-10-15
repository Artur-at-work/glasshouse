# Glasshouse

Regulary scraping the property listings from https://www.century21global.com/<br>
Data then displayed in tables and allows more filters than original website.

## Description

Displays the quick summary of listed houses with additional filters.<br>
Keeps the history of sold houses to help identify the best value for money.<br>
Track price history of each property to assist with price negotiation.<br>
<br>
TODO: Send notification when new house with matching criterias was listed.<br>
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

### Setup the access and databases:

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
![image](https://user-images.githubusercontent.com/40683252/195998208-1617648f-cd79-4d49-8b4b-baafac0fd80a.png)
- Restart containers. This time celery-beat container must start
```
docker-compose down
docker-compose up
```
- Verify your shcedule task is executed in logs
```
celery-beat_1  | [2022-09-20 18:01:00,021: INFO/MainProcess] Scheduler: Sending due task hourly scrape price test (scrape.tasks.archive_prices)
```

* Manual scraping<br>
During first time installation (or debugging) it’s recommended to verify scraping manually before creating the automated celery-beat task.

- Go to http://localhost:8000/scrape and press "Scrape Houses"<br>
It must start scraping the website and may take around 15 min.

![image](https://user-images.githubusercontent.com/40683252/195998482-9eff534f-d4e7-4edc-b023-8e28623c2959.png)

- Press “Generate Cities and Districts”<br>
It will extract distinct City and District names from the scraped houses table and store into separate table. Those records are used to populate the drop-down menu

- Go to http://localhost:8000 to see the scraped results (or refresh the page)
![image](https://user-images.githubusercontent.com/40683252/195998329-d832b74f-219e-412a-8007-d174bd24cd8e.png)

### Interface:
* Home Page<br>
Scraping results are listed in one main table. 
Use dropdown menus to filter by city.
Press column headers to sort by that category from lowest to highest or vice versa.

* Sold House<br>
Keeps the history of houses that were sold.
House considered sold after it’s listing has disappeared from the agency’s website.
By default, the syncronization is done daily at 10am.

* Price History<br>
Saves the price of each house regularly and shows the price change over the time period. Straight line represents that price did not change during that time period. Houses are saved by internal listing ID which is used by the agency itself. This is the closest to unique primary key, which unlikely to change.
ID can be pasted to Search window to find the exact listing, address and other information.

![image](https://user-images.githubusercontent.com/40683252/195999237-ba5f1b96-d96f-4f74-a514-702b608cf6eb.png)

TODO: current implementation takes time to load all the records. Need to display by specific house/area

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

## Troubleshooting

1. Container failed to start<br>
- Refer to "Setup the access and databases" step for celery_beat container setup.

2. Django URL doesn't load<br>
- By default, all URLs are allowed in settings.py
```
ALLOWED_HOSTS = ['*']
```
Verify wildcard is still there, or specify your own URL

3. Celery to Redis connection

TODO: terminal output sample and redis debug commands
```
command
```

## Version History

* 0.1
    * Initial Release

<!-- ## License

This project is licensed under the MIT License -->
