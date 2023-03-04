''' It is actually quantum teleportation protocol.'''
def zenda_operator():
    """
    Quantum function corresponding to the operator to be applied by
    Zenda on her qubits. This function does not return anything,
    you must simply write the necessary gates.
    """
    # Put your code here #
    qml.CNOT(wires=["z0","z1"])
    qml.Hadamard(wires="z0")
def copier():
    """
    Quantum function encoding the copy operation cone by Zenda, on each qubit.
    This function does not return anything, you must simply write the necessary gates.
    """
    # Put your code here #
    
    # m_0 = qml.measure("z0")
    # m_1 = qml.measure("z1")
    qml.CNOT(wires=["z0","s0"])
    qml.CNOT(wires=["z1","s1"])
def printer():
    """
    Quantum function encoding the print operation done by Reece's printer.
    This function does not return anything, you must simply write the necessary gates.
    """
    # Put your code here #
    qml.CZ(wires=["s0","r1"])
    qml.CNOT(wires=["s1","r1"])

''' Guide function'''
def bell_generator():
    """
    Quantum function preparing bell state shared by Reece and Zenda.
    """

    qml.Hadamard(wires=["z1"])
    qml.CNOT(wires=["z1", "r1"])


dev = qml.device("default.qubit", wires=["z0", "z1", "r1", "s0", "s1"])

@qml.qnode(dev)
def circuit(alpha, beta, gamma):

    # we encode the initial state
    qml.U3(alpha, beta, gamma, wires = "z0")

    bell_generator()

    # Zenda acts on her qubits and establishes and copies them.
    zenda_operator()
    copier()


    # Reece programs his printer
    printer()

    # Here we are returning the expected value with respect to any observable,
    # the choice of observable is not important in this exercise.

    return qml.expval(0.25 * qml.PauliX("r1") + qml.PauliY("r1"))
# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    angles = json.loads(test_case_input)
    output = circuit(*angles)
    return str(output)


def check(solution_output: str, expected_output: str) -> None:

    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(
        solution_output, expected_output, atol=2e-1
    ), "The expected output is not quite right."

    try:
        dev1 = qml.device("default.qubit", wires = ["z0", "z1"])
        @qml.qnode(dev1)
        def circuit1():
            zenda_operator()
            return qml.probs(dev1.wires)
        circuit1()
    except:
        assert False, "zenda_operator can only act on z0 and z1 wires"

    try:
        dev1 = qml.device("default.qubit", wires = ["z0", "z1", "s0", "s1"])
        @qml.qnode(dev1)
        def circuit1():
            copier()
            return qml.probs(dev1.wires)
        circuit1()
    except:
        assert False, "copy can only act on z0, z1, s0 and s1 wires"


    try:
        dev1 = qml.device("default.qubit", wires = ["s0", "s1", "r1"])
        @qml.qnode(dev1)
        def circuit1():
            printer()
            return qml.probs(dev1.wires)
        circuit1()
    except:
        assert False, "Reece's printer can only act on s0, s1 and r1 wires"