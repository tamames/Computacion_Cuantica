# importing Qiskit
from qiskit import IBMQ, BasicAer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, execute

# import basic plot tools
from qiskit.visualization import plot_histogram
from qiskit_textbook.tools import simon_oracle

# import other things
from numpy.random import randint

def oraculo(b,n):

    # qiskit ya tiene un oraculo de simon implementado pero queria construir
    # el mio propio

    # primero definimos el circuito cuantico
    oracle=QuantumCircuit(2*n)

    # definimos un nuevo str que es igual a b pero al reves, nos servira para
    # luego
    b_invertido=b[::-1]

    # primero copiamos el estado de los qubits input a los qubits output
    for i in range(n):
        oracle.cx(i,n+i)

    # si la cadena es '00...0' no hace falta hacer nada mas, la funcion es 1-to-1
    if b=='0'*n:
        return oracle

    # chequear cual es la ultima cifra de b distinta de cero y tomar ese qubit
    # como qubit de partida de las siguientes CNOT y el target son las posiciones
    # i /b[i]=='1' pero dadas la vuelta (b_invertido)

    # asi designamos cual es el ultimo bit de b distinto de cero y tomamos ese
    # numero como la posicion del qubit control
    for i in range(len(b)):
        if b_invertido[i]=='1':
            pos_control=i
            break

    # para los qubit target necesitamos los valores de b_invertido que son '1'
    pos_target=[]
    for i in range(len(b_invertido)):
        if b_invertido[i]=='1':
            pos_target.append(i)
        else:
            continue

    # construimos las CNOT finales
    for i in pos_target:
        oracle.cx(pos_control,n+i)


    return oracle




n=4# int(input('Introduce el numero de caracteres de tu str: '))

# se genera una cadena de longitud n aleatoria de 0 y 1
# t=randint(2,size=n)
# b=''.join([str(i) for i in t])
b='0000'

# simon=QuantumCircuit(2*n,n)
#
# #aplicamos Hadamard a todo
# simon.h(range(n))
#
# simon.barrier()
#
# simon+=simon_oracle(b)
#hemos descubierto como funciona el oraculo de simon, EUREKAA!!

print(b,'\n QISKIT \n')
k=simon_oracle(b)
print(k.draw())
print('\n\n MIO \n')
j=oraculo(b,n)
print(j.draw())
