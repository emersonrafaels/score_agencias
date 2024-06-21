from loguru import logger
from pydantic import BaseModel, validator
from typing import Dict, Union


class Weight_Float(BaseModel):
    column: str
    categories: Dict[Union[str, bool], float]

    @validator("categories")
    def check_categories_values(cls, v):
        # O PESO DEVE SER UM VALOR ENTRE 0 E 1
        if any(weight < 0 or weight > 1 for weight in v.values()):
            raise ValueError("Os pesos das categorias devem estar entre 0 e 1.")
        return v

class Weight_Str(BaseModel):
    column: str
    categories: Dict[Union[str, bool], str]

    @validator("categories")
    def check_categories_values(cls, v):
        # O PESO DEVE SER UM VALOR ENTRE 0 E 1
        if any(not isinstance(weight, str) for weight in v.values()):
            raise ValueError("Os pesos das categorias devem ser string")
        return v


class Score:
    def __init__(self):
        """
        INICIALIZA UMA INSTÂNCIA DA CLASSE SCORE, PREPARANDO UM DICIONÁRIO PARA ARMAZENAR OS PESOS.
        """
        self.weights = {}

    def insert_values(self, weight: Dict):
        """
        INSERE UM DICIONÁRIO DE PESOS NA INSTÂNCIA DE SCORE, VALIDADO PELO MODELO PYDANTIC.

        O PESO DEVE SER UM DICIONÁRIO QUE SEGUE O PADRÃO, VALIDADO PELO MODELO `Weight`:
        - "COLUMN": NOME DA COLUNA PARA A QUAL O PESO SERÁ APLICADO,
        - "CATEGORIES": UM SUBDICIONÁRIO COM CATEGORIAS DA COLUNA E SEUS PESOS ASSOCIADOS.

        EXEMPLOS:
        - EX 01:
            WEIGHTS_REFORMA = {
                "COLUMN": "DEPOIS DA REFORMA",
                "CATEGORIES": {TRUE: 0.7, FALSE: 0.3}
            }

        - EX 02:
            WEIGHTS_TIPO_DE_MANUTENCAO = {
                "COLUMN": "TIPO DE MANUTENÇÃO",
                "CATEGORIES": {
                    "ELÉTRICA": 0.25,
                    "HIDRÁULICA": 0.2,
                    "CIVIL": 0.2,
                    "AR CONDICIONADO": 0.2,
                    "MECÂNICA": 0.2
                }
            }

        PARÂMETROS:
            WEIGHT (DICT): O PESO A SER INSERIDO, CONFORME O PADRÃO DESCRITO.

        RETORNA:
            BOOL: TRUE SE O PESO FOI INSERIDO COM SUCESSO, FALSE CASO CONTRÁRIO.
        """
        try:
            valid_weight = Weight_Float(**weight)
            self.weights[valid_weight.column] = valid_weight.categories
            logger.info(
                f"PESO INSERIDO COM SUCESSO - COLUMN: {valid_weight.column}, CATEGORIES: {valid_weight.categories}"
            )
            return True
        except Exception as e:
            logger.error(f"PESO NÃO INSERIDO COM SUCESSO - {str(e)}")
            return False

    def insert_str(self, weight: Dict):
        """
        INSERE UM DICIONÁRIO DE PESOS NA INSTÂNCIA DE SCORE, VALIDADO PELO MODELO PYDANTIC.

        O PESO DEVE SER UM DICIONÁRIO QUE SEGUE O PADRÃO, VALIDADO PELO MODELO `Weight`:
        - "COLUMN": NOME DA COLUNA PARA A QUAL O PESO SERÁ APLICADO,
        - "CATEGORIES": UM SUBDICIONÁRIO COM CATEGORIAS DA COLUNA E SEUS PESOS ASSOCIADOS.

        PARÂMETROS:
            WEIGHT (DICT): O PESO A SER INSERIDO, CONFORME O PADRÃO DESCRITO.

        RETORNA:
            BOOL: TRUE SE O PESO FOI INSERIDO COM SUCESSO, FALSE CASO CONTRÁRIO.
        """
        try:
            valid_weight = Weight_Str(**weight)
            self.weights[valid_weight.column] = valid_weight.categories
            logger.info(
                f"PESO INSERIDO COM SUCESSO - COLUMN: {valid_weight.column}, CATEGORIES: {valid_weight.categories}"
            )
            return True
        except Exception as e:
            logger.error(f"PESO NÃO INSERIDO COM SUCESSO - {str(e)}")
            return False
