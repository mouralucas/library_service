"""
README: Usando pytest-mock no projeto library_service

Este guia mostra como usar pytest-mock para mockar o banco de dados nos testes
do projeto library_service.

CONTEÚDO:
  1. O que foi instalado
  2. Arquivos de referência
  3. Como usar
  4. Exemplos práticos
"""

# ============================================================================
# 1. O QUE FOI INSTALADO
# ============================================================================

"""
✓ pytest-mock==3.14.0 foi instalado no seu ambiente virtual

Verificar instalação:
    pip list | grep pytest-mock
    
Ou no projeto:
    python -m pip list | grep pytest-mock
"""


# ============================================================================
# 2. ARQUIVOS DE REFERÊNCIA CRIADOS
# ============================================================================

"""
tests/test_mocking_database.py
    └─ 10 exemplos completos de uso de pytest-mock
    └─ Desde básico até avançado
    └─ Tópicos:
       - Mockar métodos de serviço
       - Mockar sessão do banco
       - Múltiplos mocks
       - Side effects
       - Monitoramento com spy
       - Parametrização

tests/test_mock_examples.py
    └─ Comparação antes/depois de refatoração
    └─ Versão 1: Usando banco real (atual)
    └─ Versão 2-6: Refatorado com pytest-mock
    └─ Mostra vantagens/desvantagens de cada abordagem
    └─ Boas práticas

tests/conftest_mock_fixtures.py
    └─ Fixtures reutilizáveis pronta para usar
    └─ mock_db_session
    └─ mock_get_session
    └─ mock_exec_query
    └─ mock_service_factory
    └─ mock_all_services
    └─ mock_manager_factory
    └─ E muito mais...

PYTEST_MOCK_GUIDE.md
    └─ 15 seções com referência rápida
    └─ Cheat sheet para consulta rápida
    └─ Resolução de problemas comuns
    └─ Snippets copiáveis
"""


# ============================================================================
# 3. COMO COMEÇAR (Quick Start)
# ============================================================================

"""
OPÇÃO 1: Usar em um teste novo

    import pytest
    from unittest.mock import AsyncMock
    
    @pytest.mark.asyncio
    async def test_get_items(mocker):
        # Criar um mock
        mock_service = mocker.patch("services.item.ItemService")
        mock_service.return_value.get_items = AsyncMock(return_value=[])
        
        # Seu teste aqui
        # ...
        
        # Verificar
        mock_service.return_value.get_items.assert_called_once()


OPÇÃO 2: Refatorar um teste existente

    Arquivo: tests/graphql/test_item_gql.py
    
    # ANTES (usa banco real):
    @pytest.mark.asyncio
    async def test_mutation_new_item_success(
        client,
        create_languages,  # Cria no banco
        create_series,     # Cria no banco
        # ... muitos mais fixtures
    ):
        # ... código que depende de todas essas fixtures
    
    # DEPOIS (usa mocks):
    @pytest.mark.asyncio
    async def test_mutation_new_item_success_fast(mocker, client):
        # Mockar os serviços que a mutation usa
        mock_item_service = mocker.patch("resolvers.item.ItemService")
        mock_item_service.return_value.create_item = AsyncMock(
            return_value={"created": True, "id": 42}
        )
        
        # Restante do teste idêntico
        mutation = \"\"\"...\"\"\"
        variables = {...}
        response = await client.post("/graphql/library", ...)
        assert response.status_code == 200


OPÇÃO 3: Adicionar fixtures reutilizáveis

    Copie o conteúdo de tests/conftest_mock_fixtures.py para seu conftest.py
    ou import dele:
    
    # Em conftest.py:
    from tests.conftest_mock_fixtures import *  # noqa: F403
    
    # Agora em qualquer teste:
    @pytest.mark.asyncio
    async def test_something(mock_db_session):
        # mock_db_session já pronto
        mock_db_session.exec.return_value.all.return_value = [...]
"""


# ============================================================================
# 4. EXEMPLOS PRÁTICOS PARA SEU PROJETO
# ============================================================================

"""
EXEMPLO 1: Mockar ItemService para teste GraphQL

    @pytest.mark.asyncio
    async def test_create_item_resolver(mocker, client):
        mock_item_service = mocker.patch("resolvers.item.ItemService")
        mock_instance = mock_item_service.return_value
        
        # Configurar o retorno
        mock_instance.create_item = AsyncMock(return_value={
            "created": True,
            "id": 123
        })
        
        # GraphQL mutation
        mutation = '''
            mutation CreateItem($input: CreateItemInput) {
                createItem(item: $input) {
                    created
                    id
                }
            }
        '''
        
        # Executar
        response = await client.post(
            "/graphql/library",
            json={"query": mutation, "variables": {"input": {...}}}
        )
        
        # Verificar
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["createItem"]["created"] is True
        mock_instance.create_item.assert_called_once()


EXEMPLO 2: Mockar múltiplos serviços

    @pytest.mark.asyncio
    async def test_complex_resolver(mocker, client):
        # Mockar 3 serviços diferentes
        item_service = mocker.patch("resolvers.item.ItemService")
        author_service = mocker.patch("resolvers.item.AuthorService")
        publisher_service = mocker.patch("resolvers.item.PublisherService")
        
        # Configurar comportamentos
        item_service.return_value.get_items = AsyncMock(return_value=[...])
        author_service.return_value.get_author = AsyncMock(return_value={...})
        publisher_service.return_value.get_publisher = AsyncMock(return_value={...})
        
        # Seu teste aqui
        # ...


EXEMPLO 3: Mockar conexão com banco com erro

    @pytest.mark.asyncio
    async def test_handles_database_error(mocker):
        mock_session = AsyncMock()
        mock_session.exec.side_effect = Exception("Connection refused")
        
        mocker.patch("backend.database.get_session", return_value=mock_session)
        
        # Seu código deve tratar o erro
        with pytest.raises(Exception, match="Connection refused"):
            # ... código que tenta acessar banco
            pass


EXEMPLO 4: Mockar com Fixture parametrizada

    @pytest.fixture
    def mock_item_service_scenarios(mocker):
        return {
            "empty": mocker.patch(
                "services.item.ItemService",
                return_value=AsyncMock(get_items=AsyncMock(return_value=[]))
            ),
            "one_item": mocker.patch(
                "services.item.ItemService",
                return_value=AsyncMock(
                    get_items=AsyncMock(return_value=[{"id": 1}])
                )
            ),
            "error": mocker.patch(
                "services.item.ItemService",
                return_value=AsyncMock(
                    get_items=AsyncMock(side_effect=Exception("DB Error"))
                )
            ),
        }
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("scenario", ["empty", "one_item", "error"])
    async def test_scenarios(mock_item_service_scenarios, scenario):
        service = mock_item_service_scenarios[scenario]
        # Testar cada cenário
"""


