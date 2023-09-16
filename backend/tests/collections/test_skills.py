import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "json_data, expected_status",
    [
        ({"name": "Python"}, status.HTTP_200_OK),
        ({"name": "JS"}, status.HTTP_200_OK),
        ({"name": "Java"}, status.HTTP_200_OK),
        (
            {"name": "Checking_max_length_acceptable"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    ],
)
async def test_add_skill(test_client: AsyncClient, json_data, expected_status):
    response = await test_client.post("/api/v1/skills/", json=json_data)
    assert response.status_code == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "limit, expected_len, expected_status",
    [
        ("limit=1", 1, status.HTTP_200_OK),
        ("limit=2", 2, status.HTTP_200_OK),
        ("", 3, status.HTTP_200_OK),
    ],
)
async def test_get_skills(
    test_client: AsyncClient, limit, expected_len, expected_status
):
    response = await test_client.get("/api/v1/skills/", params=limit)
    assert response.status_code == expected_status
    assert len(response.json()) == expected_len
    assert {"name": "Python"} in response.json()
