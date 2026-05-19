# -*- coding: utf-8 -*-
"""
====================================================================================================
Modelo do Guia de Onda - Responsável pelos dados e cálculos físicos

Data: 13/04/2026
====================================================================================================
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Tuple, Optional
from enum import Enum


class Polarization(Enum):
    """Enum para tipos de polarização"""
    TE = 1  # Modo TE (E_x)
    TM = 2  # Modo TM (E_y)


@dataclass
class WaveguideParameters:
    """Parâmetros de entrada do guia de onda"""
    width: float = 4e-6          # Largura total (2a) em metros
    height: float = 4e-6         # Altura total (2b) em metros
    wavelength: float = 1.55e-6  # Comprimento de onda em metros
    n_core: float = 1.5          # Índice de refração do núcleo
    n_cladding: float = 1.4      # Índice de refração do revestimento
    mode_x: int = 0              # Número do modo em x (p)
    mode_y: int = 0              # Número do modo em y (q)
    polarization: Polarization = Polarization.TE
    resolution: int = 301        # Resolução da malha
    extension: float = 2.5       # Fator de extensão da janela
    
    def __post_init__(self):
        """Valida os parâmetros após inicialização"""
        self._validate()
    
    def _validate(self):
        """Valida os parâmetros de entrada"""
        if self.width <= 0:
            raise ValueError("Largura deve ser positiva")
        if self.height <= 0:
            raise ValueError("Altura deve ser positiva")
        if self.wavelength <= 0:
            raise ValueError("Comprimento de onda deve ser positivo")
        if self.n_core <= 0:
            raise ValueError("Índice do núcleo deve ser positivo")
        if self.n_cladding <= 0:
            raise ValueError("Índice do revestimento deve ser positivo")
        if self.n_cladding >= self.n_core:
            raise ValueError("Índice do revestimento deve ser menor que o do núcleo")
        if self.mode_x < 0:
            raise ValueError("Número do modo em x deve ser ≥ 0")
        if self.mode_y < 0:
            raise ValueError("Número do modo em y deve ser ≥ 0")
        if self.resolution < 50:
            raise ValueError("Resolução deve ser ≥ 50")
        if self.extension < 1.2 or self.extension > 4.0:
            raise ValueError("Extensão deve estar entre 1.2 e 4.0")
    
    @property
    def half_width(self) -> float:
        """Meia-largura a"""
        return self.width / 2
    
    @property
    def half_height(self) -> float:
        """Meia-altura b"""
        return self.height / 2
    
    @property
    def delta(self) -> float:
        """Diferença relativa de índice"""
        return (self.n_core**2 - self.n_cladding**2) / (2 * self.n_core**2) * 100


@dataclass
class WaveguideResults:
    """Resultados dos cálculos do guia de onda"""
    k0: float = 0.0                    # Número de onda no vácuo
    kx: float = 0.0                    # Componente x do número de onda
    ky: float = 0.0                    # Componente y do número de onda
    beta: float = 0.0                  # Constante de propagação
    n_eff: float = 0.0                 # Índice efetivo
    gamma_x: float = 0.0               # Constante de decaimento em x
    gamma_y: float = 0.0               # Constante de decaimento em y
    V: float = 0.0                     # Frequência normalizada
    C1: float = 1.0                    # Amplitude no núcleo
    C2: float = 0.0                    # Amplitude região 2
    C3: float = 0.0                    # Amplitude região 3
    C4: float = 0.0                    # Amplitude região 4
    C5: float = 0.0                    # Amplitude região 5
    field: Optional[np.ndarray] = None     # Campo elétrico
    intensity: Optional[np.ndarray] = None # Intensidade
    x_grid: Optional[np.ndarray] = None    # Malha x
    y_grid: Optional[np.ndarray] = None    # Malha y
    X_mesh: Optional[np.ndarray] = None    # Malha 2D X
    Y_mesh: Optional[np.ndarray] = None    # Malha 2D Y
    
    @property
    def is_guided(self) -> bool:
        """Verifica se o modo é guiado"""
        return self.n2 <= self.n_eff <= self.n1 if hasattr(self, 'n1') else False


class WaveguideModel:
    """
    Modelo do guia de onda - Responsável pelos cálculos físicos
    Segue o padrão de design Strategy para os cálculos
    """
    
    def __init__(self, params: WaveguideParameters):
        self.params = params
        self.results = WaveguideResults()
        
    def calculate(self) -> WaveguideResults:
        """Executa todos os cálculos"""
        self._calculate_wavenumbers()
        self._calculate_propagation_constants()
        self._calculate_amplitudes()
        self._calculate_normalized_frequency()
        self._generate_mesh()
        self._calculate_field()
        return self.results
    
    def _calculate_wavenumbers(self):
        """Calcula números de onda"""
        self.results.k0 = 2 * np.pi / self.params.wavelength
        
        # Componente kx
        if self.params.mode_x == 0:
            self.results.kx = np.pi / (2 * self.params.half_width)
        else:
            self.results.kx = self.params.mode_x * np.pi / (2 * self.params.half_width)
        
        # Componente ky
        if self.params.mode_y == 0:
            self.results.ky = np.pi / (2 * self.params.half_height)
        else:
            self.results.ky = self.params.mode_y * np.pi / (2 * self.params.half_height)
    
    def _calculate_propagation_constants(self):
        """Calcula constantes de propagação e decaimento"""
        beta_squared = (self.results.k0**2 * self.params.n_core**2 - 
                        self.results.kx**2 - self.results.ky**2)
        
        if beta_squared <= 0:
            self.results.beta = np.sqrt(abs(beta_squared))
            self.results.n_eff = 0
        else:
            self.results.beta = np.sqrt(beta_squared)
            self.results.n_eff = self.results.beta / self.results.k0
        
        # Constantes de decaimento
        gamma_x_squared = (self.results.kx**2 + self.results.beta**2 - 
                          self.results.k0**2 * self.params.n_cladding**2)
        gamma_y_squared = (self.results.ky**2 + self.results.beta**2 - 
                          self.results.k0**2 * self.params.n_cladding**2)
        
        self.results.gamma_x = np.sqrt(abs(gamma_x_squared)) if gamma_x_squared > 0 else 0
        self.results.gamma_y = np.sqrt(abs(gamma_y_squared)) if gamma_y_squared > 0 else 0
    
    def _calculate_amplitudes(self):
        """Calcula constantes de amplitude"""
        self.results.C1 = 1.0
        
        if abs(self.results.ky) > 1e-10:
            self.results.C2 = self.results.C1 * np.cos(self.results.ky * self.params.half_height)
            self.results.C4 = self.results.C1 * np.cos(self.results.ky * self.params.half_height)
        else:
            self.results.C2 = self.results.C1
            self.results.C4 = self.results.C1
            
        if abs(self.results.kx) > 1e-10:
            self.results.C3 = self.results.C1 * np.cos(self.results.kx * self.params.half_width)
            self.results.C5 = self.results.C1 * np.cos(self.results.kx * self.params.half_width)
        else:
            self.results.C3 = self.results.C1
            self.results.C5 = self.results.C1
    
    def _calculate_normalized_frequency(self):
        """Calcula frequência normalizada V"""
        if self.params.n_core > self.params.n_cladding:
            self.results.V = (self.results.k0 * self.params.half_width * 
                             np.sqrt(self.params.n_core**2 - self.params.n_cladding**2))
        else:
            self.results.V = 0
    
    def _generate_mesh(self):
        """Gera a malha para cálculo do campo"""
        x_max = self.params.extension * self.params.half_width
        y_max = self.params.extension * self.params.half_height
        
        self.results.x_grid = np.linspace(-x_max, x_max, self.params.resolution)
        self.results.y_grid = np.linspace(-y_max, y_max, self.params.resolution)
        self.results.X_mesh, self.results.Y_mesh = np.meshgrid(self.results.x_grid, 
                                                                self.results.y_grid)
    
    def _calculate_field(self):
        """Calcula a distribuição do campo elétrico"""
        field = np.zeros_like(self.results.X_mesh)
        
        for i in range(len(self.results.x_grid)):
            for j in range(len(self.results.y_grid)):
                x = self.results.X_mesh[i, j]
                y = self.results.Y_mesh[i, j]
                field[i, j] = self._field_at_point(x, y)
        
        # Normalização
        max_field = np.max(np.abs(field))
        if max_field > 0:
            field = field / max_field
        
        self.results.field = field
        self.results.intensity = field**2
    
    def _field_at_point(self, x: float, y: float) -> float:
        """Calcula o campo em um ponto específico"""
        a = self.params.half_width
        b = self.params.half_height
        
        # Região 1: Núcleo
        if abs(x) <= a and abs(y) <= b:
            return self.results.C1 * np.cos(self.results.kx * x) * np.cos(self.results.ky * y)
        
        # Região 2: Acima do núcleo
        elif abs(x) <= a and y > b:
            if self.results.gamma_y > 0:
                return (self.results.C2 * np.cos(self.results.kx * x) * 
                       np.exp(-self.results.gamma_y * (y - b)))
            return 0
        
        # Região 4: Abaixo do núcleo
        elif abs(x) <= a and y < -b:
            if self.results.gamma_y > 0:
                return (self.results.C4 * np.cos(self.results.kx * x) * 
                       np.exp(self.results.gamma_y * (y + b)))
            return 0
        
        # Região 3: À direita do núcleo
        elif x > a and abs(y) <= b:
            if self.results.gamma_x > 0:
                return (self.results.C3 * np.exp(-self.results.gamma_x * (x - a)) * 
                       np.cos(self.results.ky * y))
            return 0
        
        # Região 5: À esquerda do núcleo
        elif x < -a and abs(y) <= b:
            if self.results.gamma_x > 0:
                return (self.results.C5 * np.exp(self.results.gamma_x * (x + a)) * 
                       np.cos(self.results.ky * y))
            return 0
        
        # Cantos
        return 0
    
    def get_summary_text(self) -> str:
        """Retorna texto resumo dos resultados"""
        params = self.params
        res = self.results
        
        # Determina tipo de modo
        tipo_modo = f"TE_{{{params.mode_x}{params.mode_y}}}^x (E_x)" if params.polarization == Polarization.TE else f"TE_{{{params.mode_x}{params.mode_y}}}^y (E_y)"
        
        # Status do modo
        if res.n_eff >= params.n_cladding and res.n_eff <= params.n_core and res.n_eff > 0:
            status_modo = "Modo guiado (n₂ ≤ n_eff ≤ n₁)"
        elif res.n_eff <= 0:
            status_modo = "Modo abaixo do cutoff"
        else:
            status_modo = "AVISO - Índice efetivo fora da faixa esperada!"
        
        # Regime da fibra
        if res.V < np.pi/2:
            status_V = "Região de corte para modos de ordem superior"
        elif res.V < np.pi:
            status_V = "Região de modo único aproximado"
        else:
            status_V = "Região multimodo"
        
        return f"""
{'='*49}
RESULTADOS NUMÉRICOS - MÉTODO DE MARCATILI
{'='*49}

