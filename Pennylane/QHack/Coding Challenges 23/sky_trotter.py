dev = qml.device('default.qubit', wires = 2)

@qml.qnode(dev)
def trotterize(alpha, beta, time, depth):
    """This quantum circuit implements the Trotterization of a Hamiltonian given by a linear combination
    of tensor products of X and Z Pauli gates.

    Args:
        alpha (float): The coefficient of the XX term in the Hamiltonian, as in the statement of the problem.
        beta (float): The coefficient of the YY term in the Hamiltonian, as in the statement of the problem.
        time (float): Time interval during which the quantum state evolves under the interactions specified by the Hamiltonian.
        depth (int): The Trotterization depth.

    Returns:
        (numpy.array): The probabilities of each measuring each computational basis state.
    """
    dt = time/depth
    for d in range(depth):
        qml.IsingXX(2*alpha*dt, wires=[0, 1])
        qml.IsingZZ(2*beta*dt, wires=[0, 1])
    return qml.probs()
# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    dev = qml.device("default.qubit", wires=2)
    ins = json.loads(test_case_input)
    output = list(trotterize(*ins).numpy())

    return str(output)

def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(
        solution_output, expected_output, rtol=1e-4
    ), "Your circuit does not give the correct probabilities."

    tape = trotterize.qtape

    names = [op.name for op in tape.operations]
    
    assert names.count('ApproxTimeEvolution') == 0, "Your circuit is using the built-in PennyLane Trotterization"
    assert names.count('QubitUnitary') == 0, "Can't use custom-built gates!"