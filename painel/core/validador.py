from painel.core.entidades import Aluno, Nota

def campo_valido(valor: str | None) -> bool:
    return valor is not None and bool(valor.strip())

def nota_valida(valor: str) -> bool:
    try:
        float(valor)
    except ValueError:
        return False
    return True

def validar_alunos(
    linhas: list[tuple[int, dict[str, str]]],
) -> tuple[list[Aluno], list[str]]:
    alunos_validos = []
    erros = []
    matriculas_cadastradas = set()

    for numero_linha, linha in linhas:
        campos_vazios = [
            campo
            for campo in ("matricula", "nome", "turma")
            if not campo_valido(linha.get(campo, ""))
        ]

        if campos_vazios:
            erros.append(
                f"alunos.csv:{numero_linha} campo_vazio: "
                f"{', '.join(campos_vazios)}"
            )
            continue

        matricula_texto = linha["matricula"].strip()
        nome = linha["nome"].strip()
        turma = linha["turma"].strip()

        try:
            matricula = int(matricula_texto)
        except ValueError:
            erros.append(
                f"alunos.csv:{numero_linha}  "
                f"matricula inexistente {matricula_texto}"
            )
            continue

        if matricula in matriculas_cadastradas:
            erros.append(
                f"alunos.csv:{numero_linha}  "
                f"matricula {matricula} já cadastrada"
            )
            continue

        matriculas_cadastradas.add(matricula)
        alunos_validos.append(Aluno(matricula, nome, turma))

    return alunos_validos, erros

def validar_notas(
    linhas: list[tuple[int, dict[str, str]]],
    alunos: list[Aluno],
    nota_maxima: float,
) -> tuple[list[Nota], list[str]]:
    notas_validas = []
    erros = []
    matriculas_existentes = {aluno.matricula for aluno in alunos}
    avaliacoes_cadastradas = set()

    for numero_linha, linha in linhas:
        campos_vazios = [
            campo 
            for campo in ("matricula", "disciplina", "avaliacao", "nota")
            if not campo_valido(linha.get(campo))
        ]

        if campos_vazios:
            erros.append(
                f"notas.csv:{numero_linha} campo_vazio: "
                f"{', '.join(campos_vazios)}"
            )
            continue

        matricula_texto = linha["matricula"].strip()
        disciplina = linha["disciplina"].strip()
        avaliacao = linha["avaliacao"].strip()
        nota_texto = linha["nota"].strip()

        if not nota_valida(nota_texto):
            erros.append(
                f"notas.csv:{numero_linha} nota_invalida: {nota_texto}"
            )
            continue

        valor_nota = float(nota_texto)
        if not 0 <= valor_nota <= nota_maxima:
            erros.append(
                f"notas.csv:{numero_linha} "
                f"nota_fora_do_intervalo: {nota_texto}"
            )
            continue

        try:
            matricula = int(matricula_texto)
        except ValueError:
            matricula = None

        if matricula not in matriculas_existentes:
            erros.append(
                f"notas.csv:{numero_linha} "
                f"matricula_inexistente: {matricula_texto}"
            )
            continue

        chave_avaliacao = (matricula, disciplina, avaliacao)
        if chave_avaliacao in avaliacoes_cadastradas:
            erros.append(
                f"notas.csv:{numero_linha} "
                f"avaliacao_duplicada: {matricula_texto}"
                f"{disciplina} {avaliacao}"
            )
            continue

        avaliacoes_cadastradas.add(chave_avaliacao)
        notas_validas.append(
            Nota(matricula, disciplina, avaliacao, valor_nota)
        )

    return notas_validas, erros