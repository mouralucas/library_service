"""
PYTEST-MOCK QUICK REFERENCE GUIDE

Referência rápida para usar pytest-mock em testes async com FastAPI/SQLAlchemy.
"""

# ============================================================================
# INSTALAÇÃO
# ============================================================================

"""
pip install pytest-mock

ou adicione ao requirements.txt:
pytest-mock==3.14.0
"""


# ============================================================================
# 1. MOCKAR FUNÇÃO/MÉTODO
# ============================================================================

# Forma simples:
def test_simple_mock(mocker):
    mock_func = mocker.patch("module.function")
    mock_func.return_value = "valor"

# Com return_value:
def test_with_return(mocker):
    mock = mocker.patch("module.function", return_value=42)
    result = module.function()
    assert result == 42

# Função async:
def test_async_mock(mocker):
    mock = mocker.patch("module.async_function")
    mock.return_value = AsyncMock(return_value="dato")

# Ou melhor, use AsyncMock diretamente:
from unittest.mock import AsyncMock

def test_async_directly(mocker):
    async_mock = AsyncMock(return_value="dato")
    mocker.patch("module.async_function", new=async_mock)


# ============================================================================
# 2. MOCKAR MÉTODO DE CLASSE
# ============================================================================

# Mockar método de classe:
def test_class_method(mocker):
    from services.item import ItemService
    
    mock_method = AsyncMock(return_value=[])
    mocker.patch.object(ItemService, "get_items", mock_method)

# Mockar propriedade:
def test_class_property(mocker):
    from services.item import ItemService
    
    mocker.patch.object(
        ItemService,
        "database",
        new_callable=lambda: AsyncMock()
    )


# ============================================================================
# 3. MOCKAR COM SIDE_EFFECT (múltiplos valores)
# ============================================================================

# Retornar valores diferentes em cada chamada:
def test_side_effect_sequence(mocker):
    mock = mocker.patch("module.function")
    mock.side_effect = [1, 2, 3]  # Primeira chamada retorna 1, segunda 2, etc
    
    assert module.function() == 1
    assert module.function() == 2
    assert module.function() == 3

# Lançar exceção em determinada chamada:
def test_side_effect_exception(mocker):
    mock = mocker.patch("module.function")
    mock.side_effect = [
        {"data": "ok"},
        Exception("Database error"),
        {"data": "recovered"}
    ]

# Side effect com função:
def test_side_effect_callable(mocker):
    def side_effect_func(*args, **kwargs):
        if args[0] == "error":
            raise ValueError("Invalid input")
        return f"Processed: {args[0]}"
    
    mock = mocker.patch("module.process")
    mock.side_effect = side_effect_func


# ============================================================================
# 4. VERIFICAR CHAMADAS (Assertions)
# ============================================================================

def test_mock_assertions(mocker):
    mock = mocker.patch("module.function")
    
    # Função chamada exatamente uma vez:
    mock.assert_called_once()
    
    # Com argumentos específicos:
    mock.assert_called_once_with(1, 2, key="value")
    
    # Chamada foi feita (pode ser múltiplas vezes):
    mock.assert_called()
    
    # Com argumentos (última chamada):
    mock.assert_called_with(42)
    
    # Número de chamadas:
    assert mock.call_count == 5
    
    # Nunca foi chamado:
    mock.assert_not_called()
    
    # Uma das chamadas foi com esses args:
    mock.assert_any_call(1, 2, 3)
    
    # Ver todos as calls:
    print(mock.call_args_list)


# ============================================================================
# 5. MOCKAR SESSION DO BANCO DE DADOS
# ============================================================================

async def test_mock_database_session(mocker):
    from backend.database import get_session
    
    # Criar mock da sessão
    mock_session = AsyncMock()
    
    # Mockar métodos comuns
    mock_session.exec = AsyncMock()
    mock_session.add = AsyncMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    # Mockar resultado de query
    mock_session.exec.return_value.all.return_value = [item1, item2]
    
    # Mockar o get_session globalmente
    mocker.patch("backend.database.get_session", return_value=mock_session)
    
    # Agora qualquer código que injetar get_session() usará o mock
    session = get_session()
    items = await session.exec(select(ItemModel)).all()
    assert len(items) == 2


# ============================================================================
# 6. SPY (Monitorar sem substituir)
# ============================================================================

def test_spy(mocker):
    # Spy coloca um "spy" em um método real, monitorando chamadas
    # mas deixando o método rodar normalmente
    from services.item import ItemService
    
    service = ItemService(session=None)
    
    # Monitorar método real
    spy = mocker.spy(service, "get_items")
    
    # resultado = service.get_items()  # Roda normal mas é monitorado
    
    # Verificar que foi chamado
    # spy.assert_called_once()


# ============================================================================
# 7. MOCKAR MÚLTIPLOS MOCKS JUNTOS
# ============================================================================

def test_multiple_mocks(mocker):
    mock1 = mocker.patch("module.function1", return_value=1)
    mock2 = mocker.patch("module.function2", return_value=2)
    mock3 = mocker.patch("module.function3", return_value=3)
    
    # Usar todos os mocks
    result1 = module.function1()
    result2 = module.function2()
    result3 = module.function3()
    
    # Verificar todos
    mock1.assert_called_once()
    mock2.assert_called_once()
    mock3.assert_called_once()


