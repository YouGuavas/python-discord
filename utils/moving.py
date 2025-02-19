import requests
import heapq

from urllib.parse import urlencode
from utils.data_functions import get_room_data
from utils.getting import room_data

async def gorganus(url, channel, character):
    turns = [{"direction": "north", "steps": 10}, 
             {"direction": "west", "steps": 5},
             {"direction": "north", "steps": 2},
             {"direction": "west", "steps": 4},
             {"direction": "north", "steps": 3},
             {"direction": "west", "steps": 3},
             {"direction": "north", "steps": 3},
             {"direction": "west", "steps": 1},
             {"direction": "north", "steps": 2},
             {"direction": "west", "steps": 2},
             {"direction": "north", "steps": 4},
             {"direction": "east", "steps": 1},
             {"direction": "north", "steps": 1},
             {"direction": "east", "steps": 1},
             {"direction": "north", "steps": 2},
             {"direction": "east", "steps": 1},
             {"direction": "north", "steps": 5},
             {"direction": "west", "steps": 1},
             {"direction": "north", "steps": 3},
             {"direction": "west", "steps": 1},
             {"direction": "north", "steps": 2},
             {"direction": "west", "steps": 1},
             {"direction": "north", "steps": 3},
             {"direction": "west", "steps": 3},
             {"direction": "north", "steps": 1},
             {"direction": "west", "steps": 1},
             {"direction": "north", "steps": 3},
             {"direction": "west", "steps": 3},
             {"direction": "south", "steps": 1},
             {"direction": "west", "steps": 2},
             {"direction": "south", "steps": 1},
             {"direction": "west", "steps": 1},
             {"direction": "south", "steps": 1},
             {"direction": "west", "steps": 3},
             {"direction": "north", "steps": 3},
             {"direction": "west", "steps": 4},
             {"direction": "south", "steps": 2},
             {"direction": "west", "steps": 3},
             {"direction": "north", "steps": 1},
             {"direction": "west", "steps": 1},
             {"direction": "north", "steps": 2},
             {"direction": "east", "steps": 1},
             {"direction": "north", "steps": 5},
             {"direction": "east", "steps": 1},




             ]
    for turn in turns:
        i = 0 
        while i < turn["steps"]:
            await move(url, channel, character, turn["direction"])
            i += 1
    
    
    await channel["message"].send("Arrived")
    
    

async def move(url, channel, character, direction):
    try:
        """
        Handles moving either in a direction or to a specific position.

        :param base_url: API base URL
        :param ctx: Discord message context
        :param session: Dictionary holding auth session
        :param direction: Optional string for movement direction (e.g., 'up', 'down')
        :param position: Optional tuple (x, y) for absolute movement -- currently disabled
        """
        directions = ['north', 'south', 'east', 'west']
        if not character["session"]["session"]:
            await channel["message"].send("Error: Not logged in.")
            return
        room_data = await get_room_data(url, channel, character)
        data = room_data["data"]
        available_moves = room_data["available_moves"]

        #allows us to inform user of incorrect moves
                

        if len(available_moves) > 0:
            move = direction.lower()
            if move in available_moves:
                move_to = data[move]
                requests.get(f'{url}ajax_changeroomb?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}&room={move_to}&lastroom={data['current_room']}').json()
                new_room = await get_room_data(url, channel, character)
                next_moves = new_room["available_moves"]
                if "error" in new_room.keys():
                    await channel["message"].send(f"Failed to move to room: {move_to}. Please try again.")
                if new_room:
                    await channel["message"].send(f"Successfully moved to room: {move_to}. Avaialable moves: {', '.join(next_moves)}")
            else:
                await channel["message"].send(f"Failed to move {move}. Please select a valid move direction. Moves available: {', '.join(available_moves)}")
                return {"status": 400, "moves": available_moves}
        else:
            await channel["message"].reply("There was a grievous error with moving. Check your logs.")
            return {"status": 400, "moves": available_moves}
        return {"status": 200}
    except Exception as e:
            print(f'error: {e}')
            if "message" in channel:
                await channel["message"].reply("There was an error with moving. Check your logs.")



def heuristic(node, goal):
    return 1.5 * (abs(goal[0] - node[0]) + abs(goal[1] - node[1]))  # Bias toward goal
def get_neighbors(current, grid):
    neighbors = room_data(current)
    return [neighbors["north"], neighbors["south"], neighbors["east"], neighbors["west"]]
def reconstruct_path(came_from, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]  # Move to the previous node
    path.append(start)  # Add start node at the end
    path.reverse()  # Reverse to get the correct order
    return path

def astar_pathfinding(start, goal, grid):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while open_list:
        _, current = heapq.heappop(open_list)
        if current == goal:
            break
        
        for next_node in get_neighbors(current, grid):
            new_cost = cost_so_far[current] + 1
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(next_node, goal)
                heapq.heappush(open_list, (priority, next_node))
                came_from[next_node] = current

    return reconstruct_path(came_from, start, goal)
