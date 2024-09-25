from pathlib import Path

from src.models.models_pilar.performance.calculator_score_pilar import ScorePilarPerformance

# OBTENDO O DIRETÓRIO RAIZ DE PERFORMANCE
dir_root = Path(Path(__file__).parent.parent.parent,
				"data/result/PERFORMANCE")

# Uso da classe
file_paths = {
    'AA': Path(dir_root, "AA", "BASE_SCORE_AA.xlsx"),
    'AB': Path(dir_root, "AA", "BASE_SCORE_AB.xlsx"),
    'Infra_Civil': Path(dir_root, "AA", "BASE_SCORE_INFRA_CIVIL.xlsx")
}

pesos = {
    'peso_aa': 0.3,
    'peso_ab': 0.5,
    'peso_infra_civil': 0.2
}

# Criando uma instância da classe com os parâmetros desejados
score_calculator = ScorePilarPerformance(pesos['peso_aa'], pesos['peso_ab'], pesos['peso_infra_civil'], file_paths)
print(score_calculator.score_pilar)