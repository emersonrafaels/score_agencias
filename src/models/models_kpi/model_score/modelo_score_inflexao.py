from typing import Tuple
import numpy as np


class Score_Inflexao:
    """
    Classe para mapear valores de uma variável X para um score ajustável.

    Suporta dois casos principais:
    1. Score decresce com o aumento de X.
    2. Score cresce com o aumento de X.
    """

    def __init__(
        self,
        ponto_central: Tuple[float, float],
        max_score: float = 10,
        min_score: float = 0,
        direcao: str = "decrescente",
        limite_superior: float = None,
        limite_inferior: float = None,
    ):
        """
        Inicializa a classe com os parâmetros de mapeamento.

        Parameters:
        ponto_central (tuple): O ponto central (x, score).
        max_score (float): O score máximo alcançável (default: 10).
        min_score (float): O score mínimo alcançável (default: 0).
        direcao (str): Define se o score é "crescente" ou "decrescente".
        limite_superior (float, optional): Limite superior para X (caso crescente).
        limite_inferior (float, optional): Limite inferior para X (caso decrescente).
        """
        self.ponto_central = ponto_central
        self.max_score = max_score
        self.min_score = min_score
        self.direcao = direcao

        # Configura limites com base na direção
        if direcao == "crescente":
            self.limite_superior = limite_superior or ponto_central[0] + 1
            self.limite_inferior = limite_inferior or 0
        elif direcao == "decrescente":
            self.limite_inferior = limite_inferior or 0
            self.limite_superior = limite_superior or ponto_central[0] + 1
        else:
            raise ValueError("A direção deve ser 'crescente' ou 'decrescente'.")

        # Declives das retas (antes e depois do ponto central)
        self._calcular_declives()

    def _calcular_declives(self):
        """
        Calcula os declives para as duas regiões da função linear.
        """
        x_central, score_central = self.ponto_central

        # Verificação para evitar divisão por zero no limite superior
        if self.limite_superior <= x_central:
            self.limite_superior = x_central + 1

        if self.direcao == "decrescente":
            # Antes do ponto central (crescendo para max_score)
            self.declive_antes = -((self.max_score - score_central) / (x_central - self.limite_inferior))
            # Depois do ponto central (decrescendo para min_score)
            self.declive_depois = (self.min_score - score_central) / (self.limite_superior - x_central)
        elif self.direcao == "crescente":
            # Antes do ponto central (decrescendo para min_score)
            self.declive_antes = (score_central - self.min_score) / (x_central - self.limite_inferior)
            # Depois do ponto central (crescendo para max_score)
            self.declive_depois = (self.max_score - score_central) / (self.limite_superior - x_central)

    def _calcular_intercepto(self, declive: float, ponto: Tuple[float, float]) -> float:
        """
        Calcula o intercepto da linha com base no declive e em um ponto.

        Parameters:
        declive (float): O declive da linha.
        ponto (tuple): Um ponto (x, y) que a linha passa.

        Returns:
        float: O intercepto da linha.
        """
        x, y = ponto
        return y - declive * x

    def calcular_score(self, valor_x: float, casas_decimais: int = 2) -> float:
        """
        Calcula o score com base no valor de X.

        Parameters:
        valor_x (float): O valor de X.
        casas_decimais (int, optional): Número de casas decimais para arredondamento. Default é 2.

        Returns:
        float: O score calculado.
        """
        x_central, score_central = self.ponto_central

        if valor_x < x_central:
            # Antes ou no ponto central
            declive = self.declive_antes
            intercepto = self._calcular_intercepto(declive, (self.limite_inferior, self.max_score))
        else:
            # Depois do ponto central
            declive = self.declive_depois
            intercepto = self._calcular_intercepto(declive, (x_central, score_central))

        # Calcula o score
        score = declive * valor_x + intercepto

        # Garante que o score está no intervalo permitido
        score = max(self.min_score, min(self.max_score, score))

        return round(score, casas_decimais)

    def __str__(self):
        """
        Representação amigável da configuração da classe.
        """
        return (
            f"Score_Inflexao("
            f"Ponto central: {self.ponto_central}, "
            f"Score máximo: {self.max_score}, "
            f"Score mínimo: {self.min_score}, "
            f"Direção: {self.direcao}, "
            f"Limite superior: {self.limite_superior}, "
            f"Limite inferior: {self.limite_inferior})"
        )


# Testes
if __name__ == "__main__":
    score_model = Score_Inflexao(ponto_central=(2, 7), direcao="decrescente")
    test_values = [4, 2, 1, 0, 7]

    for value in test_values:
        print(f"VALOR DE ENTRADA: ({value},) --> SCORE: {score_model.calcular_score(value)}")
