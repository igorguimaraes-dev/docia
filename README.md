# DocAI

**Plataforma de documentação técnica de repositórios com análise estática e inteligência artificial.**

O DocAI é um projeto de aprendizado e portfólio, construído progressivamente para transformar código-fonte em documentação técnica baseada em evidências. A proposta é receber um repositório público do GitHub, identificar suas tecnologias, extrair informações estruturadas e usar IA para auxiliar na geração da documentação.

> **Em desenvolvimento inicial.** Atualmente, o projeto possui uma API FastAPI com a rota `GET /health` e documentação interativa. A análise de repositórios, a geração de documentação e a integração com IA ainda não foram implementadas.

## Objetivo

Construir uma aplicação real enquanto são estudados backend, frontend, APIs, arquitetura, análise estática, testes, Git, Docker, segurança e integração com IA.

O desenvolvimento acontece em pequenos incrementos: entender o problema, implementar uma parte, validar o resultado e evoluir a estrutura conforme necessário.

## Princípio central

O DocAI não pretende enviar um repositório inteiro a um modelo de linguagem para que ele descubra tudo sozinho. A arquitetura planejada separa a extração de evidências da geração de texto:

```text
Código-fonte
    ↓
Análise determinística e estática
    ↓
Informações estruturadas
    ↓
Seleção de contexto
    ↓
Modelo de linguagem
    ↓
Documentação técnica
```

A análise determinística usará regras e leitura de arquivos para produzir resultados verificáveis. A IA será uma camada de interpretação e redação. Inferências, como possíveis regras de negócio, deverão ser diferenciadas de fatos extraídos do código.

## Estado atual

- [x] Ambiente virtual Python configurado localmente.
- [x] Dependências diretas e indiretas registradas em `backend/requirements.txt`.
- [x] Git inicializado e regras de exclusão para ambiente virtual e cache.
- [x] Aplicação FastAPI executada com Uvicorn.
- [x] Rota `GET /health` respondendo com HTTP 200.
- [x] Swagger UI disponível em `/docs`.
- [x] Teste automatizado de `/health` com pytest e TestClient.
- [x] Dependências de desenvolvimento registradas em `backend/requirements-dev.txt`.
- [ ] Recebimento e clonagem de repositórios públicos.
- [ ] Scanner de arquivos e detecção de tecnologias.
- [ ] Modelo intermediário e analisadores específicos.
- [ ] Geração de documentação e integração com IA.
- [ ] Interface web, upload ZIP, persistência e Docker.

Além das verificações manuais, o teste automatizado confere o status HTTP 200 e o corpo JSON de `/health`.

## Arquitetura planejada

```text
Frontend → URL pública do GitHub → Backend
                                    ↓
                             Clone do repositório
                                    ↓
                             Scanner de arquivos
                                    ↓
                          Detecção de tecnologias
                                    ↓
                       Analisadores de código estático
                                    ↓
                     Modelo intermediário: ProjectAnalysis
                                    ↓
                       Seleção de contexto → IA
                                    ↓
                         Documentação → Frontend
```

O upload de projetos ZIP será uma alternativa futura à entrada por URL.

### Descoberta de tecnologias

O sistema deverá identificar linguagens, frameworks, ferramentas de build e dependências a partir dos arquivos encontrados, como `pom.xml`, `build.gradle`, `package.json`, `requirements.txt`, `pyproject.toml`, `Dockerfile` e `docker-compose.yml`.

O primeiro laboratório previsto é um repositório público Spring Boot. O sistema deverá descobrir essa tecnologia pelas evidências do projeto, sem recebê-la como uma suposição prévia.

### Analisadores especializados

A organização conceitual dos analisadores é:

```text
analyzers/
├── generic/
├── java/
├── python/
├── javascript/
└── typescript/
```

Essa estrutura ainda não existe no código. A intenção é combinar uma análise genérica com implementações específicas, como `SpringBootAnalyzer`, `FastAPIAnalyzer` e `NestJSAnalyzer`.

O suporte será incremental. Entre as tecnologias consideradas estão Spring Boot, FastAPI, Django, Flask, Express e NestJS; nenhuma delas é analisada pelo sistema atualmente.

### Modelo intermediário

O modelo conceitual `ProjectAnalysis` deverá reunir informações de projetos diferentes em uma representação comum:

- Identificação do projeto, tecnologias, arquivos e módulos.
- Dependências, configurações e integrações externas.
- Rotas, endpoints, controllers, services e repositories.
- Models, entities, DTOs e relacionamentos.
- Evidências de regras de negócio, exceções e avisos da análise.

Nem toda tecnologia terá todos esses elementos. Campos, tipos e critérios de extração serão definidos durante a implementação. Essa representação permitirá que a geração de documentação use uma interface comum, independentemente da linguagem analisada.

## Tecnologias

| Área | Tecnologia | Situação |
| --- | --- | --- |
| Backend | Python 3.12, FastAPI e Uvicorn | Em uso |
| Validação e modelos | Pydantic | Instalado como dependência do FastAPI; modelos próprios ainda não implementados |
| Frontend | Next.js, React, TypeScript e Tailwind CSS | Planejado |
| IA | OpenAI API | Planejado |
| Testes | pytest, TestClient e HTTPX2 | Em uso |
| Infraestrutura | Docker e Docker Compose | Planejado |
| Persistência | PostgreSQL | Evolução futura |

