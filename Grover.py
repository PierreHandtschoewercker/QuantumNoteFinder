import matplotlib.pyplot as plt
import numpy as np

# importing Qiskit
from qiskit import IBMQ, Aer, QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.providers.ibmq import least_busy
from qiskit.quantum_info import Statevector

# import basic plot tools
from qiskit.visualization import plot_histogram

freq = 440
notes = {'A': 110, 'B': 123.5, 'C': 65.41, 'D': 73.42, 'E': 82.41, 'F': 87.31, 'G': 98}
#        000       001          010         011         100         101         111


def findNoteFororacle(qc, freq, notes):
    for index,n in enumerate(notes):
        if (notes[n] - 2) < freq < (notes[n] + 2):
            qc.cz()



n = 4
oracle_circuit = QuantumCircuit(n, name='Oracle')
oracle_circuit.cz(0, 3)  # Oracle
oracle_circuit.cz(1, 3)  # Oracle
oracle_circuit.cz(2, 3)  # Oracle
oracle_ex4 = oracle_circuit.to_gate()
oracle_circuit.draw()


# superposition of all qbits
def initialize_s(qc, qubits):
    """Apply a H-gate to 'qubits' in qc"""
    for q in qubits:
        qc.h(q)
    return qc


def diffuser(nqubits):
    qc = QuantumCircuit(nqubits)
    # Apply transformation |s> -> |00..0> (H-gates)
    for qubit in range(nqubits):
        qc.h(qubit)
    # Apply transformation |00..0> -> |11..1> (X-gates)
    for qubit in range(nqubits):
        qc.x(qubit)
    # Do multi-controlled-Z gate
    qc.h(nqubits - 1)
    qc.mct(list(range(nqubits - 1)), nqubits - 1)  # multi-controlled-toffoli
    qc.h(nqubits - 1)
    # Apply transformation |11..1> -> |00..0>
    for qubit in range(nqubits):
        qc.x(qubit)
    # Apply transformation |00..0> -> |s>
    for qubit in range(nqubits):
        qc.h(qubit)
    # We will return the diffuser as a gate
    U_s = qc.to_gate()
    U_s.name = "$U_superposition$"
    return U_s


grover_circuit = QuantumCircuit(n)
grover_circuit = initialize_s(grover_circuit, [0, 1, 2, 3])
grover_circuit.append(oracle_ex4, [0, 1, 2, 3])
grover_circuit.append(diffuser(n), [0, 1, 2, 3])
grover_circuit.measure_all()
grover_circuit.draw()
