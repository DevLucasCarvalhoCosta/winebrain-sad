"""
Script principal para executar o backend
"""

import uvicorn
import sys
from pathlib import Path

# Adicionar diretório ao path
sys.path.append(str(Path(__file__).parent))

from api.main import app

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🍷 WINEBRAIN - INICIANDO SERVIDOR")
    print("=" * 60)
    print("\n🌐 Servidor rodando em: http://localhost:8000")
    print("📚 Documentação: http://localhost:8000/docs")
    print("🔧 ReDoc: http://localhost:8000/redoc")
    print("\n" + "=" * 60 + "\n")
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
