#====================================================================================================
#!/bin/bash
# setup_venv.sh - Configura ambiente virtual automaticamente
#
#   Para executar no linux 1º:>  chmod +x setup_venv.sh
#                          2º:>  ./setup_venv.sh
#
#Data: 14/04/2026
#====================================================================================================

echo "=========================================="
echo "  Configurando Ambiente Virtual"
echo "=========================================="

# Nome do ambiente virtual
VENV_NAME="marcatili_env"

echo "📦 Instalando python3-venv..."
sudo apt install -y python3-venv python3-full
python3 -m venv marcatili_env
source marcatili_env/bin/activate
pip install numpy matplotlib pyinstaller    

echo ""
echo "✅ Ambiente virtual criado com sucesso!"
echo ""
echo "Para usar:"
echo "  source $VENV_NAME/bin/activate"
echo "  python3 main.py"
echo ""
echo "Para sair:"
echo "  deactivate"


python3 main.py
deactivate
