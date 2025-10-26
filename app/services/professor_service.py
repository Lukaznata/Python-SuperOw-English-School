from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from app.models import professor
from app.models.idioma import Idioma
from ..models import Professor, Aluno
from ..schemas import ProfessorCreate
from fastapi import HTTPException, status
from PIL import Image
import io
import base64

class ProfessorService:
    def __init__(self, db: Session):
        self.db = db

    def processar_foto_perfil(self, imagem_base64: str) -> bytes:
        """Processa e otimiza a foto de perfil mantendo TAMANHO ORIGINAL"""
        try:
            # Decodifica
            img_data = base64.b64decode(imagem_base64)
            img = Image.open(io.BytesIO(img_data))
            
            # Converte para RGB se necessário
            if img.mode == 'RGBA':
                # Cria fundo branco para imagens com transparência
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # NÃO redimensiona - mantém tamanho original
            # WebP com qualidade MAIOR para arquivo ~77KB
            buffer = io.BytesIO()
            img.save(buffer, format='WEBP', quality=92, method=6)
            
            return buffer.getvalue()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao processar imagem: {str(e)}"
            )

    def verificar_duplicidade(self, professor_data: dict, professor_id: int = None):
        """Verifica se CPF, telefone ou MEI já existem no banco"""
        erros = []
        
        # Verificar CPF
        if professor_data.get('cpf'):
            query_cpf = self.db.query(Professor).filter(Professor.cpf == professor_data['cpf'])
            if professor_id:
                query_cpf = query_cpf.filter(Professor.id != professor_id)
            if query_cpf.first():
                erros.append("CPF já cadastrado")
        
        # Verificar Telefone
        if professor_data.get('telefone'):
            query_telefone = self.db.query(Professor).filter(Professor.telefone == professor_data['telefone'])
            if professor_id:
                query_telefone = query_telefone.filter(Professor.id != professor_id)
            if query_telefone.first():
                erros.append("Telefone já cadastrado")
        
        # Verificar MEI
        if professor_data.get('mei'):
            query_mei = self.db.query(Professor).filter(Professor.mei == professor_data['mei'])
            if professor_id:
                query_mei = query_mei.filter(Professor.id != professor_id)
            if query_mei.first():
                erros.append("MEI já cadastrado")
        
        if erros:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=", ".join(erros)
            )

    def criar_professor(self, professor: ProfessorCreate):
        # Verificar se o idioma existe
        idioma = self.db.query(Idioma).filter(Idioma.id == professor.id_idioma).first()
        if not idioma:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Idioma com id {professor.id_idioma} não encontrado"
            )
        
        # Processa a foto mantendo qualidade
        professor_data = professor.model_dump()
        
        # Verificar duplicidade ANTES de processar foto
        self.verificar_duplicidade(professor_data)
        
        if professor_data.get('foto_perfil'):
            professor_data['foto_perfil'] = self.processar_foto_perfil(professor_data['foto_perfil'])
        
        # Criar o professor
        try:
            db_professor = Professor(**professor_data)
            self.db.add(db_professor)
            self.db.commit()
            self.db.refresh(db_professor)
            return db_professor
        except IntegrityError as e:
            self.db.rollback()
            # Caso alguma constraint do banco pegue algo que não verificamos
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao criar professor: dado duplicado no banco de dados"
            )

    def listar_professores(self, skip: int = 0, limit: int = 100):
        professores = self.db.query(Professor).offset(skip).limit(limit).all()
        
        # NÃO normaliza CPF nem MEI - deixa None se for None
        # foto_perfil e pdf_contrato são tratados pelo validator do schema
        
        return professores
    
    def contar_professores(self) -> int:
        """Conta o total de professores"""
        return self.db.query(Professor).count()

    def obter_professor(self, professor_id: int):
        professor = self.db.query(Professor).filter(Professor.id == professor_id).first()
        if professor is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor não encontrado")
        
        # NÃO normaliza CPF nem MEI - deixa None se for None
        # foto_perfil e pdf_contrato são tratados pelo validator do schema
            
        return professor

    def atualizar_professor(self, professor_id: int, professor: ProfessorCreate):
        db_professor = self.obter_professor(professor_id)
        
        # Processar dados
        professor_data = professor.model_dump(exclude_unset=True)
        
        # Verificar duplicidade ANTES de processar foto (excluindo o próprio professor)
        self.verificar_duplicidade(professor_data, professor_id)
        
        # Processar foto de perfil se foi enviada
        if 'foto_perfil' in professor_data and professor_data['foto_perfil']:
            professor_data['foto_perfil'] = self.processar_foto_perfil(professor_data['foto_perfil'])
        
        # Atualizar campos
        try:
            for key, value in professor_data.items():
                setattr(db_professor, key, value)
                
            self.db.commit()
            self.db.refresh(db_professor)
            return db_professor
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao atualizar professor: dado duplicado no banco de dados"
            )

    def deletar_professor(self, professor_id: int):
        professor = self.obter_professor(professor_id)
        self.db.delete(professor)
        self.db.commit()
        return {"message": "Professor deletado com sucesso"}

    def listar_alunos_do_professor(self, professor_id: int):
        professor = (
            self.db.query(Professor)
            .options(joinedload(Professor.alunos))
            .filter(Professor.id == professor_id)
            .first()
        )
        if not professor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor não encontrado")
        return professor.alunos
    
    def associar_aluno(self, professor_id: int, aluno_id: int):
        professor = self.obter_professor(professor_id)
        aluno = self.db.query(Aluno).filter(Aluno.id == aluno_id).first()

        if not aluno:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
        
        if aluno in professor.alunos:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Aluno já associado ao professor")
        professor.alunos.append(aluno)
        self.db.commit()
        self.db.refresh(professor)
        return {"message": f"Aluno {aluno.nome_completo} associado ao professor {professor.nome_completo} com sucesso"}

    def desassociar_aluno(self, professor_id: int, aluno_id: int):
        professor = self.obter_professor(professor_id)
        aluno = self.db.query(Aluno).filter(Aluno.id == aluno_id).first()

        if not aluno:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")

        if aluno not in professor.alunos:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Aluno não associado ao professor")

        professor.alunos.remove(aluno)
        self.db.commit()
        self.db.refresh(professor)
        return {"message": f"Aluno {aluno.nome_completo} desassociado do professor {professor.nome_completo} com sucesso"}