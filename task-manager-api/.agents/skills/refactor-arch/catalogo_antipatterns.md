# Catálogo de Anti-patterns

Os problemas identificados nos códigos legados estão estruturados sob duas categorias clássicas da Portland Pattern Repository (C2 Wiki):

## A. Categoria: Development Anti-Patterns (Código & Micro-design)

### 1. Spaghetti Code / SQL Injection (Severidade: CRITICAL)
- **Sinais:** Concatenação direta de parâmetros dinâmicos em strings de consultas SQL brutas.
- **Exemplo:** `SELECT * FROM produtos WHERE id = " + str(id)`.
- **Impacto:** Execução de queries maliciosas que comprometem a segurança do banco de dados.

### 2. Insecure / Custom Cryptography (Severidade: CRITICAL)
- **Sinais:** Armazenamento de senhas em texto plano, uso de MD5 sem salt (`hashlib.md5`) ou funções baseadas em base64 (`badCrypto`).
- **Impacto:** Quebra fácil de credenciais em caso de vazamento da base de dados.

### 3. Hardcoded Secrets & Info Leakage (Severidade: CRITICAL / HIGH)
- **Sinais:** Segredos (`SECRET_KEY`), chaves de gateways ou senhas de SMTP salvas no código-fonte, ou expostas em rotas de `/health`/logs.
- **Impacto:** Exposição de segredos confidenciais em repositórios e monitoramentos públicos.

### 4. Auth Illusion / Fake Security Tokens (Severidade: CRITICAL)
- **Sinais:** Geração de tokens de login fixos (`fake-jwt-token-`) sem assinatura real (JWT) e sem middlewares de proteção.
- **Impacto:** Ausência de autorização real; rotas críticas acessíveis por qualquer requisição HTTP.

### 5. Cover Your Assets / Generic Exception Swallowing (Severidade: MEDIUM)
- **Sinais:** Uso de blocos de captura genéricos (`except:` / `catch(err)`) que silenciam logs reais e retornam apenas mensagens opacas.
- **Impacto:** Dificulta a depuração e monitoração de falhas em produção.

---

## B. Categoria: Architecture Anti-Patterns (Estrutura & Macro-design)

### 6. The Blob / God Class (Severidade: CRITICAL / HIGH)
- **Sinais:** Módulos centralizando inicialização do banco, roteamento, lógica de negócio e serialização HTTP em um único local.
- **Impacto:** Código altamente acoplado e impossível de testar de forma isolada.

### 7. Stovepipe System / Lack of Cohesive Domains (Severidade: HIGH / MEDIUM)
- **Sinais:** Mistura de responsabilidade de domínios diferentes (ex: CRUD de categoria dentro de relatórios, ou controladores acessando banco diretamente).
- **Impacto:** Desorganização onde alterar regras exige mexer em arquivos não correlacionados.

### 8. Query N+1 Performance Bottleneck (Severidade: HIGH / MEDIUM)
- **Sinais:** Execução de sub-queries para buscar dados filhos/relacionados dentro de loops da consulta inicial.
- **Impacto:** Multiplica a latência e conexões com o banco exponencialmente de acordo com a escala de dados.

### 9. Referential Integrity Failure / Cascade Deleter (Severidade: HIGH / MEDIUM)
- **Sinais:** Exclusões diretas de entidades pai que mantêm chaves estrangeiras órfãs, e ausência de restrições relacionais importantes (UNIQUE).
- **Impacto:** Dados inconsistentes e corrupção da consistência funcional.

### 10. Accidental Complexity / Startup Side-Effects (Severidade: HIGH)
- **Sinais:** Chamada estrutural de `db.create_all()` no startup de requisições de API.
- **Impacto:** Lentidão no boot do servidor e risco operacional de alteração estrutural inesperada.
