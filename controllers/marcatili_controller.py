# -*- coding: utf-8 -*-
"""
Controller para o método de Marcatili (versão 5 regiões)
Data: 19/05/2026
"""

from typing import Optional, Callable
from models.waveguide import (
    WaveguideParameters,
    WaveguideModel,
    Polarization,
    WaveguideResults,
)


class MarcatiliController:
    def __init__(self):
        self._params: Optional[WaveguideParameters] = None
        self._model: Optional[WaveguideModel] = None
        self._results: Optional[WaveguideResults] = None
        self._observers: list = []

    def add_observer(self, callback: Callable):
        self._observers.append(callback)

    def _notify_observers(self):
        for cb in self._observers:
            cb()

    def set_parameters(
        self,
        width_um: float,
        height_um: float,
        wavelength_um: float,
        n1: float,
        n2: float,
        n3: float,
        n4: float,
        n5: float,
        mode_x: int,
        mode_y: int,
        polarization: int,
        resolution: int,
        extension: float,
    ) -> bool:
        try:
            self._params = WaveguideParameters(
                width=width_um * 1e-6,
                height=height_um * 1e-6,
                wavelength=wavelength_um * 1e-6,
                n1=n1,
                n2=n2,
                n3=n3,
                n4=n4,
                n5=n5,
                mode_x=mode_x,
                mode_y=mode_y,
                polarization=Polarization.TE if polarization == 1 else Polarization.TM,
                resolution=resolution,
                extension=extension,
            )
            self._notify_observers()
            return True
        except Exception as e:
            raise ValueError(f"Parâmetros inválidos: {e}")

    def calculate(self):
        if self._params is None:
            raise ValueError("Parâmetros não definidos")
        self._model = WaveguideModel(self._params)
        self._results = self._model.calculate()
        self._notify_observers()

    @property
    def results(self):
        return self._results

    @property
    def params(self):
        return self._params

    def get_summary(self) -> str:
        if self._model is None:
            return "Nenhum cálculo realizado"
        return self._model.get_summary_text()

    def get_field_data(self):
        if self._results is None:
            return None, None, None, None
        x_um = self._results.x_grid * 1e6
        y_um = self._results.y_grid * 1e6
        return x_um, y_um, self._results.field, self._results.intensity

    def reset(self):
        self._params = None
        self._model = None
        self._results = None
        self._notify_observers()
