import json
from abc import ABC, abstractmethod

from painel.services.processamento import ResultadoProcessamento

class GeradorRelatorio(ABC):
    @abstractmethod
    def render(self, resultado: ResultadoProcessamento) -> str:
        pass

class RelatorioTexto(GeradorRelatorio):
    def render(self, resultado: ResultadoProcessamento) -> str:
        linhas = [
            "PAINEL DE NOTAS - RESUMO",
            f"Alunos processados: {len(resultado.resumos_alunos)}",
            (
                f"Registros de nota válidos: {len(resultado.notas_validas)} "
                f"| inválidos: {len(resultado.erros_notas)}"
            ),
            "",
            "Situação dos alunos",
        ]

        for resumo in resultado.resumos_alunos:
            media = (
                f"{resumo.media:.2f}"
                if resumo.media is not None
                else "sem média"
            )
            linhas.append(
                f" {resumo.aluno.nome:<25} {resumo.aluno.turma:<6} "
                f"média {media:<8} {resumo.situacao}"
            )

        linhas.extend(["", "Média por disciplina"])
        for disciplina, media in sorted(resultado.medias_disciplinas.items()):
            linhas.append(f" {disciplina:<25} {media:.2f}")

        linhas.extend(["", f"Erros encontrados ({len(resultado.erros)})"])
        linhas.extend(f"{erro}   " for erro in resultado.erros)

        return "\n".join(linhas) + "\n"

class RelatorioJson(GeradorRelatorio):
    def render(self, resultado: ResultadoProcessamento) -> str:
        documento = {
            "resumo": {
                "alunos_processados": len(resultado.resumos_alunos),
                "notas_validas": len(resultado.notas_validas),
                "notas_invalidas": len(resultado.erros_notas),
            },
            "alunos": [
                {
                    "matricula": resumo.aluno.matricula,
                    "nome": resumo.aluno.nome,
                    "turma": resumo.aluno.turma,
                    "media": resumo.media,
                    "situacao": resumo.situacao,
                }
                for resumo in resultado.resumos_alunos
            ],
            "medias_disciplinas": resultado.medias_disciplinas,
            "erros": resultado.erros,
        }
        return json.dumps(documento, ensure_ascii=False, indent=2) + "\n"

def criar_gerador(formato: str) -> GeradorRelatorio:
    geradores: dict[str, type[GeradorRelatorio]] = {
        "texto": RelatorioTexto,
        "json": RelatorioJson,
    }

    try:
        classe_geradora = geradores[formato]
    except KeyError as erro:
        raise ValueError(f"Formato de relatório inválido: {formato}") from erro
    
    return classe_geradora()