from pydantic import BaseModel, root_validator, ValidationError
from typing import Optional


class IndiceConsumoBase:
    """
    Classe base para cálculo de índices de consumo (ICA, ICE).

    Contém a lógica comum para calcular o slope, intercepto e score.
    """

    def __init__(self, ponto_a, ponto_b):
        """
        Inicializa a classe base com dois pontos para a equação linear.

        Parameters:
        ponto_a (tuple): O primeiro ponto (x1, y1).
        ponto_b (tuple): O segundo ponto (x2, y2).
        """

        # RECEBENDO O PONTO A (COM X1 E Y1)
        self.ponto_a = ponto_a

        # RECEBENDO O PONTO B (COM X2 E Y2)
        self.ponto_b = ponto_b

        # CALCULANDO O COEFICIENTE ANGULAR (m)
        self.declive = self.calcular_declive(ponto_a, ponto_b)

        # CALCULANDO O COEFICIENTE LINEAR (b)
        self.intercepto = self.calcular_intercepto(self.declive, ponto_a)

    def calcular_declive(self, ponto_a, ponto_b):
        """
        Calcula o declive (slope) da linha que conecta dois pontos.

        Parameters:
        ponto_a (tuple): O primeiro ponto (x1, y1).
        ponto_b (tuple): O segundo ponto (x2, y2).

        Returns:
        float: O declive da linha.
        """
        x1, y1 = ponto_a
        x2, y2 = ponto_b
        return (y2 - y1) / (x2 - x1)

    def calcular_intercepto(self, declive, ponto):
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

    def calcular_valor(self, x):
        """
        Calcula o valor de y com base em x, usando a equação da linha.

        Parameters:
        x (float): O valor de entrada para calcular y.

        Returns:
        float: O valor calculado de y.
        """
        return self.declive * x + self.intercepto


class ConsumoModel(BaseModel):
    """
    Modelo de validação de dados para consumo (ICA, ICE).

    Utiliza Pydantic para garantir que os dados fornecidos sejam válidos.
    """

    indice: Optional[float] = None
    percentual_acima: Optional[float] = None

    @root_validator(pre=True)
    def check_indice_or_percentual(cls, values):
        """
        Valida se apenas um dos campos (indice ou percentual_acima) foi fornecido.

        Raises:
        ValueError: Se ambos os valores forem fornecidos ou se nenhum for fornecido.

        Returns:
        dict: Os valores validados.
        """
        indice = values.get("indice")
        percentual_acima = values.get("percentual_acima")

        if indice is not None and percentual_acima is not None:
            raise ValueError(
                "Você deve fornecer apenas 'indice' ou 'percentual_acima', não ambos."
            )
        elif indice is None and percentual_acima is None:
            raise ValueError("Você deve fornecer 'indice' ou 'percentual_acima'.")

        return values


class IndiceConsumo(IndiceConsumoBase):
    """
    Classe principal para cálculo do score de consumo, estendida da base IndiceConsumoBase.
    """

    def __init__(self, ponto_a, ponto_b, indice=None, percentual_acima=None):
        """
        Inicializa a classe com dados validados pelo modelo Pydantic.

        Parameters:
        ponto_a (tuple): O primeiro ponto (x1, y1).
        ponto_b (tuple): O segundo ponto (x2, y2).
        indice (float, optional): O índice de consumo (ICA ou ICE).
        percentual_acima (float, optional): O percentual acima do consumo ideal.
        """

        # CRIANDO A EQUAÇÃO
        super().__init__(ponto_a, ponto_b)

        # VALIDANDO OS DADOS
        model = ConsumoModel(indice=indice, percentual_acima=percentual_acima)

        # INICIANDO AS VARIÁVEIS
        self.indice = model.indice
        self.percentual_acima = model.percentual_acima

    def calcular_percentual(self):
        """
        Calcula o percentual acima do ideal baseado no índice de consumo.

        Returns:
        float: O percentual acima do ideal, se o índice for >= 1, ou 0 se for menor que 1.
        """
        if self.indice >= 1:
            return (self.indice - 1) * 100
        return 0

    def calcular_indice(self):
        """
        Calcula o índice de consumo baseado no percentual acima do ideal.

        Returns:
        float: O valor do índice de consumo.
        """
        return (self.percentual_acima / 100) + 1

    def calcular_score(self, minimo=None, maximo=None, casas_decimais=2):
        """
        Calcula o score com base no índice de consumo usando a equação linear.

        Parameters:
        minimo (float, optional): O valor mínimo que o score pode assumir.
        maximo (float, optional): O valor máximo que o score pode assumir.
        casas_decimais (int, optional): O número de casas decimais para arredondamento. Default é 2.

        Returns:
        float: O score calculado com base no índice de consumo, ajustado para a escala mínima e máxima, e arredondado.
        """
        if self.indice is not None:
            score = self.calcular_valor(self.indice)

            # Normaliza o score para a escala mínima e máxima, se fornecida
            if minimo is not None and maximo is not None:
                score = max(minimo, min(maximo, score))
            else:
                score = min(
                    max(score, 0), 10
                )  # Garante que o score esteja entre 0 e 10

            # Arredonda o score para o número especificado de casas decimais
            return round(score, casas_decimais)
        return None