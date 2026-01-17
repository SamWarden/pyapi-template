import httpx

from tests.checkers.response import assert_response


async def test_get_health(back_client: httpx.AsyncClient) -> None:
    response = await back_client.get("/health")
    assert_response(
        response,
        status_code=200,
        data={
            "status": "ok",
        },
    )
