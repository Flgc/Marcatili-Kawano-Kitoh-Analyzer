# -*- coding: utf-8 -*-
"""
Modelo do Guia de Onda - 5 regiões (com cinco índices de revestimento - Kawano & Kitoh)
Implementa as equações transcendentais completas.

Data: 19/05/2026
"""

import numpy as np
from dataclasses import dataclass
from enum import Enum


class Polarization(Enum):
    TE = 1  # E_x (quasi-TM na notação de Kawano)
    TM = 2  # E_y (quasi-TE)


@dataclass
class WaveguideParameters:
    # Dimensões
    width: float = 4e-6  # 2a (m)
    height: float = 4e-6  # 2b (m)
    wavelength: float = 1.55e-6  # λ (m)

    # Índices das 5 regiões (Kawano Fig. 2.3)
    n1: float = 1.5  # núcleo
    n2: float = 1.0  # revestimento superior (cover)
    n3: float = 1.45  # revestimento direito
    n4: float = 1.45  # revestimento inferior
    n5: float = 1.45  # revestimento esquerdo

    mode_x: int = 0
    mode_y: int = 0
    polarization: Polarization = Polarization.TE
    resolution: int = 301
    extension: float = 2.5

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Dimensões devem ser positivas")
        if self.wavelength <= 0:
            raise ValueError("Comprimento de onda positivo")
        if self.n1 <= max(self.n2, self.n3, self.n4, self.n5):
            raise ValueError("n1 deve ser maior que todos os revestimentos")
        if self.mode_x < 0 or self.mode_y < 0:
            raise ValueError("Ordens de modo não negativas")
        if self.resolution < 50:
            raise ValueError("Resolução deve ser ≥ 50")
        if not (1.2 <= self.extension <= 4.0):
            raise ValueError("Extensão deve estar entre 1.2 e 4.0")

    @property
    def half_width(self):
        return self.width / 2

    @property
    def half_height(self):
        return self.height / 2

    @property
    def delta_rel(self):
        return (self.n1**2 - self.n2**2) / (2 * self.n1**2) * 100


@dataclass
class WaveguideResults:
    k0: float = 0.0
    kx: float = 0.0
    ky: float = 0.0
    beta: float = 0.0
    n_eff: float = 0.0
    gamma_x3: float = 0.0  # γx3 (direita)
    gamma_x5: float = 0.0  # γx5 (esquerda)
    gamma_y2: float = 0.0  # γy2 (cima)
    gamma_y4: float = 0.0  # γy4 (baixo)
    V: float = 0.0
    # amplitudes
    C1: float = 1.0
    C2: float = 0.0
    C3: float = 0.0
    C4: float = 0.0
    C5: float = 0.0
    field: np.ndarray = None
    intensity: np.ndarray = None
    x_grid: np.ndarray = None
    y_grid: np.ndarray = None
    X_mesh: np.ndarray = None
    Y_mesh: np.ndarray = None

    """ Adequação experimental, adicionada das fases - 01-06-26

    Motivação: As soluções no núcleo devem ser cos(kx*x + φx) * cos(ky*y + φy),
    não apenas cos(kx*x)*cos(ky*y). As fases são determinadas pelas condições
    de contorno e são essenciais para reproduzir o deslocamento do pico do
    campo em guias assimétricos (ex: n2=1, n4=1.45)."
    """
    phi_x: float = 0.0  # fase na direção X (rad)
    phi_y: float = 0.0  # fase na direção Y (rad)


