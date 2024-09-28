"""
Módulo de Detalhes e Cálculo de Score

Este módulo define as classes para detalhes de score e cálculo base de score pilar,
utilizando pesos especificados para calcular e armazenar os resultados em um DataFrame.

Autor: Emerson V. Rafael (emervin)
Versão: 1.0.0
Data de Atualização: 26/09/2024
"""

from pydantic import BaseModel
from typing import Any


class ScoreDetails(BaseModel):
    """
    Modelo de detalhes do score para armazenar informações necessárias para o cálculo do score.

    Attributes:
        dataframe (Any): DataFrame contendo os dados necessários para o cálculo.
        score_column (str): Nome da coluna no DataFrame que contém os scores a serem ponderados.
        weight (float): Peso aplicado ao score durante o cálculo do score pilar.
    """

    dataframe: Any
    score_column: str
    weight: float
    category: str


class BaseScore:
    """
    Classe base para cálculo do score pilar com base em detalhes fornecidos.

    Attributes:
        details (ScoreDetails): Objeto contendo os detalhes necessários para o cálculo do score.

    Methods:
        weighted_score: Multiplica os scores pela respectiva ponderação e armazena o resultado no DataFrame.
    """

    def __init__(self, details: ScoreDetails):
        self.dataframe = details.dataframe
        self.score_column = details.score_column
        self.weight = details.weight
        self.weighted_score()

    def weighted_score(self):
        """
        Calcula o score pilar multiplicando os valores da
        coluna de score pelo peso e armazenando o
        resultado de volta no DataFrame.

        Modifica o DataFrame original adicionando
        uma nova coluna 'SCORE_PILAR'
        que contém os scores ponderados.
        """
        self.dataframe["SCORE_PILAR"] = self.dataframe[self.score_column] * self.weight
