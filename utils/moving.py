import requests
from urllib.parse import urlencode

def move(url, channel, character):
    print(character["session"])
   #room_data = requests.get(f"{url}ajax_changeroomb.php?suid={character["character_id"]}&serverid={character["server_id"]}&rg_sess_id={charcter["session"]}&code=1")
   #print(room_data.json())
   #current_room = room_data.split('"curRoom"')[1].split(',')[0].split('"')[1]
   #print(current_room)

def north(url, channel, character, room_data, curRoom):
    room_data = requests.get(f"{url}ajax_changeroomb.php?suid={character["character_id"]}&serverid={character["server_id"]}&rg_sess_id={character["session"]}&code=1")
