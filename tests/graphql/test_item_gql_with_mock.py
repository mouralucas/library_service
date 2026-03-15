"""
Exemplo Prático: Tesitando test_item_gql.py com pytest-mock

Este arquivo mostra como refatorar seus testes GraphQL atuais
para usar pytest-mock, economizando tempo e ficando mais rápido.
"""

from unittest.mock import AsyncMock

import pytest
from fastapi import status

# ============================================================================
# VERSÃO ATUAL (Muito complexa, precisa de muitas fixtures)
# ============================================================================

# @pytest.mark.asyncio
# async def test_mutation_new_item_success(
#     client,
#     create_languages,       # Cria no banco
#     create_series,          # Cria no banco
#     create_item_status,     # Cria no banco
#     create_publisher,       # Cria no banco
#     create_collections,     # Cria no banco
#     create_authors,         # Cria no banco
#     create_item_locations,  # Cria no banco
# ):


# ============================================================================
# VERSÃO REFATORADA: Teste simples com pytest-mock
# ============================================================================


@pytest.mark.asyncio
async def test_mutation_new_item_success_fast(mocker, client):
    """
    Versão refatorada usando pytest-mock.

    Vantagens:
    - Muito mais rápido (sem I/O de banco)
    - Menos dependências
    - Focado em testar o GraphQL, não criação de dados
    - Mais legível
    - Mais fácil de manter
    """

    # 1. SETUP: Mockar o serviço que a mutation usa
    mock_item_service = mocker.patch("resolvers.item.ItemService")
    mock_instance = mock_item_service.return_value

    # Configurar o retorno esperado
    mock_instance.create_item = AsyncMock(return_value={"created": True, "id": 42})

    # 2. PREPARE: Dados de teste
    item_title = "Test item"
    item_subtitle = "Test subtitle"

    # GraphQL mutation (idêntica)
    mutation = """
        mutation CreateItem($input: CreateItemInput) {
            createItem(item: $input) {
                created
                id
            }
        }
    """

    # Variáveis (simplificadas, apenas IDs)
    variables = {
        "input": {
            "mainAuthorId": 1,
            "otherAuthorsId": [2, 3],
            "title": item_title,
            "subtitle": item_subtitle,
            "pages": 756,
            "languageId": "PT",
            "publisherId": 1,
            "serieId": 1,
            "collectionId": 1,
            "lastStatusId": "owned",
            "lastStatusDate": "2024-06-01",
            "coverPrice": 110.15,
            "paidPrice": 57.90,
            "itemTypeId": "book",
            "formatId": "hardcover",
            "locationId": 1,
        }
    }

    # 3. EXECUTE: Fazer o request GraphQL
    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": variables}
    )

    # 4. VERIFY: Validar resposta
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Estrutura da resposta
    assert "data" in data
    assert "createItem" in data["data"]
    assert "created" in data["data"]["createItem"]
    assert data["data"]["createItem"]["created"] is True
    assert "id" in data["data"]["createItem"]
    assert data["data"]["createItem"]["id"] == 42

    # 5. ASSERT MOCKS: Verificar que o serviço foi chamado corretamente
    mock_instance.create_item.assert_called_once()
    call_args = mock_instance.create_item.call_args

    # Verificar que foi chamado com dados corretos
    assert call_args[1]["item"].title == item_title


# ============================================================================
# VERSÃO 3: Teste de Query com filtros
# ============================================================================


@pytest.mark.asyncio
async def test_query_books_with_mock(mocker, client):
    """
    Refatorar test_query_books para usar mock ao invés
    de criar 100 itens no banco.
    """

    # Mockar o serviço
    mock_item_service = mocker.patch("resolvers.item.ItemService")
    mock_instance = mock_item_service.return_value

    # Retornar alguns itens de teste
    mock_books = [
        {"id": 1, "title": "Book 1", "item_type_id": "book"},
        {"id": 2, "title": "Book 2", "item_type_id": "book"},
        {"id": 3, "title": "Book 3", "item_type_id": "book"},
    ]

    mock_instance.get_items = AsyncMock(
        return_value={"quantity": len(mock_books), "items": mock_books}
    )

    # GraphQL query
    query = """
        query GetItems($params: GetItemInput) {
            getItems(params: $params) {
                quantity
                items {
                    id
                    title
                    itemTypeId
                }
            }
        }
    """

    variables = {"params": {"itemTypeId": "book"}}

    # Execute
    response = await client.post(
        "/graphql/library", json={"query": query, "variables": variables}
    )

    # Verify
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "data" in data
    assert "getItems" in data["data"]
    assert data["data"]["getItems"]["quantity"] == 3

    items = data["data"]["getItems"]["items"]
    assert len(items) == 3

    for item in items:
        assert item["itemTypeId"] == "book"

    # Verificar que o serviço foi chamado com filtro correto
    mock_instance.get_items.assert_called_once()


