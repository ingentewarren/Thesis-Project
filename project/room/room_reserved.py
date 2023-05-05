import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
from datetime import datetime, timedelta

if not firebase_admin._apps:
    # Initialize the app with a service account
    cred = credentials.Certificate('thesis-project-7aa0b-firebase-adminsdk-g64il-a24eeab54a.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://thesis-project-7aa0b-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })
def reserve_room(room_number, name, account_type, event, subject_code, time_start, time_end):
    # Check if the room is available for reservation
    room_ref = db.reference('room/' + room_number)
    room_status = room_ref.child('status').get()
    if room_status != 'available':
        print('Room is not available for reservation.')
        return

    # Convert time strings to datetime objects
    time_start = datetime.strptime(time_start, '%Y-%m-%d %H:%M:%S')
    time_end = datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S')

    # Check if the reservation time is valid
    if time_start >= time_end:
        print('Invalid reservation time.')
        return

    # Create a reservation object
    reservation = {
        'name': name,
        'account_type': account_type,
        'room_number': room_number,
        'event': event,
        'subject_code': subject_code,
        'time_start': time_start.strftime('%Y-%m-%d %H:%M:%S'),
        'time_end': time_end.strftime('%Y-%m-%d %H:%M:%S')
    }

    # Add the reservation to the reservation node
    reservation_ref = db.reference('reservation')
    reservation_key = reservation_ref.push(reservation).key

    # Update the room status to reserved
    room_ref.update({'status': 'reserved', 'reservation_key': reservation_key})

    # Schedule a job to check if the reservation time has started
    now = datetime.now()
    if time_start > now:
        schedule_time = time_start
    else:
        schedule_time = now + timedelta(seconds=1)

    job = schedule.every().day.at(schedule_time.strftime('%H:%M')).do(check_reservation_time, reservation_key)

    return reservation_key

def check_reservation_time(reservation_key):
    reservation_ref = db.reference('reservation/' + reservation_key)
    reservation = reservation_ref.get()
    time_start = datetime.strptime(reservation['time_start'], '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    if now >= time_start:
        # Move the reservation to the booked node
        booked_ref = db.reference('booked')
        booked_ref.push(reservation)
        # Delete the reservation from the reservation node
        reservation_ref.delete()
        # Update the room status to available
        room_number = reservation['room_number']
        room_ref = db.reference('room/' + room_number)
        room_ref.update({'status': 'available', 'reservation_key': ''})

room_number = '123'
name = 'John Doe'
account_type = 'Student'
event = 'Meeting'
subject_code = 'CS101'
time_start = '2022-05-01 14:00:00'
time_end = '2022-05-01 15:00:00'

reservation_key = reserve_room(room_number, name, account_type, event, subject_code, time_start, time_end)
print('Reservation successful. Reservation key:', reservation_key)