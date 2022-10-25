from typing import Tuple, List, Dict, NewType

# DATA ###

coord = NewType("coordinate", Tuple[int, int])

state = NewType("robot_state", Dict[str, coord | str])

grid = coord((5, 5))

directions = {
    "north": {
        "left": "west",
        "right": "east",
        "move": (0, 1),
    },
    "east": {
        "left": "north",
        "right": "south",
        "move": (1, 0),
    },
    "south": {
        "left": "east",
        "right": "west",
        "move": (0, -1),
    },
    "west": {
        "left": "south",
        "right": "north",
        "move": (-1, 0),
    }
}

commands = [
    "place", "move", "left", "right", "report", "exit"
]


# CALCULATIONS ###

def move(frm: coord, to: coord) -> coord:
    new_frm, new_to = list(zip(frm, to))
    return coord((sum(new_frm), sum(new_to)))


def is_valid_move(movement: coord, grid_size: coord) -> bool:
    if (0 <= movement[0] <= grid_size[0]) and (0 <= movement[1] <= grid_size[1]):
        return True
    else:
        return False


def is_valid_command(input_cmd: str, command_list: List[str]) -> bool:
    command = input_cmd.strip().split("(")
    if len(command) > 1:
        return True if command[0] in command_list else False
    else:
        return False


def is_valid_placing(argument: str) -> bool:
    split_args = argument.strip().split(",")
    try:
        assert len(split_args) == 3
        assert split_args[2].strip().lower() in directions.keys()
        x = int(split_args[0])
        y = int(split_args[1])
        assert is_valid_move(coord((x, y)), grid)
        return True
    except AssertionError:
        return False
    except ValueError:
        return False


def place_robot(coords: coord, face: str) -> state:
    return state({"location": coords, "face": face})


def get_coords(args: str) -> coord:
    if is_valid_placing(args):
        x, y, _ = args.strip().split(",")
        return coord((int(x), int(y)))


def set_robot_state(current, new):
    current["location"] = new["location"]
    current["face"] = new["face"]
    return current


def move_robot(new_coords: coord, face: str) -> state:
    return state({"location": new_coords, "face": face})


def user_wants_exit(usr_input: str) -> bool:
    if usr_input == "exit()" or usr_input == "exit":
        return True

    return False


# ACTIONS ###

def do(command: str, current_state: state):
    cmd = command.strip().split("(")[0]

    match cmd:

        case "place":
            coords = command.strip().split("(")[1][:-1]
            if is_valid_placing(coords):
                x_coord, y_coord, face = coords.split(",")
                new_state = place_robot(coord((int(x_coord.strip()), int(y_coord.strip()))), face)
                return new_state, True
            else:
                print("Can't set robot to these coordinates!")
                return current_state, False

        case "report":
            print(f"I am at: {current_state['location']}, facing:{current_state['face']}")
            return current_state, True

        case "move":
            coords = move(current_state["location"], directions[current_state["face"].strip().lower()]["move"])
            if is_valid_move(coords, grid):
                print(f"Moved to: {coords[0]}, {coords[1]}")
                new_state = set_robot_state(current_state, move_robot(coords, current_state["face"]))
                return new_state, True
            else:
                print("Can't move there or I might fall down! :-(")
                return current_state, True

        case "left":
            new_state = {
                "location": current_state["location"],
                "face": directions[current_state['face'].strip().lower()]['left']
            }
            print(f"Turned left! Now facing {new_state['face']}")
            return set_robot_state(current_state, new_state), True

        case "right":
            new_state = {
                "location": current_state["location"],
                "face": directions[current_state['face'].strip().lower()]['right']
            }
            print(f"Turned right! Now facing {new_state['face']}")
            return set_robot_state(current_state, new_state), True


def evaluate(user_ipt: str, current_state: state, placed: bool):
    if is_valid_command(user_ipt, commands):
        return do(user_ipt, current_state)
    else:
        print("I don't know this command!")
        return current_state, placed


assert is_valid_move(coord((0, 0)), grid) is True
assert is_valid_move(coord((5, 5)), grid) is True
assert is_valid_move(coord((3, 2)), grid) is True
assert is_valid_move(coord((-1, 0)), grid) is False
assert is_valid_move(coord((0, -1)), grid) is False
assert is_valid_move(coord((5, 6)), grid) is False
assert is_valid_move(coord((6, 5)), grid) is False
assert is_valid_command("left()", commands) is True
assert is_valid_command("left", commands) is False
assert is_valid_command(" left(7777777) ", commands) is True

if __name__ == '__main__':

    exited = False

    robot_placed = False

    robot_state = state({})

    while True:
        if not robot_placed:
            user_input = input("First: place the robot!\n>> ")
            exited = user_wants_exit(user_input)
            if exited:
                break
            robot_state, robot_placed = evaluate(user_input, robot_state, robot_placed)

        else:
            user_input = input(">> ")
            exited = user_wants_exit(user_input)
            if exited:
                break
            robot_state, robot_placed = evaluate(user_input, robot_state, robot_placed)
