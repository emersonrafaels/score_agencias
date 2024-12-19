import numpy as np

from src.models.models_kpi.calculator_score.performance.ab.score_tcx import Model_Score_TCX

def execute_calc_score_tcx():
    """
    Testa o cálculo do score para TCX com diferentes parâmetros.
    """

    # INICIANDO A LISTA DE PARÂMETROS
    # Gera os valores de entrada de 0 a 10 com steps de 0.1
    list_params = np.arange(0, 10.1, 0.1)

    # PERCORRENDO A LISTA DE PARÂMETROS
    for parameters in list_params:

        # CHAMANDO A FUNÇAO PARA CALCULAR O SCORE ICA
        score = Model_Score_TCX(parameters)

        print("VALOR DE ENTRADA: {} --> SCORE: {}".format(parameters, score))


if __name__ == "__main__":
    execute_calc_score_tcx()
