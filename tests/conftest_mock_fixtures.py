"""
Fixtures reutilizáveis com pytest-mock para mockar banco de dados.

Copie estas fixtures para seu conftest.py ou import deste arquivo
para usar em seus testes.

Exemplo de uso:
    @pytest.mark.asyncio
    async def test_something(mock_db_session):
        # mock_db_session já está pronto para usar
        mock_db_session.exec.return_value.all.return_value = [...]
"""

from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def mock_db_session(mocker):
    """
    Fornece uma sessão de banco de dados completamente mockada.

    Útil para testes unitários que não precisam de um banco real.

    Exemplo:
        @pytest.mark.asyncio
        async def test_with_mock(mock_db_session):
            mock_db_session.exec.return_value.all.return_value = [item1, item2]
    """
    session = AsyncMock()

    # Configurar métodos comuns do SQLAlchemy
    session.exec = AsyncMock()
    session.add = AsyncMock()
    session.delete = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.refresh = AsyncMock()
    session.close = AsyncMock()

    return session


@pytest.fixture
def mock_get_session(mocker, mock_db_session):
    """
    Mocka a função get_session globalmente.

    Qualquer código que injetar get_session() receberá o mock.

    Exemplo:
        @pytest.mark.asyncio
        async def test_with_injected_mock(mock_get_session):
            # Agora get_session() retorno o mock
            session = get_session()
            assert isinstance(session, AsyncMock)
    """
    return mocker.patch("backend.database.get_session", return_value=mock_db_session)


@pytest.fixture
def mock_exec_query(mock_db_session):
    """
    Helper para configurar facilmente queries exec.

    Exemplo:
        @pytest.mark.asyncio
        async def test_query(mock_db_session, mock_exec_query):
            mock_exec_query([item1, item2], method="all")
            items = await session.exec(select(ItemModel)).all()
    """

    def configure_query(result=None, method="all", **kwargs):
        """
        result: O que retornar (lista, objeto, etc)
        method: "all", "first", "one", etc
        """
        if method == "all":
            mock_db_session.exec.return_value.all.return_value = result or []
        elif method == "first":
            mock_db_session.exec.return_value.first.return_value = result
        elif method == "one":
            mock_db_session.exec.return_value.one.return_value = result
        elif method == "scalars":
            mock_db_session.exec.return_value.scalars.return_value = result or []

        return mock_db_session

    return configure_query


@pytest.fixture
def mock_transaction(mocker):
    """
    Mocka uma transação SQLAlchemy para testes de commit/rollback.

    Exemplo:
        @pytest.mark.asyncio
        async def test_transaction(mock_transaction):
            async with mock_transaction as tx:
                await tx.execute(...)
                # Em caso de erro, testa rollback
    """
    tx = AsyncMock()
    tx.execute = AsyncMock()
    tx.commit = AsyncMock()
    tx.rollback = AsyncMock()

    return tx


@pytest.fixture
def mock_service_factory(mocker, mock_db_session):
    """
    Factory para criar serviços mockados facilmente.

    Exemplo:
        @pytest.mark.asyncio
        async def test_with_service(mock_service_factory):
            service = mock_service_factory("ItemService", {
                "get_items": [item1, item2],
                "create_item": item1,
            })
    """

    def create_mock_service(service_class_name, methods_config=None):
        from services import author, item, reading

        modules = {
            "ItemService": item,
            "AuthorService": author,
            "ReadingService": reading,
        }

        if service_class_name not in modules:
            raise ValueError(f"Service {service_class_name} not found")

        module = modules[service_class_name]
        service_class = getattr(module, service_class_name)

        # Mockar métodos
        for method_name, return_value in (methods_config or {}).items():
            setattr(service_class, method_name, AsyncMock(return_value=return_value))

        # Retorna instância com sessão mockada
        return service_class(session=mock_db_session)

    return create_mock_service


