# -*- coding: utf-8 -*-
"""
templates.py — Templates de código MVC e dicionário de mapeamento de módulos das ADRs.
"""

import re

# Dicionário de metadados estáticos para os módulos baseados nas ADRs
MODULOS = {
    "cliente": {
        "singular": "Cliente",
        "plural": "Clientes",
        "fields": [
            {"name": "id", "type": "int", "required": True, "desc": "Identificador único do cliente"},
            {"name": "nome", "type": "str", "required": True, "desc": "Nome completo do cliente"},
            {"name": "cpf", "type": "str", "required": True, "desc": "CPF único para validação de duplicidade"},
            {"name": "email", "type": "str", "required": False, "desc": "E-mail de contato do cliente"},
        ],
        "custom_validations": """        # Validação de CPF obrigatória e formato (ADR-02)
        if not self.cpf or len(self.cpf.strip()) != 11 or not self.cpf.isdigit():
            erros.append("CPF inválido! Deve conter exatamente 11 dígitos numéricos.")
        if not self.nome or len(self.nome.strip()) < 3:
            erros.append("Nome deve conter pelo menos 3 caracteres.")""",
        "duplicate_check": """        # Checagem de duplicidade via CPF (ADR-02)
        for c in db_session:
            if hasattr(c, 'cpf') and c.cpf == self.cpf and c.id != self.id:
                return True
        return False"""
    },
    "produto": {
        "singular": "Produto",
        "plural": "Produtos",
        "fields": [
            {"name": "id", "type": "int", "required": True, "desc": "Identificador único do produto"},
            {"name": "nome", "type": "str", "required": True, "desc": "Nome do produto no catálogo"},
            {"name": "fornecedor_id", "type": "int", "required": True, "desc": "Vínculo obrigatório com o fornecedor"},
            {"name": "codigo_barras", "type": "str", "required": True, "desc": "Código de barras único (EAN-13)"},
            {"name": "preco", "type": "float", "required": True, "desc": "Preço de venda do produto"},
        ],
        "custom_validations": """        # Validação de código de barras (EAN-13) e fornecedor (ADR-03)
        if not self.codigo_barras or len(self.codigo_barras.strip()) != 13 or not self.codigo_barras.isdigit():
            erros.append("Código de barras inválido! Deve conter exatamente 13 dígitos numéricos (EAN-13).")
        if not self.fornecedor_id or self.fornecedor_id <= 0:
            erros.append("Produto deve estar vinculado a um ID de fornecedor válido.")
        if self.preco is None or self.preco <= 0:
            erros.append("Preço do produto deve ser maior que zero.")""",
        "duplicate_check": """        # Checagem de duplicidade via Código de Barras (ADR-03)
        for p in db_session:
            if hasattr(p, 'codigo_barras') and p.codigo_barras == self.codigo_barras and p.id != self.id:
                return True
        return False"""
    },
    "estoque": {
        "singular": "Estoque",
        "plural": "Estoques",
        "fields": [
            {"name": "id", "type": "int", "required": True, "desc": "Identificador único do registro de estoque"},
            {"name": "produto_id", "type": "int", "required": True, "desc": "Vínculo com o cadastro de produtos"},
            {"name": "quantidade", "type": "int", "required": True, "desc": "Quantidade disponível em estoque"},
            {"name": "localizacao", "type": "str", "required": False, "desc": "Corredor/Prateleira física no galpão"},
        ],
        "custom_validations": """        # Validação das informações inseridas (ADR-04)
        if not self.produto_id or self.produto_id <= 0:
            erros.append("Estoque deve estar integrado a um ID de produto válido.")
        if self.quantidade is None or self.quantidade < 0:
            erros.append("Quantidade em estoque não pode ser negativa.")""",
        "duplicate_check": """        # Checagem se já existe estoque registrado para o mesmo produto (ADR-04)
        for e in db_session:
            if hasattr(e, 'produto_id') and e.produto_id == self.produto_id and e.id != self.id:
                return True
        return False"""
    },
    "venda": {
        "singular": "Venda",
        "plural": "Vendas",
        "fields": [
            {"name": "id", "type": "int", "required": True, "desc": "Identificador único da venda"},
            {"name": "cliente_id", "type": "int", "required": True, "desc": "ID do cliente comprador"},
            {"name": "produto_id", "type": "int", "required": True, "desc": "ID do produto vendido"},
            {"name": "quantidade", "type": "int", "required": True, "desc": "Quantidade de itens vendidos"},
            {"name": "valor_total", "type": "float", "required": True, "desc": "Valor total da venda"},
            {"name": "data_venda", "type": "str", "required": True, "desc": "Data da venda (YYYY-MM-DD)"},
        ],
        "custom_validations": """        # Validação automática dos dados obrigatórios (ADR-05)
        if not self.cliente_id or self.cliente_id <= 0:
            erros.append("Venda deve ter um cliente associado.")
        if not self.produto_id or self.produto_id <= 0:
            erros.append("Venda deve ter um produto associado.")
        if not self.quantidade or self.quantidade <= 0:
            erros.append("Quantidade vendida deve ser maior que zero.")
        if not self.data_venda or not re.match(r"^\\d{4}-\\d{2}-\\d{2}$", self.data_venda):
            erros.append("Data da venda inválida! Deve estar no formato YYYY-MM-DD.")""",
        "duplicate_check": """        # Vendas não possuem chave de unicidade natural simples além do ID
        return False"""
    },
    "caixa": {
        "singular": "Caixa",
        "plural": "Caixas",
        "fields": [
            {"name": "id", "type": "int", "required": True, "desc": "Identificador da transação do caixa"},
            {"name": "data", "type": "str", "required": True, "desc": "Data da operação (YYYY-MM-DD)"},
            {"name": "tipo_operacao", "type": "str", "required": True, "desc": "Tipo de operação ('entrada' ou 'saida')"},
            {"name": "valor", "type": "float", "required": True, "desc": "Valor monetário da transação"},
            {"name": "descricao", "type": "str", "required": False, "desc": "Descrição/justificativa da movimentação"},
        ],
        "custom_validations": """        # Validação de datas, tipos de operação e valores obrigatórios (ADR-06)
        if not self.data or not re.match(r"^\\d{4}-\\d{2}-\\d{2}$", self.data):
            erros.append("Data do caixa inválida! Deve estar no formato YYYY-MM-DD.")
        if self.tipo_operacao not in ['entrada', 'saida']:
            erros.append("Tipo de operação inválido! Deve ser 'entrada' ou 'saida'.")
        if self.valor is None or self.valor <= 0:
            erros.append("Valor da operação deve ser maior que zero.")""",
        "duplicate_check": """        # Caixa não possui checagem de duplicidade natural além do ID
        return False"""
    }
}

