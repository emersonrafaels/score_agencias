"""
Módulo de Cálculo de Score Pilar

Este módulo calcula os scores combinados dos pilares com base em pesos especificados e salva o resultado em um arquivo Excel.

"""

__author__ = "Emerson V. Rafael (emervin)"
__version__ = "1.0.0"
__data_atualizacao__ = "26/09/2024"

from pathlib import Path
from loguru import logger

from src.models.models_pilar.score_pilar_performance.performance_calculator import (
    ScorePilarPerformance,
)
from src.models.models_pilar.score_pilar_performance.models import ScoreDetails
from src.utils.pandas_functions import load_data_auto, save_data_auto


def main_execute_score_performance():
    """
    Executa a função principal para carregar scores, calcular o score pilar combinado e salvar a saída.

    Este script realiza as seguintes etapas:
    - Carrega dados de score de arquivos Excel para diferentes categorias.
    - Calcula o score pilar combinado usando pesos especificados para cada categoria.
    - Salva o DataFrame resultante em um arquivo Excel.

    Arguments:
        None

    Returns:
        None
    """
    dir_root = Path(Path(__file__).parent.parent.parent.parent)
    dir_root_performance = Path(dir_root, "data/data_tema/PERFORMANCE")

    # Carregando os dataframes
    df_aa = load_data_auto(Path(dir_root_performance, "AA", "BASE_SCORE_AA.xlsx"))
    df_ab = load_data_auto(Path(dir_root_performance, "AB", "BASE_SCORE_AB.xlsx"))

    details_list = [
        ScoreDetails(
            dataframe=df_aa,
            score_column="SCORE_TEMA",
            weight=0.5,
            category="AA",
        ),
        ScoreDetails(
            dataframe=df_ab,
            score_column="SCORE_TEMA",
            weight=0.5,
            category="AB",
        ),
    ]

    # Extraindo uma data comum dos dados, assumindo uniformidade
    dia = df_aa["DIA"].iloc[0]
    mes = df_aa["MES"].iloc[0]
    ano = df_aa["ANO"].iloc[0]

    # Calculando o score pilar
    score_calculator = ScorePilarPerformance(
        details_list=details_list, dia=dia, mes=mes, ano=ano
    )
    score_pilar_df = score_calculator.score_pilar

    save_data_auto(
        dataframe=score_pilar_df,
        file_path=Path(
            dir_root,
            "data/data_pilar/PERFORMANCE",
            "BASE_SCORE_TEMA_PERFORMANCE_v2.xlsx",
        ),
        index=False,
    )

    logger.info("Processo realizado com sucesso")


if __name__ == "__main__":
    main_execute_score_performance()
