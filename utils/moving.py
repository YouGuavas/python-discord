import requests
import heapq

from urllib.parse import urlencode
from utils.data_functions import get_room_data
from utils.getting import room_data

async def move_by_direction(url, channel, character, direction):
    try:
        """
        Handles moving in a direction.
        :param base_url: API base URL
        :param ctx: Discord message context
        :param session: Dictionary holding auth session
        :param direction: Optional string for movement direction (e.g., 'up', 'down')
        """
        directions = ['north', 'south', 'east', 'west']
        if not character["session"]["session"]:
            await channel["message"].send("Error: Not logged in.")
            return
        room_data = await get_room_data(url, channel, character)
        data = room_data["data"]
        available_moves = room_data["available_moves"]
        available_moves.remove('map')

        #allows us to inform user of incorrect moves
                

        if len(available_moves) > 0:
            move = direction.lower()
            if move in available_moves:
                move_to = data[move]
                requests.get(f'{url}ajax_changeroomb?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}&room={move_to}&lastroom={data['current_room']}').json()
                new_room = await get_room_data(url, channel, character)
                next_moves = new_room["available_moves"]
                next_moves.remove('map')

                if "error" in new_room.keys():
                    await channel["message"].send(f"Screwed that one up: {move_to}. Please try again.")
                if new_room:
                    await channel["message"].send(f"You take a step to the {direction.lower()}. ({move_to}) Avaialable moves: {', '.join(next_moves)}")
            else:
                await channel["message"].send(f"What are you thinking? You can't go {direction.lower()}! Try again. Moves available: {', '.join(available_moves)}")
                return {"status": 400, "moves": available_moves}
        else:
            await channel["message"].reply("There was a grievous error with moving. Check your logs.")
            return {"status": 400, "moves": available_moves}
        return {"status": 200}
    except Exception as e:
            print(f'error: {e}')
            if "message" in channel:
                await channel["message"].reply(f"There was an error moving {direction.lower()}. Check your logs.")


async def move_to_room(url, channel, character, current_room, next_room):
    try:
        print(f"Current room: {current_room}, next room: {next_room}")
        requests.get(f'{url}ajax_changeroomb?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}&room={next_room}&lastroom={current_room}').json()
    except Exception as e:
            print(f'error: {e}')
            if "message" in channel:
                await channel["message"].reply(f"There was an error moving to room: {next_room}. Check your logs.")

def heuristic(node, goal):
    weight = 1.5 * abs(int(goal) - int(node))  # Bias toward goal
    print(f"Weight of move: {weight}")
    return weight

async def get_neighbors(channel, current: int):
    neighbors = await room_data(channel, current)
    return [neighbors[1], neighbors[2], neighbors[3], neighbors[4]]

def reconstruct_path(came_from, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]  # Move to the previous node
    path.append(start)  # Add start node at the end
    path.reverse()  # Reverse to get the correct order
    return path

async def a_star_search(channel, character, start, goal):
    """Performs A* search on room graph."""
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}  # For each room, store (previous_room, next_room)
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            reconstructed = reconstruct_path(came_from, start, goal)
            return reconstructed
        neighbors = await get_neighbors(channel, current)
        for neighbor in neighbors:
            new_neighbors = []
            if int(neighbor) > 0:
                new_neighbors.append(neighbor)
                tentative_g_score = g_score[current] + 1  # Static cost of 1 per move
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(int(neighbor), int(goal))
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No valid path found
