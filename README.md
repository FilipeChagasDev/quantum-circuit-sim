# Quantum Circuit Simulator
An ideal quantum circuit simulator, without noise and decoherence.

Version: 0.2.0

By Filipe Chagas

2020

## How to use

1 - Import codes:

```python
import dirac
import gates as qg
import circuit as qc
```

2 - Create the n-qubits circuit object:

```python
number_of_qubits = 2
my_circuit = qc.QuantumCircuit( number_of_qubits )
```

3 - Add gates:

```python

my_circuit.add_gate( qg.Hadamard(0) ) #Hadamard gate at q[0] qubit
my_circuit.add_gate( qg.CNot(0,1) ) #Controled-Not with q[0] control and q[1] target
```

4 - Get results:

```python
result = my_circuit.get_result()
result.print_math()
```

The output is:
```
output state:
|φ〉 = ω0*|00〉 + ω1*|01〉 + ω2*|10〉 + ω3*|11〉

amplitudes:
ω0 = (0.7071067811865475+0j)
ω1 = 0j
ω2 = 0j
ω3 = (0.7071067811865475+0j)

probabilities:
|ω0|² = 0.4999999999999999
|ω1|² = 0.0
|ω2|² = 0.0
|ω3|² = 0.4999999999999999
```

## Available gates
* Hardamard ( target\_qubit )
* Pauli-X ( target\_qubit )
* Pauli-Y ( target\_qubit )
* Pauli-Z ( target\_qubit )
* Phase ( target\_qubit )
* T ( target\_qubit )
* CNot ( control\_qubit , target\_qubit )


