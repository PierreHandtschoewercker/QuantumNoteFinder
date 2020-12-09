from qiskit import *
import matplotlib
from matplotlib import pyplot as plt

freq = 440
notes = {'A': 110, 'B': 123.5, 'C': 65.41, 'D': 73.42, 'E': 82.41, 'F': 87.31, 'G': 98}
#        000       001          010         011         100         101         111

"""def findNoteFororacle(qc, freq, notes):
    for index,n in enumerate(notes):
        if (notes[n] - 2) < freq < (notes[n] + 2):
            qc.cz()
"""

backend = Aer.get_backend('unitary_simulator')
matplotlib.use('Qt5Agg')

n = 3
oracle_circuit = QuantumCircuit(n, name='Oracle')
c = 0
t = 2
oracle_circuit.cz(0, 2).cz(2, 0)  # Oracle
#oracle_circuit.cz(2, 1)  # Oracle
# print(, t)

job = execute(oracle_circuit, backend)
result = job.result()
print(result.get_unitary(oracle_circuit))
oracle_ex4 = oracle_circuit.to_gate()
# print(oracle_ex4.to_matrix())
# oracle_ex4.draw()
