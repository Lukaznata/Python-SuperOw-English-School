from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import ContaReceber, Administrador
from ..schemas import ContaReceberCreate, ContaReceberUpdate
from fastapi import HTTPException, status
from datetime import date

class ContaReceberService:
    def __init__(self, db: Session):
        self.db = db

    def criar_conta(self, id_adm: int, conta: ContaReceberCreate):
        # Verificar se administrador existe
        administrador = self.db.query(Administrador).filter(Administrador.id == id_adm).first()
        if not administrador:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrador não encontrado"
            )
        
        db_conta = ContaReceber(
            id_adm=id_adm,
            **conta.model_dump()
        )
        self.db.add(db_conta)
        self.db.commit()
        self.db.refresh(db_conta)
        return db_conta

    def listar_contas(self, id_adm: int = None, skip: int = 0, limit: int = 100, status: bool = None):
        query = self.db.query(ContaReceber)
        
        if id_adm:
            query = query.filter(ContaReceber.id_adm == id_adm)
        
        if status is not None:
            query = query.filter(ContaReceber.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    def contar_contas(self, id_adm: int = None, status: bool = None) -> int:
        """Conta o total de contas a receber"""
        query = self.db.query(ContaReceber)
        
        if id_adm:
            query = query.filter(ContaReceber.id_adm == id_adm)
        
        if status is not None:
            query = query.filter(ContaReceber.status == status)
        
        return query.count()

    def obter_conta(self, conta_id: int, id_adm: int):
        conta = self.db.query(ContaReceber).filter(ContaReceber.id == conta_id).first()
        if not conta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conta a receber não encontrada"
            )
        
        # Verificar se a conta pertence ao administrador
        if conta.id_adm != id_adm:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar esta conta"
            )
        
        return conta

    def atualizar_conta(self, conta_id: int, conta: ContaReceberUpdate, id_adm: int):
        db_conta = self.obter_conta(conta_id, id_adm)
        for key, value in conta.model_dump(exclude_unset=True).items():
            setattr(db_conta, key, value)
        self.db.commit()
        self.db.refresh(db_conta)
        return db_conta

    def marcar_como_recebida(self, conta_id: int, id_adm: int):
        db_conta = self.obter_conta(conta_id, id_adm)
        db_conta.status = True
        self.db.commit()
        self.db.refresh(db_conta)
        return db_conta
    
    def marcar_como_pendente(self, conta_id: int, id_adm: int):
        db_conta = self.obter_conta(conta_id, id_adm)
        db_conta.status = False
        self.db.commit()
        self.db.refresh(db_conta)
        return db_conta

    def deletar_conta(self, conta_id: int, id_adm: int):
        conta = self.obter_conta(conta_id, id_adm)
        self.db.delete(conta)
        self.db.commit()
        return {"message": "Conta a receber deletada com sucesso"}

    def total_a_receber(self, id_adm: int, status: bool = None):
        """Retorna total de contas a receber (filtrado por status se fornecido)"""
        query = self.db.query(func.sum(ContaReceber.valor)).filter(ContaReceber.id_adm == id_adm)
        
        if status is not None:
            query = query.filter(ContaReceber.status == status)
        
        total = query.scalar()
        return total or 0