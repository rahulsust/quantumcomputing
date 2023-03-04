'''How do we model this energy exchange at finite temperature? The Generalized Amplitude Damping channel provides a good approximation. Suppose gamma is the photon loss rate at zero temperature, and p is the probability that a qubit emits a photon to the finite-temperature environment (the system will also absorb photons with probability (1-p). We can approximate the interaction with the environment for a duration  via the circuit below.

rho_{in}--|GAD(gamma*del t,P)|...(N=t/del t times)-P_{out}
GAD=generalized amplitude damping channel

That is, we compose many Generalized Amplitude Damping channels with infinitesimal noise parameters gamma*del t and de-excitation probability p. A shorter step del t gives a more precise calculation, but we will need more Generalized Amplitude Damping channels to model the same duration T.

Zenda and Reece need to figure out a measure of how quickly Sqynet can relax its fiducial state, given some photon loss rate gamma and emission probability p. Assuming that Sqynet is in the initial state |+>

your task is to estimate the relaxation half-life, which is the time at which we obtain the outcome |1> with probability 1/4 (the measurement is performed in the computational basis)
'''

import json
import pennylane as qml
import pennylane.numpy as np

def half_life(gamma, p):
    """Calculates the relaxation half-life of a quantum system that exchanges energy with its environment.
    This process is modeled via Generalized Amplitude Damping.

    Args:
        gamma (float): 
            The probability per unit time of the system losing a quantum of energy
            to the environment.
        p (float): The de-excitation probability due to environmental effect

    Returns:
        (float): The relaxation haf-life of the system, as explained in the problem statement.
    """

    num_wires = 1

    dev = qml.device("default.mixed", wires=num_wires)


       # Feel free to write helper functions or global variables here
    dt = 0.05
    @qml.qnode(dev)
    def noise(
        gamma, N # add optional parameters, delete if you don't need any
    ):
        """Implement the sequence of Generalized Amplitude Damping channels in this QNode
        You may pass instead of return if you solved this problem analytically, it's possible!

        Args:
            gamma (float): The probability per unit time of the system losing a quantum of energy
            to the environment.
        
        Returns:
            (float): The relaxation half-life.
        """
        # Don't forget to initialize the state
        qml.Hadamard(wires=0)
        # Put your code here #
        for i in range(N):
            qml.GeneralizedAmplitudeDamping(gamma*dt, p, wires=0)
        # Return something or pass if you solved this analytically!
        return qml.probs()

    # Write any subroutines you may need to find the relaxation time here
    N = 1
    prob = noise(gamma, N)[1]
    while prob > 0.25:
        N += 1
        prob = noise(gamma, N)[1]
    # Return the relaxation half-life
    return N*dt


# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:

    ins = json.loads(test_case_input)
    output = half_life(*ins)

    return str(output)

def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(
        solution_output, expected_output, atol=2e-1
    ), "The relaxation half-life is not quite right."


test_cases = [['[0.1,0.92]', '9.05'], ['[0.2,0.83]', '7.09']]

for i, (input_, expected_output) in enumerate(test_cases):
    print(f"Running test case {i} with input '{input_}'...")

    try:
        output = run(input_)

    except Exception as exc:
        print(f"Runtime Error. {exc}")

    else:
        if message := check(output, expected_output):
            print(f"Wrong Answer. Have: '{output}'. Want: '{expected_output}'.")

        else:
            print("Correct!")