'''del_lambda[rho]=(1-lambda)*rho+lambda/2*Identity operator
   here, lambda means, probability of the state being deleted and replaced by something random.

any density matrix on  qubits can be written as a linear combination of a special set of 
"Pauli" density matrices. These have the form
    
    rho_{p}=1/2**n(Identity operator + P)

where p belongs to {I,X,Y,Z}tensor power n, is a tensor product of n single qubit Pauli operators called pauli word.

after applying noise it becomes,

rho_p(lambda) = del_{lambda}^{tensor n}[rho_{p}]

If adding noise makes a Pauli density matrix look random, a combination of Pauli densities — in other words, any matrix! — will look random. Here, "looks random" means "the expectation of any measurement is similar to the maximally mixed density matrix, 

rho_naught=I/2**n

we can capture all expectations at once using something called trace distance between density matrices. This is defined as,

T(rho, sigma) = 1/2 * Tr|rho-sigma|

where |A|=sqrt(A_daggar*A)

For any (projective) measurement M, the trace distance between two density matrices rho and sigma bounds the difference in expectations:

<M>_{rho} - <M>_{sigma} = Tr|M(rho-sigma)|<=T(rho,sigma)

If the trace distance is small, the two states are hard to tell apart with any measurement.

Zenda and Reece suspect that the noise in their circuitry is blurring the states and making them hard to distinguish. Your goal is to write a function which verifies the bound,

T(rho_{P}(lambda),rho_naught)<=(1-lambda)**|P|
where |P| is the number of non-identity operators in the Pauli word P. You should find this is always positive! Since a Pauli density matrix gets exponentially blurry, and all states can be built from these Pauli densities, most states will be exponentially hard to distinguish.
'''
import json
import pennylane as qml
import pennylane.numpy as np
import scipy

def abs_dist(rho, sigma):
    """A function to compute the absolute value |rho - sigma|."""
    polar = scipy.linalg.polar(rho - sigma)
    return polar[1]

def word_dist(word):
    """A function which counts the non-identity operators in a Pauli word"""
    return sum(word[i] != "I" for i in range(len(word)))


# Produce the Pauli density for a given Pauli word and apply noise

def noisy_Pauli_density(word, lmbda):
    """
       A subcircuit which prepares a density matrix (I + P)/2**n for a given Pauli
       word P, and applies depolarizing noise to each qubit. Nothing is returned.

    Args:
            word (str): A Pauli word represented as a string with characters I,  X, Y and Z.
            lmbda (float): The probability of replacing a qubit with something random.
    """


    # Put your code here #
    l=word_dist(word)
    T= (qml.pauli.PauliWord({i:a for i,a in enumerate(word)}).to_mat(wire_order=range(l))+ np.eye(2**l,2**l))/2**l
    qml.QubitDensityMatrix(T, wires=range(l))
    for i in range(l):
        qml.DepolarizingChannel(lmbda, wires=i)


# Compute the trace distance from a noisy Pauli density to the maximally mixed density

def maxmix_trace_dist(word, lmbda):
    """
       A function compute the trace distance between a noisy density matrix, specified
       by a Pauli word, and the maximally mixed matrix.

    Args:
            word (str): A Pauli word represented as a string with characters I, X, Y and Z.
            lmbda (float): The probability of replacing a qubit with something random.

    Returns:
            float: The trace distance between two matrices encoding Pauli words.
    """


    # Put your code here #
    l=word_dist(word)
    T= (qml.pauli.PauliWord({i:a for i,a in enumerate(word)}).to_mat(wire_order=range(l))+ np.eye(2**l,2**l))/2**l
    qml.QubitDensityMatrix(T, wires=range(l))
    noisy_Pauli_density(word, lmbda)
    when I am trying to return the density matrix  matrix after noisy_pauli_density  function I am getting error
    P=np.matrix.H(abs_dist(T,np.eye(2**l,2**l)/2**l))/2
    return P


def bound_verifier(word, lmbda):
    """
       A simple check function which verifies the trace distance from a noisy Pauli density
       to the maximally mixed matrix is bounded by (1 - lambda)^|P|.

    Args:
            word (str): A Pauli word represented as a string with characters I, X, Y and Z.
            lmbda (float): The probability of replacing a qubit with something random.

    Returns:
            float: The difference between (1 - lambda)^|P| and T(rho_P(lambda), rho_0).
    """


    # Put your code here #
    return (1-lmbda)**word_dist(word) - maxmix_trace_dist(word, lmbda)

# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:

    word, lmbda = json.loads(test_case_input)
    output = np.real(bound_verifier(word, lmbda))

    return str(output)


def check(solution_output: str, expected_output: str) -> None:

    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(
        solution_output, expected_output, rtol=1e-4
    ), "Your trace distance isn't quite right!"


test_cases = [['["XXI", 0.7]', '0.0877777777777777'], ['["XXIZ", 0.1]', '0.4035185185185055'], ['["YIZ", 0.3]', '0.30999999999999284'], ['["ZZZZZZZXXX", 0.1]', '0.22914458207245006']]

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