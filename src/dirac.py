'''
Author: Filipe Chagas
Email: filipe.ferraz@gmail.com
GitHub: github.com/filipechagasdev
June 2020
'''

import numpy as np 
import math

#Qubit basis
ZERO = np.array([[1],[0]],np.complex128)
ONE = np.array([[0],[1]],np.complex128)
PLUS = (ZERO + ONE)/math.sqrt(2)
MINUS = (ZERO - 1j*ONE)/math.sqrt(2)
CLOCKWISE = (ZERO + ONE)/math.sqrt(2)
COUNTERCLOCKWISE = (ZERO - 1j*ONE)/math.sqrt(2)

BASIS_DICT = {
    0: ZERO,
    '0': ZERO,
    1: ONE,
    '1': ONE,
    '+': PLUS,
    '-': MINUS,
    '->': CLOCKWISE,
    'cw': CLOCKWISE,
    'clockwise': CLOCKWISE,
    '<-': COUNTERCLOCKWISE,
    'ccw': COUNTERCLOCKWISE,
    'counterclockwise': COUNTERCLOCKWISE
}

'''
@brief Kron product of a list
@param lst list of numpy vectors [v_n, v_n-1, ..., v3, v2, v1, v0]
@return kron product (v_n <x> ( ... <x> (v3 <x> (v2 <x> (v1 <x> v0)))))
'''
def recursive_kron(lst):
    if len(lst) == 2:
        return np.kron(lst[0],lst[1])
    elif len(lst) > 2:
        a = lst[0]
        return np.kron(a, recursive_kron(lst[1:]))
    else:
        raise Exception("argument list/tuple must have len>=2")

'''
@brief Returns ket vectors for quantum states such as |1>, |0>, |a,b,...,c>
@param states Symbols to the quantum basis (1, 0, '1', '0', '+', '-', '->', '<-') or vectors of symbols for kron products
'''
def ket(states):
    if isinstance(states, np.ndarray):
        return states
    elif isinstance(states, list) or isinstance(states, tuple):
        return recursive_kron(states)
    elif isinstance(states, int) or isinstance(states, str):
        return BASIS_DICT[states]        

'''
@brief Convert Natural numbers to qubit sequences
@param val Natural number
@param n_qubits Number of qubits for the sequence
@return list: [|qubit_{2^n}>, |qubit_{2^(n-1)}>, ..., |qubit_2^0>]
'''
def int_to_qubits(val, n_qubits):
    assert val >= 0
    binary = bin(val).split('b')[1]
    blen = len(binary)
    if blen > n_qubits:
        raise Exception('Cannot fit ' + str(val) + ' into ' + str(n_qubits) + ' qubits')
    elif blen < n_qubits:
        binary = '0'*(n_qubits - blen) + binary

    return [BASIS_DICT[x] for x in list(binary)]