# -*- coding: utf-8 -*-
"""
====================================================================================================
Constants Module - Constantes do sistema

Este módulo contém todas as constantes utilizadas na aplicação,
centralizando valores que podem ser reutilizados em diferentes partes do código.

Data: 13/04/2026
====================================================================================================
"""

import numpy as np

# ==================================================================================================
# CONSTANTES FÍSICAS
# ==================================================================================================

C = 299792458.0                             # Velocidade da luz no vácuo (m/s)
MU0 = 4 * np.pi * 1e-7                      # Permeabilidade do vácuo (H/m)
EPS0 = 8.854187817e-12                      # Permissividade do vácuo (F/m)

# ==================================================================================================
# CONFIGURAÇÕES PADRÃO DA APLICAÇÃO
# ==================================================================================================

DEFAULT_RESOLUTION = 301                    # Resolução padrão da malha (número de pontos por eixo)
DEFAULT_EXTENSION = 2.5                     # Fator de extensão padrão da janela de visualização

# Valores mínimos permitidos
MIN_RESOLUTION = 50
MIN_EXTENSION = 1.2
MIN_DIMENSION_UM = 0.1                      # Dimensão mínima em micrômetros
MIN_WAVELENGTH_UM = 0.1                     # Comprimento de onda mínimo em micrômetros

# Valores máximos permitidos
MAX_EXTENSION = 4.0
MAX_DIMENSION_UM = 100.0                    # Dimensão máxima em micrômetros
MAX_WAVELENGTH_UM = 10.0                    # Comprimento de onda máximo em micrômetros

# ==================================================================================================
# CONSTANTES PARA VALIDAÇÃO DE ÍNDICES DE REFRAÇÃO
# ==================================================================================================

# Limites para índices de refração (materiais ópticos típicos)
MIN_REFRACTIVE_INDEX = 1.0                  # Ar/vácuo
MAX_REFRACTIVE_INDEX = 5.0                  # Materiais semicondutores como Silício/Germânio

# Limites para comprimento de onda (metros)
MIN_WAVELENGTH = MIN_WAVELENGTH_UM * 1e-6   # 0.1 μm (ultravioleta)
MAX_WAVELENGTH = MAX_WAVELENGTH_UM * 1e-6   # 10 μm (infravermelho médio)

# Limites para dimensões do guia (metros)
MIN_DIMENSION = MIN_DIMENSION_UM * 1e-6     # 0.1 μm
MAX_DIMENSION = MAX_DIMENSION_UM * 1e-6     # 100 μm

# ==================================================================================================
# MENSAGENS DA INTERFACE
# ==================================================================================================

# Títulos para caixas de diálogo
ERROR_TITLE = "Erro"
WARNING_TITLE = "Aviso"
INFO_TITLE = "Informação"
SUCCESS_TITLE = "Sucesso"

# Mensagens padrão
MSG_CALCULATION_SUCCESS = "Cálculo realizado com sucesso!"
MSG_SAVE_SUCCESS = "Arquivo salvo com sucesso!"
MSG_EXPORT_SUCCESS = "Dados exportados com sucesso!"

MSG_NO_DATA = "Nenhum dado para salvar. Execute o cálculo primeiro."
MSG_INVALID_PARAMS = "Parâmetros inválidos. Verifique os valores informados."
MSG_CALCULATION_ERROR = "Erro durante o cálculo. Verifique os parâmetros."

# ==================================================================================================
# STRINGS DA APLICAÇÃO
# ==================================================================================================

APP_NAME = "Marcatili Analyzer"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Marcatili Analyzer Team"
APP_DESCRIPTION = "Análise de Guias de Onda Ópticos pelo Método de Marcatili"

# ==================================================================================================
# CORES E ESTILOS (para interface gráfica)
# ==================================================================================================

# Cores principais
COLOR_PRIMARY = "#2c3e50"                 # Azul escuro
COLOR_SECONDARY = "#34495e"               # Azul médio
COLOR_ACCENT = "#3498db"                  # Azul claro
COLOR_SUCCESS = "#27ae60"                 # Verde
COLOR_WARNING = "#f39c12"                 # Laranja
COLOR_ERROR = "#e74c3c"                   # Vermelho
COLOR_BACKGROUND = "#f0f0f0"              # Cinza claro
COLOR_WHITE = "#ffffff"                   # Branco

# Estilos para gráficos
PLOT_CMAP_2D = 'jet'                        # Mapa de cores para campos 2D
PLOT_CMAP_INTENSITY = 'hot'                 # Mapa de cores para intensidade
PLOT_CMAP_CONTOUR = 'viridis'               # Mapa de cores para curvas de nível
PLOT_ALPHA = 0.9                            # Transparência para superfícies 3D

# ==================================================================================================
# CONSTANTES NUMÉRICAS PARA CÁLCULOS
# ==================================================================================================

EPSILON = 1e-10                             # Tolerância para comparações numéricas
SAFE_DIVISOR = 1e-12                        # Valor para evitar divisão por zero

# ==================================================================================================
# LIMITES PARA MODOS DE PROPAGAÇÃO
# ==================================================================================================

# Limites para frequência normalizada V
V_SINGLE_MODE_LOWER = 0.0                   # Modo fundamental
V_SINGLE_MODE_UPPER = np.pi / 2             # Limite aproximado para modo único
V_MULTIMODE_LOWER = np.pi                   # Início da região multimodo

# ==================================================================================================
# CONFIGURAÇÕES PARA EXPORTAÇÃO DE DADOS
# ==================================================================================================

# Formatos de arquivo suportados
SUPPORTED_EXPORT_FORMATS = ['.npz', '.npy', '.txt', '.csv']
DEFAULT_EXPORT_FORMAT = '.npz'

