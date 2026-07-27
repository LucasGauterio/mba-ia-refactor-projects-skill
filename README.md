# Desafio de Refatoração Arquitetural Automatizada (MVC)

Este repositório contém a implementação de uma Skill de IA para refatoração arquitetural para o padrão MVC, conforme os requisitos do desafio.

## A) Análise Manual

### 1. Projeto `code-smells-project` (Python/Flask)

1. **CRITICAL: Execução de SQL Arbitrário**
   - **Arquivo/Linhas:** [app.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/app.py#L59-L79) (rota `/admin/query`)
   - **Justificativa:** Comprometimento direto do banco de dados por requisições HTTP normais de qualquer cliente.
   
2. **CRITICAL: Reset de DB sem Autenticação**
   - **Arquivo/Linhas:** [app.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/app.py#L47-L57) (rota `/admin/reset-db`)
   - **Justificativa:** Perda total de dados com uma única chamada HTTP GET/POST, sem qualquer validação de segurança.

3. **CRITICAL: Queries por Concatenação de Strings**
   - **Arquivo/Linhas:** [models.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/models.py#L28) e [models.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/models.py#L47-L50)
   - **Justificativa:** Múltiplos pontos de SQL Injection direta que permitem leitura e deleção não autorizada de dados.

4. **CRITICAL: Senhas em Texto Puro e Exposição na API**
   - **Arquivo/Linhas:** [database.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/database.py#L76-L79) e [models.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/models.py#L83)
   - **Justificativa:** Armazenamento de senhas sem hash e devolução do campo de senha diretamente na resposta JSON da API.

5. **HIGH: SECRET_KEY e DEBUG=True Hardcoded**
   - **Arquivo/Linhas:** [app.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/app.py#L7-L8)
   - **Justificativa:** Acoplamento inseguro do segredo criptográfico ao código e riscos de execução no modo de depuração em produção.

6. **HIGH: Rota de Healthcheck Expõe Segredos**
   - **Arquivo/Linhas:** [controllers.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/controllers.py#L289-L290)
   - **Justificativa:** Vazamento desnecessário do caminho do banco e da `SECRET_KEY` no payload JSON de `/health`.

7. **HIGH: Conexão SQLite Global Compartilhada**
   - **Arquivo/Linhas:** [database.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/database.py#L10)
   - **Justificativa:** Concorrência frágil em requisições assíncronas do Flask, gerando erros e dificultando testes isolados.

8. **HIGH: Fluxo de Pedido sem Rollback Transacional**
   - **Arquivo/Linhas:** [models.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/models.py#L133-L169)
   - **Justificativa:** Sem controle de transação (commit intermediário e sem rollback). Em caso de falha a meio, o estoque e os pedidos podem ficar inconsistentes.

9. **MEDIUM: Mistura de Responsabilidades nos Controllers**
   - **Arquivo/Linhas:** [controllers.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/controllers.py)
   - **Justificativa:** Controllers misturam regras de roteamento HTTP, validações de payload e lógicas complexas de negócio.

10. **MEDIUM: Gargalo N+1 nas Consultas de Pedidos**
    - **Arquivo/Linhas:** [models.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/models.py#L171-L233)
    - **Justificativa:** Execução de múltiplas sub-queries no banco de dados para buscar itens e produtos de cada pedido em um loop.

11. **MEDIUM: Schema sem Constraints Relacionais**
    - **Arquivo/Linhas:** [database.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/database.py#L37-L53)
    - **Justificativa:** Tabelas criadas sem Foreign Keys (FKs) ativas e restrições integras, facilitando a existência de registros órfãos.

12. **LOW: Constantes de Domínio Repetidas Inline**
    - **Arquivo/Linhas:** [controllers.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/controllers.py#L52)
    - **Justificativa:** Categorias válidas repetidas como literais de string em múltiplos trechos de validação.

---

### 2. Projeto `ecommerce-api-legacy` (Node.js/Express)

1. **CRITICAL: Segredos Hardcoded no Código**
   - **Arquivo/Linhas:** [utils.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/utils.js#L1-L7)
   - **Justificativa:** Exposição de chaves privadas do gateway de pagamento, credenciais do SMTP e senhas de banco no código-fonte.

2. **CRITICAL: Log de Dados Sensíveis de Pagamento**
   - **Arquivo/Linhas:** [AppManager.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js#L45)
   - **Justificativa:** Chave do gateway e o número do cartão de crédito são printados no console no momento do checkout, expondo dados financeiros.

3. **CRITICAL: Senha de Seed em Texto Puro**
   - **Arquivo/Linhas:** [AppManager.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js#L18)
   - **Justificativa:** Inserção inicial do usuário 'Leonan' com a senha literal '123' sem hashing no banco de dados.

4. **CRITICAL: Algoritmo badCrypto Fraco e Determinístico**
   - **Arquivo/Linhas:** [utils.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/utils.js#L17-L23)
   - **Justificativa:** Algoritmo customizado de hash baseado em base64 repetido que gera colisões e não possui salt ou fator de trabalho.

5. **HIGH: Rota do Relatório Financeiro Pública**
   - **Arquivo/Linhas:** [AppManager.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js#L80)
   - **Justificativa:** Rota `/api/admin/financial-report` expõe faturamento total e dados de alunos sem nenhuma autenticação admin.

6. **HIGH: Checkout sem Transação de Banco**
   - **Arquivo/Linhas:** [AppManager.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js#L50-L63)
   - **Justificativa:** Inserção de matrícula e pagamento ocorrem em statements separados assíncronos. Falhas deixam matrículas criadas sem registro de pagamento.

7. **HIGH: Schema sem Constraints e UNIQUE**
   - **Arquivo/Linhas:** [AppManager.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js#L12-L16)
   - **Justificativa:** Ausência de `UNIQUE(email)` em users e ausência de restrições relacionais explícitas nas tabelas de junção.

8. **HIGH: Deleção Limpa Usuário mas deixa Órfãos**
   - **Arquivo/Linhas:** [AppManager.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js#L131-L137)
   - **Justificativa:** Rota DELETE `/api/users/:id` apaga o usuário mas mantém matrículas e pagamentos órfãos apontando para IDs inexistentes.

9. **MEDIUM: Payload com Nomes Opacos**
   - **Arquivo/Linhas:** [AppManager.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js#L29-L33)
   - **Justificativa:** Propriedades de requisição curtas e obscuras (`usr`, `eml`, `pwd`, `c_id`, `card`) dificultando integração e clareza do contrato.

10. **MEDIUM: Senha Padrão Fraca e Previsível**
    - **Arquivo/Linhas:** [AppManager.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js#L68)
    - **Justificativa:** Atribuição da senha padrão literal `'123456'` caso o parâmetro de senha (`pwd`) esteja ausente no checkout.

11. **MEDIUM: Gargalo N+1 no Relatório Financeiro**
    - **Arquivo/Linhas:** [AppManager.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js#L89-L127)
    - **Justificativa:** Nested queries executadas em loops assíncronos para cada curso e para cada matrícula, sobrecarregando o banco de dados.

12. **MEDIUM: Banco em Memória de Curta Duração**
    - **Arquivo/Linhas:** [AppManager.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js#L7)
    - **Justificativa:** Banco SQLite inicializado em `:memory:`, fazendo com que todas as matrículas, usuários e pagamentos se percam ao reiniciar a app.

---

### 3. Projeto `task-manager-api` (Python/Flask)

1. **CRITICAL: Password Exposta no Serializador to_dict**
   - **Arquivo/Linhas:** [user.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/models/user.py#L21)
   - **Justificativa:** O método `to_dict` expõe diretamente a senha/hash do usuário para chamadas HTTP externas.

2. **CRITICAL: Hash de Senha Inseguro com MD5 puro**
   - **Arquivo/Linhas:** [user.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/models/user.py#L29-L32)
   - **Justificativa:** Uso do algoritmo MD5 desatualizado e sem salt para armazenar as credenciais de acesso no banco de dados.

3. **CRITICAL: Autenticação por Token Fake e Previsível**
   - **Arquivo/Linhas:** [user_routes.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/routes/user_routes.py#L210)
   - **Justificativa:** O login apenas devolve `'fake-jwt-token-' + str(user.id)` e nenhuma rota valida autenticação ou valida a presença do token.

4. **CRITICAL: Segredos de SMTP Hardcoded**
   - **Arquivo/Linhas:** [notification_service.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/services/notification_service.py#L7-L10)
   - **Justificativa:** Host, porta, usuário e senha literal do servidor de e-mails de notificação estão expostos como constantes de instância.

5. **HIGH: db.create_all() Executado no Startup**
   - **Arquivo/Linhas:** [app.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/app.py#L30-L31)
   - **Justificativa:** Side-effect estrutural no boot da aplicação, recriando tabelas silenciosamente sem controle de migrações estruturadas.

6. **HIGH: God Handlers no Fluxo de Tasks**
   - **Arquivo/Linhas:** [task_routes.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/routes/task_routes.py)
   - **Justificativa:** Controladores concentram regras de negócios, serializações sob medida, e consultas SQL complexas acoplados na camada HTTP.

7. **HIGH: Gargalo N+1 nas Tasks e Relatórios**
   - **Arquivo/Linhas:** [task_routes.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/routes/task_routes.py#L41-L57) e [report_routes.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/routes/report_routes.py#L55-L68)
   - **Justificativa:** Realização de queries adicionais repetidas para buscar dados de categoria e usuários associados em loops.

8. **HIGH: Módulo de Relatórios Contém CRUD de Categorias**
   - **Arquivo/Linhas:** [report_routes.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/routes/report_routes.py#L157-L223)
   - **Justificativa:** Violação grave de coesão do domínio, agrupando criação, atualização e exclusão de categorias no arquivo de relatórios.

9. **MEDIUM: Captura de Exceção Genérica (Bare Except)**
   - **Arquivo/Linhas:** [task_routes.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/routes/task_routes.py#L62) e [report_routes.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/routes/report_routes.py#L186)
   - **Justificativa:** Silenciamento de stack traces e mascaramento de erros reais do banco de dados por capturas com `except:`.

10. **MEDIUM: Casts sem Validação no Search de Tasks**
    - **Arquivo/Linhas:** [task_routes.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/routes/task_routes.py#L261-L264)
    - **Justificativa:** Conversão direta de inputs de requisição para `int` sem tratar exceções, gerando erros HTTP 500 do servidor se forem fornecidos valores inválidos.

11. **MEDIUM: Lógica de Status, Overdue e Parsing Duplicada**
    - **Arquivo/Linhas:** [task.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/models/task.py) e [helpers.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/utils/helpers.py)
    - **Justificativa:** Lógicas repetidas e inconsistentes de formatação de datas e checagem de prazos expirados geram riscos de manutenção.

12. **MEDIUM: Camada de Serviços Subutilizada**
    - **Arquivo/Linhas:** [notification_service.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/services/notification_service.py)
    - **Justificativa:** Estruturação de pasta `services/` e `utils/` criada mas a maior parte da lógica permanece espalhada nos handlers de rotas.

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
*A ser preenchido durante a criação da skill.*

### Desafios Encontrados e Resoluções
*A ser preenchido durante a criação da skill.*

---

## C) Resultados

### Resumo dos Relatórios de Auditoria
| Projeto | CRITICAL | HIGH | MEDIUM | LOW | Total |
|---|---|---|---|---|---|
| `code-smells-project` | - | - | - | - | - |
| `ecommerce-api-legacy` | - | - | - | - | - |
| `task-manager-api` | - | - | - | - | - |

### Comparação Antes/Depois da Estrutura

#### `code-smells-project`
```
Antes:
(estrutura original)

Depois:
(estrutura refatorada)
```

#### `ecommerce-api-legacy`
```
Antes:
(estrutura original)

Depois:
(estrutura refatorada)
```

#### `task-manager-api`
```
Antes:
(estrutura original)

Depois:
(estrutura refatorada)
```

### Checklist de Validação

#### Projeto 1: `code-smells-project`
- [ ] Fase 1: Linguagem detectada corretamente
- [ ] Fase 1: Framework detectado corretamente
- [ ] Fase 1: Domínio da aplicação descrito corretamente
- [ ] Fase 1: Número de arquivos analisados condiz com a realidade
- [ ] Fase 2: Relatório segue o template definido nos arquivos de referência
- [ ] Fase 2: Cada finding tem arquivo e linhas exatos
- [ ] Fase 2: Findings ordenados por severidade (CRITICAL -> LOW)
- [ ] Fase 2: Mínimo de 5 findings identificados
- [ ] Fase 2: Detecção de APIs deprecated incluída (se aplicável)
- [ ] Fase 2: Skill pausa e pede confirmação antes da Fase 3
- [ ] Fase 3: Estrutura de diretórios segue padrão MVC
- [ ] Fase 3: Configuração extraída para módulo de config (sem hardcoded)
- [ ] Fase 3: Models criados para abstrair dados
- [ ] Fase 3: Views/Routes separadas para visualização ou roteamento
- [ ] Fase 3: Controllers concentram o fluxo da aplicação
- [ ] Fase 3: Error handling centralizado
- [ ] Fase 3: Entry point claro
- [ ] Fase 3: Aplicação inicia sem erros
- [ ] Fase 3: Endpoints originais respondem corretamente

#### Projeto 2: `ecommerce-api-legacy`
- [ ] Fase 1: Linguagem detectada corretamente
- [ ] Fase 1: Framework detectado corretamente
- [ ] Fase 1: Domínio da aplicação descrito corretamente
- [ ] Fase 1: Número de arquivos analisados condiz com a realidade
- [ ] Fase 2: Relatório segue o template definido nos arquivos de referência
- [ ] Fase 2: Cada finding tem arquivo e linhas exatos
- [ ] Fase 2: Findings ordenados por severidade (CRITICAL -> LOW)
- [ ] Fase 2: Mínimo de 5 findings identificados
- [ ] Fase 2: Detecção de APIs deprecated incluída (se aplicável)
- [ ] Fase 2: Skill pausa e pede confirmação antes da Fase 3
- [ ] Fase 3: Estrutura de diretórios segue padrão MVC
- [ ] Fase 3: Configuração extraída para módulo de config (sem hardcoded)
- [ ] Fase 3: Models criados para abstrair dados
- [ ] Fase 3: Views/Routes separadas para visualização ou roteamento
- [ ] Fase 3: Controllers concentram o fluxo da aplicação
- [ ] Fase 3: Error handling centralizado
- [ ] Fase 3: Entry point claro
- [ ] Fase 3: Aplicação inicia sem erros
- [ ] Fase 3: Endpoints originais respondem corretamente

#### Projeto 3: `task-manager-api`
- [ ] Fase 1: Linguagem detectada corretamente
- [ ] Fase 1: Framework detectado corretamente
- [ ] Fase 1: Domínio da aplicação descrito corretamente
- [ ] Fase 1: Número de arquivos analisados condiz com a realidade
- [ ] Fase 2: Relatório segue o template definido nos arquivos de referência
- [ ] Fase 2: Cada finding tem arquivo e linhas exatos
- [ ] Fase 2: Findings ordenados por severidade (CRITICAL -> LOW)
- [ ] Fase 2: Mínimo de 5 findings identificados
- [ ] Fase 2: Detecção de APIs deprecated incluída (se aplicável)
- [ ] Fase 2: Skill pausa e pede confirmação antes da Fase 3
- [ ] Fase 3: Estrutura de diretórios segue padrão MVC
- [ ] Fase 3: Configuração extraída para módulo de config (sem hardcoded)
- [ ] Fase 3: Models criados para abstrair dados
- [ ] Fase 3: Views/Routes separadas para visualização ou roteamento
- [ ] Fase 3: Controllers concentram o fluxo da aplicação
- [ ] Fase 3: Error handling centralizado
- [ ] Fase 3: Entry point claro
- [ ] Fase 3: Aplicação inicia sem erros
- [ ] Fase 3: Endpoints originais respondem corretamente