------------- PARÂMETROS DO GUIA --------------

Largura do núcleo (2a)        : {params.width*1e6:.3f} µm
Altura do núcleo (2b)         : {params.height*1e6:.3f} µm
Comprimento de onda (λ)       : {params.wavelength*1e6:.3f} µm
Índice do núcleo (n₁)         : {params.n_core:.4f}
Índice do revestimento (n₂)   : {params.n_cladding:.4f}
Diferença relativa (Δ)        : {params.delta:.4f} %

------------- PARÂMETROS DO MODO -------------

Modo                          : {tipo_modo}
kx (componente x)             : {res.kx:.3e} rad/m
ky (componente y)             : {res.ky:.3e} rad/m

----------- CONSTANTES DE PROPAGAÇÃO ----------

Constante de propagação (β)   : {res.beta:.3e} rad/m
Índice efetivo (n_eff)        : {res.n_eff:.6f}
Status                        : {status_modo}

----------- CONSTANTES DE DECAIMENTO ----------

γx (decaimento em x)          : {res.gamma_x:.3e} m⁻¹
γy (decaimento em y)          : {res.gamma_y:.3e} m⁻¹

------------ FREQUÊNCIA NORMALIZADA ------------

Parâmetro V                   : {res.V:.4f}
Status                        : {status_V}
{'='*49}











"""