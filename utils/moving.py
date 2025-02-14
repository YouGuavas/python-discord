import requests
from urllib.parse import urlencode

async def move(url, channel, character, direction=None, position=None):
    try:
        """
        Handles moving either in a direction or to a specific position.

        :param base_url: API base URL
        :param ctx: Discord message context
        :param session: Dictionary holding auth session
        :param direction: Optional string for movement direction (e.g., 'up', 'down')
        :param position: Optional tuple (x, y) for absolute movement
        """
        if not character["session"]["session"]:
            await channel["message"].send("Error: Not logged in.")
            return
        data = {}
        if direction:
            data["move"] = direction
        elif position:
            data["position"] = position
        else:
            await channel["message"].send("Error: No valid move command provided.")
            return
        # Make request (replace with actual request logic)
        if not data['current_room']:
            response = await requests.get(f'{url}ajax_changeroomb?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']}')["data"]
            print('response: ' + response)
            data['current_room'] = response.curRoom
            data['north'] = response.north
            data['south'] = response.south
            data['east'] = response.east
            data['west'] = response.west
        #await channel["message"].send(data)
        if data['north']:
            move_to = data["move"]
            #print(move_to)
            response = await requests.get(f'{url}ajax_changeroomb?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']}&room={data[data['move']]}&lastroom={data['current_room']}')
        if response["success"]:
            await channel["message"].send(f"Move successful: {response['message']}")
        else:
            await channel["message"].send(f"Move failed: {response['error']}")
    except Exception as e:
            print(e)
            if "message" in channel:
                await channel["message"].reply("There was an error with moving. Check your logs.")
