# Regra de Workspace: Restrição de Escopo e Contenção de Diretórios

Este arquivo define regras globais de comportamento para todas as sessões do agente iniciadas dentro deste repositório.

---

## Metadados
- **Name:** restricao-escopo
- **Description:** Restringe a atuação do agente exclusivamente ao diretório local do projeto ativo.
- **Activation:** Always On

---

## Diretrizes de Comportamento Obrigatórias

1. **Escopo de Execução Estrito:**
   Você (o agente) deve limitar todas as suas operações de leitura, escrita, deleção, listagem (`ListDir` / `Get-ChildItem`) e análise de arquivos **exclusivamente ao subdiretório do projeto atual** onde você foi invocado (ex: `code-smells-project/`, `ecommerce-api-legacy/` ou `task-manager-api/`).

2. **Proibição de Varredura Externa (Workspace Boundaries):**
   É **terminantemente proibido** ler, listar ou executar comandos exploratórios na raiz do repositório (`G:\Projects\mba-ia-refactor-projects-skill`) ou em pastas de projetos vizinhos durante a sua fase de boot, descoberta de contexto ou auditoria. Ignore completamente a existência dos outros diretórios no repositório.

3. **Mapeamento de Domínio e Contexto:**
   Se precisar de dados de contexto para inicializar, auditar ou refatorar o código, obtenha-os **apenas** a partir dos arquivos presentes no próprio subdiretório do projeto local em que você está operando.

4. **Respeito às Permissões de Leitura/Escrita:**
   Caso tente ler qualquer arquivo fora do projeto ativo, aborte a ação imediatamente e reporte ao usuário que a leitura está fora do escopo definido.
