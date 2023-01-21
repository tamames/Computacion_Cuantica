"""This code replicate Grover algorithm with the difusion and inversion operators.
as it's presented in https://arxiv.org/abs/quant-ph/9605043 """

import numpy as np


def grover_iteration(state: np.ndarray, marked: int, diffusion_matrix: np.ndarray) -> np.ndarray:
    """In the grover iteration we have to repeat the process sqrt(n) times
    to assert that the marked state has enough amplitude"""

    n = len(state)
    for _ in range(int(np.sqrt(n))):
        state[marked] = -state[marked]
        state = np.dot(diffusion_matrix, state)
    return state


def one_iteration():

    n = 20
    state = np.zeros(n)+1/np.sqrt(n)
    marked = np.random.randint(n)
    diffusion_matrix = np.zeros((n, n)) - 2/n + np.identity(n)
    
    state = grover_iteration(state, marked, diffusion_matrix)

    measure = np.random.choice(range(n), p=state*state)
    if measure == marked:
        print('Congratulations!! you have found the marked state.\n The algorithm has worked.')
    else:
        print("You have not found the marked state.")


def several_iterations():

    n = 20
    diffusion_matrix = np.zeros((n, n)) - 2/n + np.identity(n)
    iterations = 1000
    correct_measures = 0
    for i in range(iterations):

        state = np.zeros(n)+1/np.sqrt(n)
        marked = np.random.randint(n)

        state = grover_iteration(state, marked, diffusion_matrix)

        measure = np.random.choice(range(n), p=state*state)

        if measure == marked:
            correct_measures +=1

    print(f"You have measure the correct state {correct_measures} times. \nThat is {correct_measures/iterations:.2%} of the times")


if __name__ == "__main__":
    one_iteration()
    several_iterations()

