from config_project.config_app import settings

from src.models.models_kpi.model_score.modelo_score_indice import IndiceConsumo


class ICA(IndiceConsumo):
    """
    Classe específica para o cálculo do Índice de Consumo de Água (ICA).
    Herda da classe IndiceConsumo.
    """

    def __init__(self, indice=None, percentual_acima=None):
        """
        Inicializa a classe ICA com os pontos específicos para cálculo.

        Parameters:
        indice (float, optional): O Índice de Consumo de Água (ICA).
        percentual_acima (float, optional): O percentual acima do consumo ideal de água.
        """
        ponto_a = settings.get("ICA.MODEL.PONTO_A")  # Ponto específico para ICA
        ponto_b = settings.get("ICA.MODEL.PONTO_B")  # Ponto específico para ICA
        super().__init__(
            ponto_a, ponto_b, indice=indice, percentual_acima=percentual_acima
        )


def Model_Score_ICA(indice, minimo, maximo, casas_decimais):
    """
    Realiza o cálculo do score para ICA.

    Parameters:
    indice (float): O valor do índice de consumo de água.
    minimo (float): O valor mínimo permitido para o score.
    maximo (float): O valor máximo permitido para o score.
    casas_decimais (int): O número de casas decimais para o arredondamento do score.
    """

    # INSTANCIANDO A CLASSE ICA
    ica = ICA(indice=indice)

    # CALCULANDO O SCORE
    score = ica.calcular_score(
        minimo=minimo, maximo=maximo, casas_decimais=casas_decimais
    )

    return score
