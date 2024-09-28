"""
Módulo de Cálculo de Score Pilar

Este módulo calcula os scores combinados dos pilares com base em pesos especificados e salva o resultado em um arquivo Excel.

"""

__author__ = "Emerson V. Rafael (emervin)"
__version__ = "1.0.0"
__data_atualizacao__ = "26/09/2024"

from pathlib import Path
from loguru import logger

from src.models.models_global.score_global.global_calculator import (
    ScoreGlobalCalculator,
)
from src.models.models_global.score_global.models import ScoreDetails
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
    dir_root_pilar = Path(dir_root, "data/data_pilar")

    # Carregando os dataframes
    df_tema_esg = load_data_auto(
        Path(dir_root_pilar, "ESG", "BASE_SCORE_TEMA_ESG.xlsx")
    )
    df_tema_performance = load_data_auto(
        Path(dir_root_pilar, "PERFORMANCE", "BASE_SCORE_TEMA_PERFORMANCE.xlsx")
    )

    details_list = [
        ScoreDetails(
            dataframe=df_tema_esg,
            score_column="SCORE_PILAR",
            farol_column="FAROL_PILAR",
            weight=0.7,
            category="ESG",
        ),
        ScoreDetails(
            dataframe=df_tema_performance,
            score_column="SCORE_PILAR",
            farol_column="FAROL_PILAR",
            weight=0.3,
            category="PERFORMANCE",
        ),
    ]

    # Extraindo uma data comum dos dados, assumindo uniformidade
    dia = df_tema_esg["DIA"].iloc[0]
    mes = df_tema_esg["MES"].iloc[0]
    ano = df_tema_esg["ANO"].iloc[0]

    # Calculando o score pilar
    score_calculator = ScoreGlobalCalculator(
        details_list=details_list, dia=dia, mes=mes, ano=ano
    )
    df_score_global = score_calculator.score_global

    save_data_auto(
        dataframe=df_score_global,
        file_path=Path(dir_root, "data/data_global", "BASE_SCORE_GLOBAL.xlsx"),
        index=False,
    )

    logger.info("Processo realizado com sucesso")


if __name__ == "__main__":
    main_execute_score_performance()
