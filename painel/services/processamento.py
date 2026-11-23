from dataclasses import dataclass

from painel.core.entidades import Aluno, Nota
from painel.core.metricas import calcular_media_disciplina
from painel.core.validador import validar_alunos, validar_notas
from painel.infra.arquivos import ler_csv, ler_json

@dataclass(frozen=True)
class ResumoAluno:
    aluno: Aluno
    media: float | None
    situacao: str

@dataclass(frozen=True)
class ResultadoProcessamento:
    resumos_alunos: list[ResumoAluno]
    notas_validas: list[Nota]
    medias_disciplinas: dict[str, float]
    erros_alunos: list[str]
    erros_notas: list[str]

    @property
    def erros(self) -> list[str]:
        return self.erros_alunos + self.erros_notas

def executar_processamento(
        caminho_alunos: str,
        caminho_notas: str,
        caminho_config: str,
    ) -> ResultadoProcessamento:
        config = ler_json(caminho_config)

        linhas_alunos = ler_csv(caminho_alunos)
        alunos, erros_alunos = validar_alunos(linhas_alunos)

        linhas_notas = ler_csv(caminho_notas)
        notas, erros_notas = validar_notas(
            linhas_notas,
            alunos,
            config["nota_maxima"],
        )

        resumos_alunos = [
            ResumoAluno(
                aluno=aluno,
                media=aluno.media(notas),
                situacao=aluno.situacao(
                    notas,
                    config["media_aprovacao"],
                    config["media_recuperacao"],
                ),
            )
            for aluno in alunos
        ]

        return ResultadoProcessamento(
            resumos_alunos=resumos_alunos,
            notas_validas=notas,
            medias_disciplinas=calcular_media_disciplina(notas),
            erros_alunos=erros_alunos,
            erros_notas=erros_notas,
        )
