import os
from pathlib import Path
from typing import Optional, Union

import pandas as pd
from loguru import logger


def load_data_auto(
    file_path: str,
    sheet_name: Optional[Union[str, int]] = 0,
    usecols: Optional[Union[str, list]] = None,
    skiprows: Optional[Union[int, list]] = None,
    nrows: Optional[int] = None,
    dtype: Optional[dict] = None,
    parse_dates: Optional[Union[bool, list, dict]] = False,
) -> pd.DataFrame:
    """
    Carrega um DataFrame automaticamente baseado no tipo de arquivo (Excel, CSV, Parquet).

    :param file_path: Caminho completo para o arquivo de dados.
    :param sheet_name: Nome ou índice da folha para arquivos Excel.
    :param usecols: Colunas a serem lidas.
    :param skiprows: Linhas iniciais a pular ao ler o arquivo.
    :param nrows: Número de linhas para ler.
    :param dtype: Tipos de dados para as colunas.
    :param parse_dates: Analisar colunas como datas.
    :return: DataFrame carregado do arquivo.
    """
    # Determina o tipo do arquivo pela extensão
    file_extension = Path(file_path).suffix.lower()

    try:
        if file_extension in [".xls", ".xlsx"]:
            df = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                usecols=usecols,
                skiprows=skiprows,
                nrows=nrows,
                dtype=dtype,
                parse_dates=parse_dates,
                engine="openpyxl",
            )
        elif file_extension == ".csv":
            df = pd.read_csv(
                file_path,
                usecols=usecols,
                skiprows=skiprows,
                nrows=nrows,
                dtype=dtype,
                parse_dates=parse_dates,
            )
        elif file_extension == ".parquet":
            df = pd.read_parquet(file_path, columns=usecols, engine="pyarrow")
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

        logger.info(f"DataFrame carregado com sucesso de {file_path}")
        return df

    except Exception as e:
        logger.error(f"Erro ao carregar o arquivo {file_path}: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro


def save_data_auto(
    dataframe: pd.DataFrame, file_path: str, index: bool = False, **kwargs
) -> None:
    """
    Salva um DataFrame em um arquivo especificado, criando diretórios se não existirem.

    :param dataframe: DataFrame a ser salvo.
    :param file_path: Caminho completo para o arquivo de destino.
    :param index: Se deve incluir o índice do DataFrame na saída.
    :param kwargs: Argumentos adicionais específicos para cada tipo de arquivo.
    """
    # Cria o diretório se não existir
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Determina o tipo do arquivo pela extensão
    file_extension = Path(file_path).suffix.lower().strip(".")

    # Mapeia a extensão para o método de salvamento adequado
    if file_extension == "csv":
        dataframe.to_csv(file_path, index=index, **kwargs)
    elif file_extension == "xlsx":
        dataframe.to_excel(file_path, index=index, engine="openpyxl", **kwargs)
    elif file_extension == "parquet":
        dataframe.to_parquet(file_path, index=index, engine="pyarrow", **kwargs)
    else:
        raise ValueError(f"Unsupported file format for extension {file_extension}")

    logger.info(f"DataFrame salvo com sucesso em {file_path}")
