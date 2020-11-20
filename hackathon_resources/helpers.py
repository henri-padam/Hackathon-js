import json
import os
from termcolor import cprint
import sys


PERSONAL_BESTS_FILENAME = "personal_bests"
INSTANCES_FILENAME = "instances.json"


def get_solution_value(solution, weights, values, max_weight):
    """Compute input solution value

    Parameters
    ----------
    solution : list[bool]
        Description of solution we want to get score for
    weights : list[int]
        List of weights of all the objects
    values : list[int]
        List of values of all the objects
    max_weight : int
        Maximum weight the knapsack can handle

    Returns
    -------
    int
        Solution value, if computing it was successful
    str
        Error message if any, None otherwise
    """

    if not isinstance(solution, list):
        cprint(
            f"The return value of your 'get_knapsack_solution' function must be a list of booleans.",
            color="red",
        )
        sys.exit()

    # Check solution format
    if len(solution) != len(weights):
        error_message = (
            f"Wrong solution format: Your solution has length {len(solution)}, expected length is {len(weights)}."
        )
        return None, error_message
    for i in range(len(solution)):
        if solution[i] not in [True, False]:
            error_message = (
                f"Wrong Solution format: index {i} has value '{solution[i]}', should be either True or False (or 0 or 1)."
            )
            return None, error_message

    # Compute solution value and weights
    current_value, current_weight = 0, 0
    for sol, val, wei in zip(solution, values, weights):
        if not sol:
            continue
        current_value += val
        current_weight += wei

    # Check solution weight
    if current_weight > max_weight:
        error_message = f"Solution has a weight that is too big: Solution weight is {current_weight}, maximum weight is {max_weight}."
        return None, error_message

    # Solution is ok, return its value
    return current_value, None


def get_solutions_from_json(solutions_filename, instances):
    """Returns the solution of a given instance stored in a JSON file.

    Parameters
    ----------
    solutions_filename : str
        File where the computed solutions have been stored.

    instances : dict
        Considered instance.

    Returns
    -------
    list[bool]
        List of the objects you decide to put in the knapsack for this instance.
    """
    if not os.path.isfile(solutions_filename):
        cprint(f"The solutions must be saved in '{solutions_filename}' file to be retrieved.", color="red")
        sys.exit()
    else:
        with open(solutions_filename, "r") as solutions_file:
            solutions = json.load(solutions_file)
        for instance_id, solution in solutions.items():
            if instance_id not in instances:
                continue
            if not isinstance(solution, list):
                cprint(
                    f"'{solutions_filename}' must be a dictionary mapping 'instance_identifier' to 'array of boolean'. Exiting.",
                    color="red",
                )
                sys.exit()
        return solutions
