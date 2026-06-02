# -*- coding: utf-8 -*-
"""
servidor_mvc.py — Servidor MCP que expõe a ferramenta de geração de estrutura MVC.
"""

from mcp.server.fastmcp import FastMCP
import os
import logging
from parser_adrs import parse_adrs, find_adr_for_module
from templates import gerar_fontes

# Configuração de logs para exibição no console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("gerador-mvc-server")

mcp = FastMCP("gerador-mvc")

@mcp.tool(
    name="gerar_mvc",
    title="Gerar Estrutura MVC",
    description=(
        "Gera automaticamente os arquivos Model, View e Controller (esqueletos de código) "
        "para um módulo informado, baseando-se no padrão arquitetural MVC da ADR-01 "
        "e nos campos/regras de validação definidos na ADR específica desse módulo."
    )
)
def gerar_mvc(modulo: str) -> dict:
    """
    Gera o esqueleto MVC para o módulo fornecido, salvando os arquivos no diretório output.
    
    Argumentos:
        modulo (str): Nome do módulo (ex: 'Cliente', 'Produto', 'Estoque', 'Venda', 'Caixa')
        
    Retorno:
        dict: Informações sobre os arquivos criados e a ADR de referência.
    """
    modulo_clean = modulo.strip().lower()
    logger.info(f"Solicitação recebida para gerar MVC do módulo: '{modulo}'")
    
    # 1. Carrega e busca ADR correspondente
    adrs = parse_adrs()
    adr_meta = find_adr_for_module(modulo, adrs)
    
    if not adr_meta:
        msg_erro = f"Módulo '{modulo}' não possui uma ADR correspondente em ADRs_Strong_Nutrition.md. A geração foi abortada para garantir a conformidade arquitetural."
        logger.error(msg_erro)
        return {
            "status": "error",
            "message": msg_erro
        }
        
    logger.info(f"ADR encontrada: {adr_meta['id']} - {adr_meta['titulo']}")

    # 2. Gera os códigos base
    fontes = gerar_fontes(modulo_clean, adr_meta)
    
    # 3. Cria diretório de output
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output", modulo_clean)
    os.makedirs(output_dir, exist_ok=True)
    
    # 4. Determina nome da classe e gera arquivo __init__.py
    from templates import MODULOS
    if modulo_clean in MODULOS:
        class_name = MODULOS[modulo_clean]["singular"].replace("_", "").replace(" ", "")
    else:
        class_name = modulo_clean.capitalize().replace("_", "").replace(" ", "")
        
    init_content = f"""# -*- coding: utf-8 -*-
from .{modulo_clean}_model import {class_name}Model
from .{modulo_clean}_view import {class_name}View
from .{modulo_clean}_controller import {class_name}Controller
"""

    # 5. Mapeia e escreve os arquivos no disco
    arquivos_criados = {}
    mapa_arquivos = {
        f"{modulo_clean}_model.py": fontes["model"],
        f"{modulo_clean}_view.py": fontes["view"],
        f"{modulo_clean}_controller.py": fontes["controller"],
        "__init__.py": init_content
    }
    
    for nome_arq, conteudo in mapa_arquivos.items():
        caminho_completo = os.path.join(output_dir, nome_arq)
        with open(caminho_completo, "w", encoding="utf-8") as f:
            f.write(conteudo)
        # Usamos barras normais do windows ou formatamos caminho absoluto
        caminho_abs = os.path.abspath(caminho_completo).replace("\\", "/")
        arquivos_criados[nome_arq] = caminho_abs
        logger.info(f"Arquivo gerado: {caminho_abs}")

    caminho_dir_abs = os.path.abspath(output_dir).replace("\\", "/")
    retorno = {
        "status": "success",
        "modulo": modulo,
        "adr_referenciada": f"{adr_meta['id']}: {adr_meta['titulo']}" if adr_meta else "Nenhuma (Fallback Genérico)",
        "diretorio_saida": caminho_dir_abs,
        "arquivos": arquivos_criados
    }
    return retorno

if __name__ == "__main__":
    logger.info("Iniciando FastMCP Server...")
    mcp.run()
