import numpy as np

from src.models.models_kpi.model_score.modelo_score_faixa import FaixaScore, ScorePorFaixa

# Faixas do Score de ATM
faixas_score = [
    FaixaScore(
        limite_inferior=0, limite_superior=99.5, score_min=0, score_max=7
    ),
    FaixaScore(
        limite_inferior=99.51, limite_superior=100, score_min=7, score_max=10
    ),
]

# Instanciando a calculadora genérica do Score por faixa
calculadora_score = ScorePorFaixa(faixas=faixas_score)

# INICIANDO A LISTA DE PARÂMETROS
# Gera os valores de entrada de 0 a 10 com steps de 0.1
list_params = np.arange(0, 100.1, 0.1)
for entrada in list_params:
    score = calculadora_score.calcular_score(entrada, model="disponibilidade")
    print(f"Entrada: {entrada} -> Score calculado: {score}")