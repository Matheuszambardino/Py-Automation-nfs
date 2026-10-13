# Extrator e Consolidador de Notas Fiscais Eletrônicas (NF-e) em Python

##  Descrição do Projeto

Este projeto consiste em um script em Python desenvolvido para automatizar a leitura, extração e consolidação de dados de Notas Fiscais Eletrônicas (NF-e) no formato XML (padrão SEFAZ). A ferramenta varre um diretório com múltiplos arquivos XML, extrai as informações estruturadas do cabeçalho e dos itens de cada nota, consolida tudo em um formato tabular e exporta os resultados para uma planilha Excel, abrindo o arquivo automaticamente ao final do processo.

##  Problema e Objetivo

**O Problema:** A análise manual de dados fiscais contidos em arquivos XML de NF-e é um processo repetitivo, lento e suscetível a erros, especialmente quando lidando com dezenas ou centenas de arquivos separados.

**O Objetivo:** Criar um pipeline de automação leve e robusto que elimine o trabalho manual, unificando informações dispersas em arquivos individuais de XML em um único relatório consolidado pronto para auditoria ou análise gerencial.

##  Funcionalidades Implementadas

- **Leitura em Lote:** Varredura automática de diretórios em busca de arquivos com extensão `.xml`.
- **Parsing de XML com Namespace:** Navegação segura na árvore de elementos XML utilizando o namespace oficial da SEFAZ (`http://www.portalfiscal.inf.br/nfe`).
- **Extração Desnormalizada:** Captura tanto os dados gerais da nota (cabeçalho, emitente, valores totais) quanto o detalhamento de cada produto comercializado (`det`).
- **Tratamento de Exceções Defensivo:** Funções de busca seguras que evitam quebras de execução (`AttributeError`, `NoneType`) caso uma tag opcional ou ausente seja encontrada, além de isolar erros de arquivos corrompidos ou inválidos.
- **Exportação Organizada:** Consolidação dos itens em um DataFrame do Pandas e exportação para `.xlsx`.
- **Gerenciamento Inteligente de Caminhos:** Uso de caminhos absolutos baseados no diretório do script (`__file__`), garantindo que o arquivo Excel seja salvo na mesma pasta do código-fonte independentemente de onde o script seja acionado.
- **Automação de Abertura:** Disparo automático do visualizador de planilhas padrão do sistema operacional (Windows, macOS ou Linux) após a geração do arquivo.

##  Tecnologias e Bibliotecas Utilizadas

- **Python 3.x:** Linguagem principal para a lógica de automação e manipulação de dados.
- **`xml.etree.ElementTree` (Biblioteca Padrão):** Utilizada para o parsing e varredura hierárquica dos arquivos XML das notas fiscais.
- **`pandas`:** Biblioteca de manipulação e estruturação de dados em formato tabular (DataFrames), essencial para a preparação dos dados antes da exportação.
- **`os` e `sys` (Biblioteca Padrão):** Gerenciamento de diretórios do sistema operacional, caminhos de arquivos e identificação da plataforma em execução.
- **`subprocess` (Biblioteca Padrão):** Utilizada para invocar comandos do sistema operacional para abrir o arquivo Excel gerado.

##  Fluxo de Funcionamento em Etapas

1. **Definição do Diretório:** O script localiza dinamicamente a pasta onde está instalado e aponta para a pasta de entrada (`xmls_teste`).
2. **Varredura:** O programa lista todos os arquivos do diretório e filtra apenas aqueles com a extensão `.xml`.
3. **Leitura e Parsing Individual (`ler_xml_nfe`):**
   - Cada arquivo é aberto e convertido em uma árvore de elementos XML (`ElementTree`).
   - O script localiza a tag de informações da NF-e (`infNFe`) e extrai a chave de acesso.
   - Extrai os dados do cabeçalho (número da nota, série, natureza da operação, data de emissão, CNPJ e nome do emitente, e valor total).
   - Itera sobre todas as ocorrências de itens (`det`), extraindo código, descrição, NCM, CFOP, unidade, quantidade, valor unitário e valor total do item.
