# MarcatiliKawanoGUI – Simulador de Guias de Onda Retangulares (Método de Marcatili)

Este software implementa o método analítico aproximado de Marcatili (conforme Kawano & Kitoh, 2001) para cálculo dos modos de propagação em guias de onda retangulares assimétricos. O programa possui interface gráfica (GUI) desenvolvida em Python, permitindo a definição dos parâmetros do guia, a resolução das equações de dispersão e a visualização dos campos elétricos (cortes 2D e superfície 3D).

## Tecnologias e Bibliotecas Utilizadas

| Tecnologia/Biblioteca  | Versão mínima | Finalidade                               |
| ---------------------- | ------------- | ---------------------------------------- |
| Python                 | 3.8           | Linguagem principal                      |
| NumPy                  | 1.21          | Operações matemáticas e vetoriais        |
| SciPy                  | 1.7           | Otimização (método da bisseção)          |
| Matplotlib             | 3.4           | Visualização dos campos (2D, cortes, 3D) |
| Tkinter                | (nativa)      | Interface gráfica                        |
| PyInstaller (opcional) | 5.0           | Geração de executável via `build.py`     |

## Estrutura do Projeto

MarcatiliKawanoGUI/
├── marcatili_gui.py # Código principal da interface e lógica de cálculo
├── build.py # Script para gerar executável com PyInstaller
├── figuras/ # Diretório para salvar gráficos (opcional)
└── README.md # Este arquivo

## Instalação e Execução

### Linux (Ubuntu/Debian)

1. **Instalar Python e pip** (se ainda não tiver):

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-tk

   ```

2. **Instalar as depêndências**:

   ```bash
   pip3 install numpy scipy matplotlib

   ```

3. **Execução do programa**:
   ```bash
   python3 marcatili_gui.py
   ```

### Windows

1. **nstalar Python** – Baixe e instale o Python 3.8+ em python.org. **Marque a opção “Add Python to PATH”** durante a instalação.

2. **Abrir o Prompt de Comando (cmd)** e instalar as dependências:

   ```cmd
   pip install numpy scipy matplotlib

   ```

3. **Execução do programa**:
   ```cmd
   python marcatili_gui.py
   ```

## Gerando um Executável Independente (build.py)

O arquivo build.py utiliza o PyInstaller para criar um executável que pode ser distribuído sem necessidade de ambiente Python. Se o script não existir ou estiver desatualizado, utilize o seguinte conteúdo (corrigido e otimizado):

# build.py

import PyInstaller.**main**
import sys
import platform

APP_NAME = "MarcatiliKawanoGUI"
MAIN_SCRIPT = "marcatili_gui.py"

if platform.system() == "Windows":
suffix = ".exe"
console_arg = "--console" # ou "--noconsole" para janela sem terminal
else:
suffix = ""
console_arg = "--console"

PyInstaller.**main**.run([
MAIN_SCRIPT,
"--name", APP_NAME,
"--onefile",
console_arg,
"--add-data", "marcatili_gui.py;.",
"--hidden-import", "numpy",
"--hidden-import", "scipy",
"--hidden-import", "matplotlib",
"--clean"
])

## Como usar:

    Instale o PyInstaller: pip install pyinstaller

    Execute no terminal: python build.py

    O executável será gerado em dist/MarcatiliKawanoGUI (Windows) ou dist/MarcatiliKawanoGUI (Linux – sem extensão).

    Nota: No Linux, o executável gerado pode precisar de permissão de execução: chmod +x dist/MarcatiliKawanoGUI

## Corrigindo Possíveis Problemas no build.py Original:

Caso o build.py original apresente erros, verifique:

    Caminhos errados – Substitua "marcatili_gui.py;." pelo caminho correto do script principal.

    Falta de dependências ocultas – Adicione --hidden-import para numpy, scipy, matplotlib, tkinter (embora tkinter seja nativo, pode ser necessário forçar).

    Modo console vs. janela – Use --noconsole se quiser ocultar a janela do terminal (apenas para GUI). Em Windows, isso evita uma janela extra.

    Multiplataforma – O script acima detecta o sistema operacional e ajusta o nome do executável automaticamente.

## Utilização do Programa

1. **Preencha os parâmetros:**
   - Índices do núcleo e dos quatro revestimentos (n1 a n5)
   - Meia-largura (a) e meia-altura (b) do núcleo (em µm)
   - Comprimento de onda (lambda, em µm)
   - Ordens modais p (direção x) e q (direção y)
   - Polarização (quasi-TE ou quasi-TM)
   - Resolução da malha e extensão da janela de visualização

2. **Clique em "CALCULAR"** – O programa resolverá as equações transcendentais de dispersão e exibirá:

   -Números de onda transversais kx, ky
   -Constante de propagação beta e índice efetivo neff
   -Constantes de decaimento nos revestimentos
   -Status do modo (guiado ou em corte)

3. **Visualização** – Serão mostrados automaticamente:

   -Mapa de contorno 2D do campo (Ex ou Ey)
   -Cortes horizontais (y=0) e verticais (x=0)
   -Superfície 3D do campo (gráfico interativo)

**Referência Teórica**

    Kawano, K. & Kitoh, T. (2001). Introduction to Optical Waveguide Analysis. John Wiley & Sons.
    Método de Marcatili – Seção 2.3 do livro.

**Autoria e Desenvolvimento**

_Fábio Luís Guia da Conceição_

Contribuições:
Implementação completa do método de Marcatili em Python.
Desenvolvimento da interface gráfica (MarcatiliKawanoGUI).
Integração das rotinas numéricas (bisseção, resolução das equações transcendentais).
Geração das visualizações 2D e 3D dos campos modais.
