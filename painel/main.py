import argparse
import logging
from pathlib import Path

from painel.infra.relatorios import criar_gerador
from painel.services.processamento import executar_processamento

def configurar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Processa notas e gera relatórios da turma."
    )
    parser.add_argument("--alunos", required=True)
    parser.add_argument("--notas", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--formato", choices=("texto", "json"), default="texto",
    )
    parser.add_argument("--output", default="output")
    return parser

def main() -> int:
    args = configurar_parser().parse_args()
    diretorio_saida = Path(args.output)

    try:
        diretorio_saida.mkdir(parents=True, exist_ok=True)
    except OSError as erro:
        print(f"[ERRO] Não foi possível criar a pasta de saída: {erro}")
        return 1


    logging.basicConfig(
        filename=diretorio_saida/ "painel.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        encoding="utf-8",
    )
    logging.info("Iniciando processamento")

    try:
        resultado = executar_processamento(
            args.alunos,
            args.notas,
            args.config,
        )
        relatorio = criar_gerador(args.formato).render(resultado)
        nome_arquivo = (
            "relatorio.txt" if args.formato == "texto" else "relatorio.json"
        )
        caminho_relatorio = diretorio_saida / nome_arquivo
        caminho_relatorio.write_text(relatorio, encoding="utf-8")
    except (OSError, ValueError, KeyError) as erro:
        logging.exception("Falha no processamento")
        print(f"[ERRO] {erro}")
        return 1

    logging.info(
        "Processamento concluído: %d alunos, %d notas válidas e %d erros",
        len(resultado.resumos_alunos),
        len(resultado.notas_validas),
        len(resultado.erros),
    )

    print(f"Relatório salvo em: {caminho_relatorio}")
    return 0
