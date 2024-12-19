from config_project.config_app import settings
from src.models.models_kpi.model_score.modelo_score_inflexao import Score_Inflexao


class TCX(Score_Inflexao):
    """
    Classe específica para o cálculo do Score de TCX baseado em reinicializações.
    Herda da classe Score_Inflexao.
    """

    def __init__(self):
        """
        Inicializa a classe TCX com os pontos específicos para cálculo.

        Parameters:
        """
        # Obtendo o ponto central do modelo a partir das configurações
        ponto_central = settings.get("TCX.MODEL.PONTO_A")  # Ponto central (x1, y1)

        # Definimos qual será o comportamento do score, após o ponto central (x > ponto central)
        direcao = "decrescente"

        # Valor maximo de reinicializações
        limite_superior = 5
        # Valor minimo de reinicializações
        limite_inferior = 0

        # Inicializando a classe pai com os pontos
        super().__init__(ponto_central=ponto_central,
                         direcao=direcao,
                         limite_superior=limite_superior,
                         limite_inferior=limite_inferior)


def Model_Score_TCX(reinicializacoes):
    """
    Realiza o cálculo do score para TCX.

    Parameters:
    reinicializacoes (float): Número de reinicializações do equipamento.

    Returns:
    float: O score calculado.
    """
    # Instanciando a classe TCX
    tcx = TCX()

    # Calculando o score
    score = tcx.calcular_score(valor_x=reinicializacoes)

    return score
