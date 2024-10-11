import json

def format_commands(data):
    commands = data['data']['commands']
    formatted_commands = []

    for command in commands:
        if command == "FIN":
            break  # Stop processing when "FIN" is encountered

        if "SNAP" in command:
            continue  # Ignore SNAP commands

        cmd_type = command[:2]
        value = command[2:]

        if cmd_type == "FW":  # Forward
            formatted_commands.append(f"f {value}")
        elif cmd_type == "BW":  # Backward
            formatted_commands.append(f"b {value}")
        elif cmd_type == "FR":  # Forward Right
            formatted_commands.append(f"fr 90")
        elif cmd_type == "FL":  # Forward Left
            formatted_commands.append(f"fl 90")
        elif cmd_type == "BR":  # Backward Right
            formatted_commands.append(f"br 90")
        elif cmd_type == "BL":  # Backward Left
            formatted_commands.append(f"bl 90")

    # Join the formatted commands with a comma and space
    return ','.join(formatted_commands) + ','

json_data = {
  "data": {
    "commands": [
      "FW90",
      "FW70",
      "BR00",
      "BW50",
      "BR00",
      "FW10",
      "SNAP1_C",
      "BW10",
      "FL00",
      "FW10",
      "FR00",
      "FW30",
      "FR00",
      "SNAP5_R",
      "FW10",
      "FL00",
      "FW20",
      "FL00",
      "SNAP2_C",
      "BW30",
      "FL00",
      "FW40",
      "SNAP7_L",
      "FIN"
    ],
    "distance": 241.0,
    "path": [
      {
        "d": 0,
        "s": -1,
        "x": 1,
        "y": 1
      },
      {
        "d": 0,
        "s": -1,
        "x": 1,
        "y": 10
      },
      {
        "d": 0,
        "s": -1,
        "x": 1,
        "y": 17
      },
      {
        "d": 6,
        "s": -1,
        "x": 2,
        "y": 14
      },
      {
        "d": 6,
        "s": -1,
        "x": 7,
        "y": 14
      },
      {
        "d": 4,
        "s": -1,
        "x": 10,
        "y": 15
      },
      {
        "d": 4,
        "s": 1,
        "x": 10,
        "y": 14
      },
      {
        "d": 4,
        "s": -1,
        "x": 10,
        "y": 15
      },
      {
        "d": 2,
        "s": -1,
        "x": 13,
        "y": 14
      },
      {
        "d": 2,
        "s": -1,
        "x": 14,
        "y": 14
      },
      {
        "d": 4,
        "s": -1,
        "x": 15,
        "y": 11
      },
      {
        "d": 4,
        "s": -1,
        "x": 15,
        "y": 8
      },
      {
        "d": 6,
        "s": 5,
        "x": 12,
        "y": 7
      },
      {
        "d": 6,
        "s": -1,
        "x": 11,
        "y": 7
      },
      {
        "d": 4,
        "s": -1,
        "x": 10,
        "y": 4
      },
      {
        "d": 4,
        "s": -1,
        "x": 10,
        "y": 2
      },
      {
        "d": 2,
        "s": 2,
        "x": 13,
        "y": 1
      },
      {
        "d": 2,
        "s": -1,
        "x": 10,
        "y": 1
      },
      {
        "d": 0,
        "s": -1,
        "x": 11,
        "y": 4
      },
      {
        "d": 0,
        "s": 7,
        "x": 11,
        "y": 8
      }
    ]
  },
  "error": None
}

# formatted_result = format_commands(json_data)
# print(formatted_result)
