#====================================================================================================
#!/usr/bin/env python3
# build_with_venv.py - Compila com ambiente virtual automático
#
#Data: 14/04/2026
#====================================================================================================

import os
import sys
import subprocess
import venv
from pathlib import Path

VENV_DIR = "build_venv"

def create_venv():
    """Cria ambiente virtual"""
    print("📦 Criando ambiente virtual...")
    venv_path = Path.cwd() / VENV_DIR
    
    if venv_path.exists():
        import shutil
        shutil.rmtree(venv_path)
    
    builder = venv.EnvBuilder(with_pip=True)
    builder.create(venv_path)
    print(f"✅ Ambiente virtual criado em {venv_path}")
    return venv_path

def get_python_path(venv_path):
    """Retorna caminho do Python no venv"""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"

def run_in_venv(cmd, venv_path):
    """Executa comando dentro do ambiente virtual"""
    python_path = get_python_path(venv_path)
    full_cmd = [str(python_path), "-c", cmd]
    return subprocess.run(full_cmd, capture_output=True, text=True)

def install_dependencies(venv_path):
    """Instala dependências no venv"""
    print("📦 Instalando dependências...")
    
    deps = ["numpy", "matplotlib", "pyinstaller"]
    python_path = get_python_path(venv_path)
    
    for dep in deps:
        print(f"  Instalando {dep}...")
        result = subprocess.run([str(python_path), "-m", "pip", "install", dep],
                               capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ❌ Erro ao instalar {dep}")
            return False
    
    print("✅ Dependências instaladas")
    return True

def compile_app(venv_path):
    """Compila o aplicativo usando pyinstaller"""
    print("📦 Compilando aplicativo...")
    
    python_path = get_python_path(venv_path)
    
    cmd = [
        str(python_path), "-m", "PyInstaller",
        "--name", "MarcatiliAnalyzer",
        "--onefile",
        "--windowed",
        "--clean",
        "main.py"
    ]
    
    result = subprocess.run(cmd)
    return result.returncode == 0

def main():
    print("=" * 50)
    print("  Build Automático com Ambiente Virtual")
    print("=" * 50)
    
    # Criar ambiente virtual
    venv_path = create_venv()
    
    # Instalar dependências
    if not install_dependencies(venv_path):
        print("❌ Falha ao instalar dependências")
        sys.exit(1)
    
    # Compilar
    if compile_app(venv_path):
        print("✅ Compilação concluída!")
        print("📁 Executável em: ./dist/MarcatiliAnalyzer")
    else:
        print("❌ Falha na compilação")
        sys.exit(1)

if __name__ == "__main__":
    main()