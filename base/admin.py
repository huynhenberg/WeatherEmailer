import requests
import traceback

from datetime import date

from django.contrib import admin
from django.core.mail import send_mass_mail

from .models import Locale, User


WEATHER_API_KEY = 'ea30cfe95f0647be97a41421181411'

WEATHER_URL = 'https://api.worldweatheronline.com/premium/v1/weather.ashx'

EMAIL_FROM = 'weatheremailer@gmail.com'
SUBJECT_GOOD = 'It\'s nice out! Enjoy a discount on us.'
SUBJECT_BAD = 'Not so nice out? That\'s okay, enjoy a discount on us.'
SUBJECT_NEUTRAL = 'Enjoy a discount on us.'

# Weather codes returned by the api.
WEATHER_CODES_SUNNY = ['113', '116']
WEATHER_CODES_NONPREC = ['113', '116', '119', '122']


class UserAdmin(admin.ModelAdmin):
    fields = [
        'email',
        'locale_id',
        'active'
    ]
    list_display = [
        'email',
        'locale_id',
        'active',
        'activation_datetime'
    ]
    actions = ['send_emails_to_users']

    def log_error(self, err):
        print(''.join(traceback.format_exception(etype=type(err), value=err, tb=err.__traceback__)))

    # Get current weather along with the climate average
    def get_weather(self, locale):
        city=[locale.city.replace(' ', '+'), ',', locale.state_province_code]
        url = [
            WEATHER_URL,
            '?q=', ''.join(city),
            #'&num_of_days=1',
            '&fx=no',
            '&mca=yes',
            '&format=json',
            '&key=', WEATHER_API_KEY,
        ]
        weather = None
        try:
            weather = requests.get(''.join(url))
            weather = weather.json()
        except (requests.ConnectionError, requests.Timeout, ValueError, AttributeError) as err:
            self.log_error(err)
        return weather

    def is_good_weather(self, temp, avg_temp, code):
        return temp - avg_temp >= 5 or code in WEATHER_CODES_SUNNY

    def is_bad_weather(self, temp, avg_temp, code):
        return temp - avg_temp <= -5 or code not in WEATHER_CODES_NONPREC

    # Create message tuple for use in send_mass_mail
    def get_message_tuple(self, user):
        temp, avg_temp, weather_code, weather_desc = None, None, None, None
        try:
            weather = self.get_weather(user.locale_id)
            weather = weather['data']
            temp = weather['current_condition'][0]['temp_F']
            weather_code = weather['current_condition'][0]['weatherCode']
            weather_desc = weather['current_condition'][0]['weatherDesc'][0]['value']
            month = date.today().strftime('%m').replace('0','')
            month = int(month)
            avg_temp = weather['ClimateAverages'][0]['month'][month]['avgMinTemp_F']
        except (KeyError, TypeError) as err:
            self.log_error(err)

        # Generate the subject
        subject = SUBJECT_NEUTRAL
        if self.is_good_weather(float(temp), float(avg_temp), weather_code):
            subject = SUBJECT_GOOD
        elif self.is_bad_weather(float(temp), float(avg_temp), weather_code):
            subject = SUBJECT_BAD

        # Generate the message
        message = [
            user.locale_id.__str__(),
            '. ',
            temp,
            ' degrees, ',
            weather_desc,
            '.'
        ]

        return (subject, ''.join(message), EMAIL_FROM, [user.email])
        
    # Send an email to all selected users that are active
    def send_emails_to_users(self, request, queryset):
        message_list = list()
        good_recip = list()
        for obj in queryset:
            if obj.active:
                datatuple = self.get_message_tuple(obj)
                message_list.append(datatuple)         

        send_mass_mail(tuple(message_list), fail_silently=False)
    send_emails_to_users.short_description = 'Send discount email to selected users'


admin.site.register(Locale)
admin.site.register(User, UserAdmin)
