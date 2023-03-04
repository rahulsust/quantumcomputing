def create_Hamiltonian(h):
    """
    Function in charge of generating the Hamiltonian of the statement.

    Args:
        h (float): magnetic field strength

    Returns:
        (qml.Hamiltonian): Hamiltonian of the statement associated to h
    """
    # Put your code here #
    N = 4
    c1 = [-1.0 for i in range(N)]
    obs1 = [qml.PauliZ(i%N) @ qml.PauliZ((i+1)%N) for i in range(N)]
    H1= qml.Hamiltonian(c1, obs1)
    
    c2 = [-h for i in range(N)]
    obs2 = [qml.PauliX(i%N) for i in range(N)]
    
    H2 = qml.Hamiltonian(c2, obs2)
    return H1+H2
dev = qml.device("default.qubit", wires=4)

@qml.qnode(dev)
def model(params, H):
    """
    To implement VQE you need an ansatz for the candidate ground state!
    Define here the VQE ansatz in terms of some parameters (params) that
    create the candidate ground state. These parameters will
    be optimized later.

    Args:
        params (numpy.array): parameters to be used in the variational circuit
        H (qml.Hamiltonian): Hamiltonian used to calculate the expected value

    Returns:
        (float): Expected value with respect to the Hamiltonian H
    """
    # Put your code here #
    N=4
    qml.StronglyEntanglingLayers(weights=params, wires=range(N))
        
    return qml.expval(H)
def train(h):
    """
    In this function you must design a subroutine that returns the
    parameters that best approximate the ground state.

    Args:
        h (float): magnetic field strength

    Returns:
        (numpy.array): parameters that best approximate the ground state.
    """
    # Put your code here #
    H = create_Hamiltonian(h)
    
    def cost(params):
        return model(params, H)
    def my_gradient_descent(cost, params, lr, max_iter):
        for i in range(max_iter):
            # Calculate the cost and gradient
            c = cost(params)
            g = qml.grad(cost)(params)

            # Update the parameters using the gradient descent rule
            params = params - lr * g

        return params
    
    shape = qml.StronglyEntanglingLayers.shape(n_layers=4, n_wires=4)
    params = np.random.random(size=shape)
    params = my_gradient_descent(cost, params, lr=0.1, max_iter=150)
    return params
# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    ins = json.loads(test_case_input)
    params = train(ins)
    return str(model(params, create_Hamiltonian(ins)))


def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(
        solution_output, expected_output, rtol=1e-1
    ), "The expected value is not correct."