class WaveguideModel:
    def __init__(self, params: WaveguideParameters):
        self.params = params
        self.res = WaveguideResults()

    def calculate(self) -> WaveguideResults:
        self._calc_wavenumbers()
        self._calc_propagation()
        self._calc_amplitudes()
        self._calc_V()
        self._generate_mesh()
        self._calc_field()
        return self.res

    def _calc_wavenumbers(self):
        k0 = 2 * np.pi / self.params.wavelength
        self.res.k0 = k0

        # Estimativa inicial dos números de onda transversais
        # Usa aproximação de guia planar equivalente
        a, b = self.params.half_width, self.params.half_height
        p, q = self.params.mode_x, self.params.mode_y

        # Direção x
        if p == 0:
            kx_est = np.pi / (2 * a)
        else:
            kx_est = p * np.pi / (2 * a)

        # Direção y
        if q == 0:
            ky_est = np.pi / (2 * b)
        else:
            ky_est = q * np.pi / (2 * b)

        # Resolve as equações transcendentais via bisseção
        kx_sol = self._solve_kx(kx_est, a)
        ky_sol = self._solve_ky(ky_est, b)

        self.res.kx = kx_sol
        self.res.ky = ky_sol

    def _solve_kx(self, kx_est, a):
        k0 = self.res.k0
        n1 = self.params.n1
        n3 = self.params.n3
        n5 = self.params.n5

        # limites de busca: 0 até próximo do corte
        kmax = k0 * np.sqrt(n1**2 - max(n3, n5) ** 2) - 1e-5
        if kmax <= 0:
            return kx_est

        def eq(kx):
            if kx <= 0:
                return 1e9
            gam3 = np.sqrt(k0**2 * (n1**2 - n3**2) - kx**2) if n1 > n3 else 0
            gam5 = np.sqrt(k0**2 * (n1**2 - n5**2) - kx**2) if n1 > n5 else 0
            term1 = np.arctan((n1**2 * gam3) / (n3**2 * kx)) if gam3 > 0 else np.pi / 2
            term2 = np.arctan((n1**2 * gam5) / (n5**2 * kx)) if gam5 > 0 else np.pi / 2
            return kx * a - term1 - term2 - self.params.mode_x * np.pi

        try:
            from scipy.optimize import bisect

            return bisect(eq, 1e-6, kmax)
        except ImportError:
            # fallback simples (não usar scipy)
            for kx in np.linspace(1e-6, kmax, 200):
                if abs(eq(kx)) < 1e-6:
                    return kx
            return kx_est

    def _solve_ky(self, ky_est, b):
        k0 = self.res.k0
        n1 = self.params.n1
        n2 = self.params.n2
        n4 = self.params.n4

        kmax = k0 * np.sqrt(n1**2 - max(n2, n4) ** 2) - 1e-5
        if kmax <= 0:
            return ky_est

        def eq(ky):
            if ky <= 0:
                return 1e9
            gam2 = np.sqrt(k0**2 * (n1**2 - n2**2) - ky**2) if n1 > n2 else 0
            gam4 = np.sqrt(k0**2 * (n1**2 - n4**2) - ky**2) if n1 > n4 else 0
            term1 = np.arctan(gam2 / ky) if gam2 > 0 else np.pi / 2
            term2 = np.arctan(gam4 / ky) if gam4 > 0 else np.pi / 2
            return ky * b - term1 - term2 - self.params.mode_y * np.pi

        try:
            from scipy.optimize import bisect

            return bisect(eq, 1e-6, kmax)
        except ImportError:
            for ky in np.linspace(1e-6, kmax, 200):
                if abs(eq(ky)) < 1e-6:
                    return ky
            return ky_est

    def _calc_propagation(self):
        """02-06-26
        Calcula a constante de propagação beta, índice efetivo n_eff,
        constantes de decaimento nas cinco regiões e as fases phi_x e phi_y.
        """
        k0 = self.res.k0
        n1 = self.params.n1
        kx = self.res.kx
        ky = self.res.ky

        # 1. Constante de propagação
        beta2 = k0**2 * n1**2 - (kx**2 + ky**2)
        if beta2 < 0:
            self.res.beta = 0.0
            self.res.n_eff = 0.0
        else:
            self.res.beta = np.sqrt(beta2)
            self.res.n_eff = self.res.beta / k0

        # 2. Constantes de decaimento (gammas)
        n1, n2, n3, n4, n5 = (
            self.params.n1,
            self.params.n2,
            self.params.n3,
            self.params.n4,
            self.params.n5,
        )
        k0 = self.res.k0
        beta = self.res.beta

        self.res.gamma_y2 = np.sqrt(beta**2 - k0**2 * n2**2) if beta > k0 * n2 else 0.0
        self.res.gamma_y4 = np.sqrt(beta**2 - k0**2 * n4**2) if beta > k0 * n4 else 0.0
        self.res.gamma_x3 = np.sqrt(beta**2 - k0**2 * n3**2) if beta > k0 * n3 else 0.0
        self.res.gamma_x5 = np.sqrt(beta**2 - k0**2 * n5**2) if beta > k0 * n5 else 0.0

        # 3. Cálculo das fases phi_x e phi_y (conforme polarização)
        kx = self.res.kx
        ky = self.res.ky
        gamma_x3 = self.res.gamma_x3
        gamma_x5 = self.res.gamma_x5
        gamma_y2 = self.res.gamma_y2
        gamma_y4 = self.res.gamma_y4  # (reservado para uso futuro)

        # Permitirá a escolha da expressão correta com base no tipo de polarização
        if self.params.polarization == Polarization.TE:
            # TE: continuidade da derivada -> arctan(gamma/k)
            phi_x = np.arctan2(gamma_x5, kx)  # usando interface esquerda (x = -a)
            phi_y = np.arctan2(gamma_y2, ky)  # usando interface superior (y = b)
            # Observação: Para guia totalmente assimétrico, o ideal seria usar uma média
            # ou resolver um sistema, mas essa aproximação é aceitável para TE.
        else:  # TM
            # TM: continuidade da derivada com fatores dos índices
            phi_x = np.arctan2((n1**2 * gamma_x5), (n5**2 * kx))
            phi_y = np.arctan2((n1**2 * gamma_y2), (n2**2 * ky))

        # Armazena as fases nos resultados
        # Fase em x
        self.res.phi_x = phi_x
        # Fase em y
        self.res.phi_y = phi_y

    def _calc_amplitudes(self):

        # Adequação experimental - 01-06-26
        """
        As amplitudes dos campos evanescentes nos revestimentos dependem do valor
        do campo nos cantos do núcleo. Com as fases corretas, a continuidade em
        x=±a e y=±b é garantida, eliminando descontinuidades artificiais."
        """

        kx = self.res.kx
        ky = self.res.ky
        a = self.params.half_width
        b = self.params.half_height
        phi_x = self.res.phi_x
        phi_y = self.res.phi_y

        # Amplitudes nas interfaces
        self.res.C1 = 1.0  # normalização arbitrária
        self.res.C2 = (
            self.res.C1
            * np.cos(kx * a + phi_x)
            * np.cos(ky * b + phi_y)
            / np.cos(ky * b + phi_y)
        )  # simplifica
        self.res.C3 = (
            self.res.C1
            * np.cos(kx * a + phi_x)
            * np.cos(ky * b + phi_y)
            / np.cos(kx * a + phi_x)
        )
        self.res.C4 = (
            self.res.C1
            * np.cos(kx * a + phi_x)
            * np.cos(ky * b + phi_y)
            / np.cos(ky * b + phi_y)
        )
        self.res.C5 = (
            self.res.C1
            * np.cos(kx * a + phi_x)
            * np.cos(ky * b + phi_y)
            / np.cos(kx * a + phi_x)
        )

    def _calc_V(self):
        k0 = self.res.k0
        a = self.params.half_width
        n1 = self.params.n1
        n2 = self.params.n2  # uso do menor índice para aproximação
        self.res.V = k0 * a * np.sqrt(n1**2 - n2**2) if n1 > n2 else 0

    def _generate_mesh(self):
        x_max = self.params.extension * self.params.half_width
        y_max = self.params.extension * self.params.half_height
        res = self.params.resolution
        self.res.x_grid = np.linspace(-x_max, x_max, res)
        self.res.y_grid = np.linspace(-y_max, y_max, res)
        self.res.X_mesh, self.res.Y_mesh = np.meshgrid(self.res.x_grid, self.res.y_grid)

    def _calc_field(self):
        field = np.zeros_like(self.res.X_mesh)
        for i in range(len(self.res.x_grid)):
            for j in range(len(self.res.y_grid)):
                x = self.res.X_mesh[i, j]
                y = self.res.Y_mesh[i, j]
                field[i, j] = self._field_at_point(x, y)

        # Teste para verificar se a correção funcionou no console
        print("Máximo:", np.max(np.abs(field)))
        print("Mínimo:", np.min(np.abs(field)))
        print("Pontos não nulos:", np.count_nonzero(np.abs(field) > 1e-12))

        # Facilita a comparação visual entre diferentes parâmetros e torna o deslocamento
        # do pico mais evidente nos gráficos
        # A ideia é facilitar a comparação visual entre diferentes parâmetros e torna o
        # deslocamento do pico mais evidente nos gráficos.
        max_f = np.max(np.abs(field))
        if max_f > 0:
            field /= max_f
        self.res.field = field
        self.res.intensity = field**2

    def _field_at_point(self, x, y):
        # Adequação experimental - 01-06-26
        """
        Agora o campo obedecerá:
            - Núcleo: C1 * cos(kx*x + φx) * cos(ky*y + φy)
            - Revestimentos: decaimento exponencial multiplicado pelo cosseno apropriado.
        Com isso espero ser possível reproduzir fielmente as equações (1.38) e (1.82),
        afim de mostrar o deslocamento do pico em guias assimétricos e o decaimento
        exponencial visível nos cortes transversais.
        """

        a = self.params.half_width
        b = self.params.half_height
        kx = self.res.kx
        ky = self.res.ky
        phi_x = self.res.phi_x
        phi_y = self.res.phi_y
        C1 = self.res.C1
        C2 = self.res.C2
        C3 = self.res.C3
        C4 = self.res.C4
        C5 = self.res.C5
        gx3 = self.res.gamma_x3
        gx5 = self.res.gamma_x5
        gy2 = self.res.gamma_y2
        gy4 = self.res.gamma_y4

        # Região 1: núcleo
        if abs(x) <= a and abs(y) <= b:
            return C1 * np.cos(kx * x + phi_x) * np.cos(ky * y + phi_y)

        # Região 2: revestimento superior (y > b, |x| <= a)
        elif abs(x) <= a and y > b:
            if gy2 > 0:
                return C2 * np.cos(kx * x + phi_x) * np.exp(-gy2 * (y - b))

        # Região 4: revestimento inferior (y < -b, |x| <= a)
        elif abs(x) <= a and y < -b:
            if gy4 > 0:
                return C4 * np.cos(kx * x + phi_x) * np.exp(gy4 * (y + b))

        # Região 3: revestimento direito (x > a, |y| <= b)
        elif x > a and abs(y) <= b:
            if gx3 > 0:
                return C3 * np.exp(-gx3 * (x - a)) * np.cos(ky * y + phi_y)

        # Região 5: revestimento esquerdo (x < -a, |y| <= b)
        elif x < -a and abs(y) <= b:
            if gx5 > 0:
                return C5 * np.exp(gx5 * (x + a)) * np.cos(ky * y + phi_y)
        else:
            # Cantos externos (desprezados pelo método de Marcatili)
            return 0.0

    def get_summary_text(self) -> str:
        p = self.params
        r = self.res
        tipo = "TE (E_x)" if p.polarization == Polarization.TE else "TM (E_y)"
        status = "Guiado" if (p.n2 < r.n_eff < p.n1) else "Não guiado (cut-off)"
        return f"""
{'='*50}
 RESULTADOS - MÉTODO DE MARCATILI (5 REGIÕES)
{'='*50}
 Guia: {p.width*1e6:.2f} × {p.height*1e6:.2f} μm²   λ = {p.wavelength*1e6:.3f} μm
 n1={p.n1:.3f}  n2={p.n2:.3f}  n3={p.n3:.3f}  n4={p.n4:.3f}  n5={p.n5:.3f}
 Modo: {tipo}  (p={p.mode_x}, q={p.mode_y})

 kx = {r.kx:.3e} rad/m    ky = {r.ky:.3e} rad/m
 β  = {r.beta:.3e} rad/m    n_eff = {r.n_eff:.6f}
 γy2 = {r.gamma_y2:.3e}   γy4 = {r.gamma_y4:.3e}
 γx3 = {r.gamma_x3:.3e}   γx5 = {r.gamma_x5:.3e}
 resumo += f" φx = {r.phi_x:.3f} rad  φy = {r.phi_y:.3f} rad"
 V   = {r.V:.4f}  →  {status}
{'='*50}
"""