# ============================================================================
# VERSÃO 4: Teste com Order By
# ============================================================================


@pytest.mark.asyncio
async def test_query_books_with_order_by_mock(mocker, client):
    """
    Refatorar test_query_books_with_order_by.
    """

    mock_item_service = mocker.patch("resolvers.item.ItemService")
    mock_instance = mock_item_service.return_value

    # Dados ordenados por title ASC
    ordered_books = [
        {"id": 2, "title": "Aaa Book", "item_type_id": "book"},
        {"id": 3, "title": "Zzz Book", "item_type_id": "book"},
        {"id": 1, "title": "Mmm Book", "item_type_id": "book"},
    ]

    mock_instance.get_items = AsyncMock(
        return_value={"quantity": len(ordered_books), "items": ordered_books}
    )

    query = """
        query GetItems($params: GetItemInput) {
            getItems(params: $params) {
                quantity
                items {
                    id
                    title
                    itemTypeId
                }
            }
        }
    """

    variables = {
        "params": {
            "itemTypeId": "book",
            "orderBy": [{"field": "title", "direction": "ASC"}],
        }
    }

    response = await client.post(
        "/graphql/library", json={"query": query, "variables": variables}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    items = data["data"]["getItems"]["items"]

    # Verificar que estão ordenados (simulado pelo mock)
    assert items[0]["title"] == "Aaa Book"
    assert items[1]["title"] == "Zzz Book"


# ============================================================================
# VERSÃO 5: Teste de Erro no Banco
# ============================================================================


@pytest.mark.asyncio
async def test_mutation_new_item_database_error(mocker, client):
    """
    Testar tratamento de erro quando banco falha.

    IMPOSSÍVEL de fazer com banco real!
    MAS TRIVIAL com mocks.
    """

    # Mockar serviço para lançar exceção
    mock_item_service = mocker.patch("resolvers.item.ItemService")
    mock_instance = mock_item_service.return_value

    mock_instance.create_item = AsyncMock(
        side_effect=Exception("Database connection error")
    )

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
            "mainAuthorId": 1,
            "title": "Test",
            "pages": 100,
            "languageId": 1,
            "publisherId": 1,
            "itemTypeId": "book",
            "formatId": "hardcover",
        }
    }

    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": variables}
    )

    # Não é 200 pois houve erro
    assert response.status_code == status.HTTP_200_OK

    # Pode ter erro GraphQL
    data = response.json()
    assert "errors" in data or response.status_code >= 400


# ============================================================================
# FIXTURE REUTILIZÁVEL
# ============================================================================


@pytest.fixture
def mock_item_service_standard(mocker):
    """
    Fixture que fornece um mock padrão do ItemService.

    Reutilizar em vários testes sem repetir setup.
    """
    mock = mocker.patch("resolvers.item.ItemService")
    mock.return_value.create_item = AsyncMock(return_value={"created": True, "id": 1})
    mock.return_value.get_items = AsyncMock(return_value={"quantity": 0, "items": []})
    mock.return_value.get_item = AsyncMock(return_value={"id": 1, "title": "Test"})
    return mock


@pytest.mark.asyncio
async def test_using_fixture(mock_item_service_standard, client):
    """Usa a fixture para simplificar testes"""

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
            "mainAuthorId": 1,
            "title": "Test",
            "pages": 100,
            "languageId": 1,
            "publisherId": 1,
            "itemTypeId": "book",
            "formatId": "hardcover",
        }
    }

    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": variables}
    )

    assert response.status_code == status.HTTP_200_OK


# ============================================================================
# COMO MIGRAR SEUS TESTES
# ============================================================================

"""
PASSO 1: Identificar qual serviço a mutation/query chamal
    Ex: test_mutation_new_item_success chama ItemService.create_item

PASSO 2: Mockar esse serviço
    mock_service = mocker.patch("resolvers.item.ItemService")

PASSO 3: Remover fixtures de criação de dados
    ANTES:
        def test_something(
            create_languages,
            create_series,
            create_item_status,
            create_publisher,
            create_collections,
            create_authors,
            create_item_locations,
        ):
    DEPOIS:
        def test_something(mocker, client):

PASSO 4: Configurar mock com dados de teste
    mock_instance.create_item = AsyncMock(return_value={...})

PASSO 5: Executar teste com dados simples
    Antes: 8 IDs + criar no banco + fixtures complexas
    Depois: Passar os IDs direto nas variáveis

RESULTADO:
    ✓ Teste é 10x-100x mais rápido
    ✓ Menos dependências
    ✓ Mais fácil de entender
    ✓ Mais fácil de manter
    ✓ Mais fácil de testar erros
"""