# Extensões para salvamento de imagens
SUPPORTED_IMAGE_FORMATS = ['.png', '.jpg', '.jpeg', '.pdf', '.svg']
DEFAULT_IMAGE_FORMAT = '.png'
DEFAULT_DPI = 300

# ==================================================================================================
# CONFIGURAÇÕES DE PERFORMANCE
# ==================================================================================================

MAX_REAL_TIME_POINTS = 500                  # Máximo de pontos para cálculos em tempo real (evita travamentos)
MAX_MESH_MEMORY_MB = 500                    # Limite de memória para malhas (aproximado em MB)

# ==================================================================================================
# HELP TEXT (para tooltips e documentação)
# ==================================================================================================

HELP_TEXT = {
    'width': 'Largura total do núcleo do guia na direção x (2a).\n'
             'Valores típicos: 2-10 μm para guias ópticos.',
    
    'height': 'Altura total do núcleo do guia na direção y (2b).\n'
              'Valores típicos: 2-10 μm para guias ópticos.',
    
    'wavelength': 'Comprimento de onda da luz no vácuo.\n'
                  'Valores típicos: 0.85 μm (GaAs), 1.31 μm, 1.55 μm (fibras).',
    
    'n_core': 'Índice de refração do núcleo do guia.\n'
              'Exemplos: SiO₂=1.45, Si=3.5, InP=3.17, GaAs=3.39.',
    
    'n_cladding': 'Índice de refração do revestimento.\n'
                  'Deve ser menor que o índice do núcleo.',
    
    'mode_x': 'Número do modo na direção x (p).\n'
              '0=modo fundamental, 1=primeiro modo, etc.',
    
    'mode_y': 'Número do modo na direção y (q).\n'
              '0=modo fundamental, 1=primeiro modo, etc.',
    
    'polarization': 'Tipo de polarização do campo elétrico.\n'
                    'TE: Campo elétrico polarizado em x.\n'
                    'TM: Campo elétrico polarizado em y.',
    
    'resolution': 'Número de pontos na malha de cálculo.\n'
                  'Maior resolução = mais preciso, porém mais lento.\n'
                  'Recomendado: 201-401 pontos.',
    
    'extension': 'Fator de extensão da janela de visualização.\n'
                 'Define o quanto além do núcleo a simulação se estende.\n'
                 'Recomendado: 2.0-3.0.'
}

# ==================================================================================================
# FUNÇÕES AUXILIARES
# ==================================================================================================

def get_version_string():
    """Retorna string formatada com versão da aplicação"""
    return f"{APP_NAME} v{APP_VERSION}"

def get_copyright_string():
    """Retorna string de copyright"""
    return f"© 2024-2025 {APP_AUTHOR}. Todos os direitos reservados."

def get_window_title():
    """Retorna título formatado para janela principal"""
    return f"{APP_NAME} - {APP_DESCRIPTION}"

# ==================================================================================================
# EXPORTAÇÃO
# ==================================================================================================

# Esta seção lista tudo o que será exportado quando usar
# "from utils.constants import *"
__all__ = [
    # Constantes físicas
    'C', 'MU0', 'EPS0',
    
    # Configurações padrão
    'DEFAULT_RESOLUTION', 'DEFAULT_EXTENSION',
    'MIN_RESOLUTION', 'MAX_EXTENSION', 'MIN_EXTENSION',
    'MIN_DIMENSION_UM', 'MAX_DIMENSION_UM',
    'MIN_WAVELENGTH_UM', 'MAX_WAVELENGTH_UM',
    
    # Constantes para validação
    'MIN_REFRACTIVE_INDEX', 'MAX_REFRACTIVE_INDEX',
    'MIN_WAVELENGTH', 'MAX_WAVELENGTH',
    'MIN_DIMENSION', 'MAX_DIMENSION',
    
    # Mensagens
    'ERROR_TITLE', 'WARNING_TITLE', 'INFO_TITLE', 'SUCCESS_TITLE',
    'MSG_CALCULATION_SUCCESS', 'MSG_SAVE_SUCCESS', 'MSG_EXPORT_SUCCESS',
    'MSG_NO_DATA', 'MSG_INVALID_PARAMS', 'MSG_CALCULATION_ERROR',
    
    # Strings da aplicação
    'APP_NAME', 'APP_VERSION', 'APP_AUTHOR', 'APP_DESCRIPTION',
    
    # Cores e estilos
    'COLOR_PRIMARY', 'COLOR_SECONDARY', 'COLOR_ACCENT',
    'COLOR_SUCCESS', 'COLOR_WARNING', 'COLOR_ERROR',
    'COLOR_BACKGROUND', 'COLOR_WHITE',
    'PLOT_CMAP_2D', 'PLOT_CMAP_INTENSITY', 'PLOT_CMAP_CONTOUR', 'PLOT_ALPHA',
    
    # Constantes numéricas
    'EPSILON', 'SAFE_DIVISOR',
    
    # Limites para modos
    'V_SINGLE_MODE_LOWER', 'V_SINGLE_MODE_UPPER', 'V_MULTIMODE_LOWER',
    
    # Configurações de exportação
    'SUPPORTED_EXPORT_FORMATS', 'DEFAULT_EXPORT_FORMAT',
    'SUPPORTED_IMAGE_FORMATS', 'DEFAULT_IMAGE_FORMAT', 'DEFAULT_DPI',
    
    # Configurações de performance
    'MAX_REAL_TIME_POINTS', 'MAX_MESH_MEMORY_MB',
    
    # Help text
    'HELP_TEXT',
    
    # Funções utilitárias
    'get_version_string', 'get_copyright_string', 'get_window_title'
]