# ============================================================================
# 5. ESTRUTURA RECOMENDADA DE TESTES
# ============================================================================

"""
Organize seus testes em 3. camadas:

┌─────────────────────────────────────────────────────────────┐
│ Testes de Integração (poucos, com banco real)               │
│ - tests/integration/test_full_flow.py                       │
│ - Usa fixtures create_test_session                          │
│ - Testa casos críticos completos                            │
│ - Mais lentos mas encontram bugs reais                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Testes de Componentes (muitos, com mocks parciais)          │
│ - tests/graphql/test_*_gql.py (refatorados)                │
│ - Testes de resolvers GraphQL                              │
│ - Mocka serviços, usa sessão real                           │
│ - Velocidade média                                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Testes Unitários (muitos, com mocks totais)                 │
│ - tests/unit/test_*_service.py (novos)                     │
│ - Testes de serviços isolados                              │
│ - Mocka banco de dados completamente                        │
│ - Muito rápidos                                             │
│ - Máxima cobertura de código                                │
└─────────────────────────────────────────────────────────────┘
"""


# ============================================================================
# 6. CASOS DE USO COMUNS
# ============================================================================

"""
Caso 1: Teste de validação GraphQL
    → Use mocks, não precisa banco real
    → Mockar serviço que a mutation chama

Caso 2: Teste de tratamento de erro
    → Use mocks com side_effect para simular erro
    → Impossível com banco real de forma controlada

Caso 3: Teste de performance
    → Use mocks, muito mais rápido
    → Testa lógica sem I/O

Caso 4: Teste de fluxo completo
    → Use banco real (fixture create_test_session)
    → Garante que tudo funciona junto

Caso 5: Teste de mutations GraphQL
    → Opção 1: Bancso real (atual, lento)
    → Opção 2: Mockar serviço (rápido, apenas validar input)
    → Recomendação: Testar entrada/saída com mocks,
                     fluxo crítico com banco real
"""


# ============================================================================
# 7. PRÓXIMOS PASSOS
# ============================================================================

"""
1. Leia os arquivos:
   - tests/test_mocking_database.py (10 exemplos)
   - tests/test_mock_examples.py (comparações)
   - PYTEST_MOCK_GUIDE.md (referência)

2. Escolha um teste para refatorar:
   - Comece com algo simples
   - ex: um teste GraphQL

3. Adicione as fixtures:
   - Copie de conftest_mock_fixtures.py
   - Ou import desse arquivo

4. Aumente cobertura:
   - Escreva testes unitários para serviços
   - Combine com testes de integração existentes

5. Configure CI/CD:
   - Teste rápido com mocks no PR
   - Teste completo com banco em merge
"""


# ============================================================================
# 8. TROUBLESHOOTING
# ============================================================================

"""
Problema: "ModuleNotFoundError" ao mockar

    mocker.patch("wrong.path.Service")
    
Solução:
    - Use o caminho real de import: "services.item.ItemService"
    - Ou "resolvers.item.ItemService" se vem de resolver

Problema: Mock não está sendo usado

    mock = mocker.patch("services.item.ItemService")
    # ... mas código ainda chama banco real
    
Solução:
    - Verificar se o import está correto
    - Mockar no módulo que usa, não onde é definido
    - mocker.patch("MODULO_QUE_IMPORTA.ItemService")

Problema: Async mock não funciona

    mock = mocker.patch("module.async_func", return_value=42)
    result = await async_func()  # TypeError!
    
Solução:
    - Use AsyncMock para funções async:
    from unittest.mock import AsyncMock
    mock = AsyncMock(return_value=42)

Problema: Session não está mockada

    Solução: Mockar "backend.database.get_session"
    mocker.patch("backend.database.get_session", return_value=mock_session)

Problema: Querys SQL não funcionam com mock

    Solução: Configure return_value manualmente
    mock_session.exec.return_value.all.return_value = [item1, item2]
"""


# ============================================================================
# 9. DOCUMENTAÇÃO OFICIAL
# ============================================================================

"""
- pytest-mock docs: https://pytest-mock.readthedocs.io/
- unittest.mock docs: https://docs.python.org/3/library/unittest.mock.html
- AsyncMock: https://docs.python.org/3/library/unittest.mock.html#asyncmock
"""