MODEL_TEMPLATE = """# -*- coding: utf-8 -*-
\"\"\"
Módulo Model para {singular} (Padrão MVC - ADR-01)
Referência Arquitetural: {adr_id} - {adr_titulo}

Descrição da ADR associada:
{adr_decisao}
\"\"\"

import re

class {class_name}Model:
    def __init__(self, {init_params}):
        \"\"\"
        Inicializa o modelo {class_name} com os campos definidos.
{fields_docstring}
        \"\"\"
{fields_assignment}

    def validar(self) -> list[str]:
        \"\"\"
        Realiza as validações de dados obrigatórios conforme as regras da ADR.
        Retorna uma lista de erros. Se vazia, os dados são válidos.
        \"\"\"
        erros = []
        
        # Validação de tipos e presença dos campos obrigatórios
{type_presence_checks}
        
        # Validações de negócio específicas da ADR
{custom_validations}
        
        return erros

    def verificar_duplicidade(self, db_session: list) -> bool:
        \"\"\"
        Verifica se já existe registro com dados duplicados no banco (ADR correspondente).
        \"\"\"
{duplicate_check}

    def __str__(self):
        return f"<{class_name}Model(id={{self.id}})>"
"""

VIEW_TEMPLATE = """# -*- coding: utf-8 -*-
\"\"\"
Módulo View para {singular} (Padrão MVC - ADR-01)
Responsável por interagir com o usuário e exibir os dados do modelo.
\"\"\"

class {class_name}View:
    @staticmethod
    def exibir_detalhes(model_data: dict):
        \"\"\"Exibe os detalhes de um {singular} de forma formatada.\"\"\"
        print("\\n" + "=" * 50)
        print("            DETALHES DO {singular_upper}")
        print("=" * 50)
        for campo, valor in model_data.items():
            print(f"  • {{campo.upper().ljust(15)}}: {{valor}}")
        print("=" * 50 + "\\n")

    @staticmethod
    def exibir_lista(lista_itens: list[dict]):
        \"\"\"Exibe a listagem de todos os {plural}.\"\"\"
        print("\\n" + "=" * 60)
        print("            LISTAGEM DE {plural_upper}")
        print("=" * 60)
        if not lista_itens:
            print("  [Nenhum registro encontrado.]")
        else:
            for item in lista_itens:
                identificador = item.get('id')
                valores_secundarios = [str(v) for k, v in item.items() if k != 'id']
                print(f"  ID: {{str(identificador).ljust(5)}} | Info: {{', '.join(valores_secundarios[:2])}}")
        print("=" * 60 + "\\n")

    @staticmethod
    def exibir_mensagem(mensagem: str, tipo: str = "info"):
        \"\"\"Exibe mensagens de status (info, sucesso, erro).\"\"\"
        if tipo == "erro":
            print(f"❌  [ERRO] {{mensagem}}")
        elif tipo == "sucesso":
            print(f"✅  [SUCESSO] {{mensagem}}")
        else:
            print(f"ℹ️  [INFO] {{mensagem}}")

    @staticmethod
    def obter_dados_formulario() -> dict:
        \"\"\"
        Interface/Simulador para coletar dados de inserção do usuário.
        Pode ser adaptado para CLI, Web, etc. (ADR-07 Componentes Web)
        \"\"\"
        print("=" * 45)
        print("   NOVO CADASTRO DE {singular_upper}")
        print("=" * 45)
        dados = {{}}
{fields_input_prompts}
        return dados
"""

