#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
====================================================================================================
Página inicial do aplicativo
Método Marcatili - Análise de Guias de Onda Ópticos

Este programa foi desenvolvido para auxiliar na elaboração do relatório analítico e 
fornecerá cálculos e representações gráficas da distribuição do campo elétrico 
para guias de onda ópticos retangulares utilizando o método Marcatili.

Bibliografia
INTRODUÇÃO À ANÁLISE DE GUIAS DE ONDA ÓPTICOS - Resolução das Equações de Maxwell e da Equação de Schrödinger
FOTÔNICA INTEGRADA: FUNDAMENTOS - Ginés Lifante

Inspiração do projeto
App_Marcatili_Analysis - MatLab R2025b

Data: 13/04/2026
====================================================================================================
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from views.marcatili_gui import MarcatiliGUI

def main():    
    print("=" * 70)
    print("  MÉTODO DE MARCATILI - ANÁLISE DE GUIAS DE ONDA ÓPTICOS")
    print("=" * 70)
    print("  Iniciando aplicação...")
    print("=" * 70)
    
    app = MarcatiliGUI()
    app.run()


if __name__ == "__main__":
    main()