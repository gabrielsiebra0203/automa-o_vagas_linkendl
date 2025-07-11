#!/usr/bin/env python3
"""
Script de setup para LinkedIn Automation
Instala todas as dependências necessárias
"""

import subprocess
import sys
import os

def run_command(command):
    """Executa um comando e retorna True se bem-sucedido"""
    try:
        print(f"Executando: {command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {command} executado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar {command}: {e}")
        return False

def main():
    print("🚀 Configurando LinkedIn Automation...")
    
    # Verificar se Python está instalado
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 ou superior é necessário!")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    
    # Instalar dependências do pip
    print("\n📦 Instalando dependências...")
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt"):
        print("❌ Falha ao instalar dependências")
        sys.exit(1)
    
    # Instalar navegadores do Playwright
    print("\n🌐 Instalando navegadores do Playwright...")
    if not run_command(f"{sys.executable} -m playwright install"):
        print("❌ Falha ao instalar navegadores")
        sys.exit(1)
    
    # Verificar se config.json existe
    if not os.path.exists('config.json'):
        print("\n⚠️ Arquivo config.json não encontrado!")
        print("Execute o script main.py uma vez para criar o template")
    else:
        print("\n✅ Arquivo config.json encontrado")
    
    print("\n🎉 Setup concluído com sucesso!")
    print("\n📝 Próximos passos:")
    print("1. Configure suas credenciais no arquivo config.json")
    print("2. Execute: python main.py")
    print("\n⚠️ Lembre-se de usar com responsabilidade!")

if __name__ == "__main__":
    main() 