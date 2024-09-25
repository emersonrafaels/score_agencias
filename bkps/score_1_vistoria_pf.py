from src.utils.pandas_functions import load_data
from src.models_kpi.model_score import score_functions
from src.models_kpi.model_score.score import Score


def transformar_pesos(df):
    """
    Transforma um DataFrame de pesos em um
    dicionário de categorias e pesos por coluna.

    # Arguments:
        df                     - Required: DataFrame contendo as colunas
                                          'COLUNA', 'CATEGORIA' e
                                          'PESO'. (pd.DataFrame)

    # Returns:
        dict                   - Required: Um dicionário onde cada chave
                                            é uma coluna do DataFrame e
                                            o valor é um dicionário
                                            com a estrutura:
                                                {
                                                    "column": <nome_da_coluna>,
                                                    "categories": {
                                                        <categoria1>: <peso1>,
                                                        <categoria2>: <peso2>,
                                                        ...
                                                    }
                                                }
                                            (Dict)

        Exemplo:
        # DataFrame de entrada:
        df_weights = pd.DataFrame({
            "COLUNA": ["STATUS", "STATUS", "STATUS", "DATA_VISTORIA"],
            "CATEGORIA": ["APROVADO", "REJEITADA", "REVERTIDA", "TEMPO"],
            "PESO": [-1, 1, 0.5, "EXPONENCIAL"]
        })

        # Chamada da função:
        pesos_transformados = transformar_pesos(df_weights)

        # Resultado esperado:
        {
            "STATUS": {
                "column": "STATUS",
                "categories": {
                    "APROVADO": -1,
                    "REJEITADA": 1,
                    "REVERTIDA": 0.5
                }
            },
            "DATA_VISTORIA": {
                "column": "DATA_VISTORIA",
                "categories": {
                    "TEMPO": "EXPONENCIAL"
                }
            }
        }

        Exemplo desejado:
        # DECLARANDO OS PESOS ANTES/DEPOIS DA REFORMA
        weights_reforma = {
            "column": "Depois da Reforma",
            "categories": {"Sim": 0.7, "Não": 0.3},
        }

    """

    # INICIANDO O DICT QUE ARMAZENARÁ O RESULTADO
    pesos_dict = {}

    # PERCORRENDO CADA LINHA DO DATAFRAME DE PESOS
    for _, row in df.iterrows():
        # OBTENDO A COLUNA ATUAL
        coluna = row["COLUNA"]

        # VERIFICANDO SE A COLUNA JÁ CONSTA COMO KEY DO DATAFRAME
        if coluna not in pesos_dict:
            pesos_dict[coluna] = {"column": coluna, "categories": {}}

        # OBTENDO CATEGORIA E O PESO DO VALOR
        categoria = row["CATEGORIA"]
        peso = row["PESO"]
        pesos_dict[coluna]["categories"][categoria] = peso

    return pesos_dict


def declare_weights(df_weights):
    # INSTANCIANDO A CLASSE DE SCORE
    score = Score()

    # TRANSFORMANDO O DATAFRAME NO FORMATO DE PESOS DESEJADOS
    pesos_transformados = transformar_pesos(df_weights)

    for idx, key in pesos_transformados.items():
        # VERIFICANDO SE A KEY É LINEAR OU EXPONENCIAL, PARA INDICAR TEMPO
        if (set(key.get("categories").keys()).intersection(["TEMPO"])) and (
            set(key.get("categories").values()).intersection(["LINEAR", "EXPONENCIAL"])
        ):
            _ = score.insert_str(key)

        else:
            _ = score.insert_values(key)

    return score


def orchestra_score(
    dir_data,
    sheetname_data=0,
    dir_data_weights="",
    sheetname_weights=0,
    validator_group=False,
    list_columns_group=[],
):
    # OBTENDO OS DADOS
    df = load_data(dir_data=dir_data, sheetname=sheetname_data)

    # OBTENDO OS PESOS
    df_weights = load_data(dir_data=dir_data_weights, sheetname=sheetname_weights)

    # DECLARANDO A VARIÁVEL DE PESOS
    score = declare_weights(df_weights)

    # NOME DA COLUNA QUE RECEBERÁ A QUANTIDADE COM PESOS
    column_quantity_weight = "Resultado Ponderado"

    # NOME DA COLUNA QUE RECEBERÁ O SCORE CALCULADO
    name_column_result_score = "Score"

    normalize_to_high_score = True

    if validator_group:
        # AGRUPANDO OS DADOS
        df_group = score_functions.group_dataframe(
            df=df,
            aggregation_type="size",
            list_columns_group=["AGENCIA", "DATA_VISTORIA", "STATUS"],
            name_column_result="QUANTIDADE",
        )

    else:
        df_group = df.copy()

    # APLICANDO OS PESOS
    df_group[column_quantity_weight] = df_group.apply(
        lambda row: score_functions.apply_weights(
            row,
            column_value="QUANTIDADE",
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
        list_columns_group_result=["AGENCIA"],
    )

    return df_result_score


if __name__ == "__main__":
    # BASE COM DADOS A SEREM LIDOS
    dir_data = r"C:\Users\Emerson\Desktop\Itaú\Comunidade Infra de Canais Físicos\Projetos\Score de Agências\Calculadora_Pesos.xlsx"
    sheetname_data = "BASE DE DADOS VISTORIA PF STA"

    # BASE CONTENDO OS PESOS PARA SCORAR
    dir_data_weights = "../data/Bases_Score.xlsx"
    sheetname_weights = "PESO_VISTORIA_PF"

    validator_group = False
    list_columns_group = ["AGENCIA", "DATA_VISTORIA", "STATUS"]

    _ = orchestra_score(
        dir_data=dir_data,
        sheetname_data=sheetname_data,
        dir_data_weights=dir_data_weights,
        sheetname_weights=sheetname_weights,
        validator_group=validator_group,
        list_columns_group=list_columns_group,
    )
