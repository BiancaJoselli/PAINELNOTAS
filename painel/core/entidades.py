from dataclasses import dataclass


@dataclass(frozen=True)
class Nota:
    matricula: int
    disciplina: str
    avaliacao: str
    nota: float


@dataclass(frozen=True)
class Aluno:
    matricula: int
    nome: str
    turma:str

    def media(self, notas: list[Nota]) -> float | None:
        notas_aluno = [
            item.nota for item in notas
            if item.matricula == self.matricula
        ]

        if not notas_aluno:
            return None
        
        return sum(notas_aluno) / len(notas_aluno)

    def situacao(self, notas: list[Nota], media_aprovacao: float, media_recuperacao: float,) -> str:
        media_aluno = self.media(notas)

        if media_aluno is None:
            return "sem notas"
        if media_aluno >= media_aprovacao:
            return "aprovado"
        if media_aluno >= media_recuperacao:
            return "recuperação"
        return "reprovado"