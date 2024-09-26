from src.models.models_kpi.model_score import score_functions
from src.utils.pandas_functions import load_data_auto

from src.models.models_kpi.model_score.score import Score


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


def orchestra_score(dir_data):
    # DECLARANDO A VARIÁVEL DE PESOS
    score = declare_weights()

    # NOME DA COLUNA QUE RECEBERÁ A QUANTIDADE COM PESOS
    column_quantity_weight = "Resultado Ponderado"

    # NOME DA COLUNA QUE RECEBERÁ O SCORE CALCULADO
    name_column_result_score = "Score"

    # OBTENDO OS DADOS
    df = load_data_auto(dir_data=dir_data)

    # AGRUPANDO OS DADOS
    df_group = score_functions.group_dataframe(
        df=df,
        aggregation_type="size",
        list_columns_group=["Agência", "Depois da Reforma", "Tipo de Manutenção"],
        name_column_result="Quantidade",
    )

    # APLICANDO OS PESOS
    df_group[column_quantity_weight] = df_group.apply(
        lambda row: score_functions.apply_weights(
            row,
            column_value="Quantidade",
            weights=score.weights,
        ),
        axis=1,
    )

    # OBTENDO O SCORE NORMALIZADO
    df_result_score = score_functions.get_score(
        df=df_group,
        normalize_to_high_score=True,
        name_column_value=column_quantity_weight,
        name_column_result=name_column_result_score,
        list_columns_group_result=["Agência"],
    )

    return df_result_score


if __name__ == "__main__":
    dir_data = "../data/Manutencoes_Agencias.xlsx"

    df_result_score = orchestra_score(dir_data=dir_data)

    print(df_result_score)
