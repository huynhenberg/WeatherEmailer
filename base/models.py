from django.db import models


# Holds top 100 cities in USA.
# The length of these fields are limited according to USPS standards.
# We may want to allow the use of postal codes in the future.
# We may also want to add a country code in order to represent cities outside of
# the USA.
class Locale(models.Model):
    city = models.CharField(max_length=28)
    state_province_code = models.CharField(max_length=2)

    def __str__(self):
        return '{0}, {1}'.format(self.city, self.state_province_code)


    class Meta:
        unique_together = (
            'city',
            'state_province_code',
        )


# I chose not to extend the existing Django classes since this is more of a list
# of subscribed users as opposed to users requiring a password.
class User(models.Model):
    email = models.EmailField(primary_key=True, max_length=100)
    locale_id = models.ForeignKey(Locale, on_delete=models.PROTECT)
    active = models.BooleanField()
    activation_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
