"""
Exemplo prático: Refatorar testes existentes para usar pytest-mock.

Este arquivo mostra:
1. Como um teste ANTES (com database real) se parece
2. Como refatorar para usar pytest-mock
3. As vantagens de cada abordagem
"""

import pytest
from fastapi import status


# ============================================================================
# VERSÃO 1: Teste usando banco de dados real (abordagem atual)
# ============================================================================
@pytest.mark.asyncio
async def test_mutation_new_item_success_with_real_db(
    client,
    create_languages,
    create_series,
    create_item_status,
    create_publisher,
    create_collections,
    create_authors,
    create_item_locations,
):
    """
    VANTAGENS:
    - Testa a integração completa
    - Detecta problemas reais de banco de dados
    - Valida migrations e schemas

    DESVANTAGENS:
    - Lento (cria e destrói dados em DB)
    - Frágil (depende de fixtures complexas)
    - Difícil de testar casos extremos
    - Difícil de testar comportamentos de erro
    """
    item_title = "Test item"
    item_subtitle = "Test subtitle"

    mutation = """
        mutation CreateItem($input: CreateItemInput) {
            createItem(item: $input) {
                created
                id
            }
        }
    """

    variables = {
        "input": {
            "mainAuthorId": create_authors[0].id,
            "otherAuthorsId": [create_authors[1].id, create_authors[2].id],
            "title": item_title,
            "subtitle": item_subtitle,
            "pages": 756,
            "languageId": create_languages[0].id,
            "publisherId": create_publisher[0].id,
            "serieId": create_series[0].id,
            "collectionId": create_collections[0].id,
            "lastStatusId": create_item_status[0].id,
            "lastStatusDate": "2024-06-01",
            "coverPrice": 110.15,
            "paidPrice": 57.90,
            "itemTypeId": "book",
            "formatId": "hardcover",
            "locationId": create_item_locations[0].id,
        }
    }

    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": variables}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["data"]["createItem"]["created"] is True


# ============================================================================
# BOAS PRÁTICAS
# ============================================================================

"""
QUANDO USAR CADA ABORDAGEM:

1. BANCO REAL (use as fixtures existentes):
   - Testes de integração completa
   - Testes de migrations SQLAlchemy
   - Testes de constraints do banco
   - Casos importantes de negócio que precisam de validação real

2. MOCKS COM PYTEST-MOCK:
   - Testes unitários de services/managers
   - Testes de resolvers GraphQL (apenas lógica)
   - Testes de tratamento de erro
   - Testes de validação de inputs
   - Testes rápidos e isolados

3. HYBRID (combinar ambos):
   - Um ou dois testes com DB real para integração
   - Foco em testes com mocks para cobertura rápida
   - Balance entre segurança e velocidade

DICAS:

1. Use fixtures do conftest.py para testes de integração
   @pytest.mark.asyncio
   async def test_with_db(create_test_session):
       # Usa banco real

2. Use pytest-mock para testes unitários
   @pytest.mark.asyncio
   async def test_isolated(mocker):
       # Usa mocks

3. Mocke no nível mais próximo do que você está testando
   - Testando resolver? Mocke o serviço
   - Testando serviço? Mocke a sessão
   - Testando manager? Mocke a sessão

4. Use AsyncMock para métodos async
   mock_method = AsyncMock(return_value=...)

5. Use side_effect para casos múltiplos
   mock_method = AsyncMock(side_effect=[value1, value2, Exception(...)])

6. Use mock.assert_called_once(), assert_called_with(), etc.
   para verificar comportamento

7. Organize mocks em fixtures reutilizáveis
   @pytest.fixture
   def mock_database(mocker):
       return mocker.patch("backend.database.get_session")
"""