4. **Tratamento de Erros:** Caso ocorra falha de sintaxe no XML (`ParseError`) ou o arquivo não seja encontrado, a exceção é tratada no console sem interromper o processamento das demais notas.
5. **Consolidação e Exportação (`exportar_excel`):** Os dados aninhados são "achapados" (planificados) em uma lista de dicionários, convertidos em um `pandas.DataFrame` e salvos como `notas_fiscais.xlsx` na mesma pasta do script.
6. **Abertura Automática:** O sistema operacional é acionado para abrir o arquivo Excel recém-criado.

##  Estrutura de Pastas do Projeto

```text
extrator-nfe-python/
├── extrator.py              # Script principal de automação
├── xmls_teste/              # Pasta contendo os arquivos XML de entrada
│   ├── 352600...-nfe.xml
│   └── 352600...-nfe.xml
└── notas_fiscais.xlsx       # Planilha gerada automaticamente pelo script
```

##  Requisitos e Instalação

Certifique-se de ter o Python instalado em sua máquina. O projeto depende da biblioteca `pandas` e de uma engine para arquivos Excel (`openpyxl`).

### 1. Clonar ou baixar o repositório

Abra o terminal na pasta do projeto.

### 2. Instalar as dependências

Execute o comando abaixo para instalar o Pandas e o OpenPyXL:

```bash
pip install pandas openpyxl
```

##  Como Executar o Script

1. Certifique-se de que a pasta `xmls_teste` existe no mesmo diretório do arquivo `extrator.py` e contenha arquivos `.xml` válidos de NF-e no padrão brasileiro.
2. Execute o script via terminal ou sua IDE de preferência (como o VS Code):

   ```bash
   python extrator.py
   ```

3. O terminal exibirá a quantidade de notas lidas com sucesso, o arquivo Excel será salvo na mesma pasta e aberto automaticamente na sua tela.

##  Formato dos Dados

### Entrada (XML - Padrão SEFAZ)

Arquivos `.xml` contendo a estrutura oficial da NF-e, com as tags de namespace `http://www.portalfiscal.inf.br/nfe` (ex.: `<nNF>`, `<xNome>`, `<vProd>`, etc.).

### Saída (`notas_fiscais.xlsx`)

A planilha gerada consolida os itens de todas as notas fiscais em formato tabular plano:

| **Número Nota** | **Emitente**         | **Operação**        | **Produto** | **Quantidade** | **Valor Unitário** | **Valor Item** | **Valor Total Nota** |
| --------------- | -------------------- | ------------------- | ----------- | -------------- | ------------------ | -------------- | -------------------- |
| 1234            | EMPRESA EXEMPLO LTDA | VENDA DE MERCADORIA | PRODUTO A   | 2.0            | 50.00              | 100.00         | 250.00               |
| 1234            | EMPRESA EXEMPLO LTDA | VENDA DE MERCADORIA | PRODUTO B   | 1.0            | 150.00             | 150.00         | 250.00               |

##  Decisões Técnicas e Limitações

- **Funções de Extração Defensivas (`get_text` e `get_float`):** Optou-se por criar funções auxiliares para centralizar a busca de nós no XML. Isso evita que a ausência de uma tag opcional gere erros fatais de `AttributeError` durante a execução em lote.
- **Caminhos Absolutos Dinâmicos:** O uso de `os.path.dirname(os.path.abspath(__file__))` garante robustez, evitando erros de arquivo não encontrado quando o script é executado a partir de terminais abertos em diretórios diferentes.
- **Limitação Atual:** O projeto processa arquivos XML locais em lote estático e não faz validação estrutural profunda contra esquemas XSD da SEFAZ, focando exclusivamente na extração dos campos de interesse prático para relatórios.

##  Possíveis Melhorias Futuras

*(Funcionalidades planejadas para evolução do projeto, ainda não implementadas)*:

- [ ] Implementação de logs estruturados (`logging`) para auditoria detalhada de arquivos com falha de leitura.
- [ ] Validação rigorosa de campos obrigatórios do cabeçalho antes da consolidação.
- [ ] Criação de um relatório de erros isolado para XMLs corrompidos ou fora do padrão.
- [ ] Mecanismo de prevenção de duplicidade baseado na Chave de Acesso da NF-e (`chNFe`).
- [ ] Integração com banco de dados relacional (SQLite ou PostgreSQL) para persistência dos dados fiscais.

