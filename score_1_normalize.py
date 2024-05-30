import pandas as pd

from utils import score_functions


def load_data(dir_data):
    """
    LÊ OS DADOS DO ARQUIVO EXCEL E RETORNA UM DATAFRAME.

    # Arguments
            dir_data                     - Required: Diretório onde estão
                                                                                             os dados (String | Path)

    # Returns:
            df                           - Required: Dataframe contendo os
                                                                                             dados carregados
                                                                                             (pd.DataFrame)
    """

    # Lendo os dados
    df = pd.read_excel(dir_data)

    return df


def orchestra_score(dir_data):
    # OBTENDO OS DADOS
    df = load_data(dir_data=dir_data)

    # AGRUPANDO OS DADOS
    df_group = score_functions.group_dataframe(
        df=df,
        aggregation_type="size",
        list_columns_group="Agência",
        name_column_result="Quantidade"
    )

    # OBTENDO O SCORE
    df_result_score = score_functions.get_score(
        df=df_group,
        normalize_to_high_score=True,
        name_column_value="Quantidade",
        name_column_result="Score_Normalizado",
    )

    return df_result_score


if __name__ == "__main__":
    dir_data = "data/Manutencoes_Agencias.xlsx"

    df_result_score = orchestra_score(dir_data=dir_data)

    print(df_result_score)
