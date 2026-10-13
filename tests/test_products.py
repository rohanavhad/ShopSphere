def test_create_and_list_product(client):
    payload={"name":"Desk Lamp","description":"Warm LED lamp","price":"1299.00","stock":4,"image_url":""}
    created=client.post("/api/v1/products/",json=payload)
    assert created.status_code == 201
    listed=client.get("/api/v1/products/")
    assert listed.status_code == 200
    assert listed.json()[0]["name"] == "Desk Lamp"
