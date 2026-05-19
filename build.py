#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
====================================================================================================
build.py - Script de compilação automatizada para Linux Mint

Este script automatiza completamente o processo de compilação, incluindo verificação de dependências, 
criação de ambiente virtual e geração do executável final.

Uso:
    python3 build.py              # Compilação completa
    python3 build.py --quick      # Compilação rápida (sem verificações)
    python3 build.py --debug      # Compilação com console para debug
    python3 build.py --clean      # Limpar tudo

Data: 13/04/2026
====================================================================================================    
"""

import os
import sys
import subprocess
import shutil
import venv
import argparse
from pathlib import Path
from datetime import datetime

# Configurações
PROJECT_NAME = "MarcatiliAnalyzer"
PROJECT_VERSION = "1.0.0"
VENV_DIR = "venv_build"
BUILD_DIR = "build_output"
DIST_DIR = "dist"

# Cores ANSI
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def log_info(msg):
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {msg}")

def log_success(msg):
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")

def log_warning(msg):
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {msg}")

def log_error(msg):
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")

def log_step(msg):
    print(f"\n{Colors.CYAN}{Colors.BOLD}▶ {msg}{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 60}{Colors.RESET}")

def run_command(cmd, cwd=None, capture_output=False):
    """Executa um comando no shell"""
    try:
        if capture_output:
            result = subprocess.run(cmd, shell=True, cwd=cwd, 
                                   capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        else:
            result = subprocess.run(cmd, shell=True, cwd=cwd)
            return result.returncode == 0, "", ""
    except Exception as e:
        return False, "", str(e)

def check_python():
    """Verifica instalação do Python"""
    log_step("Verificando Python")
    
    success, stdout, _ = run_command("python3 --version", capture_output=True)
    if success:
        version = stdout.strip()
        log_success(f"Python encontrado: {version}")
        
        # Verifica versão >= 3.8
        if "3.8" in version or "3.9" in version or "3.10" in version or "3.11" in version or "3.12" in version:
            log_success("Versão do Python compatível")
        else:
            log_warning(f"Versão do Python pode ser antiga: {version}")
        return True
    else:
        log_error("Python 3 não encontrado. Instale com: sudo apt install python3 python3-pip python3-venv")
        return False

def check_tkinter():
    """Verifica instalação do Tkinter"""
    log_step("Verificando Tkinter")
    
    success, stdout, _ = run_command("python3 -c 'import tkinter' 2>/dev/null && echo 'OK'", 
                                     capture_output=True)
    if success and 'OK' in stdout:
        log_success("Tkinter encontrado")
        return True
    else:
        log_warning("Tkinter não encontrado. Instale com: sudo apt install python3-tk")
        return False

def install_system_dependencies():
    """Instala dependências do sistema"""
    log_step("Verificando dependências do sistema")
    
    deps = [
        'python3-pip',
        'python3-tk',
        'python3-dev',
        'libfreetype6-dev',
        'libpng-dev',
        'libjpeg-dev'
    ]
    
    log_info("Dependências necessárias: " + ", ".join(deps))
    
    response = input(f"{Colors.YELLOW}Instalar dependências do sistema? (s/N): {Colors.RESET}")
    if response.lower() == 's':
        cmd = f"sudo apt update && sudo apt install -y {' '.join(deps)}"
        log_info("Executando: " + cmd)
        success, _, _ = run_command(cmd)
        if success:
            log_success("Dependências do sistema instaladas")
            return True
        else:
            log_error("Falha ao instalar dependências")
            return False
    else:
        log_warning("Pulando instalação de dependências do sistema")
        return True

def create_virtual_env():
    """Cria ambiente virtual para compilação isolada"""
    log_step("Criando ambiente virtual")
    
    venv_path = Path.cwd() / VENV_DIR
    
    if venv_path.exists():
        log_info(f"Removendo ambiente virtual antigo: {venv_path}")
        shutil.rmtree(venv_path)
    
    try:
        log_info(f"Criando ambiente virtual em {venv_path}")
        builder = venv.EnvBuilder(with_pip=True)
        builder.create(venv_path)
        log_success("Ambiente virtual criado")
        return True
    except Exception as e:
        log_error(f"Falha ao criar ambiente virtual: {e}")
        return False

def get_pip_path():
    """Retorna caminho do pip no ambiente virtual"""
    venv_path = Path.cwd() / VENV_DIR
    if sys.platform == "win32":
        return venv_path / "Scripts" / "pip.exe"
    else:
        return venv_path / "bin" / "pip"

def get_python_path():
    """Retorna caminho do python no ambiente virtual"""
    venv_path = Path.cwd() / VENV_DIR
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"

def install_python_dependencies():
    """Instala dependências Python no ambiente virtual"""
    log_step("Instalando dependências Python")
    
    pip_path = get_pip_path()
    
    # Dependências principais
    deps = [
        'numpy>=1.21.0',
        'matplotlib>=3.5.0',
        'pyinstaller>=5.0.0'
    ]
    
    log_info("Instalando: " + ", ".join(deps))
    
    for dep in deps:
        log_info(f"Instalando {dep}...")
        success, _, error = run_command(f"{pip_path} install --quiet {dep}")
        if not success:
            log_warning(f"Falha ao instalar {dep}: {error}")
    
    log_success("Dependências instaladas")
    return True

def compile_with_pyinstaller(debug=False):
    """Compila o projeto com PyInstaller"""
    log_step("Compilando com PyInstaller")
    
    python_path = get_python_path()
    
    # Comando base
    cmd_parts = [
        str(python_path),
        "-m", "PyInstaller",
        "--name", PROJECT_NAME,
        "--onefile",
        "--noconfirm",
        "--clean"
    ]
    
    # Adiciona flag de debug se necessário
    if debug:
        cmd_parts.append("--debug")
        cmd_parts.append("--console")  # Mantém console para debug
    else:
        cmd_parts.append("--windowed")  # Modo GUI (sem console)
    
    # Otimizações
    cmd_parts.append("--strip")
    cmd_parts.append("--noupx")  # UPX pode causar problemas em alguns Linux
    
    # Arquivo principal
    cmd_parts.append("main.py")
    
    cmd = " ".join(cmd_parts)
    log_info(f"Comando: {cmd}")
    
    success, stdout, stderr = run_command(cmd)
    
    if success:
        log_success("Compilação concluída")
        
        # Verifica se o executável foi criado
        executable = Path.cwd() / "dist" / PROJECT_NAME
        if executable.exists():
            size_mb = executable.stat().st_size / (1024 * 1024)
            log_success(f"Executável criado: {executable} ({size_mb:.1f} MB)")
            return True
        else:
            log_error("Executável não encontrado após compilação")
            return False
    else:
        log_error("Falha na compilação")
        if stderr:
            log_error(f"Erro: {stderr}")
        return False

def create_launcher_script():
    """Cria script de lançamento para o executável"""
    log_step("Criando script de lançamento")
    
    script_content = f'''#!/bin/bash
# Script de lançamento para {PROJECT_NAME}
# Gerado em {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

APP_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
EXECUTABLE="$APP_DIR/dist/{PROJECT_NAME}"

if [ -f "$EXECUTABLE" ]; then
    echo "Iniciando {PROJECT_NAME}..."
    "$EXECUTABLE"
else
    echo "Erro: Executável não encontrado em $EXECUTABLE"
    echo "Execute 'python3 build.py' para compilar primeiro"
    exit 1
fi
'''
    
    script_path = Path.cwd() / "run.sh"
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # Torna executável
    script_path.chmod(0o755)
    log_success(f"Script criado: {script_path}")
    return script_path

def create_desktop_file():
    """Cria arquivo .desktop para integração com o menu"""
    log_step("Criando arquivo .desktop")
    
    desktop_content = f"""[Desktop Entry]
