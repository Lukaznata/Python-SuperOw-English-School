import sys
import os

# Adicionar o diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine
from app.models.base import Base

# Importar TODOS os modelos explicitamente
from app.models.administrador import Administrador
from app.models.idioma import Idioma
from app.models.afazer import AfazerDiario
from app.models.professor import Professor
from app.models.aluno import Aluno
from app.models.professor_aluno_association import professor_aluno_association

# Importar Aula ANTES da associação
from app.models.aula import Aula
from app.models.aula_aluno_association import aula_aluno_association

if __name__ == "__main__":
    print("=" * 50)
    print("RECRIANDO BANCO DE DADOS")
    print("=" * 50)
    
    print("\n1. Dropando todas as tabelas...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tabelas dropadas")
    
    print("\n2. Criando todas as tabelas...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas")
    
    print("\n" + "=" * 50)
    print("✅ BANCO RECRIADO COM SUCESSO!")
    print("=" * 50)