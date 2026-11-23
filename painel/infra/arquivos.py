import csv
import json

def ler_csv(caminho: str) -> list[tuple[int, dict[str, str]]]:
    linhas = []

    with open(caminho, encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)

        for numero_linha, linha in enumerate(leitor, start=2) :
            linhas.append((numero_linha, dict(linha)))

    return linhas 

def ler_json(caminho: str) -> dict[str, float]:
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)