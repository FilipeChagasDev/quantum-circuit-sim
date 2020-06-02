'''
Author: Filipe Chagas
Email: filipe.ferraz@gmail.com
GitHub: github.com/filipechagasdev
June 2020
'''

import numpy as np
import math
from dirac import *


'''
----------------------------------
- - - - SINGLE QUBIT GATES - - - -
----------------------------------
'''

'''
Gate superclass
'''
class Gate(object):
    def __init__(self):
        self.circ_n_qubits = None
        pass

    '''
    @brief Setter of the number of qubits in the circuit.
    @param n number of qubits in the whole circuit
    '''
    def set_circuit_n_qubits(self, n: int):
        assert n > 0
        self.circ_n_qubits =  n

    '''
    @brief Getter to the circuit layer matrix
    '''
    def get_matrix(self):
        return None


'''
Superclass for single-qubit gates
'''
class SingleQubitGate(Gate):
    def __init__(self, target_qubit):
        assert target_qubit >= 0

        super(SingleQubitGate, self).__init__()
        self.target_qubit = target_qubit

    '''
    @brief Returns the single-qubit matrix of the gate
    '''
    def my_matrix(self):
        return np.eye(2).astype(np.complex128)

    '''
    @brief Returns the gate's matrix for the whole circuit qubits
    '''
    def get_matrix(self):
        assert self.circ_n_qubits > self.target_qubit
        single_matrix = self.my_matrix()
        assert single_matrix.shape == (2,2)

        matrix_list = []
        for x in range(self.circ_n_qubits):
            if x == self.target_qubit:
                matrix_list.append(single_matrix)
            else:
                matrix_list.append(np.eye(2).astype(np.complex128))
        
        return ket(matrix_list) 


'''
Hadamard gate
'''
class Hadamard(SingleQubitGate):
    def __init__(self, target_qubit):
        super(Hadamard, self).__init__(target_qubit)

    def my_matrix(self):
        return np.array([[1,1],[1,-1]], np.complex128)/math.sqrt(2)

'''
Pauli-X gate
'''
class PauliX(SingleQubitGate):
    def __init__(self, target_qubit):
        super(PauliX, self).__init__(target_qubit)

    def my_matrix(self):
        return np.array([[0,1],[1,0]], np.complex128)/math.sqrt(2)

'''
Pauli-Y gate
'''
class PauliY(SingleQubitGate):
    def __init__(self, target_qubit):
        super(PauliY, self).__init__(target_qubit)

    def my_matrix(self):
        return np.array([[0,-1j],[1j,0]], np.complex128)/math.sqrt(2)

'''
Pauli-Z gate
'''
class PauliZ(SingleQubitGate):
    def __init__(self, target_qubit):
        super(PauliZ, self).__init__(target_qubit)

    def my_matrix(self):
        return np.array([[1,0],[0,-1]], np.complex128)/math.sqrt(2)

'''
Phase gate
'''
class Phase(SingleQubitGate):
    def __init__(self, target_qubit):
        super(Phase, self).__init__(target_qubit)

    def my_matrix(self):
        return np.array([[1,0],[0,1j]], np.complex128)/math.sqrt(2)

'''
T gate
'''
class T(SingleQubitGate):
    def __init__(self, target_qubit):
        super(T, self).__init__(target_qubit)

    def my_matrix(self):
        return np.array([[1,0],[0,1j]], np.complex128)/math.sqrt(2)

'''
---------------------------------
- - - - MULTI QUBIT GATES - - - -
---------------------------------
'''

'''
@brief Controled-NOT gate
'''
class CNot(Gate):
    xor_f = lambda qb, c: ZERO if (qb == c).all() else ONE
    bypass_f = lambda qb, c: qb

    '''
    @param control_qubit index of the control qubit
    @param target_qubit index of the target qubit
    '''
    def __init__(self, control_qubit: int, target_qubit: int):
        assert control_qubit != target_qubit
        assert control_qubit >= 0 and target_qubit >= 0

        super(CNot, self).__init__()
        self.control_qubit = control_qubit
        self.target_qubit = target_qubit

    def get_matrix(self):
        assert self.circ_n_qubits > self.control_qubit
        assert self.circ_n_qubits > self.target_qubit
        gate_logic = []
        
        for i_qbit in range(self.circ_n_qubits):
            if i_qbit == self.target_qubit:
                gate_logic.append(CNot.xor_f)
            else:
                gate_logic.append(CNot.bypass_f)
        
        ans_basis = []
        for numbers in range(2**self.circ_n_qubits):
            qbits = int_to_qubits(numbers, self.circ_n_qubits)
            control_value = qbits[self.control_qubit]
            processed_qbits = []
            
            for x in range(self.circ_n_qubits):
                processed_qbits.append(gate_logic[x](qbits[x], control_value))

            ans_basis.append(ket(processed_qbits))
            
        return np.hstack(ans_basis)

'''
TODO:
    Toffoli gate
'''
