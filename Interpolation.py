import numpy as np
import matplotlib.pyplot as plt

# С-х метод на примере 1D уравнения переноса
L = 2.0 # x = [-1,1]
C = 1.0 # lyambda
T = 1.0 * L / abs(C) # 1 полный оборот начального возмущения
M = 2100 # количество узлов вдоль оси
h = L / M # шаг по координате, h
dt = 0.4 * h / abs(C) # коэффициент должен быть меньше единицы
q_curr = np.zeros(M)
q_next = np.zeros(M)
for i in range(int(1.0 / 3.0 * M), int(2.0 / 3.0 * M)):
    q_curr[i] = 1.0 # начальное ненулевое значение в средней трети области

# Рисуем график до начала расчёта
x_m = np.linspace(-1.0, L, M)
plt.plot(x_m, q_curr, label="Начальное значение")

for j in range(int (T / dt)):
    for i in range(M):
        if i == 0  : # периодические граничные условия
            q_next[i] = (q_curr[i+1] -2 * q_curr[i] + q_curr[M-1]) / 2 / (h**2) * (C * dt)**2 - (q_curr[i+1] - q_curr[M-1]) / 2 / h * (C * dt) + q_curr[i]
        elif i == M-1  :
            q_next[i] = (q_curr[0] - 2 * q_curr[i] + q_curr[i-1]) / 2 / (h**2) * (C * dt)**2 - (q_curr[0] - q_curr[i-1]) / 2 / h * (C * dt) + q_curr[i]
            
        else:
            q_next[i] = (q_curr[i+1] -2 * q_curr[i] + q_curr[i-1]) / 2 / (h**2) * (C * dt)**2 - (q_curr[i+1] - q_curr[i-1]) / 2 / h * (C * dt) + q_curr[i]
    for i in range(M):
        q_curr[i] = q_next[i]
"""

for j in range(int(T / dt)):
    for i in range(M):
        if i == 0: # периодические граничные условия
            q_next[i] = q_curr[i] - C * dt / h * (q_curr[i] - q_curr[M - 1])
        q_next[i] = q_curr[i] - C * dt / h * (q_curr[i] - q_curr[i - 1])
    for i in range(M):
        q_curr[i] = q_next[i]
 """   
# Рисуем график по окончанию расчёта
plt.plot(x_m, q_curr, 'o', label="Итоговое значение")
plt.legend()
plt.show()
