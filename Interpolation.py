# Импортируем numpy для хранения результатов расчётов
import numpy as np

# Импортируем модуль matplolib для визуализации результатов
import matplotlib.pyplot as plt
            
# С-х метод на примере 1D уравнения переноса
L = 2.0 # x = [-1,1]
CX = 1.0 # lyambdaX
CY = 1.0 # lyambdaY
T = 5.0 * L / min(abs(CX), abs(CY)) # 1 полный оборот начального возмущения
M = 41 # количество узлов вдоль оси
nx = M
ny = M
h = L / M # шаг по координате, h
dt = 0.4 * h / max(abs(CX), abs(CY))  # коэффициент должен быть меньше единицы

# dtype=[('p', np.float64), ('vx', np.float64)] - имя переменной, тип переменной.
# Скалярное уравнение, но двумерное. Все равно в узле 1 значение.
data_current = np.zeros((M, M), dtype=[('q', np.float64)])
data_next = np.zeros((M, M), dtype=[('q', np.float64)])

# Начальные значения
for j in range(ny):
    for i in range(nx):
        if (i > nx / 3.0) and (i < 2.0 * nx / 3.0) and (j > ny / 3.0) and (j < 2.0 * ny / 3.0):
            data_current[j, i]['q'] = 1.0

# Расчёт
for k in range(int(T / dt)):
    # Шаг по X
    for j in range(ny):
        for i in range(nx):
            if i == 0: # периодические граничные условия
                data_next[j, i]['q'] = (data_current[j,i+1]['q'] -2 * data_current[j,i]['q'] + data_current[j,M-1]['q']) / 2 / (h**2) * (CX * dt)**2 - (data_current[j,i+1]['q'] - data_current[j,M-1]['q']) / 2 / h * (CX * dt) + data_current[j,i]['q']
            elif i == M-1:
                data_next[j, i]['q'] = (data_current[j,0]['q'] -2 * data_current[j,i]['q'] + data_current[j,i-1]['q']) / 2 / (h**2) * (CX * dt)**2 - (data_current[j,0]['q'] - data_current[j,i-1]['q']) / 2 / h * (CX * dt) + data_current[j,i]['q']
            else:
                data_next[j, i]['q'] = (data_current[j,i+1]['q'] -2 * data_current[j,i]['q'] + data_current[j,i-1]['q']) / 2 / (h**2) * (CX * dt)**2 -  (data_current[j,i+1]['q'] - data_current[j,i-1]['q']) / 2 / h * (CX * dt) + data_current[j,i]['q']
            #data_current[j, i]['q'] = data_next[j, i]['q']

    
    # Шаг по Y
    for i in range(nx):
        for j in range(ny):
            if j == 0: # периодические граничные условия
                data_current[j, i]['q'] = (data_next[j+1,i]['q'] -2 * data_next[j,i]['q'] + data_next[M-1,i]['q']) / 2 / (h**2) * (CY * dt)**2 - (data_next[j+1,i]['q'] - data_next[M-1,i]['q']) / 2 / h * (CY * dt) + data_next[j,i]['q']
            elif j == M-1:
                data_current[j, i]['q'] = (data_next[0,i]['q'] -2 * data_next[j,i]['q'] + data_next[j-1,i]['q']) / 2 / (h**2) * (CY * dt)**2 - (data_next[0,i]['q'] - data_next[j-1,i]['q']) / 2 / h * (CY * dt) + data_next[j,i]['q']
            else:
                data_current[j, i]['q'] = (data_next[j+1,i]['q'] -2 * data_next[j,i]['q'] + data_next[j-1,i]['q']) / 2 / (h**2) * (CY * dt)**2 - (data_next[j+1,i]['q'] - data_next[j-1,i]['q']) / 2 / h * (CY * dt) + data_next[j,i]['q']       
    #Монотонизация
    for i in range(1, nx-1):
        if data_current[j,i]['q'] > max(data_current[j,i-1]['q'], data_current[j,i+1]['q']):
            data_current[j,i]['q'] = max(data_current[j,i-1]['q'], data_current[j,i+1]['q'])
        elif data_current[j,i]['q'] < min(data_current[j,i-1]['q'], data_current[j,i+1]['q']):
            data_current[j,i]['q'] = min(data_current[j,i-1]['q'], data_current[j,i+1]['q'])
    for j in range(1, ny-1):
        if data_current[j,i]['q'] > max(data_current[j-1,i]['q'], data_current[j+1,i]['q']):
            data_current[j,i]['q'] = max(data_current[j-1,i]['q'], data_current[j+1,i]['q'])
        elif data_current[j,i]['q'] < min(data_current[j-1,i]['q'], data_current[j+1,i]['q']):
            data_current[j,i]['q'] < min(data_current[j-1,i]['q'], data_current[j+1,i]['q'])

# Отображение 2Д данных цветом
fig, ax = plt.subplots()
ax.set_title('Распределение концетрации')
_ = ax.set_xlabel('Горизонталь OX, м')
_ = ax.set_ylabel('Вертикаль OY, м')
img = ax.imshow(data_current['q'], vmin = 0, vmax = 1, origin = 'lower')
_ = fig.colorbar(img)
plt.show()

