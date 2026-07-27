# Catálogo de Anti-patterns e Vulnerabilidades

Este catálogo define os principais anti-patterns a serem identificados nos projetos backend legados.

---

## 1. SQL Injection (CRITICAL)
- **Sinais de Detecção:**
  - Uso de interpolação ou concatenação de strings para criar consultas SQL.
  - Exemplo em Python: `"SELECT * FROM users WHERE id = " + str(user_id)` ou `f"SELECT * FROM users WHERE id = {user_id}"`.
  - Exemplo em Node.js: `` `SELECT * FROM users WHERE id = ${id}` ``.
- **Impacto:** Permite a atacantes roubar, alterar ou deletar registros do banco de dados, além de executar comandos arbitrários.

---

## 2. Insecure Cryptography / Deprecated APIs (CRITICAL)
- **Sinais de Detecção:**
  - Hashing de senhas com algoritmos fracos ou obsoletos como MD5 (`hashlib.md5(...)`).
  - Funções de criptografia customizadas baseadas em repetição de base64 ou rotações triviais (ex: `badCrypto`).
- **Impacto:** Senhas vazadas podem ser quebradas em segundos por ataques de força bruta ou tabelas de busca pré-computadas (Rainbow Tables).

---

## 3. Hardcoded Credentials / Secrets (CRITICAL / HIGH)
- **Sinais de Detecção:**
  - Atribuição direta de chaves de API, senhas de banco de dados, ou secrets do Express/Flask como strings no código-fonte.
  - Exemplo: `app.config["SECRET_KEY"] = "minha-chave-super-secreta"`, `password = "senha123"`.
- **Impacto:** Credenciais expostas no repositório de controle de versão comprometem toda a segurança da infraestrutura de produção.

---

## 4. Backdoor Admin / Arbitrary Executions (CRITICAL)
- **Sinais de Detecção:**
  - Rotas de API que aceitam instruções SQL puras enviadas no corpo da requisição e as executam sem autenticação ou validação prévia.
  - Exemplo: `cursor.execute(request.json.get("sql"))`.
- **Impacto:** Permite controle total do banco de dados por qualquer pessoa com acesso à rede.

---

## 5. Mutability of Global State (HIGH / MEDIUM)
- **Sinais de Detecção:**
  - Variáveis globais mutáveis em escopo de módulo ou arquivo usadas para manter dados de requisição, cache de memória ou contadores de transação.
  - Exemplo: `globalCache = {}`, `totalRevenue = 0`.
- **Impacto:** Falta de segurança em threads/processamento concorrente. Requisições simultâneas podem sobrescrever dados umas das outras, levando a vazamentos ou corrupção de estado.

---

## 6. Callback Hell / N+1 Queries (HIGH / MEDIUM)
- **Sinais de Detecção:**
  - Em Node.js: Aninhamento profundo de funções de callback para queries de banco de dados (`db.all(..., c => { db.all(..., e => { ... }) })`).
  - Em Python/Flask/SQLAlchemy ou SQL puro: Consulta de tabelas secundárias em um loop iterativo para cada registro obtido na consulta principal.
- **Impacto:** Desempenho severamente prejudicado devido ao atraso de latência cumulativo (N queries adicionais para N registros).

---

## 7. Violation of Referential Integrity (MEDIUM)
- **Sinais de Detecção:**
  - Operações de remoção (DELETE) de registros pai (ex: usuários) sem tratamento em cascata ou limpeza de registros filhos (ex: matrículas, pagamentos, tarefas).
- **Impacto:** Dados órfãos no banco de dados que causam falhas inesperadas na leitura de dados relacionados por chave estrangeira inexistente.

---

## 8. Missing Routing Layer / Monolithic Class (HIGH / MEDIUM)
- **Sinais de Detecção:**
  - Toda a inicialização de banco, lógica de negócios, mapeamento de rotas e formatação de resposta reunidas em uma única classe centralizada (ex: `AppManager.js` sem delegar para controladores ou roteadores).
- **Impacto:** Baixa manutenibilidade, impossibilidade de criar testes unitários isolados, e dificuldade para evoluir rotas e regras de negócio.

---

## 9. Lack of Standardized Error Handling (MEDIUM / LOW)
- **Sinais de Detecção:**
  - Blocos `try-except` genéricos (`except:`) que silenciam logs reais ou retornam apenas mensagens como `"Erro interno"`.
  - Falta de tratamento centralizado de erros (Middleware/Decorators), espalhando blocos `try-catch` redundantes em todos os controladores.
- **Impacto:** Falhas difíceis de depurar em produção e exposição desnecessária de detalhes internos de exceção para clientes da API.
