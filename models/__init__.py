# -*- coding: utf-8 -*-
"""
====================================================================================================
Models Package - Responsible for data models and physical calculations

This package contains the classes that represent the application's data and business logic,
following the principle of separation of concerns.

Data: 13/04/2026
====================================================================================================
"""

from models.waveguide import (
    WaveguideParameters,
    WaveguideResults,
    WaveguideModel,
    Polarization
)

__all__ = [
    'WaveguideParameters',
    'WaveguideResults', 
    'WaveguideModel',
    'Polarization'
]

__version__ = '1.0.0'
__author__ = 'Marcatili Analyzer Team'
__description__ = 'Modelos para análise de guias de onda pelo método de Marcatili'