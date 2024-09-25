from src.models_kpi.calculator_score.esg.esg.score_ica import ICA


def calc_ica_score_using_indice(indice, minimo, maximo, casas_decimais):
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
    result_score = ica.calcular_score(
        minimo=minimo, maximo=maximo, casas_decimais=casas_decimais
    )

    return result_score


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
        result_score = calc_ica_score_using_indice(*parameters)

        print("SCORE OBTIDO: {}".format(result_score))


if __name__ == "__main__":
    execute_calc_ica_score()
