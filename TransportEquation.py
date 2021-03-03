import numpy as np
import matplotlib.pyplot as plt


L = 2.0 # x = [-1,1]
C = 1.0 # lyambda
T = 1.0 * L / abs(C) # 1 полный оборот начального возмущения
M = 67 # количество узлов вдоль оси
h = L / M # шаг по координате, h
dt = 0.4 * h / abs(C) # коэффициент должен быть меньше единицы
rho = 1 # плотность среды

P_init = 1 #начальное давление в средней трети области
v_init = 1 #начальная скорость в средней трети области
w1_init = rho * C * v_init / 2 + P_init / 2 #компоненты вектора w
w2_init = - rho * C * v_init / 2 + P_init / 2
q_init = np.zeros(M) #это для посторения графика. Пусть обе компоненты вектора q в начале имели значения, равные единице, в средней трети области
for i in range(int(1.0 / 3.0 * M), int(2.0 / 3.0 * M)):
    q_init[i] = 1 

def Transport (w0): #здесь решается уравнение переноса сеточно-характеристическим методом
    w_curr = np.zeros(M)
    w_next = np.zeros(M)
    for i in range(int(1.0 / 3.0 * M), int(2.0 / 3.0 * M)):
        w_curr[i] = w0 # начальное ненулевое значение в средней трети области

    """
    for k in range(int (T / dt)):
        for i in range(M):
            if i == 0  : # периодические граничные условия
                w_next[i] = (w_curr[i+1] -2 * w_curr[i] + w_curr[M-1]) / 2 / (h**2) * (C * dt)**2 - (w_curr[i+1] - w_curr[M-1]) / 2 / h * (C * dt) + w_curr[i]
            elif i == M-1  :
                w_next[i] = (w_curr[0] - 2 * w_curr[i] + w_curr[i-1]) / 2 / (h**2) * (C * dt)**2 - (w_curr[0] - w_curr[i-1]) / 2 / h * (C * dt) + w_curr[i]
            else:
                w_next[i] = (w_curr[i+1] -2 * w_curr[i] + w_curr[i-1]) / 2 / (h**2) * (C * dt)**2 - (w_curr[i+1] - w_curr[i-1]) / 2 / h * (C * dt) + w_curr[i]
        for i in range(M):
            w_curr[i] = w_next[i]
    """
    for k in range(int(T / dt)):
        for i in range(M):
            if i == 0: # периодические граничные условия
                w_next[i] = w_curr[i] - C * dt / h * (w_curr[i] - w_curr[M - 1])
            w_next[i] = w_curr[i] - C * dt / h * (w_curr[i] - w_curr[i - 1])
        for i in range(M):
            w_curr[i] = w_next[i]
    
    return(w_curr)

x_m = np.linspace(-1,L,M) #для построения графика
w1 = Transport(w1_init)
w2 = Transport(w2_init)
P = w1 + w2 #возвращаемся к компонетам вектора q
v = (w1 - w2) / (rho * C)
fig, ax = plt.subplots(2,1)
ax[0].plot(x_m, q_init, '-', label="Начальное значение")
ax[1].plot(x_m, q_init, '-', label="Начальное значение")
ax[0].plot(x_m, P, 'o', label="Итоговое значение")
ax[1].plot(x_m, v, 'o', label="Итоговое значение")
ax[0].set_title("Давление")
ax[1].set_title("Скорость")
for _ in ax:
    _.legend()
plt.show()
