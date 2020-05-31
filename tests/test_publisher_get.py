async def test_not_found(test_cli):
    resp = await test_cli.get('/publishers/12345')
    assert resp.status == 404