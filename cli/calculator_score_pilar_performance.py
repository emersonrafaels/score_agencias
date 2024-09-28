import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import typer

from src.models.models_pilar.score_pilar_performance.performance_calculator import (
    ScorePilarPerformance,
)
from src.models.models_pilar.score_pilar_performance.models import ScoreDetails
from src.utils.pandas_functions import load_data_auto, save_data_auto

# Instanciando o typer
app = typer.Typer()

# Definindo o peso default dos temas
default_weight = 1 / 3
default_weight_rounded = round(1 / 3, 2)

def adjust_default_weights(weights, default_weight, default_weight_rounded):
    # Verifica se todos os pesos são iguais ao peso padrão arredondado
    if all(weight == default_weight_rounded for weight in weights):
        # Define todos os pesos para o valor padrão não arredondado
        return (default_weight,) * len(weights)
    return weights


@app.command()
def main(
    input_dir: Path = typer.Option(
        ...,
        exists=True,
        file_okay=False,
        help="Caminho para o diretório com os arquivos de score.",
    ),
    output_dir: Path = typer.Option(
        ..., file_okay=False, help="Caminho para salvar o arquivo de resultados."
    ),
    output_file: str = typer.Option(
        "BASE_SCORE_PILAR_PERFORMANCE.xlsx", help="Nome do arquivo de saída."
    ),
    include_aa: bool = typer.Option(default=True, help="Incluir scores de AA"),
    include_ab: bool = typer.Option(default=True, help="Incluir scores de AB"),
    include_infra: bool = typer.Option(
        default=True, help="Incluir scores de Infra Civil"
    ),
    weight_aa: float = typer.Option(
        default=default_weight_rounded, help="Peso para scores de AA"
    ),
    weight_ab: float = typer.Option(
        default=default_weight_rounded, help="Peso para scores de AB"
    ),
    weight_infra: float = typer.Option(
        default=default_weight_rounded, help="Peso para scores de Infra Civil"
    ),
):
    details_list = []

    # Obtendo o peso default padrão
    weights = adjust_default_weights([weight_aa, weight_ab, weight_infra],
                                     default_weight, default_weight_rounded)

    weight_aa, weight_ab, weight_infra = weights

    if include_aa:
        df_aa = load_data_auto(Path(input_dir, "AA", "BASE_SCORE_AA.xlsx"))
        details_list.append(
            ScoreDetails(
                dataframe=df_aa,
                score_column="SCORE_TEMA",
                weight=weight_aa,
                category="AA",
            )
        )
    if include_ab:
        df_ab = load_data_auto(Path(input_dir, "AB", "BASE_SCORE_AB.xlsx"))
        details_list.append(
            ScoreDetails(
                dataframe=df_ab,
                score_column="SCORE_TEMA",
                weight=weight_ab,
                category="AB",
            )
        )
    if include_infra:
        df_infra_civil = load_data_auto(
            Path(input_dir, "INFRA_CIVIL", "BASE_SCORE_INFRA_CIVIL.xlsx")
        )
        details_list.append(
            ScoreDetails(
                dataframe=df_infra_civil,
                score_column="SCORE_TEMA",
                weight=weight_infra,
                category="INFRA_CIVIL",
            )
        )

    if not details_list:
        typer.echo("Nenhuma categoria de score foi selecionada. Encerrando execução.")
        raise typer.Exit()

    if details_list:
        # Assumindo uniformidade nas datas entre os pilares
        dia = details_list[0].dataframe["DIA"].iloc[0]
        mes = details_list[0].dataframe["MES"].iloc[0]
        ano = details_list[0].dataframe["ANO"].iloc[0]

        score_calculator = ScorePilarPerformance(
            details_list=details_list, dia=dia, mes=mes, ano=ano
        )
        df_score_pilar = score_calculator.score_pilar

        output_path = output_dir / output_file
        output_dir.mkdir(parents=True, exist_ok=True)

        save_data_auto(dataframe=df_score_pilar, file_path=output_path)

        typer.echo(f"Scores calculados e salvos com sucesso em {output_path}")


if __name__ == "__main__":
    app()
