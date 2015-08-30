__author__ = 'micmax93'
from api import ApiConnection
from player import SinglePlayer


api = ApiConnection(host='25.152.172.38')
player = SinglePlayer()

while True:
    viewers = api.get_audience_details()
    # TODO
    player.set_next('path')
    player.wait()