Version={PROJECT_VERSION}
Name={PROJECT_NAME}
Comment=Análise de Guias de Onda pelo Método de Marcatili
Exec={Path.cwd().absolute()}/dist/{PROJECT_NAME}
Icon=applications-science
Terminal=false
Type=Application
Categories=Education;Science;Graphics;
StartupNotify=true
Keywords=optics;waveguide;marcatili;simulation;
"""
    
    desktop_path = Path.cwd() / f"{PROJECT_NAME}.desktop"
    with open(desktop_path, 'w') as f:
        f.write(desktop_content)
    
    log_success(f"Arquivo .desktop criado: {desktop_path}")
    return desktop_path

def create_install_script():
    """Cria script de instalação para o sistema"""
    log_step("Criando script de instalação")
    
    install_script = f'''#!/bin/bash
# Script de instalação para {PROJECT_NAME}
# Gerado em {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

echo "Instalando {PROJECT_NAME}..."

# Copia executável para /usr/local/bin
sudo cp dist/{PROJECT_NAME} /usr/local/bin/
sudo chmod +x /usr/local/bin/{PROJECT_NAME}

# Copia arquivo .desktop para aplicações do usuário
cp {PROJECT_NAME}.desktop ~/.local/share/applications/

echo "Instalação concluída!"
echo "Execute '{PROJECT_NAME}' no terminal ou encontre no menu de aplicações"
'''
    
    install_path = Path.cwd() / "install.sh"
    with open(install_path, 'w') as f:
        f.write(install_script)
    
    install_path.chmod(0o755)
    log_success(f"Script de instalação criado: {install_path}")
    return install_path

def clean_all():
    """Remove todos os arquivos gerados"""
    log_step("Limpando todos os arquivos gerados")
    
    dirs_to_remove = [VENV_DIR, BUILD_DIR, DIST_DIR, 'build', '__pycache__']
    files_to_remove = ['*.spec', '*.pyc', 'run.sh', f'{PROJECT_NAME}.desktop', 'install.sh']
    
    for dir_name in dirs_to_remove:
        path = Path.cwd() / dir_name
        if path.exists():
            shutil.rmtree(path)
            log_success(f"Removido: {dir_name}/")
    
    for pattern in files_to_remove:
        for file in Path.cwd().glob(pattern):
            file.unlink()
            log_success(f"Removido: {file.name}")
    
    # Remove __pycache__ recursivamente
    for pycache in Path.cwd().rglob('__pycache__'):
        shutil.rmtree(pycache)
        log_success(f"Removido: {pycache}")
    
    log_success("Limpeza concluída")

def print_summary():
    """Imprime resumo da compilação"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}{'COMPILAÇÃO CONCLUÍDA COM SUCESSO!':^70}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.RESET}")
    
    executable = Path.cwd() / "dist" / PROJECT_NAME
    if executable.exists():
        size_mb = executable.stat().st_size / (1024 * 1024)
        print(f"\n{Colors.WHITE}📦 Executável: {Colors.GREEN}{executable}{Colors.RESET}")
        print(f"{Colors.WHITE}📏 Tamanho: {Colors.YELLOW}{size_mb:.1f} MB{Colors.RESET}")
    
    print(f"\n{Colors.BOLD}Como executar:{Colors.RESET}")
    print(f"  {Colors.BLUE}./dist/{PROJECT_NAME}{Colors.RESET}")
    print(f"  {Colors.BLUE}./run.sh{Colors.RESET}")
    
    print(f"\n{Colors.BOLD}Para instalar no sistema:{Colors.RESET}")
    print(f"  {Colors.BLUE}./install.sh{Colors.RESET}")
    
    print(f"\n{Colors.DIM}{'─'*70}{Colors.RESET}\n")

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description=f'{PROJECT_NAME} - Build Script para Linux Mint',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--quick', action='store_true', 
                       help='Compilação rápida (pula verificações)')
    parser.add_argument('--debug', action='store_true',
                       help='Compilação com modo debug')
    parser.add_argument('--clean', action='store_true',
                       help='Limpar todos os arquivos gerados')
    parser.add_argument('--no-venv', action='store_true',
                       help='Não usar ambiente virtual')
    
    args = parser.parse_args()
    
    # Header
    print(f"\n{Colors.MAGENTA}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print(f"║     {PROJECT_NAME} - Build Script para Linux Mint v{PROJECT_VERSION}     ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    
    # Modo clean
    if args.clean:
        clean_all()
        return
    
    # Modo rápido
    if args.quick:
        log_warning("Modo rápido - pulando verificações")
        if compile_with_pyinstaller(debug=args.debug):
            create_launcher_script()
            create_desktop_file()
            create_install_script()
            print_summary()
        return
    
    # Modo completo
    log_info(f"Iniciando compilação em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verificações
    if not check_python():
        sys.exit(1)
    
    check_tkinter()  # Apenas aviso, não falha
    
    # Dependências do sistema
    install_system_dependencies()
    
    # Compilação
    if not args.no_venv:
        if not create_virtual_env():
            log_warning("Falha ao criar ambiente virtual, usando sistema")
        else:
            if not install_python_dependencies():
                log_warning("Falha ao instalar dependências no venv")
    else:
        log_info("Usando Python do sistema")
    
    # Compila
    if compile_with_pyinstaller(debug=args.debug):
        create_launcher_script()
        create_desktop_file()
        create_install_script()
        print_summary()
    else:
        log_error("Compilação falhou")
        sys.exit(1)

if __name__ == "__main__":
    main()