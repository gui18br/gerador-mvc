# -*- coding: utf-8 -*-
"""
cliente_mvc.py — Cliente MCP determinístico que aciona a geração de MVC sem IA.
"""

import asyncio
import json
import os
import sys

# Garante que o terminal Windows consiga exibir emojis/UTF-8 corretamente
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from mcp.client.stdio import stdio_client
from mcp import ClientSession as session, StdioServerParameters as session_parameters
from dotenv import load_dotenv

def exibir_sucesso(dados_resultado: dict):
    """Exibe o resultado da geração de forma visualmente rica e organizada."""
    modulo = dados_resultado.get("modulo", "N/A")
    adr = dados_resultado.get("adr_referenciada", "N/A")
    diretorio = dados_resultado.get("diretorio_saida", "N/A")
    arquivos = dados_resultado.get("arquivos", {})

    sep = "═" * 65
    print(f"\n{sep}")
    print(f"      GERADOR DE ESTRUTURA MVC — SUCESSO")
    print(sep)
    print(f"📦 MÓDULO GERADO      : {modulo.upper()}")
    print(f"🏛️  ADR DE REFERÊNCIA  : {adr}")
    print(f"📁 DIRETÓRIO DE SAÍDA : {diretorio}")
    print(f"\n📄 ARQUIVOS CRIADOS:")
    for nome, path in arquivos.items():
        print(f"   • {nome.ljust(25)} → {path}")
    print(sep)
    print("✨ Dica: Importe os arquivos no seu código e comece a usá-los!")
    print(f"{sep}\n")


async def executar_geracao(modulo_nome: str):
    load_dotenv()
    
    # Parâmetros do servidor MCP (adrs.py no Python do sistema)
    params = session_parameters(
        command=sys.executable,
        args=["servidor_mvc.py"],
        env=dict(os.environ)
    )

    print(f"🔄  Conectando ao Servidor MCP de Estrutura MVC…")

    try:
        async with stdio_client(params) as (read, write):
            async with session(read, write) as s:
                # Inicializa a sessão com o servidor
                await s.initialize()

                print(f"⚙️   Invocando tool 'gerar_mvc' para o módulo '{modulo_nome}'…")
                
                # Executa a ferramenta diretamente sem IA
                resultado_tool = await s.call_tool(
                    name="gerar_mvc",
                    arguments={"modulo": modulo_nome}
                )

                # Processa o retorno da ferramenta
                conteudo_str = resultado_tool.content[0].text
                
                # O retorno é um JSON serializado em string pelo MCP FastMCP
                dados = json.loads(conteudo_str)
                
                if dados.get("status") == "success":
                    exibir_sucesso(dados)
                else:
                    print(f"❌  Erro na geração: {dados.get('message', 'Erro desconhecido')}")

    except Exception as e:
        print(f"❌  Falha ao se conectar ou executar a tool no Servidor MCP: {e}")


if __name__ == "__main__":
    # Aceita o módulo via argumento da CLI ou pergunta interativamente
    if len(sys.argv) > 1:
        modulo = sys.argv[1]
    else:
        print("💡  Você pode passar o nome do módulo como argumento CLI:")
        print("    Exemplo: python cliente_mvc.py Produto\n")
        modulo = input("Qual o nome do módulo a ser gerado? ").strip()

    if not modulo:
        print("❌  Nome do módulo não pode ser vazio.")
        sys.exit(1)

    asyncio.run(executar_geracao(modulo))
