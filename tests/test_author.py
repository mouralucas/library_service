import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_author_with_name_only(client):
    author_name = "Test da Silva"

    payload = {
        "name": author_name,
    }
    mutation = """
        mutation CreateAuthor($input: CreateAuthorInput!) {
            createAuthor(author: $input) {
                author {
                    id
                    name
                    birthDate
                    description
                    countryId
                    countryName
                    languageId
                    languageName
                }
            }
        }
    """
    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": {"input": payload}}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "data" in data
    assert "createAuthor" in data["data"]
    data = data["data"]["createAuthor"]

    assert "author" in data
    assert data["author"]["name"] == author_name

    assert "countryId" in data["author"]
    assert data["author"]["countryId"] is None

    assert "languageId" in data["author"]
    assert data["author"]["languageId"] is None


@pytest.mark.asyncio
async def test_create_author_success(client, create_languages, create_countries):
    author_name = "Test da Silva"
    languages = create_languages
    countries = create_countries

    payload = {
        "name": author_name,
        "languageId": languages[0].id,
        "countryId": countries[0].id,
    }
    mutation = """
        mutation CreateAuthor($input: CreateAuthorInput!) {
            createAuthor(author: $input) {
                author {
                    id
                    name
                    birthDate
                    description
                    countryId
                    countryName
                    languageId
                    languageName
                }
            }
        }
    """
    response = await client.post(
        "/graphql/library", json={"query": mutation, "variables": {"input": payload}}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "data" in data
    assert "createAuthor" in data["data"]
    data = data["data"]["createAuthor"]
    assert "author" in data
    assert data["author"]["name"] == author_name

    assert "countryId" in data["author"]
    assert data["author"]["countryId"] == countries[0].id

    assert "languageId" in data["author"]
    assert data["author"]["languageId"] == languages[0].id


@pytest.mark.asyncio
async def test_get_author(client, create_authors):
    len_authors_list = len(create_authors)

    query = """
        query GetAuthors {
            getAuthors {
                quantity
                authors {
                    id
                    name
                    birthDate
                    description
                    countryId
                    countryName
                    languageId
                    languageName
                }
            }
        }
    """
    response = await client.post("/graphql/library", json={"query": query})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "data" in data
    assert "getAuthors" in data["data"]

    data = data["data"]["getAuthors"]

    assert "authors" in data
    assert len(data["authors"]) == len_authors_list
    assert type(data["authors"]) is list
    assert data["quantity"] == len_authors_list

    for author in data["authors"]:
        assert "id" in author
        assert author["id"] is not None
        assert "name" in author
        assert author["name"] is not None
        assert "birthDate" in author
        assert "description" in author
        assert "countryId" in author
        assert "countryName" in author
        assert "languageId" in author
        assert "languageName" in author


@pytest.mark.asyncio
async def test_get_author_empty(client):
    query = """
        query GetAuthors {
            getAuthors {
                quantity
                authors {
                    id
                    name
                    birthDate
                    description
                    countryId
                    countryName
                    languageId
                    languageName
                }
            }
        }
    """
    response = await client.post("/graphql/library", json={"query": query})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "data" in data
    assert "getAuthors" in data["data"]

    data = data["data"]["getAuthors"]

    assert "authors" in data
    assert len(data["authors"]) == 0
    assert type(data["authors"]) is list
    assert data["quantity"] == 0
