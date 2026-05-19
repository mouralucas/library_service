"""
Tests para os endpoints de metas de leitura (Reading Goals)
"""

from unittest.mock import AsyncMock

import pytest
from fastapi import status

# ============================================================================
# TESTES COM MOCKS - Recomendado para testes mais rápidos e isolados
# ============================================================================


@pytest.mark.asyncio
async def test_create_reading_goal_success(mocker, client, create_item):
    """
    Testa criação bem-sucedida de uma meta de leitura.

    Fluxo esperado:
    - Usuário cria uma meta de leitura para um item em um ano específico
    - Deve retornar created=True e reading_goal_id válido
    """
    # Mock do serviço
    mock_reading_service = mocker.patch("resolvers.reading.ReadingService")
    mock_instance = mock_reading_service.return_value

    mock_instance.update_reading_queue = AsyncMock(
        return_value={
            "created": True,
            "reading_goal_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        }
    )

    # Dados de teste
    item_id = create_item[0].id
    year = 2025

    mutation = """
        mutation UpdateReadingQueue($input: UpdateReadingQueueInput!) {
            updateReadingQueue(goal: $input) {
                created
                readingGoalId
            }
        }
    """

    variables = {
        "input": {
            "itemId": item_id,
            "year": year,
        }
    }

    # Executar
    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": variables}
    )

    # Validar
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "data" in data
    assert "updateReadingQueue" in data["data"]
    assert data["data"]["updateReadingQueue"]["created"] is True
    assert "readingGoalId" in data["data"]["updateReadingQueue"]

    # Verificar que o serviço foi chamado corretamente
    mock_instance.update_reading_queue.assert_called_once()


@pytest.mark.asyncio
async def test_create_reading_goal_already_exists(mocker, client, create_item):
    """
    Testa erro quando tenta criar uma meta para um item que já tem meta ativa.

    Fluxo esperado:
    - Sistema deve retornar erro 412 (Precondition Failed)
    - Mensagem: "Já existe uma meta ativa para esse item!"
    """
    mock_reading_service = mocker.patch("resolvers.reading.ReadingService")
    mock_instance = mock_reading_service.return_value

    # Simular erro do serviço
    from fastapi import HTTPException

    mock_instance.update_reading_queue = AsyncMock(
        side_effect=HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Já existe uma meta ativa para esse item!",
        )
    )

    item_id = create_item[0].id
    year = 2025

    mutation = """
        mutation UpdateReadingQueue($input: UpdateReadingQueueInput!) {
            updateReadingQueue(goal: $input) {
                created
                readingGoalId
            }
        }
    """

    variables = {
        "input": {
            "itemId": item_id,
            "year": year,
        }
    }

    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": variables}
    )

    # Para GraphQL, mesmo sendo erro, retorna 200
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Deve conter mensagem de erro
    assert "errors" in data


