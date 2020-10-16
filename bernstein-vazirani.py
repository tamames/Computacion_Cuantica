# initialization
import matplotlib.pyplot as plt
import numpy as np

# importing Qiskit
from qiskit import IBMQ, BasicAer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute

# import basic plot tools
from qiskit.visualization import plot_histogram

#inicializamos el numero de qubits que necesitamos
n=4#int(input('Introduce el numero de qubits que tiene tu sistema: '))
#creamos una cadena aleatoria
t=np.random.randint(0,2**n)
t_bin=bin(t)
s=str(t_bin)[2:] #hay que añadir ceros delante
if len(s)!=n:
    s='0'*(n-len(s))+s
print(s)



bv_circuit=QuantumCircuit(n+1,n)

#iniciamos el qubit n (output)
bv_circuit.h(n)
bv_circuit.z(n)

#iniciamo el resto de qubits
for i in range(n):
    bv_circuit.h(i)

#separamos el oraculo del resto
bv_circuit.barrier()

#para el oraculo tenemos que dar la vuelta a la cadena secreta
s=s[::-1]
for j in range(n):
    if s[j]=='1':
        bv_circuit.cx(j,n)
    #en la documentacion de quiskit dice que apliques
    #la puerta identidad a s[j]=='0' pero el resultado
    #aparentemente es el mismo, no estoy seguro del todo

bv_circuit.barrier()

#aplicamos H a los qubits
for i in range(n):
    bv_circuit.h(i)

#medimos
for i in range(n):
    bv_circuit.measure(i,i)

#print(bv_circuit.draw())

"""EJECUCION"""

# backend=BasicAer.get_backend('qasm_simulator')
# shots=1024
# results=execute(bv_circuit,backend=backend,shots=shots).result()
# answer=results.get_counts()

#print(s[::-1])

# plot_histogram(answer)
# plt.show()#en jupyter notebook no hace falta esto

"""En un ordenador de verdad"""
# Load our saved IBMQ accounts and get the least busy backend device with less than or equal to 5 qubits
#IBMQ.save_account('1af0e739258540ef3a9638a3d84d6879aa9e0497f755349fb18da8410ff57bbc88036c93628ec87907895b2a39b79f291a8e9fdb13ee32e365955f6183250b0c')
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')
provider.backends()
backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits <= 5 and
                                   x.configuration().n_qubits >= 2 and
                                   not x.configuration().simulator and x.status().operational==True))
print("least busy backend: ", backend)

# Run our circuit on the least busy backend. Monitor the execution of the job in the queue
from qiskit.tools.monitor import job_monitor

shots = 1024
job = execute(bv_circuit, backend=backend, shots=shots)

job_monitor(job, interval = 2)

# Get the results from the computation
results = job.result()
answer = results.get_counts()

plot_histogram(answer)
plt.show()
