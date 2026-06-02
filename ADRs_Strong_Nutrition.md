# ADRs — Sistema Strong Nutrition

---

# ADR-01: Adoção do Padrão Arquitetural MVC

## Contexto
Sistema com módulos bem definidos e regras de negócio distintas exigindo separação de responsabilidades.

## Decisão
Adotar o padrão MVC, dividindo a aplicação em View, Controller e Model.

## Consequências
- Separação clara de responsabilidades;
- Complexidade adicional na estruturação inicial.

---

# ADR-02: Cadastro de Cliente

## Contexto
Necessidade de manipular e armazenar os dados dos clientes.

## Decisão
Implementar módulo de cadastro com validação de dados obrigatória e checagem de duplicidade via CPF.

## Consequências
- Integridade e consistência dos dados de clientes;
- Necessidade de validações adicionais no back-end.

---

# ADR-03: Cadastro de Produtos

## Contexto
Necessidade de cadastrar e gerenciar no sistema os produtos que estão no catálogo.

## Decisão
Implementar módulo de cadastro de produtos vinculado ao fornecedor, com validação de código de barras e verificação de duplicidade.

## Consequências
- Catálogo de produtos organizado e consistente;
- Dependência do cadastro de fornecedores para funcionar.

---

# ADR-04: Cadastro de Estoque

## Contexto
Necessidade de registrar e armazenar informações relacionadas ao estoque dos produtos, permitindo acompanhamento das quantidades disponíveis no sistema.

## Decisão
Implementar um módulo de cadastro de estoque integrado ao cadastro de produtos, realizando validação das informações inseridas e atualização dos registros armazenados no banco de dados.

## Consequências
- Melhor organização e acompanhamento das quantidades de produtos;
- Necessidade de sincronização entre estoque e cadastro de produtos.

---

# ADR-05: Cadastro de Venda

## Contexto
Necessidade de registrar as vendas realizadas no sistema, relacionando clientes e produtos para armazenamento das informações comerciais.

## Decisão
Implementar um módulo de cadastro de vendas integrado aos módulos de clientes, produtos e estoque, realizando validação automática dos dados obrigatórios antes da persistência das informações.

## Consequências
- Maior integridade e organização dos registros de vendas;
- Aumento da complexidade das validações entre módulos.

---

# ADR-06: Cadastro de Caixa

## Contexto
Necessidade de registrar operações de entrada e saída no caixa, permitindo armazenamento e acompanhamento das movimentações financeiras.

## Decisão
Implementar um módulo de cadastro de caixa responsável pelo registro das operações financeiras, incluindo validação de datas, tipos de operação e valores obrigatórios.

## Consequências
- Melhor organização das movimentações financeiras;
- Necessidade de validações adicionais relacionadas às operações.

---

# ADR-07: Componentes Web

## Contexto
O requisito não-funcional NF002 estabelece que o sistema deve possuir componentes web acessíveis por navegador.

## Decisão
Desenvolver o sistema como uma aplicação web baseada em arquitetura cliente-servidor, utilizando interfaces acessadas diretamente pelo navegador.

## Consequências
- Facilidade de acesso ao sistema em diferentes dispositivos;
- Dependência de conexão com internet e disponibilidade do servidor.

---

# ADR-08: Agilidade na Execução das Operações

## Contexto
O requisito não-funcional NF005 exige rapidez nas operações de cadastro, pesquisa e atualização realizadas no sistema.

## Decisão
Utilizar consultas otimizadas ao banco de dados e organização modular das funcionalidades para reduzir o tempo de resposta das operações.

## Consequências
- Melhor experiência do usuário durante a utilização do sistema;
- Maior esforço de implementação e otimização das consultas.
