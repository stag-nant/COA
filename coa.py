# COA
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, IBMQ, execute
import qiskit_ibm_provider
import numpy as np

def real_map(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Scale the value to the 0-1 range
    valueScaled = (value - leftMin) / leftSpan

    # Map the value to the output range
    mappedValue = rightMin + (valueScaled * rightSpan)

    return mappedValue


def QRandom(a, b):
    qubits = 3
    q = QuantumRegister(qubits, 'q')
    circ = QuantumCircuit(q)
    c0 = ClassicalRegister(qubits, 'c0')
    circ.add_register(c0)

    for i in range(qubits):
        circ.h(q[i])

    for i in range(qubits):
        circ.measure(q[i], c0[i])


    IBMQ.save_account('d5a19667912f47144f990473b995ea95291db5ea6c044f5904c80b5d9649cbd2a94340aa5da159f0319a205f5ec664b91fbca8d08945a5c6db9d7662f7ec6106',overwrite=True)
    # Load your IBM Quantum account credentials
    IBMQ.load_account()  # Make sure you have your API token set up in your IBM Quantum account.

    provider = IBMQ.get_provider('ibm-q')
    backend = provider.get_backend('simulator_statevector')  

    # Execute the circuit on the chosen quantum computer
    job = execute(circ, backend=backend, shots=1024)  # Set shots to 1 to get a single measurement outcome

    # Monitor the job
    from qiskit.tools.monitor import job_monitor
    job_monitor(job)

    # Get the result of the job
    result = job.result()

    # Get the counts of each measurement outcome
    counts = result.get_counts()
    
    # Extract the measurement outcome (bitstring)
    outcome = list(counts.keys())[0]

    # Convert the bitstring to a decimal integer
    random_number = int(outcome, 2)

    # Map the random number to the desired range [a, b]
    mapped_number = real_map(random_number, 0, 2**qubits - 1, a, b)

    return mapped_number

a = int(input("Enter minimum:"))
b = int(input("Enter maximum:"))
print(QRandom(a, b))
