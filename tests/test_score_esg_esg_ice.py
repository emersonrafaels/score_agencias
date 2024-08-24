import pytest
from pydantic import ValidationError
from src.calculator_score.esg.esg.score_ice import ICE


@pytest.mark.parametrize(
    "indice, score_esperado, minimo, maximo, casas_decimais",
    [
        (0.76, 10.0, 0.0, 10.0, 2),  # Teste normalizado e arredondado
        (1.0, 9.0, 0.0, 10.0, 2),  # Teste padrão
        (1.3, 7.0, 0.0, 10.0, 2),  # Teste padrão
        (1.2, 7.67, 0.0, 10.0, 2),  # Teste padrão
        (1.5, 7.0, 7.0, 7.5, 3),  # Teste com arredondamento específico
    ],
)
def test_ice_calculo_score(indice, score_esperado, minimo, maximo, casas_decimais):
    """
    Testa o cálculo do score para ICE com diferentes parâmetros.

    Parameters:
    indice (float): O valor do índice de consumo de energia.
    score_esperado (float): O valor esperado do score.
    minimo (float): O valor mínimo permitido para o score.
    maximo (float): O valor máximo permitido para o score.
    casas_decimais (int): O número de casas decimais para o arredondamento do score.
    """
    ice = ICE(indice=indice)
    assert (
        ice.calcular_score(minimo=minimo, maximo=maximo, casas_decimais=casas_decimais)
        == score_esperado
    )


@pytest.mark.parametrize(
    "percentual_acima, indice_esperado",
    [
        (50, 1.5),
        (0, 1.0),
        (100, 2.0),
    ],
)
def test_ice_percentual_acima(percentual_acima, indice_esperado):
    """
    Testa o cálculo do índice de consumo de energia (ICE) com base no percentual acima do ideal.

    Parameters:
    percentual_acima (float): O percentual acima do consumo ideal.
    indice_esperado (float): O valor esperado do índice de consumo.
    """
    ice = ICE(percentual_acima=percentual_acima)
    assert ice.calcular_indice() == indice_esperado


def test_ice_validacao_erro():
    """
    Testa se a validação de erro é lançada quando ambos os parâmetros 'indice' e 'percentual_acima'
    são fornecidos, o que não é permitido.
    """
    with pytest.raises(ValidationError):
        ICE(indice=1.5, percentual_acima=50)
