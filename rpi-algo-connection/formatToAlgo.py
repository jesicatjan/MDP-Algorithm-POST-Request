# sample message stored in rpi from android
# initialPositions = "OBSTACLE,1,5,4,NORTH\nOBSTACLE,2,5,4,NORTH\nOBSTACLE,3,5,4,NORTH\nOBSTACLE,4,5,4,NORTH\nOBSTACLE,5,5,4,NORTH"

def formatToAlgo(initialPositions):
    obstacles = []
    lines = initialPositions.split("\n")
    
    for line in lines:
        if line.startswith("OBSTACLE"):
            parts = line.split(",")
            if len(parts) == 5:  # Make sure we have all the components
                obstacle_id = int(parts[1])
                x = int(parts[2])
                y = int(parts[3])
                direction = parts[4]

                # up : 0, right : 2, down : 4, left : 6
                direction_mapping = {"NORTH": 0, "EAST": 2, "SOUTH": 4, "WEST": 6}
                d = direction_mapping.get(direction, 0)  # Default to NORTH if not found
                
                obstacles.append({
                    "x": x,
                    "y": y,
                    "d": d,
                    "id": obstacle_id
                })
    
    # Build the full JSON structure
    formatted_algo = {
        "url": "/path",
        "method": "POST",
        "headers": {},
        "body": {
            "obstacles": obstacles,
            "robot_x": 1,
            "robot_y": 1,
            "robot_dir": 0,  # Assuming robot is facing "NORTH"
            "retrying": False
        }
    }

    return formatted_algo

# message = "OBSTACLE,1,5,4,NORTH\nOBSTACLE,2,5,4,NORTH\nOBSTACLE,3,5,4,NORTH\nOBSTACLE,4,5,4,NORTH\nOBSTACLE,5,5,4,NORTH"
# formatted_result = formatToAlgo(message)
# print(formatted_result)