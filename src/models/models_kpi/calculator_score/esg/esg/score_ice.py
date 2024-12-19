from src.models.models_kpi.model_score.modelo_score_indice import IndiceConsumo


class ICE(IndiceConsumo):
    """
    Classe específica para o cálculo do Índice de Consumo de Energia (ICE).
    Herda da classe IndiceConsumo.
    """

    def __init__(self, indice=None, percentual_acima=None):
        """
        Inicializa a classe ICE com os pontos específicos para cálculo.

        Parameters:
        indice (float, optional): O Índice de Consumo de Energia (ICE).
        percentual_acima (float, optional): O percentual acima do consumo ideal de energia.
        """
        ponto_a = (1.0, 9.0)  # Ponto específico para ICE
        ponto_b = (1.3, 7.0)  # Ponto específico para ICE
        super().__init__(
            ponto_a, ponto_b, indice=indice, percentual_acima=percentual_acima
        )

def Model_Score_ICE(indice, minimo, maximo, casas_decimais):
    """
    Realiza o cálculo do score para ICE.

    Parameters:
    indice (float): O valor do índice de consumo de energia.
    minimo (float): O valor mínimo permitido para o score.
    maximo (float): O valor máximo permitido para o score.
    casas_decimais (int): O número de casas decimais para o arredondamento do score.
    """

    # INSTANCIANDO A CLASSE ICA
    ice = ICE(indice=indice)

    # CALCULANDO O SCORE
    score = ice.calcular_score(
        minimo=minimo, maximo=maximo, casas_decimais=casas_decimais
    )

    return score