# -*- coding: utf-8 -*-
"""
====================================================================================================
Utils Package - Responsável por funções utilitárias e constantes

Este pacote contém funções auxiliares, constantes do sistema
e utilitários gerais usados em toda a aplicação.

Data: 13/04/2026
====================================================================================================
"""

from utils.constants import (
    # Constantes físicas
    C,
    MU0,
    EPS0,
    
    # Configurações padrão
    DEFAULT_RESOLUTION,
    DEFAULT_EXTENSION,
    MIN_RESOLUTION,
    MAX_EXTENSION,
    MIN_EXTENSION,
    
    # Constantes para validação
    MIN_REFRACTIVE_INDEX,
    MAX_REFRACTIVE_INDEX,
    MIN_WAVELENGTH,
    MAX_WAVELENGTH,
    MIN_DIMENSION,
    MAX_DIMENSION,
    
    # Mensagens
    ERROR_TITLE,
    WARNING_TITLE,
    INFO_TITLE,
    SUCCESS_TITLE,
    
    # Strings de interface
    APP_NAME,
    APP_VERSION,
    APP_AUTHOR,
    APP_DESCRIPTION
)

__all__ = [
    # Constantes físicas
    'C',
    'MU0', 
    'EPS0',
    
    # Configurações padrão
    'DEFAULT_RESOLUTION',
    'DEFAULT_EXTENSION',
    'MIN_RESOLUTION',
    'MAX_EXTENSION',
    'MIN_EXTENSION',
    
    # Constantes para validação
    'MIN_REFRACTIVE_INDEX',
    'MAX_REFRACTIVE_INDEX',
    'MIN_WAVELENGTH',
    'MAX_WAVELENGTH',
    'MIN_DIMENSION',
    'MAX_DIMENSION',
    
    # Mensagens
    'ERROR_TITLE',
    'WARNING_TITLE',
    'INFO_TITLE',
    'SUCCESS_TITLE',
    
    # Strings de interface
    'APP_NAME',
    'APP_VERSION',
    'APP_AUTHOR',
    'APP_DESCRIPTION'
]

__version__ = '1.0.0'
__author__ = 'Marcatili Analyzer Team'
__description__ = 'Utilitários e constantes para análise Marcatili'