CONTROLLER_TEMPLATE = """# -*- coding: utf-8 -*-
\"\"\"
Módulo Controller para {singular} (Padrão MVC - ADR-01)
Intermedeia o fluxo de dados entre a View e o Model de {singular}.
\"\"\"

from .{model_filename} import {class_name}Model
from .{view_filename} import {class_name}View

class {class_name}Controller:
    def __init__(self, db_mock: list = None):
        \"\"\"
        Inicializa o Controller com uma sessão de banco de dados mockada.
        \"\"\"
        self.db = db_mock if db_mock is not None else []
        self.view = {class_name}View()

    def cadastrar_novo(self, dados: dict) -> bool:
        \"\"\"
        Cadastra um novo {singular} realizando as validações do Model.
        \"\"\"
        # Cria a instância do Model a partir dos dados recebidos
        try:
            novo_modelo = {class_name}Model(
{model_instantiation}
            )
        except KeyError as e:
            self.view.exibir_mensagem(f"Campo obrigatório ausente: {{e}}", "erro")
            return False
        except Exception as e:
            self.view.exibir_mensagem(f"Erro de processamento nos dados: {{e}}", "erro")
            return False

        # Executa validações de dados (ADR)
        erros = novo_modelo.validar()
        if erros:
            for erro in erros:
                self.view.exibir_mensagem(erro, "erro")
            return False

        # Executa validação de duplicidade (ADR)
        if novo_modelo.verificar_duplicidade(self.db):
            self.view.exibir_mensagem(
                "Já existe um registro com estes dados únicos (Conflito de Duplicidade).", 
                "erro"
            )
            return False

        # Persistência mockada
        self.db.append(novo_modelo)
        self.view.exibir_mensagem(f"{singular} cadastrado(a) com sucesso!", "sucesso")
        
        # Exibe os detalhes cadastrados
        self.view.exibir_detalhes(novo_modelo.__dict__)
        return True

    def listar_todos(self):
        \"\"\"Obtém os dados dos modelos cadastrados e repassa para a View.\"\"\"
        dados = [item.__dict__ for item in self.db]
        self.view.exibir_lista(dados)
"""


def obter_tipo_cast(field_type):
    """Retorna o cast correspondente em Python para o tipo do campo."""
    if field_type == "int":
        return "int"
    elif field_type == "float":
        return "float"
    return "str"


