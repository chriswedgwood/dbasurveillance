from django.core.management.base import BaseCommand, CommandError
from dbasurveillance.sqlreports.models import Van, Appointment
from dbasurveillance.users.models import User
import environ
import csv
import json
import pprint
import datetime

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        print(environ.Path(__file__))
        incoming = environ.Path(__file__) - 3
        van_json = str(incoming.path('incoming').path('moversno_movers67_table_movers_van.json'))
        booking_json = str(incoming.path('incoming').path('moversno_movers67_table_movers_booking.json'))
        user_json = str(incoming.path('incoming').path('moversno_movers67_table_movers_user.json'))
        with open(van_json) as json_data:
            vans = json.load(json_data)
            for van in vans['data']:
                print(van['van_id'])
                p, created = Van.objects.update_or_create(id=van['van_id'],title=van['van_name'],
                                                          status=van['van_status'])
                p.created = van['van_dateadded']
                p.save()

        with open(user_json) as json_data:
            users = json.load(json_data)
            for user in users['data']:
                pprint.pprint(user)
                p, created = User.objects.update_or_create(id=user['user_id'], username=user['user_uname'])
                p.set_password(str(user['user_pwd']))
                p.name = user['user_uname']
                p.is_staff = True
                p.first_name = user['user_uname']
                if p.username == 'admin':
                    p.first_name = 'Michael'
                    p.is_superuser = True
                if p.username == 'Clinton':
                    p.is_superuser = True
                p.save()

        with open(booking_json) as json_data:
            bookings = json.load(json_data)
            for booking in bookings['data']:
                pprint.pprint(booking)
                a, created = Appointment.objects.update_or_create(id=booking['booking_id'])
                try:
                    user = User.objects.get(first_name=booking['booking_addedby'])
                except user.DoesNotExist:
                    user = User.objects.get(first_name='Michael')
                a.booked_by = user
                if booking['booking_time'] != '':
                    a.time = booking['booking_time']
                a.name = booking['booking_name']
                a.collection_address = booking['booking_collectionaddr']
                a.delivery_address = booking['booking_deliveryaddr']
                a.storage = booking['booking_storage']
                a.description = booking['booking_description']
                a.porters = booking['booking_porters']
                a.van = Van.objects.get(id=booking['booking_vanid'])
                a.phone = booking['booking_phone']
                a.date = datetime.date(int(booking['booking_year']),int(booking['booking_month']),int(booking['booking_day']))
                a.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported van'))
