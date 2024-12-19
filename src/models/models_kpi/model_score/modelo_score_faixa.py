from pydantic import BaseModel, root_validator
from typing import Optional, List, Union


class FaixaScore(BaseModel):
    """
    Modelo genérico para definição de faixas com limites e scores associados.
    """
    limite_inferior: float
    limite_superior: float
    score_min: float
    score_max: float

    @root_validator(pre=True)
    def validar_faixas(cls, values):
        """
        Valida os limites inferior e superior e os scores associados.
        """
        if values['limite_inferior'] >= values['limite_superior']:
            raise ValueError("O limite inferior deve ser menor que o limite superior.")
        if values['score_min'] > values['score_max']:
            raise ValueError("O score mínimo deve ser menor ou igual ao score máximo.")
        return values


class ScorePorFaixa:
    """
    Calculadora genérica para scores baseados em faixas.
    """

    def __init__(self, faixas: List[FaixaScore]):
        """
        Inicializa a calculadora com faixas predefinidas.

        Parameters:
        faixas (List[FaixaScore]): Lista de faixas com limites e scores.
        """
        self.faixas = sorted(faixas, key=lambda faixa: faixa.limite_inferior)

    def calcular_score(
        self, entrada: float,
            arredondar: Optional[int] = 2,
            model="indisponibilidade"
    ) -> Union[float, None]:
        """
        Calcula o score associado à entrada com base nas faixas definidas.

        Parameters:
        entrada (float): O valor de entrada a ser avaliado.
        arredondar (Optional[int]): Número de casas decimais para arredondar o resultado. Default: 2.

        Returns:
        Union[float, None]: O score calculado ou None se a entrada estiver fora das faixas.
        """

        if model == "indisponibilidade":
            for faixa in self.faixas:
                if faixa.limite_inferior <= entrada <= faixa.limite_superior:
                    score = faixa.score_max - (
                            (entrada - faixa.limite_inferior)
                            / (faixa.limite_superior - faixa.limite_inferior)
                    ) * (faixa.score_max - faixa.score_min)
                    return round(score,
                                 arredondar) if arredondar is not None else score
            return None  # Fora das faixas definidas

        if model == "disponibilidade":
            for faixa in self.faixas:
                if faixa.limite_inferior <= entrada <= faixa.limite_superior:
                    if entrada == faixa.limite_superior and faixa.score_max > faixa.score_min:
                        return faixa.score_max
                    score = faixa.score_min + ((entrada - faixa.limite_inferior) / (
                                faixa.limite_superior - faixa.limite_inferior)) * (
                                        faixa.score_max - faixa.score_min)
                    return round(score,
                                 arredondar) if arredondar is not None else score
            return None
