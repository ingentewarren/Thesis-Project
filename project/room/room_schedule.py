import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime

if not firebase_admin._apps:
    # Initialize the app with a service account
    cred = credentials.Certificate('D:/DOWNLOADS/thesismobileapp-304b0-firebase-adminsdk-2eufd-4703063921.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://thesismobileapp-304b0-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

def is_schedule():
    ref = db.reference('Room')
    rooms_snapshot = ref.get()

    if not rooms_snapshot:
        print("Error: Unable to retrieve rooms data from the database")
        return

    if not isinstance(rooms_snapshot, dict):
        print("Error: Rooms data is not in the expected format")
        return

    now = datetime.datetime.now()
    for room_id, room_data in rooms_snapshot.items():
        if not isinstance(room_data, dict):
            print(f"Error: Room data for room {room_id} is not in the expected format")
            continue
        schedule_ref = ref.child(room_id).child('Schedule')
        schedule_snapshot = schedule_ref.get()
        if not schedule_snapshot:
            continue
        for schedule_id, schedule_data in schedule_snapshot.items():
            if not isinstance(schedule_data, dict):
                print(f"Error: Schedule data for schedule {schedule_id} in room {room_id} is not in the expected format")
                continue
            start_time = datetime.datetime.strptime(schedule_data.get('Start Time', ''), '%H:%M')
            end_time = datetime.datetime.strptime(schedule_data.get('End Time', ''), '%H:%M')
            if start_time.time() <= now.time() <= end_time.time():
                room_ref = ref.child(room_id)
                room_ref.update({
                    'Availability': False,
                    'Occupant': schedule_data.get('Occupant', ''),
                    'Schedule': schedule_data
                })
                break
            else:
                room_ref = ref.child(room_id)
                room_ref.update({
                    'Availability': True,
                    'Occupant': '',
                    'Schedule': {}
                })