@pytest.mark.asyncio
async def test_get_reading_goals_success(mocker, client, create_item):
    """
    Testa busca bem-sucedida de metas de leitura.

    Fluxo esperado:
    - Retorna lista de metas de leitura
    - Cada meta contém: id, item (completo), year, achieved, dateAchieved
    """
    mock_reading_service = mocker.patch("resolvers.reading.ReadingService")
    mock_instance = mock_reading_service.return_value

    # Mock de metas de leitura
    mock_goals = [
        {
            "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "item_id": create_item[0].id,
            "year": 2025,
            "achieved": False,
            "date_achieved": None,
            "item": {
                "id": create_item[0].id,
                "title": create_item[0].title,
            },
        },
        {
            "id": "f47ac10b-58cc-4372-a567-0e02b2c3d480",
            "item_id": create_item[1].id,
            "year": 2025,
            "achieved": True,
            "date_achieved": "2025-12-31",
            "item": {
                "id": create_item[1].id,
                "title": create_item[1].title,
            },
        },
    ]

    mock_instance.get_reading_queue = AsyncMock(return_value={"goals": mock_goals})

    query = """
        query GetReadingQueue($params: GetReadingQueueInput) {
            getReadingQueue(params: $params) {
                goals {
                    id
                    year
                    achieved
                    dateAchieved
                    item {
                        id
                        title
                    }
                }
            }
        }
    """

    variables = {"params": {"year": 2025}}

    response = await client.post(
        "/graphql/library", json={"query": query, "variables": variables}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "data" in data
    assert "getReadingQueue" in data["data"]
    assert "goals" in data["data"]["getReadingQueue"]

    goals = data["data"]["getReadingQueue"]["goals"]
    assert len(goals) == 2

    # Validar estrutura de cada meta
    for goal in goals:
        assert "id" in goal
        assert "year" in goal
        assert "achieved" in goal
        assert "dateAchieved" in goal
        assert "item" in goal

    mock_instance.get_reading_queue.assert_called_once()


@pytest.mark.asyncio
async def test_get_reading_goals_empty(mocker, client):
    """
    Testa busca de metas quando não existem metas.

    Fluxo esperado:
    - Retorna lista vazia
    """
    mock_reading_service = mocker.patch("resolvers.reading.ReadingService")
    mock_instance = mock_reading_service.return_value

    mock_instance.get_reading_queue = AsyncMock(return_value={"goals": []})

    query = """
        query GetReadingQueue($params: GetReadingQueueInput) {
            getReadingQueue(params: $params) {
                goals {
                    id
                    year
                    achieved
                }
            }
        }
    """

    variables = {"params": {"year": 2025}}

    response = await client.post(
        "/graphql/library", json={"query": query, "variables": variables}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "data" in data
    assert "getReadingQueue" in data["data"]

    goals = data["data"]["getReadingQueue"]["goals"]
    assert len(goals) == 0


@pytest.mark.asyncio
async def test_get_reading_goals_by_year(mocker, client, create_item):
    """
    Testa filtro de metas por ano.

    Fluxo esperado:
    - Retorna apenas metas do ano especificado
    """
    mock_reading_service = mocker.patch("resolvers.reading.ReadingService")
    mock_instance = mock_reading_service.return_value

    mock_goals_2025 = [
        {
            "id": "goal-2025-1",
            "item_id": create_item[0].id,
            "year": 2025,
            "achieved": False,
            "date_achieved": None,
            "item": {"id": create_item[0].id, "title": create_item[0].title},
        },
    ]

    mock_instance.get_reading_queue = AsyncMock(return_value={"goals": mock_goals_2025})

    query = """
        query GetReadingQueue($params: GetReadingQueueInput) {
            getReadingQueue(params: $params) {
                goals {
                    year
                }
            }
        }
    """

    variables = {"params": {"year": 2025}}

    response = await client.post(
        "/graphql/library", json={"query": query, "variables": variables}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    goals = data["data"]["getReadingQueue"]["goals"]
    assert len(goals) == 1
    assert goals[0]["year"] == 2025


@pytest.mark.asyncio
async def test_get_reading_goals_without_year_filter(mocker, client, create_item):
    """
    Testa busca de todas as metas sem filtro de ano.

    Fluxo esperado:
    - Retorna metas de todos os anos
    """
    mock_reading_service = mocker.patch("resolvers.reading.ReadingService")
    mock_instance = mock_reading_service.return_value

    mock_goals_all_years = [
        {
            "id": "goal-2024-1",
            "item_id": create_item[0].id,
            "year": 2024,
            "achieved": True,
            "date_achieved": "2024-12-31",
            "item": {"id": create_item[0].id, "title": create_item[0].title},
        },
        {
            "id": "goal-2025-1",
            "item_id": create_item[1].id,
            "year": 2025,
            "achieved": False,
            "date_achieved": None,
            "item": {"id": create_item[1].id, "title": create_item[1].title},
        },
    ]

    mock_instance.get_reading_queue = AsyncMock(
        return_value={"goals": mock_goals_all_years}
    )

    query = """
        query GetReadingQueue($params: GetReadingQueueInput) {
            getReadingQueue(params: $params) {
                goals {
                    year
                }
            }
        }
    """

    # Sem params ou year = None
    variables = {"params": {}}

    response = await client.post(
        "/graphql/library", json={"query": query, "variables": variables}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    goals = data["data"]["getReadingQueue"]["goals"]
    assert len(goals) == 2

    years = [goal["year"] for goal in goals]
    assert 2024 in years
    assert 2025 in years


# ============================================================================
# TESTES DE VALIDAÇÃO - Testes dos validadores de input
# ============================================================================


@pytest.mark.asyncio
async def test_create_reading_goal_invalid_item_id(mocker, client):
    """
    Testa erro ao passar item_id inválido.

    Fluxo esperado:
    - Retorna erro de validação GraphQL
    """
    mock_reading_service = mocker.patch("resolvers.reading.ReadingService")
    mock_instance = mock_reading_service.return_value
    mock_instance.create_goal = AsyncMock()

    mutation = """
        mutation UpdateReadingQueue($input: UpdateReadingQueueInput!) {
            updateReadingQueue(goal: $input) {
                created
                readingGoalId
            }
        }
    """

    variables = {
        "input": {
            "itemId": "invalid",  # Inválido - deve ser Int
            "year": 2025,
        }
    }

    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": variables}
    )

    # GraphQL valida tipos, retorna 200 com erros
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Deve ter erro de validação
    assert "errors" in data


@pytest.mark.asyncio
async def test_create_reading_goal_missing_required_fields(mocker, client):
    """
    Testa erro ao não passar campos obrigatórios.

    Fluxo esperado:
    - Retorna erro de validação GraphQL (campos obrigatórios)
    """
    mock_reading_service = mocker.patch("resolvers.reading.ReadingService")
    mock_instance = mock_reading_service.return_value
    mock_instance.create_goal = AsyncMock()

    mutation = """
        mutation UpdateReadingQueue($input: UpdateReadingQueueInput!) {
            updateReadingQueue(goal: $input) {
                created
                readingGoalId
            }
        }
    """

    # Sem year (obrigatório)
    variables = {
        "input": {
            "itemId": 1,
        }
    }

    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": variables}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Deve ter erro de validação
    assert "errors" in data
