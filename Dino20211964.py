"""
Práctica 3: Sistema Musculoesquelético

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Dino Seanez Victor Silvano
Número de control: 20211964
Correo institucional: l20211964@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Parámetros
F0 = 1.0
alpha = 0.25
Cp = 100e-6
R_control = 100
R_caso = 10e3

# Tiempo (igual que Simulink)
t = np.arange(0, 15.001, 1e-3)

# Entrada
A = F0 / (1 + alpha)
F = np.zeros_like(t)
F[(t >= 1) & (t <= 2)] = A

# Modelo RC discreto
def rc_ce(u, t, tau):
    y = np.zeros_like(u)
    dt = t[1] - t[0]
    a = np.exp(-dt / tau)
    for k in range(1, len(t)):
        y[k] = a * y[k - 1] + (1 - a) * u[k - 1]
    return y

# Modelo función de transferencia
def rc_ft(u, t, tau):
    sys = signal.TransferFunction([1], [tau, 1])
    _, y, _ = signal.lsim(sys, U=u, T=t)
    return y

# Constantes de tiempo
tau_control = R_control * Cp
tau_caso = R_caso * Cp

# Señales
Pp1 = rc_ft(F, t, tau_control)   # Control FT
Pp2 = rc_ce(F, t, tau_control)   # Control CE
Pp3 = rc_ft(F, t, tau_caso)      # Caso FT

# PID
def pid_response(u, t, tau, Kp, Ki, Kd):
    num = [Kd, Kp, Ki]
    den = [tau + Kd, 1 + Kp, Ki]
    sys = signal.TransferFunction(num, den)
    _, y, _ = signal.lsim(sys, U=u, T=t)
    return y

PID1 = pid_response(F, t, tau_caso, 45, 120, 0.02)

# ----------- GRÁFICAS (igual a MATLAB) -------------

plt.rcParams['font.family'] = 'serif'

fig = plt.figure(figsize=(10, 8), facecolor='white')

# Subplot 1
plt.subplot(2,1,1)
plt.plot(t, F, '-', label='Entrada')
plt.plot(t, Pp1, '-', label='F(t): Control FT')
plt.plot(t, Pp2, ':', linewidth=2, label='F(t): Control CE')

plt.xlim(0,10)
plt.ylim(-0.2,1.2)
plt.xticks(np.arange(0,11,1))
plt.yticks(np.arange(-0.2,1.21,0.2))

plt.xlabel('t [s]')
plt.ylabel('F(t) [V]')
plt.title('Entrada vs Control')
plt.legend(loc='upper center', ncol=3, frameon=False)

# Subplot 2
plt.subplot(2,1,2)
plt.plot(t, Pp1, '-', label='F(t): Control')
plt.plot(t, Pp3, '-', label='F(t): Caso')
plt.plot(t, PID1, ':', linewidth=2, label='PID(t): Caso')

plt.xlim(0,10)
plt.ylim(-0.2,1.2)
plt.xticks(np.arange(0,11,1))
plt.yticks(np.arange(-0.2,1.21,0.2))

plt.xlabel('t [s]')
plt.ylabel('F(t) [V]')
plt.title('Control vs Caso')
plt.legend(loc='upper center', ncol=3, frameon=False)

plt.tight_layout()
plt.savefig('Musculoesqueletico_python.pdf')
plt.show()
