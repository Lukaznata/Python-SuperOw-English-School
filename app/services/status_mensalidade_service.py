from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, extract
from app.models import StatusMensalidade, Aluno
from app.schemas.status_mensalidade import StatusMensalidadeCreate, StatusMensalidadeUpdate
from typing import List, Optional
from datetime import date

class StatusMensalidadeService:
    
    @staticmethod
    def create(db: Session, mensalidade_data: StatusMensalidadeCreate) -> StatusMensalidade:
        """Criar uma nova mensalidade"""
        # Verificar se o aluno existe
        aluno = db.query(Aluno).filter(Aluno.id == mensalidade_data.aluno_id).first()
        if not aluno:
            raise ValueError("Aluno não encontrado")
        
        mensalidade = StatusMensalidade(**mensalidade_data.model_dump())
        db.add(mensalidade)
        db.commit()
        db.refresh(mensalidade)
        return mensalidade
    
    @staticmethod
    def get_by_id(db: Session, mensalidade_id: int) -> Optional[StatusMensalidade]:
        """Buscar mensalidade por ID"""
        return db.query(StatusMensalidade).options(
            joinedload(StatusMensalidade.aluno)
        ).filter(StatusMensalidade.id == mensalidade_id).first()
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        aluno_id: Optional[int] = None,
        status: Optional[str] = None,
        mes: Optional[int] = None,
        ano: Optional[int] = None
    ) -> tuple[List[StatusMensalidade], int]:
        """Listar mensalidades com filtros opcionais"""
        query = db.query(StatusMensalidade).options(
            joinedload(StatusMensalidade.aluno)
        )
        
        # Filtros
        if aluno_id:
            query = query.filter(StatusMensalidade.aluno_id == aluno_id)
        
        if status:
            query = query.filter(StatusMensalidade.status == status)
        
        if mes:
            query = query.filter(extract('month', StatusMensalidade.data) == mes)
        
        if ano:
            query = query.filter(extract('year', StatusMensalidade.data) == ano)
        
        # Ordenar por data decrescente
        query = query.order_by(StatusMensalidade.data.desc())
        
        total = query.count()
        mensalidades = query.offset(skip).limit(limit).all()
        
        return mensalidades, total
    
    @staticmethod
    def get_by_aluno(db: Session, aluno_id: int) -> List[StatusMensalidade]:
        """Buscar todas as mensalidades de um aluno"""
        return db.query(StatusMensalidade).filter(
            StatusMensalidade.aluno_id == aluno_id
        ).order_by(StatusMensalidade.data.desc()).all()
    
    @staticmethod
    def get_by_mes_ano(db: Session, mes: int, ano: int) -> List[StatusMensalidade]:
        """Buscar mensalidades por mês e ano"""
        return db.query(StatusMensalidade).options(
            joinedload(StatusMensalidade.aluno)
        ).filter(
            and_(
                extract('month', StatusMensalidade.data) == mes,
                extract('year', StatusMensalidade.data) == ano
            )
        ).all()
    
    @staticmethod
    def get_pendentes(db: Session) -> List[StatusMensalidade]:
        """Buscar mensalidades pendentes"""
        return db.query(StatusMensalidade).options(
            joinedload(StatusMensalidade.aluno)
        ).filter(
            StatusMensalidade.status.in_(["Pendente", "Atrasado"])
        ).order_by(StatusMensalidade.data).all()
    
    @staticmethod
    def update(
        db: Session,
        mensalidade_id: int,
        mensalidade_data: StatusMensalidadeUpdate
    ) -> Optional[StatusMensalidade]:
        """Atualizar uma mensalidade"""
        mensalidade = db.query(StatusMensalidade).filter(
            StatusMensalidade.id == mensalidade_id
        ).first()
        
        if not mensalidade:
            return None
        
        update_data = mensalidade_data.model_dump(exclude_unset=True)
        
        # Verificar se está mudando o aluno
        if "aluno_id" in update_data:
            aluno = db.query(Aluno).filter(Aluno.id == update_data["aluno_id"]).first()
            if not aluno:
                raise ValueError("Aluno não encontrado")
        
        for field, value in update_data.items():
            setattr(mensalidade, field, value)
        
        db.commit()
        db.refresh(mensalidade)
        return mensalidade
    
    @staticmethod
    def delete(db: Session, mensalidade_id: int) -> bool:
        """Deletar uma mensalidade"""
        mensalidade = db.query(StatusMensalidade).filter(
            StatusMensalidade.id == mensalidade_id
        ).first()
        
        if not mensalidade:
            return False
        
        db.delete(mensalidade)
        db.commit()
        return True
    
    @staticmethod
    def get_total_por_status(db: Session, mes: Optional[int] = None, ano: Optional[int] = None):
        """Obter totais agrupados por status"""
        query = db.query(StatusMensalidade)
        
        if mes:
            query = query.filter(extract('month', StatusMensalidade.data) == mes)
        if ano:
            query = query.filter(extract('year', StatusMensalidade.data) == ano)
        
        mensalidades = query.all()
        
        totais = {
            "pago": 0,
            "pendente": 0,
            "atrasado": 0,
            "total": 0
        }
        
        for m in mensalidades:
            totais["total"] += m.valor
            if m.status.lower() == "pago":
                totais["pago"] += m.valor
            elif m.status.lower() == "pendente":
                totais["pendente"] += m.valor
            elif m.status.lower() == "atrasado":
                totais["atrasado"] += m.valor
        
        return totais