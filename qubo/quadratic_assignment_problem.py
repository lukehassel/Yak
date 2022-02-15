from qiskit.algorithms import NumPyMinimumEigensolver
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.converters import LinearEqualityToPenalty

if __name__ == '__main__':

    flow = [[0, 5, 2], [5, 0, 3], [2, 3, 0]]
    distance = [[0, 8, 15], [8, 0, 13], [15, 13, 0]]
    n = 3

    qp = QuadraticProgram()

    quadratic = {}
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    factor = flow[i][j] * distance[k][l]
                    if factor > 0:
                        quadratic[("x_{" + str(i) + str(k) + "}", "x_{" + str(j) + str(l) + "}")] = factor

    linear_1_constraints = []
    for i in range(n):
        linear_1 = {}
        for j in range(n):
            linear_1["x_{" + str(i) + str(j) + "}"] = 1
        linear_1_constraints.append(linear_1)

    linear_2_constraints = []
    for j in range(n):
        linear_2 = {}
        for i in range(n):
            linear_2["x_{" + str(i) + str(j) + "}"] = 1
        linear_2_constraints.append(linear_2)

    for i in range(n):
        for k in range(n):
            qp.binary_var('x_{' + str(i) + str(k) + "}")

    qp.minimize(quadratic=quadratic)

    for i, constraint in enumerate(linear_1_constraints):
        qp.linear_constraint(linear=constraint, sense='E', rhs=1, name='const1_' + str(i))

    for i, constraint in enumerate(linear_2_constraints):
        qp.linear_constraint(linear=constraint, sense='E', rhs=1, name='const2_' + str(i))

    print(qp.export_as_lp_string())

    # Replace constraints with Penalties
    lineq2penalty = LinearEqualityToPenalty()
    qubo = lineq2penalty.convert(qp)

    # To Ising Hamiltonian
    #op, offset = qubo.to_ising()
    #print("offset: ", offset)

    print(qubo.export_as_lp_string())

    exact_mes = NumPyMinimumEigensolver()
    exact = MinimumEigenOptimizer(exact_mes)

    # Solve qubo with classical solver
    exact_result = exact.solve(qubo)
    print(exact_result)
