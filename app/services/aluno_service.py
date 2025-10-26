from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from ..models import Aluno, Professor
from ..schemas import AlunoCreate
from fastapi import HTTPException, status
from ..core.logging import logger
from PIL import Image
import io
import base64

class AlunoService:
    def __init__(self, db: Session):
        self.db = db
        logger.debug("AlunoService inicializado")

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
            logger.error(f"Erro ao processar imagem do aluno: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao processar imagem: {str(e)}"
            )
        
    def verificar_duplicidade(self, aluno_data: dict, aluno_id: int = None):
        """Verifica se CPF ou telefone já existem no banco"""
        erros = []
        
        # Verificar CPF
        if aluno_data.get('cpf'):
            query_cpf = self.db.query(Aluno).filter(Aluno.cpf == aluno_data['cpf'])
            if aluno_id:
                query_cpf = query_cpf.filter(Aluno.id != aluno_id)
            if query_cpf.first():
                erros.append("CPF já cadastrado")
        
        # Verificar Telefone
        if aluno_data.get('telefone'):
            query_telefone = self.db.query(Aluno).filter(Aluno.telefone == aluno_data['telefone'])
            if aluno_id:
                query_telefone = query_telefone.filter(Aluno.id != aluno_id)
            if query_telefone.first():
                erros.append("Telefone já cadastrado")
        
        if erros:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=", ".join(erros)
            )

    def criar_aluno(self, aluno: AlunoCreate):
        logger.debug(f"Criando aluno no banco de dados: {aluno.nome_completo}")
        try:
            aluno_data = aluno.model_dump()
            
            # Verificar duplicidade ANTES de processar foto
            self.verificar_duplicidade(aluno_data)
            
            if aluno_data.get('foto_perfil'):
                aluno_data['foto_perfil'] = self.processar_foto_perfil(aluno_data['foto_perfil'])
            
            db_aluno = Aluno(**aluno_data)
            self.db.add(db_aluno)
            self.db.commit()
            self.db.refresh(db_aluno)
            logger.info(f"Aluno criado com sucesso: ID {db_aluno.id}")
            return db_aluno
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Erro de integridade ao criar aluno: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao criar aluno: dado duplicado no banco de dados"
            )
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao criar aluno: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao criar aluno: {str(e)}"
            )
    
    def listar_alunos(self, skip: int = 0, limit: int = 100):
        alunos = self.db.query(Aluno).offset(skip).limit(limit).all()
        
        # NÃO normaliza CPF - deixa None se for None
        # foto_perfil é tratado pelo validator do schema
        
        return alunos
    
    def contar_alunos(self) -> int:
        """Conta o total de alunos"""
        return self.db.query(Aluno).count()
    
    def obter_aluno(self, aluno_id: int):
        logger.debug(f"Buscando aluno ID: {aluno_id}")
        aluno = self.db.query(Aluno).filter(Aluno.id == aluno_id).first()
        if aluno is None:
            logger.warning(f"Aluno ID: {aluno_id} não encontrado")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
        
        # NÃO normaliza CPF - deixa None se for None
        # foto_perfil é tratado pelo validator do schema
            
        logger.debug(f"Aluno encontrado: {aluno.nome_completo}")
        return aluno
    
    def atualizar_aluno(self, aluno_id: int, aluno: AlunoCreate):
        logger.debug(f"Atualizando aluno ID: {aluno_id}")
        db_aluno = self.obter_aluno(aluno_id)
        
        # Processar dados
        aluno_data = aluno.model_dump(exclude_unset=True)
        
        # Verificar duplicidade ANTES de processar foto (excluindo o próprio aluno)
        self.verificar_duplicidade(aluno_data, aluno_id)
        
        # Processar foto de perfil se foi enviada
        if 'foto_perfil' in aluno_data and aluno_data['foto_perfil']:
            aluno_data['foto_perfil'] = self.processar_foto_perfil(aluno_data['foto_perfil'])
        
        # Atualizar campos
        try:
            for key, value in aluno_data.items():
                setattr(db_aluno, key, value)
                
            self.db.commit()
            self.db.refresh(db_aluno)
            logger.info(f"Aluno ID: {aluno_id} atualizado com sucesso")
            return db_aluno
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Erro de integridade ao atualizar aluno: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao atualizar aluno: dado duplicado no banco de dados"
            )
    
    def deletar_aluno(self, aluno_id: int):
        logger.debug(f"Deletando aluno ID: {aluno_id}")
        aluno = self.obter_aluno(aluno_id)
        self.db.delete(aluno)
        self.db.commit()
        logger.info(f"Aluno ID: {aluno_id} deletado com sucesso")
        return {"message": "Aluno deletado com sucesso"}

    def listar_professores_do_aluno(self, aluno_id: int):
        aluno = (
            self.db.query(Aluno)
            .options(joinedload(Aluno.professores))
            .filter(Aluno.id == aluno_id)
            .first()
        )
        if not aluno:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
        return aluno.professores
    
    def associar_professor(self, aluno_id: int, professor_id: int):
        aluno = self.obter_aluno(aluno_id)
        professor = self.db.query(Professor).filter(Professor.id == professor_id).first()
        
        if not professor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor não encontrado")
        
        if professor in aluno.professores:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Professor já está associado a este aluno")
        
        aluno.professores.append(professor)
        self.db.commit()
        logger.info(f"Professor {professor_id} associado ao aluno {aluno_id}")
        return {"message": f"Professor {professor.nome_completo} associado ao aluno {aluno.nome_completo} com sucesso"}

    def desassociar_professor(self, aluno_id: int, professor_id: int):
        aluno = self.obter_aluno(aluno_id)
        professor = self.db.query(Professor).filter(Professor.id == professor_id).first()

        if not professor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor não encontrado")

        if professor not in aluno.professores:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Professor não está associado a este aluno")

        aluno.professores.remove(professor)
        self.db.commit()
        logger.info(f"Professor {professor_id} desassociado do aluno {aluno_id}")
        return {"message": f"Professor {professor.nome_completo} desassociado do aluno {aluno.nome_completo} com sucesso"}