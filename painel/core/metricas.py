from painel.core.entidades import Nota

def calcular_media_disciplina(notas: list[Nota]) -> dict[str, float]:
    totais = {}
    quantidades = {}

    for nota in notas:
        totais[nota.disciplina] = (
            totais.get(nota.disciplina, 0.0) + nota.nota
        )
        quantidades[nota.disciplina] = (
            quantidades.get(nota.disciplina, 0) + 1
        )

    return {
        disciplina: totais[disciplina] / quantidades[disciplina]
        for disciplina in totais
    }