@pytest.fixture
def mock_all_services(mocker, mock_db_session):
    """
    Mocka todos os serviços principais de uma vez.

    Útil para testes de resolvers que dependem de múltiplos serviços.

    Exemplo:
        @pytest.mark.asyncio
        async def test_resolver(mock_all_services):
            # mock_all_services["ItemService"] é mockado
            # mock_all_services["AuthorService"] é mockado
            # etc
    """
    services = {}

    patches = [
        "services.item.ItemService",
        "services.author.AuthorService",
        "services.reading.ReadingService",
    ]

    for patch_path in patches:
        service_name = patch_path.split(".")[-1]
        mock = mocker.patch(patch_path)
        mock.return_value.session = mock_db_session
        services[service_name] = mock

    return services


@pytest.fixture
def mock_manager_factory(mocker, mock_db_session):
    """
    Factory para criar managers mockados.

    Exemplo:
        @pytest.mark.asyncio
        async def test_manager(mock_manager_factory):
            manager = mock_manager_factory("ItemManager", {
                "add_item": item1,
            })
    """

    def create_mock_manager(manager_class_name, methods_config=None):
        from managers import author, core, item, reading

        modules = {
            "ItemManager": item,
            "AuthorManager": author,
            "ReadingManager": reading,
            "BaseDataManager": core,
        }

        if manager_class_name not in modules:
            raise ValueError(f"Manager {manager_class_name} not found")

        module = modules[manager_class_name]
        manager_class = getattr(module, manager_class_name)

        # Mockar métodos
        for method_name, return_value in (methods_config or {}).items():
            setattr(manager_class, method_name, AsyncMock(return_value=return_value))

        # Retorna instância com sessão mockada
        return manager_class(session=mock_db_session)

    return create_mock_manager


@pytest.fixture
def mock_with_side_effects(mock_db_session):
    """
    Helper para configurar side effects (múltiplos retornos ou exceções).

    Exemplo:
        @pytest.mark.asyncio
        async def test_retry(mock_with_side_effects):
            side_effect_config = [
                Exception("Network error"),
                Exception("Timeout"),
                {"status": "success"}  # Sucesso na terceira tentativa
            ]
            mock_with_side_effects(mock_db_session.exec, side_effect_config)
    """

    def configure_side_effects(mock_method, effects_list):
        mock_method.side_effect = effects_list
        return mock_method

    return configure_side_effects


@pytest.fixture
def mock_validation(mocker):
    """
    Mocka validadores para testar apenas lógica sem validação.

    Exemplo:
        @pytest.mark.asyncio
        async def test_logic(mock_validation):
            mock_validation("schemas.item.ItemSchema")
            # Agora validation não vai falhar
    """

    def disable_validation(schema_path):
        return mocker.patch(schema_path, return_value=MagicMock())

    return disable_validation


# ============================================================================
# Exemplo de fixtures compostas
# ============================================================================


@pytest.fixture
def mock_complete_item_flow(mocker, mock_db_session, mock_exec_query):
    """
    Setup completo para testar fluxo de criação de item.

    Ejemplo:
        @pytest.mark.asyncio
        async def test_item_creation(mock_complete_item_flow):
            # Tudo já está configured para um fluxo de item
    """
    from models import ItemModel

    # Mockar criação de item
    new_item = ItemModel(
        id=1,
        title="Test Item",
        type="book",
        main_author_id=1,
    )

    # Configurar queries
    mock_exec_query([new_item], method="first")

    # Mock para adição
    mock_db_session.add = AsyncMock()
    mock_db_session.commit = AsyncMock()

    return {
        "session": mock_db_session,
        "item": new_item,
    }


@pytest.fixture
def mock_graphql_resolver(mocker, mock_all_services):
    """
    Setup para testar resolvers GraphQL.

    Exemplo:
        @pytest.mark.asyncio
        async def test_resolver(mock_graphql_resolver, client):
            # Todos os serviços já estão mockados
    """
    return {
        "services": mock_all_services,
        "mocker": mocker,
    }
