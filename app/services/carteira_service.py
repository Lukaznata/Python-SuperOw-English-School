from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import Carteira, Administrador, ContaReceber, ContaPagar
from ..schemas import CarteiraCreate
from fastapi import HTTPException, status
from decimal import Decimal


class CarteiraService:
    def __init__(self, db: Session):
        self.db = db

    def _calcular_saldo(self, id_adm: int) -> Decimal:
        """Calcula o saldo: contas recebidas - contas pagas"""
        # Total recebido (status = True)
        total_recebido = (
            self.db.query(func.coalesce(func.sum(ContaReceber.valor), 0))
            .filter(ContaReceber.id_adm == id_adm)
            .filter(ContaReceber.status == True)
            .scalar()
        )
        total_recebido = Decimal(str(total_recebido)) if total_recebido else Decimal('0.00')
        
        # Total pago (status = True)
        total_pago = (
            self.db.query(func.coalesce(func.sum(ContaPagar.valor), 0))
            .filter(ContaPagar.id_adm == id_adm)
            .filter(ContaPagar.status == True)
            .scalar()
        )
        total_pago = Decimal(str(total_pago)) if total_pago else Decimal('0.00')
        
        return total_recebido - total_pago

    def _adicionar_saldo_calculado(self, carteira: Carteira):
        """Adiciona o saldo calculado ao objeto carteira"""
        saldo = self._calcular_saldo(carteira.id_adm)
        # Retorna um dicionário com os dados da carteira + saldo
        return {
            "id": carteira.id,
            "id_adm": carteira.id_adm,
            "saldo_atual": saldo
        }

    def criar_carteira(self, id_adm: int):
        # Verificar se administrador existe
        administrador = self.db.query(Administrador).filter(Administrador.id == id_adm).first()
        if not administrador:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrador não encontrado"
            )
        
        # Verificar se já existe carteira para este admin
        carteira_existente = self.db.query(Carteira).filter(Carteira.id_adm == id_adm).first()
        if carteira_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Administrador já possui uma carteira"
            )
        
        db_carteira = Carteira(id_adm=id_adm)
        self.db.add(db_carteira)
        self.db.commit()
        self.db.refresh(db_carteira)
        
        return self._adicionar_saldo_calculado(db_carteira)

    def obter_carteira(self, carteira_id: int):
        carteira = self.db.query(Carteira).filter(Carteira.id == carteira_id).first()
        if not carteira:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carteira não encontrada"
            )
        return self._adicionar_saldo_calculado(carteira)

    def obter_carteira_por_admin(self, id_adm: int):
        carteira = self.db.query(Carteira).filter(Carteira.id_adm == id_adm).first()
        if not carteira:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carteira não encontrada para este administrador"
            )
        return self._adicionar_saldo_calculado(carteira)

    def listar_carteiras(self, skip: int = 0, limit: int = 100):
        carteiras = self.db.query(Carteira).offset(skip).limit(limit).all()
        return [self._adicionar_saldo_calculado(c) for c in carteiras]

    def deletar_carteira(self, carteira_id: int):
        carteira = self.db.query(Carteira).filter(Carteira.id == carteira_id).first()
        if not carteira:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carteira não encontrada"
            )
        self.db.delete(carteira)
        self.db.commit()
        return {"message": "Carteira deletada com sucesso"}