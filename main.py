#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
 Marcatili-Kawano Analyzer - Análise Modal segundo Kawano & Kitoh (2001)
 Baseado exclusivamente nas equações do método de Marcatili com cinco regiões.

Data: 19/05/2026
================================================================================
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from views.marcatili_gui import MarcatiliKawanoGUI


def main():
    print("=" * 70)
    print("  MARCATILI-KAWANO ANALYZER (versão com 5 regiões)")
    print("  Baseado em Kawano & Kitoh (2001) - Seção 2.3")
    print("=" * 70)
    print("  Iniciando aplicação...")
    print("=" * 70)

    app = MarcatiliKawanoGUI()
    app.run()


if __name__ == "__main__":
    main()
