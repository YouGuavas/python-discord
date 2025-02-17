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
        if not 'current_room' in data:
            response = requests.get(f'{url}ajax_changeroomb.php?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}').json()
            data['current_room'] = response['curRoom']
            data['north'] = response['north']
            data['south'] = response['south']
            data['east'] = response['east']
            data['west'] = response['west']

        #allows us to inform user of incorrect moves
        available_moves = []
        for key in data.keys():
            print(f'key: {key}')
            if (key != 'move') and (key != 'current_room'): 
                if data[key] != '0':
                    available_moves.append(key)
                

        if len(available_moves) > 0:
            print(available_moves)
            move = data["move"]
            if move in available_moves:
                move_to = data[move]
                response = requests.get(f'{url}ajax_changeroomb?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}&room={move_to}&lastroom={data['current_room']}').json()
                if response["error"] == '':
                    await channel["message"].send(f"Successfully moved to room: {move_to}")
                else:
                    await channel["message"].send(f"Failed to move {move}")
            else:
                await channel["message"].send(f"Please select a valid move direction. Moves available: {', '.join(available_moves)}")
                return
        else:
            print()
            await channel["message"].reply("There was a grievous error with moving. Check your logs.")
            return

        if response["error"] == '':
            await channel["message"].send(f"Move successful: {move}")
            
        else:
            await channel["message"].send(f"Move failed: {move}")
        return
    except Exception as e:
            print(f'error: {e}')
            if "message" in channel:
                await channel["message"].reply("There was an error with moving. Check your logs.")
