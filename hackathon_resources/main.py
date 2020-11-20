"""Launch "python main.py --help" to understand the parameters this file can take
"""

import argparse
import json
import os
import pickle
from time import time
import sys
from helpers import INSTANCES_FILENAME, PERSONAL_BESTS_FILENAME, get_solution_value, get_solutions_from_json
from knapsack_solver import get_knapsack_solution
from termcolor import cprint


def parse_arguments():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--all",
        dest="all",
        required=False,
        action="store_true",
        default=False,
        help="Run your knapsack solver on all instances.",
    )
    parser.add_argument(
        "--instance-id",
        dest="instance_id",
        required=False,
        action="store",
        default=None,
        type=str,
        help="Run your solver on one instance only",
    )
    parser.add_argument(
        "--force",
        dest="force",
        required=False,
        action="store_true",
        default=False,
        help="Force rerunning your solver even on instances where you already have the optimal value",
    )
    parser.add_argument(
        "--solutions",
        dest="solutions_filename",
        required=False,
        action="store",
        default=None,
        type=str,
        help="If Python is not the language used for this work, provide path to the JSON with results.",
    )
    options = parser.parse_args()
    if options.instance_id is None and not options.all:
        raise RuntimeError(
            "Please specify the instance your want to run your code on with either '--all' or '--instance-id <id>'"
        )
    return options


def get_instances_and_pbs(options):
    # Get all instances
    with open(INSTANCES_FILENAME, "rb") as instances_file:
        all_instances = json.load(instances_file)

    # Get current personal bests
    if not os.path.isfile(PERSONAL_BESTS_FILENAME):
        cprint(f"** First launch of the script. Creating an empty {PERSONAL_BESTS_FILENAME} file **\n", color="magenta")
        personal_bests = {
            instance_identifier: dict(value=0, solution=[0 for _ in range(len(instance["weights"]))])
            for instance_identifier, instance in all_instances.items()
        }
        with open(PERSONAL_BESTS_FILENAME, "wb") as results_file:
            pickle.dump(personal_bests, results_file)
    else:
        cprint(f"Retrieving previous results from {PERSONAL_BESTS_FILENAME} file.\n", color="magenta")
        with open(PERSONAL_BESTS_FILENAME, "rb") as results_file:
            personal_bests = pickle.load(results_file)

    # If only one instance has been selected, filter the other ones.
    if options.instance_id is not None:
        if options.instance_id not in all_instances:
            cprint(
                f"Instance #{options.instance_id} does not exist! Available identifiers: {', '.join(list(all_instances.keys()))}.",
                color="red",
            )
            sys.exit()
        else:
            all_instances = {options.instance_id: all_instances[options.instance_id]}

    return all_instances, personal_bests


def launch_on_instances(options, all_instances, personal_bests):
    if options.solutions_filename:
        solutions = get_solutions_from_json(solutions_filename=options.solutions_filename, instances=all_instances)
    # Run get_knapsack_solution on instances
    for instance_id, instance in all_instances.items():
        optimal_value = instance["optimal_value"]
        current_pb = personal_bests[instance_id]["value"]
        output_string = f"Instance {instance_id}: "

        if current_pb == optimal_value and not options.force:
            output_string += f"Optimal value {optimal_value} already reached. Not re-running"
            cprint(output_string, color="white")
            continue

        if options.solutions_filename:
            if instance_id not in solutions:
                cprint(
                    f"Instance #{instance_id} has no solution provided in '{options.solutions_filename}'.", color="red"
                )
                sys.exit()
            else:
                solution = solutions[instance_id]
        else:
            solution = get_knapsack_solution(instance["weights"], instance["values"], instance["capacity"])
        current_solution_value, error_message = get_solution_value(
            solution, instance["weights"], instance["values"], instance["capacity"]
        )

        if error_message:
            output_string += f"Failed solution checks. Reason: {error_message}"
            cprint(output_string, color="red")
            continue

        if current_solution_value > current_pb:
            personal_bests[instance_id]["value"] = current_solution_value
            personal_bests[instance_id]["solution"] = solution
            if current_solution_value == optimal_value:
                output_string += (
                    "Well done! You have reached the optimal value on this instance! New best: "
                    + f"{current_solution_value}/{optimal_value} (previous best: {current_pb})"
                )
                cprint(output_string, color="cyan")
            else:
                output_string += (
                    f"Improvement! New best: {current_solution_value}/{optimal_value} (previous best: {current_pb})"
                )
                cprint(output_string, color="green")
            continue

        if current_solution_value <= current_pb:
            output_string += f"No improvement. Current solution: {current_solution_value}/{optimal_value} (current best: {current_pb})"
            cprint(output_string, color="yellow")

    return personal_bests


def compute_and_print_general_scores(all_instances, personal_bests):
    total_score = 0.0
    total_instances = len(all_instances)
    for instance_id, instance in all_instances.items():
        total_score += (personal_bests[instance_id]["value"] / instance["optimal_value"]) * 100 / total_instances

    cprint(f"\nCurrent general score: {round(total_score, 5)}/100.", "white")


def dump_personal_bests(personal_bests):
    with open(PERSONAL_BESTS_FILENAME, "wb") as f:
        pickle.dump(personal_bests, f)


if __name__ == "__main__":
    options = parse_arguments()
    all_instances, personal_bests = get_instances_and_pbs(options)
    new_personal_bests = launch_on_instances(options, all_instances, personal_bests)
    dump_personal_bests(new_personal_bests)
    if options.all:
        compute_and_print_general_scores(all_instances, new_personal_bests)
