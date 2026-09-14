import re
from dataclasses import dataclass

from .scope_validator import is_in_scope

INJECTION_PATTERNS = (
    r"ignore (todas|as|suas|qualquer).*instru",
    r"revele.*(prompt|instruções|instrucoes)",
    r"system prompt",
    r"modo desenvolvedor",
    r"developer mode",
    r"jailbreak",
)

HIGH_RISK_TERMS = {
    "choque", "incêndio", "incendio", "fio desencapado", "curto-circuito",
    "alta tensão", "alta tensao", "disjuntor", "rede elétrica", "rede eletrica",
    "esquentando", "superaquecimento", "fumaça", "fumaca", "faísca", "faisca",
}

LEGAL_FINANCIAL_TERMS = {
    "processar", "advogado", "aconselhamento jurídico", "aconselhamento juridico",
    "investimento", "comprar ações", "comprar acoes", "retorno garantido",
}

ADMIN_TECHNICAL_PATTERNS = (
    r"(preço|preco|tarifa|valor).*(kwh|energia)",
    r"(aumentar|alterar|configurar).*(potência|potencia|carregador)",
)


@dataclass(frozen=True)
class GuardrailResult:
    allowed: bool
    response: str | None = None
    category: str = "allowed"


def moderate_input(text: str) -> GuardrailResult:
    normalized = text.lower().strip()
    if any(re.search(pattern, normalized) for pattern in INJECTION_PATTERNS):
        return GuardrailResult(False, "Não posso alterar nem revelar minhas instruções internas. Posso ajudar com mobilidade elétrica e recarga GoodWe.", "prompt_injection")
    if any(term in normalized for term in HIGH_RISK_TERMS):
        return GuardrailResult(False, "Essa situação pode envolver risco elétrico. Interrompa o uso se isso puder ser feito com segurança e procure um eletricista habilitado ou o suporte oficial. Em emergência, acione o serviço local de emergência.", "electrical_safety")
    if any(term in normalized for term in LEGAL_FINANCIAL_TERMS):
        return GuardrailResult(False, "Não forneço aconselhamento jurídico ou financeiro. Procure um profissional habilitado. Posso ajudar apenas com informações gerais sobre recarga e mobilidade elétrica.", "legal_financial")
    if any(re.search(pattern, normalized) for pattern in ADMIN_TECHNICAL_PATTERNS):
        return GuardrailResult(False, "Esta consulta está fora do meu escopo. Para assuntos administrativos ou técnicos mais complexos, por favor fale com o síndico.", "administrative_or_technical")
    if not is_in_scope(text):
        return GuardrailResult(False, "Esse assunto está fora do escopo do assistente GoodWe. Posso ajudar com mobilidade elétrica, carregadores e sessões de recarga.", "out_of_scope")
    return GuardrailResult(True)
