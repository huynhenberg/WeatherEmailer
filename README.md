# Weather Emailer

By [Dan Huynh](mailto:danhuynh@protonmail.com)

## Prerequisites

Python 3.7
Django 2.1
[requests 2.20](https://github.com/requests/requests)

## Instructions

1. Navigate to [repo](https://github.com/huynhenberg/weather-emailer)
2. Clone locally using
   `git clone https://github.com:huynhenberg/weather-emailer.git`
3. Start your server using `python manage.py runserver`
4. Navigate to the app in [browser](http://127.0.0.1:8000/subscribe/)
5. Use the [admin interface](http://127.0.0.1:8000/admin/) to send emails
   Username `admin`
   Password `admin`
6. Enjoy!

## Requirements

#### Create a newsletter sign up page that allows someone to enter their
#### email address and choose their location from a list of top 100 cities in
#### US by population.

I used a form created by [Ally Reid](https://foundation.zurb.com/building-blocks/blocks/simple-subscription-form.html). The top 100 cities are taken from Wikipedia and constructed into `/base/load_cities.py` using regular expressions.

#### Create a Django management command to send a personalized email to each
#### email address in the list. For each recipient, fetch the current weather
#### for that recipient's location and compare that to historical weather.

I chose to fetch weather data from `https://www.worldweatheronline.com`
I also added `activation_date` and `active` properties for the users. These
can be useful for historical data.
