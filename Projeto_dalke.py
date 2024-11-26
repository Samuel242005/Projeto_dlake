import math
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Para manipulação de imagens no Tkinter
from matplotlib.animation import FuncAnimation

# Função para realizar a simulação com animação
def simular_lancamento(v_zero, angulo_0, altura_inicial, ace, r, A, p, c, m, dt):
    # Convertendo o ângulo para radianos
    angulo_0 = math.radians(angulo_0)

    # Componentes da velocidade inicial
    v_zero_x = v_zero * math.cos(angulo_0)
    v_zero_y = v_zero * math.sin(angulo_0)

    # Listas para armazenar os resultados da simulação
    pos_x = [0]
    pos_y = [altura_inicial]
    v_x = [v_zero_x]
    v_y = [v_zero_y]
    tempos = [0]

    # Criar a figura para animação
    fig, ax = plt.subplots(figsize=(10, 5))

    # Carregar imagem de fundo do gráfico
    img1 = mpimg.imread('branco.jpg')  # Substitua pelo caminho da sua imagem
    ax.imshow(img1, aspect='auto', extent=[0, 100, 0, 100], alpha=0.5)

    # Inicializando a linha que será animada
    line, = ax.plot([], [], label='Trajetória do projétil', color='red')

    # Ajustando limites do gráfico
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_title('Trajetória do Projétil com Resistência do Ar')
    ax.set_xlabel('Distância (m)')
    ax.set_ylabel('Altura (m)')
    ax.legend()
    ax.grid(True)

    # Função para atualizar a animação
    def update(frame):
        # Velocidade atual
        v = math.sqrt(v_x[-1]**2 + v_y[-1]**2)

        # Força de arrasto
        Fa = 0.5 * c * A * p * v**2

        # Acelerações
        aceleracao_x = -Fa * v_x[-1] / (m * v)
        aceleracao_y = -ace - Fa * v_y[-1] / (m * v)

        # Atualiza velocidades
        v_x.append(v_x[-1] + aceleracao_x * dt)
        v_y.append(v_y[-1] + aceleracao_y * dt)

        # Atualiza posições
        pos_x.append(pos_x[-1] + v_x[-1] * dt)
        pos_y.append(pos_y[-1] + v_y[-1] * dt)

        # Atualiza o tempo
        tempos.append(tempos[-1] + dt)

        # Verifica se o projétil atingiu o solo
        if pos_y[-1] < 0:
            return line,  # Retorna sem atualizar se a simulação acabou

        # Atualiza os dados do gráfico
        line.set_data(pos_x, pos_y)
        return line,

    # Inicia a animação
    ani = FuncAnimation(fig, update, frames=range(1000), interval=dt*1000, blit=True)

    # Exibindo a animação
    plt.show()

    # Exibindo informações sobre o lançamento
    print(f"Distância máxima atingida: {max(pos_x):.2f} m")
    print(f"Altura máxima atingida: {max(pos_y):.2f} m")
    print(f"Tempo total da trajetória: {max(tempos):.2f} s")

# Função para chamar a simulação com os parâmetros da interface
def iniciar_simulacao():
    # Pegando valores dos campos de entrada
    v_zero = float(entry_v_zero.get())
    angulo_0 = float(entry_angulo.get())
    altura_inicial = float(entry_altura.get())
    ace = float(entry_gravidade.get())
    r = float(entry_raio.get())
    A = float(entry_area.get())
    p = float(entry_densidade.get())
    c = float(entry_coeficiente.get())
    m = float(entry_massa.get())
    dt = float(entry_intervalo.get())
    
    # Chamando a função de simulação
    simular_lancamento(v_zero, angulo_0, altura_inicial, ace, r, A, p, c, m, dt)

# Interface com Tkinter
root = tk.Tk()
root.title("Simulação de Lançamento de Projétil")
root.geometry("400x600")

# Carregar a imagem de fundo para a interface com Tkinter
img2 = Image.open('folha.jpeg')  # Substitua pelo caminho da sua imagem
img2 = img2.resize((400, 600))  # Ajusta o tamanho da imagem para o tamanho da janela
img2_tk = ImageTk.PhotoImage(img2)

# Criar o Canvas para exibir a imagem de fundo
canvas = tk.Canvas(root, width=400, height=600)
canvas.pack(fill="both", expand=True)

# Exibir a imagem de fundo no Canvas
canvas.create_image(0, 0, image=img2_tk, anchor="nw")

# Labels e Entradas sobre o Canvas
ttk.Label(root, text="Velocidade Inicial (m/s):").place(x=20, y=20)
entry_v_zero = ttk.Entry(root)
entry_v_zero.insert(0, "13.0")
entry_v_zero.place(x=180, y=20)

ttk.Label(root, text="Ângulo (graus):").place(x=20, y=60)
entry_angulo = ttk.Entry(root)
entry_angulo.insert(0, "30.0")
entry_angulo.place(x=180, y=60)

ttk.Label(root, text="Altura Inicial (m):").place(x=20, y=100)
entry_altura = ttk.Entry(root)
entry_altura.insert(0, "7.0")
entry_altura.place(x=180, y=100)

ttk.Label(root, text="Gravidade (m/s²):").place(x=20, y=140)
entry_gravidade = ttk.Entry(root)
entry_gravidade.insert(0, "9.8")
entry_gravidade.place(x=180, y=140)

ttk.Label(root, text="Raio da Bola (m):").place(x=20, y=180)
entry_raio = ttk.Entry(root)
entry_raio.insert(0, "0.185")
entry_raio.place(x=180, y=180)

ttk.Label(root, text="Área Transversal (m²):").place(x=20, y=220)
entry_area = ttk.Entry(root)
entry_area.insert(0, "0.107")
entry_area.place(x=180, y=220)

ttk.Label(root, text="Densidade do Ar (kg/m³):").place(x=20, y=260)
entry_densidade = ttk.Entry(root)
entry_densidade.insert(0, "1.2754")
entry_densidade.place(x=180, y=260)

ttk.Label(root, text="Coef. Arrasto:").place(x=20, y=300)
entry_coeficiente = ttk.Entry(root)
entry_coeficiente.insert(0, "0.6")
entry_coeficiente.place(x=180, y=300)

ttk.Label(root, text="Massa da Bola (kg):").place(x=20, y=340)
entry_massa = ttk.Entry(root)
entry_massa.insert(0, "5.0")
entry_massa.place(x=180, y=340)

ttk.Label(root, text="Intervalo de Tempo (s):").place(x=20, y=380)
entry_intervalo = ttk.Entry(root)
entry_intervalo.insert(0, "0.1")
entry_intervalo.place(x=180, y=380)

# Botão para iniciar a simulação
button_simular = ttk.Button(root, text="Simular Lançamento", command=iniciar_simulacao)
button_simular.place(x=140, y=440)

# Iniciar a interface
root.mainloop()
