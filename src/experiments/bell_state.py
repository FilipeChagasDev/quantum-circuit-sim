import sys
sys.path.append('../')

import circuit as qc
import gates as qg

my_circuit = qc.QuantumCircuit(2) # 2 qubits circuit

my_circuit.add_gate( qg.Hadamard(0) ) #Hadamard gate at qubit 0

my_circuit.add_gate( qg.CNot(0,1) ) #CNot gate with control at qubit 0 and target at qubit 1

my_circuit.get_result().print_math() #show results


'''
circuit:

q[0] --|H|--*-----
            |
q[1] ------(+)----

'''