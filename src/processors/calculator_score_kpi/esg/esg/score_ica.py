from src.models.models_kpi.calculator_score.esg.esg.score_ica import Model_Score_ICA

def execute_calc_ica_score():
    """
    Testa o cálculo do score para ICA com diferentes parâmetros.
    """

    # INICIANDO A LISTA DE PARÂMETROS
    list_params = [
        (0.76, 0.0, 10.0, 2),  # Teste normalizado e arredondado
        (1.0, 0.0, 10.0, 2),  # Teste padrão
        (1.3, 0.0, 10.0, 2),  # Teste padrão
        (1.2, 0.0, 10.0, 2),  # Teste padrão
        (2.5, 0.0, 10.0, 2),  # Teste padrão
        (1.3, 7.123, 7.5, 3),  # Teste com arredondamento específico
    ]

    # PERCORRENDO A LISTA DE PARÂMETROS
    for parameters in list_params:
        # CHAMANDO A FUNÇAO PARA CALCULAR O SCORE ICA
        score = Model_Score_ICA(*parameters)

        print("VALOR DE ENTRADA: {} --> SCORE: {}".format(parameters, score))


if __name__ == "__main__":
    execute_calc_ica_score()