## Estrutura atual

```text
docai/
├── .gitignore
├── README.md
└── backend/
    ├── main.py
    ├── requirements.txt
    ├── requirements-dev.txt
    └── tests/
        └── test_health.py
```

O arquivo `backend/main.py` cria a aplicação FastAPI e registra a rota de verificação. A pasta local `backend/.venv` é ignorada pelo Git e não é distribuída com o repositório.

## Como executar localmente

Os comandos abaixo usam **PowerShell no Windows**. O ambiente utilizado no desenvolvimento é Python 3.12.10.

Após obter o projeto, abra um terminal na pasta raiz `docai` e execute cada comando separadamente:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Se o ambiente `.venv` já estiver criado e as dependências instaladas, basta ativá-lo e executar o último comando. Caso o PowerShell bloqueie o script de ativação, é possível usar diretamente o interpretador do ambiente:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

O arquivo `backend/requirements.txt` registra as versões das dependências diretas e indiretas do backend. A instalação em um ambiente virtual novo, a consistência das dependências e a importação da aplicação foram verificadas no Windows com Python 3.12.10. Após essa verificação, o Starlette foi atualizado para 1.7.0; essa atualização foi validada no ambiente de desenvolvimento com `pip check` e o teste de `/health`. A configuração atual completa ainda não foi reinstalada em um ambiente vazio.

Mantenha o terminal aberto enquanto utiliza a API. A opção `--reload` recarrega a aplicação quando o código é alterado e é destinada ao desenvolvimento. Para parar o servidor, pressione `Ctrl+C`.

## Como verificar

Acesse [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health). A resposta esperada é HTTP **200 OK**, com o corpo:

```json
{"status": "ok"}
```

Essa rota verifica apenas se a aplicação consegue responder; ela não valida banco de dados, IA ou serviços externos.

A documentação interativa está em [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Expanda `GET /health`, clique em **Try it out** e depois em **Execute**. A descrição OpenAPI usada por essa interface está em `/openapi.json`.

Essa é a documentação da API do próprio DocAI. A geração de documentação dos repositórios analisados será desenvolvida posteriormente.

## Desenvolvimento e testes

Com o ambiente `backend/.venv` criado, execute os comandos abaixo **dentro da pasta `backend`**:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pytest tests/test_health.py -v
```

O arquivo `requirements-dev.txt` inclui `requirements.txt` e adiciona `pytest==9.1.1` e `httpx2==2.13.1`. As dependências indiretas exclusivas dessas ferramentas de teste ainda não estão fixadas. Os comandos usam diretamente o Python do ambiente do backend, sem depender de sua ativação no terminal.

O teste em `backend/tests/test_health.py` usa o TestClient para consultar a aplicação dentro do processo de teste, sem iniciar o Uvicorn nem abrir uma porta de rede. Ele verifica se `GET /health` retorna HTTP 200 e `{"status": "ok"}`.

O resultado esperado é `1 passed`. A execução local foi validada sem avisos após a adoção de HTTPX2 e a atualização do Starlette. Esse teste cobre apenas o comportamento da rota de verificação.

Para executar todos os testes da pasta:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -v
```

## Próximas etapas

1. Validar a configuração completa de desenvolvimento em um ambiente novo e ampliar os testes conforme as funcionalidades evoluírem.
2. Evoluir a organização do backend e a validação das entradas.
3. Receber URLs públicas do GitHub e obter repositórios com limites de segurança.
4. Implementar scanner, identificação de linguagens e detecção de tecnologias.
5. Definir `ProjectAnalysis` e implementar o primeiro analisador Spring Boot.
6. Extrair endpoints, DTOs, entidades, serviços e relacionamentos progressivamente.
7. Gerar documentação estruturada e integrar IA com seleção de contexto.
8. Criar a interface web para solicitar análises e visualizar resultados.
9. Adicionar upload ZIP, persistência e execução com Docker.

Testes, tratamento de erros, logging, configuração e documentação acompanharão a evolução das funcionalidades.

## Segurança planejada

O recebimento de código externo exigirá medidas específicas, que ainda não estão implementadas:

- Não executar automaticamente código, scripts de instalação ou builds dos repositórios analisados.
- Validar URLs e evitar command injection na interação com ferramentas externas.
- Controlar caminhos, symlinks e extração de ZIP para evitar path traversal e ZIP Slip.
- Limitar tamanho, quantidade de arquivos, tempo de processamento e consumo de recursos.
- Tratar arquivos binários e conteúdos maliciosos como entradas não confiáveis.
- Reduzir a exposição de segredos em logs, documentação e contexto enviado à IA.
- Isolar o armazenamento temporário e limpar os arquivos após a análise.

## Aprendizado e evolução

O projeto prioriza incrementos pequenos, código compreensível e validação antes de avançar. Separação de responsabilidades, tipagem, design de APIs e princípios de arquitetura serão aplicados conforme resolverem necessidades concretas do sistema.
