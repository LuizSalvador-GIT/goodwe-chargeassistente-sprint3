import re

EV_TERMS = {
    "goodwe", "veículo elétrico", "veiculo eletrico", "carregador", "carregamento",
    "recarga", "bateria", "energia", "potência", "potencia", "kwh", "kw",
    "conector", "estação", "estacao", "wallbox", "faturamento", "sessão", "sessao",
    "consumo", "rateio", "carro", "cabo", "horário", "horario", "síndico", "sindico",
    "condomínio", "condominio", "agendar", "reservar", "disponível", "disponivel",
}

SOCIAL_TERMS = {"oi", "olá", "ola", "obrigado", "obrigada", "ajuda", "bom dia", "boa tarde"}


def is_in_scope(text: str) -> bool:
    normalized = re.sub(r"\s+", " ", text.lower()).strip()
    return any(term in normalized for term in EV_TERMS | SOCIAL_TERMS)
