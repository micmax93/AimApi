__author__ = 'micmax93'
from api import ApiConnection

api = ApiConnection()

print 'Liczba osob:', api.get_audience_status()

viewers = api.get_audience_details()
print 'Osoby:'
for v in viewers:
    print v.gender, v.age

print 'Live:'
api.subscribe_viewer_events(subscribe=True)

while True:
    new, viewer = api.receive_viewer_event()
    if new:
        print 'Beg:', viewer.viewer_id, viewer.gender, viewer.age
    else:
        print 'End:', viewer.viewer_id, viewer.viewing_time


