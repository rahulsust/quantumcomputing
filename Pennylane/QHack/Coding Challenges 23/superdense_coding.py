''' Three bit information send using 2 qubits, Super dense coding. '''
import pennylane as qml
import pennylane.numpy as np

dev = qml.device("default.qubit", wires=3)

@qml.qnode(dev)

def encode(i, j, k):
    """
    Quantum encoding function. It must act only on the first two qubits.
    This function does not return anything, it simply applies gates.

    Args:
        i, j, k (int): The three encoding bits. They will take the values 1 or 0.

    """


    # Put your code here #
    if i==0 and j==0 and k==1:
        qml.PauliX(wires=0)
        qml.PauliX(wires=1)
        qml.PauliZ(wires=0)
        qml.PauliZ(wires=1)
    if i==0 and j==1 and k==0:
        qml.PauliX(wires=1)
        qml.PauliZ(wires=0)
        qml.CZ(wires=[0,1])
        qml.PauliZ(wires=1)
    if i==0 and j==1 and k==1:
        qml.PauliX(wires=0)
    if i==1 and j==0 and k==0:
        qml.CZ(wires=[0,1])
    if i==1 and j==0 and k==1:
        qml.PauliX(wires=0)
        qml.PauliX(wires=1)
        qml.CZ(wires=[0,1])
    if i==1 and j==1 and k==0:
        qml.PauliX(wires=1)
        qml.PauliZ(wires=0)
    if i==1 and j==1 and k==1:
        qml.PauliX(wires=0)
        qml.PauliZ(wires=1)

def decode():
    """
    Quantum decoding function. It can act on the three qubits.
    This function does not return anything, it simply applies gates.
    """


    # Put your code here #
    qml.CNOT(wires=[0,1])
    qml.CNOT(wires=[0,2])
    qml.Hadamard(wires=0)

dev = qml.device("default.qubit", wires=3)

@qml.qnode(dev)
def circuit(i, j, k):
    """
    Circuit that generates the complete communication protocol.

    Args:
        i, j, k (int): The three encoding bits. They will take the value 1 or 0.
    """

    # We prepare the state 1/sqrt(2)(|000> + |111>)
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[0, 2])

    # Zenda encodes the bits
    encode(i, j, k)

    # Reece decode the information
    decode()

    return qml.probs(wires=range(3))


# These functions are responsible for testing the solution.



def run(test_case_input: str) -> str:

    return None

def check(solution_output: str, expected_output: str) -> None:

    for i in range(2):
        for j in range(2):
            for k in range(2):
                assert np.isclose(circuit(i, j , k)[4 * i + 2 * j + k],1)

                dev = qml.device("default.qubit", wires=3)

                @qml.qnode(dev)
                def circuit2(i, j, k):
                    encode(i, j, k)
                    return qml.probs(wires=range(3))

                circuit2(i, j, k)
                ops = circuit2.tape.operations

                for op in ops:
                    assert not (2 in op.wires), "Invalid connection between qubits."


test_cases = [['No input', 'No output']]

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