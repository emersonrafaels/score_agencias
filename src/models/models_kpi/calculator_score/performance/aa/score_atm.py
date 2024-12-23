import numpy as np

from src.models.models_kpi.model_score.modelo_score_faixa import FaixaScore, ScorePorFaixa

# Faixas do Score de ATM
faixas_score = [
    FaixaScore(
        limite_inferior=0, limite_superior=4, score_min=9, score_max=10
    ),
    FaixaScore(
        limite_inferior=4.01, limite_superior=8, score_min=7, score_max=9
    ),
    FaixaScore(
        limite_inferior=8.01, limite_superior=100, score_min=0, score_max=7
    ),
]

# Instanciando a calculadora genérica do Score por faixa
calculadora_score = ScorePorFaixa(faixas=faixas_score)

# INICIANDO A LISTA DE PARÂMETROS
# Gera os valores de entrada de 0 a 10 com steps de 0.1
list_params = np.arange(0, 100, 0.1)
for entrada in list_params:
    score = calculadora_score.calcular_score(entrada, model="indisponibilidade")
    print(f"Entrada: {entrada} -> Score calculado: {score}")