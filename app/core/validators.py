"""
Módulo de validações customizadas para o sistema
"""
import re
from typing import Optional


def validar_cpf(cpf: Optional[str]) -> Optional[str]:
    """
    Valida CPF brasileiro.
    
    Args:
        cpf: String contendo o CPF (pode conter pontos e hífen)
        
    Returns:
        CPF formatado sem pontos e hífen se válido
        
    Raises:
        ValueError: Se o CPF for inválido
    """
    if cpf is None:
        return None
    
    # Remove caracteres não numéricos
    cpf_limpo = re.sub(r'\D', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf_limpo) != 11:
        raise ValueError('CPF deve conter 11 dígitos')
    
    # Verifica se todos os dígitos são iguais (CPF inválido)
    if cpf_limpo == cpf_limpo[0] * 11:
        raise ValueError('CPF inválido')
    
    # Validação do primeiro dígito verificador
    soma = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    if int(cpf_limpo[9]) != digito1:
        raise ValueError('CPF inválido')
    
    # Validação do segundo dígito verificador
    soma = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    if int(cpf_limpo[10]) != digito2:
        raise ValueError('CPF inválido')
    
    return cpf_limpo


def validar_telefone(telefone: str) -> str:
    """
    Valida telefone brasileiro (celular ou fixo).
    
    Formatos aceitos:
    - (11) 98765-4321
    - (11) 3456-7890
    - 11987654321
    - 1134567890
    
    Args:
        telefone: String contendo o telefone
        
    Returns:
        Telefone formatado apenas com números
        
    Raises:
        ValueError: Se o telefone for inválido
    """
    if not telefone:
        raise ValueError('Telefone é obrigatório')
    
    # Remove caracteres não numéricos
    telefone_limpo = re.sub(r'\D', '', telefone)
    
    # Verifica se tem 10 ou 11 dígitos (DDD + número)
    if len(telefone_limpo) not in [10, 11]:
        raise ValueError('Telefone deve ter 10 (fixo) ou 11 (celular) dígitos com DDD')
    
    # Verifica se o DDD é válido (código de área entre 11 e 99)
    ddd = int(telefone_limpo[:2])
    if ddd < 11 or ddd > 99:
        raise ValueError('DDD inválido')
    
    # Se for celular (11 dígitos), verifica se o nono dígito é 9
    if len(telefone_limpo) == 11 and telefone_limpo[2] != '9':
        raise ValueError('Celular deve começar com 9 após o DDD')
    
    return telefone_limpo


def validar_telefone_opcional(telefone: Optional[str]) -> Optional[str]:
    """
    Valida telefone brasileiro opcional.
    
    Args:
        telefone: String contendo o telefone ou None
        
    Returns:
        Telefone formatado ou None
        
    Raises:
        ValueError: Se o telefone for inválido
    """
    if telefone is None or telefone.strip() == '':
        return None
    
    return validar_telefone(telefone)


def validar_valor_positivo(valor, nome_campo: str = 'Valor') -> float:
    """
    Valida se um valor é positivo (maior que zero).
    
    Args:
        valor: Valor numérico a ser validado
        nome_campo: Nome do campo para mensagem de erro
        
    Returns:
        O valor validado
        
    Raises:
        ValueError: Se o valor não for positivo
    """
    if valor < 0:
        raise ValueError(f'{nome_campo} deve ser maior que zero')
    return valor


def validar_dia_cobranca(dia: Optional[int]) -> Optional[int]:
    """
    Valida o dia de cobrança (1-31).
    
    Args:
        dia: Dia do mês para cobrança
        
    Returns:
        O dia validado ou None
        
    Raises:
        ValueError: Se o dia for inválido
    """
    if dia is None:
        return None
    
    if dia < 1 or dia > 31:
        raise ValueError('Dia de cobrança deve estar entre 1 e 31')
    
    return dia


def validar_mei(mei: Optional[str]) -> Optional[str]:
    """
    Valida número de MEI (14 dígitos).
    
    Args:
        mei: String contendo o número do MEI
        
    Returns:
        MEI formatado apenas com números
        
    Raises:
        ValueError: Se o MEI for inválido
    """
    if mei is None or mei.strip() == '':
        return None
    
    # Remove caracteres não numéricos
    mei_limpo = re.sub(r'\D', '', mei)
    
    # Verifica se tem 14 dígitos
    if len(mei_limpo) != 14:
        raise ValueError('MEI deve conter 14 dígitos')
    
    return mei_limpo
