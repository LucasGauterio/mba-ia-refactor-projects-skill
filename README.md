# Desafio de Refatoração Arquitetural Automatizada (MVC)

Este repositório contém a implementação de uma Skill de IA para refatoração arquitetural para o padrão MVC, conforme os requisitos do desafio.

## A) Análise Manual

### 1. Projeto `code-smells-project` (Python/Flask)

| ID | Vulnerabilidade / Code Smell | Severidade | Arquivo / Linhas | Justificativa / Descrição |
| :-: | :--- | :--- | :--- | :--- |
| 1 | **Execução de SQL Arbitrário** | CRITICAL | [app.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/code-smells-project/app.py#L59-L79) (rota `/admin/query`) | A rota `/admin/query` aceita SQL livre enviado pelo cliente e o executa. Permite comprometimento total e direto do banco via HTTP. |
| 2 | **Reset de DB sem Autenticação** | CRITICAL | [app.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/code-smells-project/app.py#L47-L57) (rota `/admin/reset-db`) | A rota `/admin/reset-db` limpa todas as tabelas sem nenhuma autenticação, gerando perda total de dados com uma única chamada externa. |
| 3 | **SQL Injection por Concatenação** | CRITICAL | [models.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/code-smells-project/models.py#L28) e [models.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/code-smells-project/models.py#L47-L50) | Consultas SQL montadas concatenando strings diretamente com inputs de requisição de usuário, abrindo múltiplas falhas graves de SQL Injection. |
| 4 | **Senhas em Texto Puro / Exposição** | CRITICAL | [database.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/code-smells-project/database.py#L76-L79) e [models.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/code-smells-project/models.py#L83) | Senhas salvas sem hashing no banco e retornadas diretamente em texto limpo no payload JSON de APIs públicas. |
| 5 | **SECRET_KEY e DEBUG Hardcoded** | HIGH | [app.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/code-smells-project/app.py#L7-L8) | Chaves criptográficas do app salvas no código-fonte e modo debug ativo, facilitando falsificação de sessões e execução remota de código. |
| 6 | **Healthcheck com Vazamento** | HIGH | [controllers.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/code-smells-project/controllers.py#L289-L290) | Endpoint `/health` expõe explicitamente a `SECRET_KEY` e caminhos físicos do sistema no payload. |
| 7 | **Conexão SQLite Global** | HIGH | [database.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/code-smells-project/database.py#L10) | Compartilhamento global de conexão SQLite entre threads paralelas do Flask com `check_same_thread=False`, gerando instabilidade de concorrência. |
| 8 | **Pedidos sem Rollback Transacional** | HIGH | [models.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/code-smells-project/models.py#L133-L169) | Ações sequenciais de criação de pedidos e decremento de estoque sem transação lógica; falhas deixam o banco inconsistente. |
| 9 | **Acoplamento nos Controllers** | MEDIUM | [controllers.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/code-smells-project/controllers.py) | Mistura de controle HTTP, parsing, validação básica e lógicas de queries diretamente dentro de arquivos de controle. |
| 10 | **Gargalo N+1 em Pedidos** | MEDIUM | [models.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/code-smells-project/models.py#L171-L233) | Consultas sequenciais a produtos e itens rodadas em laço para cada pedido, aumentando a latência com o volume de dados. |
| 11 | **Schema sem Constraints** | MEDIUM | [database.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/code-smells-project/database.py#L37-L53) | Tabelas criadas sem Foreign Keys e constraints de unicidade (`UNIQUE`), facilitando chaves órfãs e inconsistências relacionais. |
| 12 | **Constantes de Domínio Inline** | LOW | [controllers.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/code-smells-project/controllers.py#L52) | Strings de categorias de produtos válidas escritas inline como strings literais de validação repetidas em vários arquivos. |

---

### 2. Projeto `ecommerce-api-legacy` (Node.js/Express)

| ID | Vulnerabilidade / Code Smell | Severidade | Arquivo / Linhas | Justificativa / Descrição |
| :-: | :--- | :--- | :--- | :--- |
| 1 | **Segredos Hardcoded no Código** | CRITICAL | [utils.js](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/ecommerce-api-legacy/src/utils.js#L1-L7) | Chaves privadas do gateway de pagamento, SMTP e dados de banco salvos de forma estática no código-fonte. |
| 2 | **Vazamento de Cartão nos Logs** | CRITICAL | [AppManager.js](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/ecommerce-api-legacy/src/AppManager.js#L45) | Console logs exibem abertamente chaves privadas e o número de cartão de crédito no momento do checkout. |
| 3 | **Senha do Seed em Texto Puro** | CRITICAL | [AppManager.js](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/ecommerce-api-legacy/src/AppManager.js#L18) | Usuário seed inicial inserido com a senha literal plaintext `'123'` sem passar por nenhum algoritmo de hash. |
| 4 | **Hashing badCrypto Fraco e Previsível** | CRITICAL | [utils.js](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/ecommerce-api-legacy/src/utils.js#L17-L23) | Algoritmo de hash customizado usando conversões simples e previsíveis em base64, vulnerável a colisões e sem salting. |
| 5 | **Relatório Financeiro Público** | HIGH | [AppManager.js](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/ecommerce-api-legacy/src/AppManager.js#L80) | Rota administrativa `/api/admin/financial-report` expõe faturamento e dados de alunos de forma pública, sem token. |
| 6 | **Checkout sem Transação de Banco** | HIGH | [AppManager.js](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/ecommerce-api-legacy/src/AppManager.js#L50-L63) | Matrícula e pagamentos gravados de forma assíncrona desacoplada; falhas criam matrículas válidas sem nenhum pagamento. |
| 7 | **Schema sem UNIQUE / FKs** | HIGH | [AppManager.js](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/ecommerce-api-legacy/src/AppManager.js#L12-L16) | Falta de constraint `UNIQUE(email)` em users e de foreign keys nas tabelas associativas do SQLite. |
| 8 | **Cascading Delete Ausente** | HIGH | [AppManager.js](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/ecommerce-api-legacy/src/AppManager.js#L131-L137) | Deleção de usuário remove o registro pai do banco mas deixa matrículas e pagamentos órfãos apontando para IDs nulos. |
| 9 | **Payload com Nomes Opacos** | MEDIUM | [AppManager.js](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/ecommerce-api-legacy/src/AppManager.js#L29-L33) | Parâmetros de requisição curtos e opacos (`usr`, `eml`, `pwd`, `card`) que dificultam leitura e integrações limpas de contratos. |
| 10 | **Senha Fallback Fraca** | MEDIUM | [AppManager.js](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/ecommerce-api-legacy/src/AppManager.js#L68) | Atribuição da senha padrão fraca `'123456'` caso o parâmetro `pwd` seja omitido no checkout. |
| 11 | **Gargalo N+1 no Relatório** | MEDIUM | [AppManager.js](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/ecommerce-api-legacy/src/AppManager.js#L89-L127) | Laços assíncronos que executam queries extras de matrículas e pagamentos para cada curso listado. |
| 12 | **Banco SQLite em Memória** | MEDIUM | [AppManager.js](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/ecommerce-api-legacy/src/AppManager.js#L7) | Conexão inicializada em `:memory:`, provocando perda total de usuários e vendas em caso de qualquer reboot da aplicação. |

---

### 3. Projeto `task-manager-api` (Python/Flask)

| ID | Vulnerabilidade / Code Smell | Severidade | Arquivo / Linhas | Justificativa / Descrição |
| :-: | :--- | :--- | :--- | :--- |
| 1 | **Password Exposta no Serializador** | CRITICAL | [user.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/task-manager-api/models/user.py#L21) | O dicionário gerado pelo serializador `to_dict` mantém e expõe a hash de senha em requisições de saída HTTP da API. |
| 2 | **Hashing Fraco via MD5 puro** | CRITICAL | [user.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/task-manager-api/models/user.py#L29-L32) | Uso do MD5 puro e sem salting individual para guardar credenciais, vulnerável a quebra por tabelas de arco-íris. |
| 3 | **Autenticação por Token Falso** | CRITICAL | [user_routes.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/task-manager-api/routes/user_routes.py#L210) | O login apenas gera um token previsível e nenhuma rota da aplicação valida ou exige a presença do token nos cabeçalhos. |
| 4 | **Credenciais de SMTP Hardcoded** | CRITICAL | [notification_service.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/task-manager-api/services/notification_service.py#L7-L10) | Senha literal, usuário, host e porta do servidor de emails de notificação configurados estaticamente no código. |
| 5 | **Efeitos de Startup db.create_all()** | HIGH | [app.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/task-manager-api/app.py#L30-L31) | Criação de tabelas no boot da API. Gera acoplamento e efeitos operacionais inesperados se executado concorrentemente. |
| 6 | **God Handlers de Rotas** | HIGH | [task_routes.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/task-manager-api/routes/task_routes.py) | Handlers de rota centralizando lógicas complexas de busca, formatações especiais de dados e queries ORM complexas. |
| 7 | **Gargalo N+1 em Tasks e Relatórios** | HIGH | [task_routes.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/task-manager-api/routes/task_routes.py#L41-L57), [report_routes.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/task-manager-api/routes/report_routes.py#L55-L68) | Queries extras repetidas para carregar dados de relacionamento (categoria/usuário) dentro de loops iterativos de listas. |
| 8 | **Domínio de Categoria Deslocado** | HIGH | [report_routes.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/task-manager-api/routes/report_routes.py#L157-L223) | Rotas completas de CRUD de categorias agregadas indevidamente dentro do blueprint de relatórios (falta de coesão). |
| 9 | **Swallowing de Exceções Genéricas** | MEDIUM | [task_routes.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/task-manager-api/routes/task_routes.py#L62), [report_routes.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/task-manager-api/routes/report_routes.py#L186) | Captura de exceção genérica com `except:` omitindo logs detalhados e dificultando depurações estruturadas. |
| 10 | **Casts de Dados sem Validação** | MEDIUM | [task_routes.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/task-manager-api/routes/task_routes.py#L261-L264) | Parsing direto de inputs de requisição para `int` sem tratamento de `ValueError`, retornando erros 500 em entradas mal formatadas. |
| 11 | **Lógica Overdue Duplicada** | MEDIUM | [task.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/task-manager-api/models/task.py) e [helpers.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/task-manager-api/utils/helpers.py) | Cálculos e verificações de datas expiradas implementados de forma duplicada e inconsistente em múltiplos arquivos. |
| 12 | **Camadas de Serviço Ignoradas** | MEDIUM | [notification_service.py](https://github.com/LucasGauterio/mba-ia-refactor-projects-skill/blob/6d1ce6248c3e956801010a89d8bdaab48029bf30/task-manager-api/services/notification_service.py) | Estrutura de pasta de serviços criada, porém subutilizada com a maior parte da lógica acoplada nas rotas. |

---

## B) Construção da Skill

### Decisões de Design
A skill `refactor-arch` foi estruturada para ser modular e flexível, utilizando o YAML frontmatter abaixo para auto-detecção e ativação na CLI:

```yaml
---
name: refactor-arch
description: >
  Analisa de forma agnóstica de tecnologia, audita code smells e vulnerabilidades de arquitetura, 
  gera relatórios de auditoria formatados por severidade e executa a refatoração automática de 
  projetos de backend (ex: Python/Flask, Node.js/Express) para a arquitetura padrão MVC (Model-View-Controller), 
  garantindo segurança, performance e validando o boot do sistema.
triggers:
  - /refactor-arch
  - refactor-mvc
  - refactor
---
```

A estrutura conceitual da skill foi dividida nas seguintes preocupações:
- **`SKILL.md` (Arquivo Mestre):** Coordena o fluxo sequencial das 3 fases (Análise, Auditoria e Refatoração).
- **`projeto_analise.md`:** Contém heurísticas de mapeamento de stack e frameworks.
- **`catalogo_antipatterns.md`:** Cataloga 10 falhas clássicas mapeadas para padrões C2 Wiki.
- **`template_relatorio.md`:** Define a estrutura e severidades para o relatório da Fase 2.
- **`guidelines_arquitetura.md`:** Define as responsabilidades lógicas e diretórios alvo para o MVC.
- **`playbook_refatoracao.md`:** Contém receitas práticas de refatoração para cada falha detectada.


### Catálogo de Anti-patterns
Os problemas identificados nos códigos legados foram estruturados sob duas categorias clássicas da Portland Pattern Repository (C2 Wiki):

#### A. Categoria: Development Anti-Patterns (Código & Micro-design)
*Problemas relacionados à escrita do código, algoritmos locais e más práticas de implementação.*
1. **Spaghetti Code / SQL Injection (Severidade: CRITICAL):**
   - *Sinais:* Concatenação direta de parâmetros dinâmicos em strings de consultas SQL brutas.
   - *Impacto:* Execução de queries maliciosas que comprometem a segurança do banco de dados.
2. **Insecure / Custom Cryptography (Severidade: CRITICAL):**
   - *Sinais:* Armazenamento de senhas em texto plano, uso de MD5 sem salt (`hashlib.md5`) ou funções baseadas em base64 (`badCrypto`).
   - *Impacto:* Quebra fácil de credenciais em caso de vazamento da base de dados.
3. **Hardcoded Secrets & Info Leakage (Severidade: CRITICAL / HIGH):**
   - *Sinais:* Segredos, chaves de gateways ou senhas de SMTP salvas no código-fonte, ou expostos em rotas de `/health`/logs.
   - *Impacto:* Exposição de segredos confidenciais em repositórios e monitoramentos públicos.
4. **Auth Illusion / Fake Security Tokens (Severidade: CRITICAL):**
   - *Sinais:* Geração de tokens de login fixos (`fake-jwt-token-`) sem assinatura real (JWT) e sem middlewares de proteção.
   - *Impacto:* Ausência de autorização real; rotas críticas acessíveis por qualquer requisição HTTP.
5. **Cover Your Assets / Generic Exception Swallowing (Severidade: MEDIUM):**
   - *Sinais:* Uso de blocos de captura genéricos (`except:` / `catch(err)`) que silenciam logs reais e retornam apenas mensagens opacas.
   - *Impacto:* Dificulta a depuração e monitoração de falhas em produção.

#### B. Categoria: Architecture Anti-Patterns (Estrutura & Macro-design)
*Problemas relacionados à separação de camadas, limites de domínio e fluxo de dados do sistema.*
6. **The Blob / God Class (Severidade: CRITICAL / HIGH):**
   - *Sinais:* Módulos centralizando inicialização do banco, roteamento, lógica de negócio e serialização HTTP em um único local.
   - *Impacto:* Código altamente acoplado e impossível de testar de forma isolada.
7. **Stovepipe System / Lack of Cohesive Domains (Severidade: HIGH / MEDIUM):**
   - *Sinais:* Mistura de responsabilidade de domínios diferentes (ex: CRUD de categoria dentro de relatórios, ou controladores acessando banco diretamente).
   - *Impacto:* Desorganização onde alterar regras exige mexer em arquivos não correlacionados.
8. **Query N+1 Performance Bottleneck (Severidade: HIGH / MEDIUM):**
   - *Sinais:* Execução de sub-queries para buscar dados filhos/relacionados dentro de loops da consulta inicial.
   - *Impacto:* Multiplica a latência e conexões com o banco exponencialmente de acordo com a escala de dados.
9. **Referential Integrity Failure / Cascade Deleter (Severidade: HIGH / MEDIUM):**
   - *Sinais:* Exclusões diretas de entidades pai que mantêm chaves estrangeiras órfãs, e ausência de restrições relacionais importantes (UNIQUE).
   - *Impacto:* Dados inconsistentes e corrupção da consistência funcional.
10. **Accidental Complexity / Startup Side-Effects (Severidade: HIGH):**
    - **Sinais:** Chamada estrutural de `db.create_all()` no startup de requisições de API.
    - **Impacto:** Lentidão no boot do servidor e risco operacional de alteração estrutural inesperada.


### Como Garantimos que a Skill é Agnóstica
A independência de tecnologia foi garantida por meio dos seguintes pilares no design da skill:
- **Classificação Neutra e Heurísticas de Stack (Fase 1):** O arquivo `projeto_analise.md` instrui o agente a buscar arquivos de manifesto padrão (`package.json`, `requirements.txt`) e marcadores de código para determinar dinamicamente a linguagem/framework no início da execução, sem assumir a stack de antemão.
- **Catálogo Baseado em Padrões Lógicos (Fase 2):** O arquivo `catalogo_antipatterns.md` foca na descrição teórica/lógica do problema (ex: concorrência de threads no SQLite, N+1 queries) fornecendo exemplos práticos em Python e JavaScript, permitindo a detecção universal.
- **Playbook de Transformação Bilíngue (Fase 3):** O playbook `playbook_refatoracao.md` descreve as transformações sob a ótica de "Antes/Depois" para ambos os ecossistemas, fornecendo à IA a base sintática correspondente de acordo com a stack detectada na Fase 1. A validação de boot também adapta os comandos de execução ao ecossistema (`npm start` vs `python app.py`).


### Desafios Encontrados e Resoluções
- **Desafio 1: Suporte a Múltiplas Tecnologias (Agnosticismo):** Instruir a IA a refatorar em linguagens diferentes sem cruzar sintaxes. *Resolução:* Criamos um playbook "bilíngue" com receitas de "Antes/Depois" isoladas para Python e Node.js.
- **Desafio 2: Projetos com Estruturas Iniciais Diferentes:** Evitar reestruturações redundantes ou deletar arquivos errados em pastas pré-existentes. *Resolução:* Implementamos heurísticas que avaliam o layout inicial de diretórios e adaptam as tarefas de reestruturação da Fase 3.
- **Desafio 3: Validação Dinâmica de Funcionamento (Boot/Endpoints):** Automatizar checagens genéricas de boot e conectividade em portas e ecossistemas distintos. *Resolução:* O agente inspeciona arquivos manifestos para orquestrar comandos dinâmicos (npm start vs python app.py) e executa testes via curl.
- **Desafio 4: Evitar Sobrecarga de Contexto do Prompt:** Impedir perda de foco ou alucinações no `SKILL.md` por excesso de regras. *Resolução:* Dividimos a skill em 5 sub-arquivos Markdown lidos sob demanda de referência.

### Decisão de Projeto: Restrição de Escopo via Workspace Rules (`.agents/rules`)
Durante as execuções do CLI `agy`, identificou-se um vazamento de escopo (*context leak*): ao ser invocado dentro de um subdiretório de projeto (como `ecommerce-api-legacy/`), o agente realizava varreduras exploratórias de diretórios e leituras de arquivos na raiz do repositório e em pastas de outros projetos.
- **Causa:** O CLI detecta o workspace buscando a pasta `.git` mais próxima na árvore, o que definia todo o repositório como o workspace da sessão do agente.
- **Solução Implementada:** Criamos uma regra de workspace "Always On" localizada em [.agents/rules/restricao_escopo.md](.agents/rules/restricao_escopo.md).
- **Funcionamento:** O motor do Antigravity lê e carrega este arquivo de regras imediatamente ao iniciar qualquer sessão da CLI neste repositório. A regra instrui cognitivamente o agente a conter suas operações de descoberta e ferramentas de sistema estritamente no subdiretório local do projeto ativo onde a invocação ocorreu, garantindo a privacidade das outras bases de código e a aderência ao escopo correto do projeto.

---

## C) Resultados

### Resumo dos Relatórios de Auditoria
| Projeto | CRITICAL | HIGH | MEDIUM | LOW | Total |
|---|---|---|---|---|---|
| `code-smells-project` | 4 | 4 | 1 | 2 | 11 |
| `ecommerce-api-legacy` | 3 | 5 | 0 | 2 | 10 |
| `task-manager-api` | 3 | 3 | 2 | 2 | 10 |

### Comparação Antes/Depois da Estrutura

#### `code-smells-project`
```
Antes:
.
├── app.py
├── controllers.py
├── database.py
├── models.py
└── requirements.txt

Depois:
.
├── .env
├── .env.example
├── app.py (MVC Compatibility Wrapper)
├── requirements.txt
└── src/
    ├── __init__.py
    ├── app.py (Composition Root Entrypoint)
    ├── config/
    │   ├── __init__.py
    │   ├── database.py
    │   └── settings.py
    ├── controllers/
    │   ├── __init__.py
    │   ├── pedido.py
    │   ├── produto.py
    │   └── usuario.py
    ├── middlewares/
    │   ├── __init__.py
    │   └── error_handler.py
    ├── models/
    │   ├── __init__.py
    │   ├── pedido.py
    │   ├── produto.py
    │   └── usuario.py
    └── routes/
        ├── __init__.py
        ├── general.py
        ├── pedido.py
        ├── produto.py
        └── usuario.py
```


#### `ecommerce-api-legacy`
```
Antes:
.
├── api.http
├── lms.db
├── package-lock.json
├── package.json
└── src/
    ├── AppManager.js
    ├── app.js
    └── utils.js

Depois:
.
├── .env
├── .env.example
├── api.http
├── lms.db
├── package-lock.json
├── package.json
└── src/
    ├── app.js
    ├── config/
    │   ├── constants.js
    │   ├── database.js
    │   ├── env.js
    │   └── security.js
    ├── controllers/
    │   ├── AdminController.js
    │   ├── CheckoutController.js
    │   └── UserController.js
    ├── middlewares/
    │   └── errorHandler.js
    ├── models/
    │   ├── AuditLogModel.js
    │   ├── CourseModel.js
    │   ├── EnrollmentModel.js
    │   ├── PaymentModel.js
    │   ├── ReportModel.js
    │   └── UserModel.js
    └── routes/
        └── api.js
```

#### `task-manager-api`
```
Antes:
.
├── app.py
├── database.py
├── seed.py
├── requirements.txt
├── models/
│   ├── category.py
│   ├── task.py
│   └── user.py
├── routes/
│   ├── report_routes.py
│   ├── task_routes.py
│   └── user_routes.py
├── services/
│   └── notification_service.py
└── utils/
    └── helpers.py

Depois:
.
├── .env
├── .env.example
├── app.py (Composition Root Stub)
├── database.py (Legacy Context Stub)
├── seed.py
├── requirements.txt
└── src/
    ├── app.py (Composition Root Entrypoint)
    ├── config/
    │   ├── database.py
    │   └── settings.py
    ├── models/
    │   ├── category.py
    │   ├── task.py
    │   └── user.py
    ├── controllers/
    │   ├── category_controller.py
    │   ├── report_controller.py
    │   ├── task_controller.py
    │   └── user_controller.py
    ├── routes/
    │   ├── category_routes.py
    │   ├── report_routes.py
    │   ├── task_routes.py
    │   └── user_routes.py
    ├── middlewares/
    │   └── error_handler.py
    ├── services/
    │   └── notification_service.py
    └── utils/
        └── helpers.py
```

### Checklist de Validação

#### Projeto 1: `code-smells-project`
- [x] Fase 1: Linguagem detectada corretamente
- [x] Fase 1: Framework detectado corretamente
- [x] Fase 1: Domínio da aplicação descrito corretamente
- [x] Fase 1: Número de arquivos analisados condiz com a realidade
- [x] Fase 2: Relatório segue o template definido nos arquivos de referência
- [x] Fase 2: Cada finding tem arquivo e linhas exatos
- [x] Fase 2: Findings ordenados por severidade (CRITICAL -> LOW)
- [x] Fase 2: Mínimo de 5 findings identificados
- [x] Fase 2: Detecção de APIs deprecated incluída (se aplicável)
- [x] Fase 2: Skill pausa e pede confirmação antes da Fase 3
- [x] Fase 3: Estrutura de diretórios segue padrão MVC
- [x] Fase 3: Configuração extraída para módulo de config (sem hardcoded)
- [x] Fase 3: Models criados para abstrair dados
- [x] Fase 3: Views/Routes separadas para visualização ou roteamento
- [x] Fase 3: Controllers concentram o fluxo da aplicação
- [x] Fase 3: Error handling centralizado
- [x] Fase 3: Entry point claro
- [x] Fase 3: Aplicação inicia sem erros
- [x] Fase 3: Endpoints originais respondem corretamente

#### Projeto 2: `ecommerce-api-legacy`
- [x] Fase 1: Linguagem detectada corretamente
- [x] Fase 1: Framework detectado corretamente
- [x] Fase 1: Domínio da aplicação descrito corretamente
- [x] Fase 1: Número de arquivos analisados condiz com a realidade
- [x] Fase 2: Relatório segue o template definido nos arquivos de referência
- [x] Fase 2: Cada finding tem arquivo e linhas exatos
- [x] Fase 2: Findings ordenados por severidade (CRITICAL -> LOW)
- [x] Fase 2: Mínimo de 5 findings identificados
- [x] Fase 2: Detecção de APIs deprecated incluída (se aplicável)
- [x] Fase 2: Skill pausa e pede confirmação antes da Fase 3
- [x] Fase 3: Estrutura de diretórios segue padrão MVC
- [x] Fase 3: Configuração extraída para módulo de config (sem hardcoded)
- [x] Fase 3: Models criados para abstrair dados
- [x] Fase 3: Views/Routes separadas para visualização ou roteamento
- [x] Fase 3: Controllers concentram o fluxo da aplicação
- [x] Fase 3: Error handling centralizado
- [x] Fase 3: Entry point claro
- [x] Fase 3: Aplicação inicia sem erros
- [x] Fase 3: Endpoints originais respondem corretamente

#### Projeto 3: `task-manager-api`
- [x] Fase 1: Linguagem detectada corretamente
- [x] Fase 1: Framework detectado corretamente
- [x] Fase 1: Domínio da aplicação descrito corretamente
- [x] Fase 1: Número de arquivos analisados condiz com a realidade
- [x] Fase 2: Relatório segue o template definido nos arquivos de referência
- [x] Fase 2: Cada finding tem arquivo e linhas exatos
- [x] Fase 2: Findings ordenados por severidade (CRITICAL -> LOW)
- [x] Fase 2: Mínimo de 5 findings identificados
- [x] Fase 2: Detecção de APIs deprecated incluída (se aplicável)
- [x] Fase 2: Skill pausa e pede confirmação antes da Fase 3
- [x] Fase 3: Estrutura de diretórios segue padrão MVC
- [x] Fase 3: Configuração extraída para módulo de config (sem hardcoded)
- [x] Fase 3: Models criados para abstrair dados
- [x] Fase 3: Views/Routes separadas para visualização ou roteamento
- [x] Fase 3: Controllers concentram o fluxo da aplicação
- [x] Fase 3: Error handling centralizado
- [x] Fase 3: Entry point claro
- [x] Fase 3: Aplicação inicia sem erros
- [x] Fase 3: Endpoints originais respondem corretamente

### Logs e Demonstrações de Funcionamento

#### Demonstração de Validação — Projeto 1 (`code-smells-project` - Flask)
```
Iniciando bateria de testes com o Flask test_client...
  ✓ [Teste 1] GET / (200 OK)
  ✓ [Teste 2] GET /health (200 OK - Sem vazamento de segredos)
  ✓ [Teste 3] GET /produtos (200 OK - 10 produtos retornados)
  ✓ [Teste 4] POST /login (Sucesso - 200 OK com dados de login)
  ✓ [Teste 5] POST /login (Falha - 401 Unauthorized com credenciais incorretas)
  ✓ [Teste 6] POST /admin/reset-db (Sem Token - 401 Unauthorized)
  ✓ [Teste 7] POST /admin/reset-db (Token Inválido - 403 Forbidden)
  ✓ [Teste 8] GET /relatorios/vendas (Sem Token - 401 Unauthorized)
  ✓ [Teste 9] GET /relatorios/vendas (Token Válido - 200 OK)
  ✓ [Teste 10] POST /pedidos (Fluxo Transacional - 201 Created com estoque atualizado)
  ✓ [Teste 11] POST /pedidos (Falha de Estoque / Transação - 400 Bad Request e rollback de estoque)
  ✓ [Teste 12] POST /admin/reset-db (Token Válido - 200 OK com banco resetado)
Bateria de testes finalizada com SUCESSO total!
```

#### Demonstração de Validação — Projeto 2 (`ecommerce-api-legacy` - Express)
```
[Teste 1] GET /api/checkout - Sem parâmetros...
  ✓ Passou (Retornou 400)
[Teste 2] POST /api/checkout - Curso não encontrado...
  ✓ Passou (Retornou 404)
[Teste 3] POST /api/checkout - Sucesso (Criar novo usuário e matricular)...
  ✓ Passou (Retornou 200 com msg e enrollment_id)
[Teste 4] POST /api/checkout - Sucesso (Usuário Leonan que já existe)...
  ✓ Passou (Retornou 200 com msg e enrollment_id)
[Teste 5] GET /api/admin/financial-report - Sem Token de Autorização...
  ✓ Passou (Retornou 401 com erro esperado)
[Teste 6] GET /api/admin/financial-report - Com Token Inválido...
  ✓ Passou (Retornou 403 com erro esperado)
[Teste 7] GET /api/admin/financial-report - Com Token Correto...
  ✓ Passou (Retornou 200 com faturamento consolidado por LEFT JOIN)
[Teste 8] DELETE /api/users/1 - Sem Token de Autorização...
  ✓ Passou (Retornou 401 com erro esperado)
[Teste 9] DELETE /api/users/1 - Com Token Correto (Deleção em Cascata)...
  ✓ Passou (Retornou 200 com remoção e PRAGMA foreign_keys ativa)
[Teste 10] GET /api/admin/financial-report - Relatório Pós-Deleção...
  ✓ Passou (Relatório gerado sem erros pós-deleção)
STATUS FINAL: TODOS OS TESTES PASSARAM COM SUCESSO! (100% OK)
```

#### Demonstração de Validação — Projeto 3 (`task-manager-api` - Flask)
```
1. Testing root...
  ✓ 200 OK {"message": "Task Manager API", "version": "1.0"}
2. Testing health...
  ✓ 200 OK {"status": "ok", "timestamp": "2026-08-06 10:14:32"}
3. Testing login...
  ✓ 200 OK {"message": "Login realizado com sucesso", "token": "eyJ1c2VyX2lk..."} (Token Criptográfico Assinado)
4. Testing get users...
  ✓ 200 OK (3 usuários retornados)
5. Testing get tasks...
  ✓ 200 OK (10 tarefas retornadas com Eager Loading de Usuário/Categoria)
6. Testing get categories...
  ✓ 200 OK (4 categorias retornadas com contagem agregada de tarefas)
7. Testing summary report...
  ✓ 200 OK (Consolidação de produtividade de usuários, prioridades e overdue)
8. Testing user report for João (ID 1)...
  ✓ 200 OK (Filtros de privacidade aplicados)
All basic verification tests passed successfully!
```

### Observações sobre o Comportamento da Skill entre Stacks
- **Detecção e Agnosticismo:** O módulo de análise (`projeto_analise.md`) mostrou-se eficiente ao ler as dependências do projeto para diferenciar a stack Python/Flask da stack Node.js/Express. O comando de execução e os scripts de validação de boot adaptaram-se dinamicamente ao ambiente (`python app.py` vs `npm start`).
- **Resolução de Anti-patterns e Modularidade:**
  - No ecossistema Python (Flask + SQLAlchemy), a skill utilizou de maneira adequada decorators do Flask como `@app.errorhandler` para tratamento centralizado de erros e `joinedload` para otimizar queries e solucionar gargalos N+1.
  - No ecossistema Node.js (Express + sqlite3), a skill construiu middlewares clássicos de erro e autenticação baseados em assinaturas de callbacks de requisição `(req, res, next)`, além de implementar controle de transação usando o método assíncrono sequencial `db.serialize()`.
- **Adaptação de Layouts:** No Projeto 3, que já continha subpastas pré-existentes, a skill respeitou o layout parcial e portou os arquivos de forma coesa para dentro de `src/`, sem criar redundâncias ou deletar arquivos de maneira incorreta. No Projeto 1 (monolítico sem pastas), ela estruturou toda a arquitetura MVC do zero.
- **Aprimoramento de Segurança e Cobertura da Skill:**
  - Durante o processo de validação, constatou-se que a skill gerava recomendações de segurança no relatório da Fase 2 (ex: token de autenticação), mas não forçava a si mesma a validar a cobertura de todas as recomendações na Fase 3, deixando rotas sensíveis desprotegidas no `task-manager-api`.
  - Para corrigir esse comportamento, a custom skill `refactor-arch` foi atualizada: o `SKILL.md` passou a contar com uma etapa obrigatória de **"Verificação de Cobertura de Segurança (Pós-Auditoria)"** que exige que o agente liste e mapeie explicitamente cada achado no log final; e o `playbook_refatoracao.md` foi enriquecido com a receita **13. Autenticação e Autorização baseada em Token (JWT/Assinatura)** fornecendo exemplos prontos de decorators e middlewares.

---

## D) Como Executar

### Pré-requisitos
- **Antigravity CLI (`agy`):** A ferramenta CLI do Gemini configurada localmente.
- **Node.js:** Versão 18+ instalada.
- **Python:** Versão 3.10+ instalada.

### Preparação do Ambiente
Antes de rodar a skill em qualquer um dos projetos, instale as dependências de biblioteca necessárias para que as validações e testes de boot da Fase 3 funcionem sem falhar.

#### Projeto 1 — `code-smells-project` (Python/Flask)
```bash
# Navegue a partir da raiz do repositório
cd code-smells-project

# Crie e ative o ambiente virtual (opcional, mas recomendado)
python -m venv venv
# No Windows PowerShell:
.\venv\Scripts\Activate.ps1
# No Linux/macOS:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

#### Projeto 2 — `ecommerce-api-legacy` (Node.js/Express)
```bash
# Navegue a partir da raiz do repositório
cd ecommerce-api-legacy

# Instale os pacotes npm
npm install
```

#### Projeto 3 — `task-manager-api` (Python/Flask)
```bash
# Navegue a partir da raiz do repositório
cd task-manager-api

# Crie e ative o ambiente virtual (opcional, mas recomendado)
python -m venv venv
# No Windows PowerShell:
.\venv\Scripts\Activate.ps1
# No Linux/macOS:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

#### Configuração dos Diretórios de Custom Skills
Para que a CLI reconheça a custom skill `/refactor-arch` em cada projeto de forma separada, certifique-se de que a pasta da skill (`.agents/skills/refactor-arch/` ou `.claude/skills/refactor-arch/` dependendo da CLI adotada) esteja copiada na raiz de cada um dos subdiretórios de projeto correspondentes.

---

### Comandos de Invocação da Skill
Para rodar a skill de refatoração arquitetural MVC em cada projeto de forma isolada (partindo sempre da raiz do repositório), execute:

#### Projeto 1 — `code-smells-project` (Python/Flask)
```bash
# Navegue a partir da raiz do repositório
cd code-smells-project
agy --prompt-interactive "/refactor-arch"
```

#### Projeto 2 — `ecommerce-api-legacy` (Node.js/Express)
```bash
# Navegue a partir da raiz do repositório
cd ecommerce-api-legacy
agy --prompt-interactive "/refactor-arch"
```

#### Projeto 3 — `task-manager-api` (Python/Flask)
```bash
# Navegue a partir da raiz do repositório
cd task-manager-api
agy --prompt-interactive "/refactor-arch"
```

---

### Como Validar que a Refatoração Funcionou
Após concluir as refatorações arquiteturais para MVC, você pode validar o funcionamento dos servidores e endpoints das APIs de forma isolada executando estes comandos no terminal PowerShell:

#### 1. Validando o Projeto 1 (`code-smells-project`)
```powershell
# Entre na pasta do projeto a partir da raiz
cd code-smells-project

# Inicialize o servidor Flask de forma detached no PowerShell
Start-Process -FilePath "venv\Scripts\python.exe" -ArgumentList "app.py" -NoNewWindow

# Aguarde 3 segundos para o boot e faça a consulta ao endpoint de saúde
Start-Sleep -Seconds 3
Invoke-RestMethod -Uri "http://127.0.0.1:5000/health"

# Finalize o processo Python após a validação
Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue
```

#### 2. Validando o Projeto 2 (`ecommerce-api-legacy`)
```powershell
# Entre na pasta do projeto a partir da raiz (volte antes se necessário)
cd ../ecommerce-api-legacy

# Inicialize o servidor Node.js de forma detached no PowerShell
Start-Process -FilePath "node" -ArgumentList "src/app.js" -NoNewWindow

# Aguarde 3 segundos para o boot e faça a consulta ao endpoint de relatório financeiro protegido
Start-Sleep -Seconds 3
try {
    Invoke-RestMethod -Uri "http://127.0.0.1:3000/api/admin/financial-report"
} catch {
    # Exibe a resposta HTTP 401 de acesso negado interceptada pelo middleware adminAuth
    $_.Exception.Response
}

# Finalize o processo Node após a validação
Stop-Process -Name "node" -Force -ErrorAction SilentlyContinue
```

#### 3. Validando o Projeto 3 (`task-manager-api`)
```powershell
# Entre na pasta do projeto a partir da raiz
cd ../task-manager-api

# Inicialize o servidor Flask de forma detached no PowerShell
Start-Process -FilePath "venv\Scripts\python.exe" -ArgumentList "app.py" -NoNewWindow

# Aguarde 3 segundos para o boot e faça a consulta ao endpoint de saúde
Start-Sleep -Seconds 3
Invoke-RestMethod -Uri "http://127.0.0.1:5000/health"

# Finalize o processo Python após a validação
Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue
```

---

#### Validação via WSL (Linux/Bash)
Se você estiver utilizando um terminal Linux dentro do WSL (Windows Subsystem for Linux), pode executar a validação de forma isolada e em background usando o operador `&` e utilitários nativos de Linux:

##### 1. Validando o Projeto 1 (`code-smells-project`)
```bash
# Entre na pasta do projeto
cd code-smells-project

# Crie e instale dependências do venv Linux (caso não tenha instalado no WSL)
python3 -m venv venv-wsl
venv-wsl/bin/pip install -r requirements.txt

# Inicie o servidor Flask em background redirecionando a saída
venv-wsl/bin/python app.py > wsl_debug.log 2>&1 &

# Aguarde 5 segundos para o boot e faça a requisição ignorando proxies locais
sleep 5
curl -s --noproxy localhost,127.0.0.1 http://127.0.0.1:5000/health

# Mate o processo Python iniciado no WSL para liberar a porta 5000
pkill -f "python.*app.py"
```

##### 2. Validando o Projeto 2 (`ecommerce-api-legacy`)
```bash
# Entre na pasta do projeto
cd ../ecommerce-api-legacy

# Instale as dependências nativas npm no Linux (caso não tenha instalado no WSL)
npm install

# Inicie o servidor Express em background
node src/app.js > wsl_debug.log 2>&1 &

# Aguarde 5 segundos para o boot e faça a requisição ignorando proxies locais
sleep 5
curl -s --noproxy localhost,127.0.0.1 http://127.0.0.1:3000/api/admin/financial-report

# Mate o processo Node iniciado no WSL para liberar a porta 3000
pkill -f "node.*app.js"
```

##### 3. Validando o Projeto 3 (`task-manager-api`)
```bash
# Entre na pasta do projeto
cd ../task-manager-api

# Crie e instale dependências do venv Linux (caso não tenha instalado no WSL)
python3 -m venv venv-wsl
venv-wsl/bin/pip install -r requirements.txt

# Inicie o servidor Flask em background redirecionando a saída
venv-wsl/bin/python app.py > wsl_debug.log 2>&1 &

# Aguarde 5 segundos para o boot e faça a requisição ignorando proxies locais
sleep 5
curl -s --noproxy localhost,127.0.0.1 http://127.0.0.1:5000/health

# Mate o processo Python iniciado no WSL para liberar a porta 5000
pkill -f "python.*app.py"
```


