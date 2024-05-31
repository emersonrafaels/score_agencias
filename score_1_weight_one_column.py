from utils import score_functions
from utils.pandas_functions import load_data


def orchestra_score(dir_data):
    # NOME DA COLUNA QUE RECEBERÁ A QUANTIDADE COM PESOS
    column_quantity_weight = "Quantidade Peso"

    # NOME DA COLUNA QUE RECEBERÁ O SCORE CALCULADO
    name_column_result_score = "Score"

    # OBTENDO OS DADOS
    df = load_data(dir_data=dir_data)

    # AGRUPANDO OS DADOS
    df_group = score_functions.group_dataframe(
        df=df,
        aggregation_type="size",
        list_columns_group=["Agência", "Depois da Reforma"],
        name_column_result="Quantidade",
    )

    # APLICANDO PESOS DIFERENTES PARA A COLUNA DEPOIS DA REFORMA
    # ANTES = PESO 0.3
    # DEPOIS = PES 0.7

    df_group[column_quantity_weight] = df_group.apply(
        lambda row: score_functions.apply_weight(
            row,
            column_value="Quantidade",
            column_weight="Depois da Reforma",
            weight_false=0.3,
            weight_true=0.7,
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
    dir_data = "data/Manutencoes_Agencias.xlsx"

    df_result_score = orchestra_score(dir_data=dir_data)

    print(df_result_score)
