import pandas as pd

def load_data(dir_data):

    """
		LÊ OS DADOS DO ARQUIVO EXCEL E RETORNA UM DATAFRAME.

		# Arguments
				dir_data             - Required: Diretório onde estão
								                 os dados (String | Path)

		# Returns:
				df                   - Required: Dataframe contendo os
							                     dados carregados
							                     (pd.DataFrame)
    """

    # Lendo os dados
    df = pd.read_excel(dir_data)

    return df