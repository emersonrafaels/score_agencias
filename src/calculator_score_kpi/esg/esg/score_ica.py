from src.model_score.modelo_score_indice import IndiceConsumo


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
        ponto_a = (1.0, 9.0)  # Ponto específico para ICA
        ponto_b = (1.3, 7.0)  # Ponto específico para ICA
        super().__init__(
            ponto_a, ponto_b, indice=indice, percentual_acima=percentual_acima
        )