def gerar_fontes(module_name: str, adr_meta: dict | None = None) -> dict[str, str]:
    """
    Gera as strings contendo os códigos-fonte para Model, View e Controller
    do módulo selecionado.
    """
    key = module_name.strip().lower()
    
    if key in MODULOS:
        config = MODULOS[key]
    else:
        # Fallback genérico para módulos desconhecidos
        singular = module_name.strip().capitalize()
        config = {
            "singular": singular,
            "plural": singular + "s",
            "fields": [
                {"name": "id", "type": "int", "required": True, "desc": "Identificador único"},
                {"name": "nome", "type": "str", "required": True, "desc": f"Nome do/da {singular}"},
            ],
            "custom_validations": f'        if not self.nome or len(self.nome.strip()) < 1:\n            erros.append("O campo nome é obrigatório.")',
            "duplicate_check": """        for x in db_session:
            if hasattr(x, 'nome') and x.nome == self.nome and x.id != self.id:
                return True
        return False"""
        }

    singular = config["singular"]
    plural = config["plural"]
    fields = config["fields"]
    class_name = singular.replace("_", "").replace(" ", "")

    adr_id = adr_meta.get("id", "N/A") if adr_meta else "N/A"
    adr_titulo = adr_meta.get("titulo", "N/A") if adr_meta else "N/A"
    adr_decisao = adr_meta.get("decisao", "Nenhum mapeamento direto de decisão arquitetural encontrado.") if adr_meta else "N/A"

    # Preparar variáveis para o MODEL_TEMPLATE
    init_params = []
    fields_docstring = []
    fields_assignment = []
    type_presence_checks = []

    for f in fields:
        param = f"{f['name']}: {f['type']}"
        if not f["required"]:
            param += " = None"
        init_params.append(param)
        
        fields_docstring.append(f"        :param {f['name']}: {f['desc']} ({f['type']})")
        fields_assignment.append(f"        self.{f['name']} = {f['name']}")

        # Geração automática de validação básica de tipos e presença
        if f["required"]:
            type_presence_checks.append(f'        if self.{f["name"]} is None:\n            erros.append("O campo \'{f["name"]}\' é obrigatório.")')
            
            # Adiciona validação de tipo específica
            if f["type"] == "int":
                type_presence_checks.append(f'        elif not isinstance(self.{f["name"]}, int):\n            erros.append("O campo \'{f["name"]}\' deve ser do tipo inteiro.")')
            elif f["type"] == "float":
                type_presence_checks.append(f'        elif not isinstance(self.{f["name"]}, (int, float)):\n            erros.append("O campo \'{f["name"]}\' deve ser do tipo numérico.")')
            elif f["type"] == "str":
                type_presence_checks.append(f'        elif not isinstance(self.{f["name"]}, str):\n            erros.append("O campo \'{f["name"]}\' deve ser do tipo string.")')

    init_params_str = ", ".join(init_params)
    fields_docstring_str = "\n".join(fields_docstring)
    fields_assignment_str = "\n".join(fields_assignment)
    type_presence_checks_str = "\n".join(type_presence_checks)
    custom_validations_str = config["custom_validations"]
    duplicate_check_str = config["duplicate_check"]

    model_code = MODEL_TEMPLATE.format(
        singular=singular,
        adr_id=adr_id,
        adr_titulo=adr_titulo,
        adr_decisao=adr_decisao,
        class_name=class_name,
        init_params=init_params_str,
        fields_docstring=fields_docstring_str,
        fields_assignment=fields_assignment_str,
        type_presence_checks=type_presence_checks_str,
        custom_validations=custom_validations_str,
        duplicate_check=duplicate_check_str
    )

    # Preparar variáveis para o VIEW_TEMPLATE
    fields_input_prompts = []
    for f in fields:
        if f["name"] == "id":
            # Geralmente ID é autogerado ou simulado
            fields_input_prompts.append(f'        try:\n            dados["id"] = int(input("Digite o ID: ").strip())\n        except ValueError:\n            dados["id"] = None')
        else:
            tipo_cast = obter_tipo_cast(f["type"])
            label = f"{f['name'].replace('_', ' ').title()} ({f['type']})"
            if f["required"]:
                label += " [obrigatório]"
            fields_input_prompts.append(
                f'        val = input("Digite o {label}: ").strip()\n'
                f'        if val:\n'
                f'            try:\n'
                f'                dados["{f["name"]}"] = {tipo_cast}(val)\n'
                f'            except ValueError:\n'
                f'                dados["{f["name"]}"] = None\n'
                f'        else:\n'
                f'            dados["{f["name"]}"] = None'
            )

    fields_input_prompts_str = "\n".join([f"        {line}" for item in fields_input_prompts for line in item.split("\n")])

    view_code = VIEW_TEMPLATE.format(
        singular=singular,
        singular_upper=singular.upper(),
        plural=plural,
        plural_upper=plural.upper(),
        class_name=class_name,
        fields_input_prompts=fields_input_prompts_str
    )

    # Preparar variáveis para o CONTROLLER_TEMPLATE
    model_filename = f"{key}_model"
    view_filename = f"{key}_view"
    
    model_instantiation = []
    for f in fields:
        model_instantiation.append(f"                {f['name']}=dados.get('{f['name']}')")
    model_instantiation_str = ",\n".join(model_instantiation)

    controller_code = CONTROLLER_TEMPLATE.format(
        singular=singular,
        class_name=class_name,
        model_filename=model_filename,
        view_filename=view_filename,
        model_instantiation=model_instantiation_str
    )

    return {
        "model": model_code,
        "view": view_code,
        "controller": controller_code
    }
