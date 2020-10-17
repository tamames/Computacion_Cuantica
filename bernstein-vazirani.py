"""Este algoritmo sirve para averiguar una cadena de bits, que en este caso
llamaremos s. El algoritmo cuantico presenta ventajas frente al clasico ya que
es capaz de averiguar la cadena en un solo intento, mientras que el algoritmo
clasico tendria que hacer n repeticiones, siendo n el numero de caracteres que
tiene la cadena s.
Para mas informacion sobre el codigo y el algoritmo:
https://qiskit.org/textbook/ch-algorithms/bernstein-vazirani.html"""


# initialization
import matplotlib.pyplot as plt
import numpy as np

# importing Qiskit
from qiskit import IBMQ, BasicAer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute

# import basic plot tools
from qiskit.visualization import plot_histogram

#inicializamos la longitud de nuestra cadena
# ten en cuenta que el simulador llega hata 30 qubits
n=int(input('Introduce el numero de qubits que tiene tu sistema: '))

#creamos una cadena aleatoria, tambien podemos poner nosotros la cadena
#que queramos ( tiene que ser un str de 0 y 1 y con longitud igual a n
t=np.random.randint(0,2**n)
t_bin=bin(t)# transforma el numero en binario pero tiene delante dos caracteres
# que no nos interesan (0b)
s=str(t_bin)[2:] #hay que añadir ceros delante
if len(s)!=n:# nos aseguramos que s tenga n caracteres
    s='0'*(n-len(s))+s


#con esto creamos un circuito cuantico al con n+1 qubits y n registros clasicos
#que utilizaremos para medir
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
#ejecutamos el circuito en un simulador de ordenador cuantico
backend=BasicAer.get_backend('qasm_simulator')
shots=1024
results=execute(bv_circuit,backend=backend,shots=shots).result()
answer=results.get_counts()

plot_histogram(answer)
plt.show()# en jupyter notebook no hace falta esto