# ============================================================================
# 8. MOCKAR COM CONTEXT MANAGER
# ============================================================================

def test_with_patch_context(mocker):
    with mocker.patch("module.function", return_value=42) as mock:
        result = module.function()
        assert result == 42
        mock.assert_called_once()


# ============================================================================
# 9. MOCKAR IMPORTS
# ============================================================================

def test_mock_import(mocker):
    # Mockar um módulo inteiro:
    mock_module = mocker.patch("module_to_mock")
    mock_module.function.return_value = "mocked"
    
    # Mockar import específico:
    mocker.patch("module.ClassName", return_value=MagicMock())
    
    # Mockar função de biblioteca:
    mock_random = mocker.patch("random.randint", return_value=42)


# ============================================================================
# 10. ASYNCIO COM PYTEST-MOCK
# ============================================================================

# AsyncMock - para funções async:
from unittest.mock import AsyncMock

async def test_async_function(mocker):
    # Criar AsyncMock
    mock = AsyncMock(return_value="dato")
    
    # Ou com side_effect:
    mock = AsyncMock(side_effect=[1, 2, AsyncMock(), Exception()])
    
    # Mockar:
    mocker.patch("module.async_func", new=mock)
    
    # Usar:
    result = await module.async_func()
    mock.assert_called_once()


# ============================================================================
# 11. EXEMPLO COMPLETO: GraphQL Resolver
# ============================================================================

import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_graphql_resolver_with_mocks(mocker):
    """
    Exemplo realista de teste de resolver GraphQL com múltiplos mocks
    """
    # 1. Mockar os serviços
    mock_item_service = mocker.patch("resolvers.item.ItemService")
    mock_author_service = mocker.patch("resolvers.item.AuthorService")
    
    # 2. Configurar comportamentos
    mock_item_instance = mock_item_service.return_value
    mock_item_instance.get_item = AsyncMock(return_value={
        "id": 1,
        "title": "Test Item",
        "main_author_id": 1
    })
    
    mock_author_instance = mock_author_service.return_value
    mock_author_instance.get_author = AsyncMock(return_value={
        "id": 1,
        "name": "Author Name"
    })
    
    # 3. Fazer request GraphQL
    response = await client.post("/graphql", json={
        "query": "{ getItem(id: 1) { id title } }"
    })
    
    # 4. Verificar resposta
    assert response.status_code == 200
    
    # 5. Verificar que serviços foram chamados
    mock_item_instance.get_item.assert_called_once_with(1)
    # mock_author_instance.get_author.assert_called_once_with(1)  # Se aplicável


# ============================================================================
# 12. BOAS PRÁTICAS
# ============================================================================

"""
✓ DO:
  - Use AsyncMock para funções async
  - Mocke no nível mais próximo (serviço ao invés de banco)
  - Use nomes descritivos para mocks
  - Organize mocks em fixtures reutilizáveis
  - Teste comportamento, não implementação
  - Use assert_called_with() para validar argumentos

✗ DON'T:
  - Não mocke tudo - alguns testes precisam de integração
  - Não use mocks muito genéricos
  - Não misture mocks reais com testes de integração
  - Não ignore exceções em testes
  - Não reutilize objetos mockados entre testes

PADRÃO RECOMENDADO:
  @pytest.mark.asyncio
  async def test_feature(mocker):
      # Setup
      mock_service = mocker.patch("path.to.Service")
      mock_service.return_value.method = AsyncMock(return_value=data)
      
      # Execute
      result = await some_function()
      
      # Assert
      assert result == expected
      mock_service.return_value.method.assert_called_once()
"""


# ============================================================================
# 13. MOCKAR COM FIXTURE
# ============================================================================

@pytest.fixture
def mock_item_service(mocker):
    """Fixture reutilizável para mockar ItemService"""
    mock = mocker.patch("services.item.ItemService")
    mock.return_value.get_items = AsyncMock(return_value=[])
    mock.return_value.create_item = AsyncMock(return_value={"id": 1})
    return mock

@pytest.mark.asyncio
async def test_with_fixture(mock_item_service):
    """Usa a fixture em múltiplos testes"""
    service = services.item.ItemService()
    items = await service.get_items()
    mock_item_service.return_value.get_items.assert_called_once()


# ============================================================================
# 14. MOCKAR PARAMETRIZADO
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.parametrize("input,expected", [
    ("valid", True),
    ("invalid", False),
    ("error", Exception),
])
async def test_parametrized_with_mock(mocker, input, expected):
    """Combina parametrização com mocks"""
    mock = mocker.patch("module.validate")
    
    if expected is Exception:
        mock.side_effect = Exception("Invalid")
    else:
        mock.return_value = expected
    
    if expected is Exception:
        with pytest.raises(Exception):
            module.validate(input)
    else:
        result = module.validate(input)
        assert result == expected


# ============================================================================
# 15. CLEAN UP E ISOLAMENTO
# ============================================================================

"""
pytest-mock cuida automaticamente de clean up:
- Mocks são resetados após cada teste
- Patches são removidas automaticamente
- Sem necessidade de adicionar teardown

Mas você PODE resetar manualmente se precisar:
    mock.reset_mock()
    mock.reset_mock(return_value=True, side_effect=False)
"""
