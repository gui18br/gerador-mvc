# Gerador de Estrutura MVC via MCP (Sem IA)

Este projeto implementa uma ferramenta baseada no protocolo **Model Context Protocol (MCP)** para gerar de forma automática e determinística o esqueleto de arquivos **Model, View e Controller (MVC)** para os módulos do sistema **Strong Nutrition**. 

A geração segue rigorosamente as diretrizes da **ADR-01** (Adoção do Padrão Arquitetural MVC) e incorpora nos arquivos as regras de negócio e validações de dados específicas descritas nas ADRs de cada módulo.

---

## 🏛️ Arquitetura do Projeto

Ao contrário do fluxo tradicional onde um LLM (Inteligência Artificial) gerencia prompts e decide as chamadas de ferramentas, este projeto demonstra o uso do **MCP como um canal robusto de RPC local e modular**, operando de forma 100% determinística (sem IA).

```
gerador-mvc/
├── ADRs_Strong_Nutrition.md # Fonte de regras das decisões arquiteturais
├── parser_adrs.py           # Parser local de ADRs para obter contexto
├── templates.py             # Esqueletos e mapeamentos estruturados de MVC
├── servidor_mvc.py          # Servidor MCP (FastMCP) expondo a tool 'gerar_mvc'
├── cliente_mvc.py           # Cliente MCP (Stdio) determinístico que consome a tool
└── requirements.txt         # Dependências do protocolo MCP
```

---

## 🚀 Pré-requisitos e Instalação

1. Certifique-se de possuir o Python 3.11+.
2. Crie ou use um ambiente virtual e instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Como Utilizar

Você pode rodar o cliente MCP passando o nome do módulo como argumento CLI, ou de forma interativa.

### Via Argumento CLI:
```bash
python cliente_mvc.py Produto
```

### Via Modo Interativo:
```bash
python cliente_mvc.py
# O cliente perguntará: Qual o nome do módulo a ser gerado?
```

### Saída Esperada no Console:
```
🔄  Conectando ao Servidor MCP de Estrutura MVC…
⚙️   Invocando tool 'gerar_mvc' para o módulo 'Produto'…

═════════════════════════════════════════════════════════════════
      GERADOR DE ESTRUTURA MVC — SUCESSO
═════════════════════════════════════════════════════════════════
📦 MÓDULO GERADO      : PRODUTO
🏛️  ADR DE REFERÊNCIA  : ADR-03: Cadastro de Produtos
📁 DIRETÓRIO DE SAÍDA : C:/Projetos/gerador-mvc/output/produto

📄 ARQUIVOS CRIADOS:
   • produto_model.py          → C:/Projetos/gerador-mvc/output/produto/produto_model.py
   • produto_view.py           → C:/Projetos/gerador-mvc/output/produto/produto_view.py
   • produto_controller.py     → C:/Projetos/gerador-mvc/output/produto/produto_controller.py
   • __init__.py               → C:/Projetos/gerador-mvc/output/produto/__init__.py
═════════════════════════════════════════════════════════════════
✨ Dica: Importe os arquivos no seu código e comece a usá-los!
═════════════════════════════════════════════════════════════════
```

---

## 📂 Módulos Mapeados com ADRs

O gerador extrai regras específicas das seguintes ADRs do **Strong Nutrition**:
*   `Cliente` (ADR-02: Cadastro de Cliente) — Gera validações estruturadas de CPF e unicidade de cadastro.
*   `Produto` (ADR-03: Cadastro de Produtos) — Cria dependência de `fornecedor_id` e validação estruturada de código de barras (EAN-13).
*   `Estoque` (ADR-04: Cadastro de Estoque) — Gera controle de quantidade não negativa integrado a produtos.
*   `Venda` (ADR-05: Cadastro de Venda) — Valida cliente, produto, estoque e formato de data obrigatórios antes de persistir.
*   `Caixa` (ADR-06: Cadastro de Caixa) — Valida tipos de movimentação (entrada/saída) e valores obrigatórios.

> ⚠️ **Bloqueio de Conformidade**: Caso seja solicitado um módulo não mapeado nas ADRs (ex: `Usuario`), a geração será **bloqueada** com uma mensagem de erro, garantindo que a estrutura só seja criada para módulos previamente documentados nas ADRs do projeto.
