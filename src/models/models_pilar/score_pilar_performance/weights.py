"""
Módulo de Validação de Pesos

Este módulo contém a classe Weights, que é usada para validar a soma dos pesos em diversas partes do sistema,
assegurando que a soma dos pesos seja exatamente 1.0, conforme necessário para o cálculo proporcional correto dos scores.

Autor: Emerson V. Rafael (emervin)
Versão: 1.0.0
Data de Atualização: 26/09/2024
"""

from pydantic import BaseModel, validator


class Weights(BaseModel):
    """
    Classe Weights usada para validar se a soma dos pesos em uma lista de pesos é igual a 1.0.

    Attributes:
        weights (list): Lista de pesos numéricos que devem somar 1.0.
    """

    weights: list

    @validator("weights", pre=True, always=True)
    def check_weights_sum(cls, v):
        """
        Valida se a soma dos pesos na lista é igual a 1.0.

        Arguments:
            v (list): Lista de pesos a ser validada.

        Returns:
            list: Retorna a lista original se a soma for 1.0.

        Raises:
            ValueError: Se a soma dos pesos não for igual a 1.0.
        """
        if sum(v) != 1.0:
            raise ValueError("A soma dos pesos deve ser igual a 1.0")
        return v
