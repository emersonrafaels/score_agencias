from src.utils.pandas_functions import load_data_auto
from src.models.models_kpi.model_score.score import Score
from src.models.models_kpi.model_score.normalization_functions import *
from src.utils.plot_functions import seaborn_functions, plotly_functions


def declare_weights():
    # INSTANCIANDO A CLASSE DE SCORE
    score = Score()

    # DECLARANDO OS PESOS ANTES/DEPOIS DA REFORMA
    weights_reforma = {
        "column": "Depois da Reforma",
        "categories": {"Sim": 0.7, "Não": 0.3},
    }

    # DECLARANDO OS PESOS POR TIPO DE MANUTENÇÃO
    weights_tipo_de_manutencao = {
        "column": "Tipo de Manutenção",
        "categories": {
            "Elétrica": 0.25,
            "Hidráulica": 0.2,
            "Civil": 0.2,
            "Ar condicionado": 0.2,
            "Mecânica": 0.2,
        },
    }

    # SALVANDO TODOS OS PESOS INICIALIZADOS NA VARIÁVEL DE PESOS
    _ = score.insert(weights_reforma)
    _ = score.insert(weights_tipo_de_manutencao)

    return score


def orchestra_score(dir_data, sheetname=0, col_name=""):
    # DECLARANDO A VARIÁVEL DE PESOS
    score = declare_weights()

    # NOME DA COLUNA QUE RECEBERÁ A QUANTIDADE COM PESOS
    column_quantity_weight = "Resultado Ponderado"

    # NOME DA COLUNA QUE RECEBERÁ O SCORE CALCULADO
    name_column_result_score = "Score"

    normalize_to_high_score = True

    # OBTENDO OS DADOS
    df = load_data_auto(dir_data=dir_data, sheetname=sheetname)

    # APLICANDO A NORMALIZAÇÃO
    df["SCORE_ROBUST_NORM"] = robust_normalizaton(
        values=df[col_name], option_normalize_to_high_score=normalize_to_high_score
    )

    # APLICANDO A NORMALIZAÇÃO
    df["SCORE_NORM"] = normalize_values(
        values=df[col_name], option_normalize_to_high_score=normalize_to_high_score
    )

    # REMOVENDO OUTLIERS E APLICANDO A NORMALIZAÇÃO
    df["SCORE_NORM2"] = normalize_data_with_outliers(
        values=df[col_name], option_normalize_to_high_score=normalize_to_high_score
    )

    try:
        df.to_excel(
            f"normalizaton_high_{str(normalize_to_high_score)}.xlsx", index=None
        )
    except Exception as ex:
        print(ex)

    # VISUALIZANDO O RESULTADO
    seaborn_functions.boxplot(
        df,
        ["Custo 2", "SCORE_NORM", "SCORE_ROBUST_NORM", "SCORE_NORM2"],
        "Boxplot para Múltiplas Colunas",
        color_points=True,
    )

    plotly_functions.boxplot_plotly(
        df,
        ["Custo 2", "SCORE_NORM", "SCORE_ROBUST_NORM", "SCORE_NORM2"],
        "Boxplot para Múltiplas Colunas",
        color_points=True,
    )

    return df


if __name__ == "__main__":
    dir_data = "../data/Manutencoes_Agencias.xlsx"

    sheetname = "CUSTO"

    col_name = "Custo 2"

    _ = orchestra_score(dir_data=dir_data, sheetname=sheetname, col_name=col_name)
