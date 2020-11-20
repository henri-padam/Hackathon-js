"""
YOU ONLY HAVE TO ADD CODE HERE IN THE FUNCTION get_knapsack_solution
"""


def get_knapsack_solution(weights, values, capacity):
    """Return your best shot at solving the knapack problem for the given input data

    Parameters
    ----------
    weights : list[int]
        List of weights of all the objects
    values : list[int]
        List of values of all the objects
    capacity : int
        Maximum weight the knapsack can handle

    Returns
    -------
    list[bool]
        List of the objects you decide to put in the knapsack.
        If object with index i is included in the knapsack, then the returned_list must have True at index i, False otherwise
        The length of the returned list must have the same length as weights and values.
    """

    assert len(weights) == len(values)
    n = len(weights)  # total amount of objects

    import random

    solution = [(random.random() < 0.01) for i in range(n)]  # randomly pick objects and return the list
    return solution
