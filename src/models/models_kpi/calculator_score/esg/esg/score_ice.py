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
