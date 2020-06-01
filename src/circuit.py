'''
Author: Filipe Chagas
Email: filipe.ferraz@gmail.com
GitHub: github.com/filipechagasdev
June 2020
'''

import numpy as np
import dirac
import gates

class TestResult(object):
    def __init__(self):
        self.basis_list = []
        self.ket_list = []
        self.amplitude_list = []
        self.probability_list = []

    '''
    @brief print to the terminal a math representation of the results
    '''
    def print_math(self):
        #First, build expression string
        state_str = u'|φ〉 = '

        for n in range(len(self.basis_list)):
            state_str += u'ω' + str(n) + '*|' + self.ket_list[n] + u'〉'
            if n < (len(self.basis_list)-1):
                state_str += ' + '

        print('output state:')
        print(state_str) #print expression string

        #print omega's values
        print('\namplitudes:')
        for n in range(len(self.basis_list)):
            print(u'ω' + str(n) + ' = ' + str(self.amplitude_list[n]))

        #print probabilitys
        print('\nprobabilities:')
        for n in range(len(self.basis_list)):
            print(u'|ω' + str(n) + u'|² = ' + str(self.probability_list[n]))
        
    
class QuantumCircuit(object):
    '''
    @param n_qubits Number of qubits
    '''
    def __init__(self, n_qubits):
        assert n_qubits > 0
        self.n_qubits = n_qubits
        self.gates = []
        self.circuit_matrix = dirac.ket([np.eye(2)]*n_qubits)

    '''
    @brief Add a gate to the circuit
    @param gate Gate object
    '''
    def add_gate(self, gate: gates.Gate):
        gate.set_circuit_n_qubits(self.n_qubits)
        self.gates.append(gate)
    
    '''
    @brief Internal method. Set the circuit's matrix to identity
    '''
    def ___load_identity__(self):
        self.circuit_matrix = dirac.ket([np.eye(2).astype(np.complex128)]*self.n_qubits)


    '''
    @brief Internal method. Generate the circuit's matrix
    '''
    def __gen_matrix__(self):
        self.___load_identity__()
        reverse_gates = self.gates.copy()
        reverse_gates.reverse()
        for gate in reverse_gates:
            self.circuit_matrix = self.circuit_matrix.dot(gate.get_matrix())

    '''
    @brief Get the output state vector of the circuit for a input state vector.
    @param input_vec Input state vector
    @return Output state vector
    '''
    def process(self, input_vec: np.ndarray) -> np.ndarray:
        self.__gen_matrix__()
        return self.circuit_matrix.dot(input_vec)

    '''
    @brief Get the output state vector with all input qubits in |0> state.
    @return Output state vector
    '''
    def process_default_input(self) -> np.ndarray:
        input = dirac.ket([dirac.ZERO]*self.n_qubits)
        output = self.process(input)
        return output
    
    '''
    @brief Get a TestResult object with the circuit results (basis, amplitudes and probabilities).
    @return The TestResult object with the results
    '''
    def get_result(self) -> TestResult:
        output = self.process_default_input()
        amp_list = list(output[:,0])
        
        result = TestResult()

        for n in range(len(amp_list)):
            result.basis_list.append(dirac.int_to_qubits(n, self.n_qubits))
            bin_str = bin(n).split('b')[1]
            result.ket_list.append('0'*(self.n_qubits - len(bin_str)) + bin_str) 
            result.amplitude_list.append(amp_list[n])
            result.probability_list.append(abs(amp_list[n])**2)
        
        return result
