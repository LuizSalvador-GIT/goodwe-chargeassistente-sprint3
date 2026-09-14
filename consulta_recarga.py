from enum import Enum

from pydantic import BaseModel, Field, field_validator


class EstadoCarregador(str, Enum):
    disponivel = "disponivel"
    carregando = "carregando"
    indisponivel = "indisponivel"
    desconhecido = "desconhecido"


class ConsultaRecarga(BaseModel):
    """Informações normalizadas de uma consulta sobre uma sessão de recarga."""

    carregador_id: str = Field(min_length=1, description="Identificador do carregador")
    estado: EstadoCarregador = EstadoCarregador.desconhecido
    potencia_kw: float | None = Field(default=None, ge=0, le=1000)
    energia_kwh: float | None = Field(default=None, ge=0)
    valor_brl: float | None = Field(default=None, ge=0)
    mensagem: str = Field(min_length=1, max_length=500)

    @field_validator("carregador_id")
    @classmethod
    def normalizar_id(cls, value: str) -> str:
        normalized = value.strip().upper()
        if not normalized:
            raise ValueError("carregador_id não pode ser vazio")
        return normalized

    @field_validator("potencia_kw", "energia_kwh", "valor_brl", mode="before")
    @classmethod
    def aceitar_decimal_com_virgula(cls, value):
        if isinstance(value, str):
            return value.replace(",", ".")
        return value
