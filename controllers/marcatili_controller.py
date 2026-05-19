# -*- coding: utf-8 -*-
"""
====================================================================================================
Controller - Gerencia a comunicação entre Model e View
Implementa o padrão MVC com observers

Data: 14/04/2026
====================================================================================================
"""

import numpy as np
from typing import Optional, Callable
from models.waveguide import WaveguideParameters, WaveguideModel, Polarization, WaveguideResults


class MarcatiliController:
    """
    Controlador principal da aplicação
    Gerencia o estado da aplicação e coordena as operações
    """
    
    def __init__(self):
        self._params: Optional[WaveguideParameters] = None
        self._model: Optional[WaveguideModel] = None
        self._results: Optional[WaveguideResults] = None
        self._observers: list = []
    
    def add_observer(self, callback: Callable):
        """Adiciona um observer para notificações de mudança"""
        self._observers.append(callback)
    
    def _notify_observers(self):
        """Notifica todos os observers sobre mudanças"""
        for callback in self._observers:
            callback()
    
    def set_parameters(self, width_um: float, height_um: float, wavelength_um: float,
                      n_core: float, n_cladding: float, mode_x: int, mode_y: int,
                      polarization: int, resolution: int, extension: float) -> bool:
        """
        Define os parâmetros do guia de onda
        
        Returns:
            bool: True se os parâmetros são válidos
        """
        try:
            self._params = WaveguideParameters(
                width=width_um * 1e-6,
                height=height_um * 1e-6,
                wavelength=wavelength_um * 1e-6,
                n_core=n_core,
                n_cladding=n_cladding,
                mode_x=mode_x,
                mode_y=mode_y,
                polarization=Polarization.TE if polarization == 1 else Polarization.TM,
                resolution=resolution,
                extension=extension
            )
            self._notify_observers()
            return True
        except ValueError as e:
            raise ValueError(f"Parâmetros inválidos: {str(e)}")
    
    def calculate(self):
        """Executa o cálculo do modelo"""
        if self._params is None:
            raise ValueError("Parâmetros não definidos")
        
        self._model = WaveguideModel(self._params)
        self._results = self._model.calculate()
        self._notify_observers()
    
    @property
    def results(self) -> Optional[WaveguideResults]:
        """Retorna os resultados do cálculo"""
        return self._results
    
    @property
    def params(self) -> Optional[WaveguideParameters]:
        """Retorna os parâmetros atuais"""
        return self._params
    
    def get_summary(self) -> str:
        """Retorna o resumo dos resultados"""
        if self._model is None:
            return "Nenhum cálculo realizado"
        return self._model.get_summary_text()
    
    def get_field_data(self):
        """Retorna os dados do campo para plotagem"""
        if self._results is None:
            return None, None, None, None
        
        x_um = self._results.x_grid * 1e6
        y_um = self._results.y_grid * 1e6
        return x_um, y_um, self._results.field, self._results.intensity

    def reset(self):
        """Retorna os dados do campo para plotagem"""
        self._params = None
        self._model = None
        self._results = None
        self._notify_observers()   
        
