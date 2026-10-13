def test_authenticated_order_reduces_stock(client):
    user=client.post("/api/v1/auth/register",json={"email":"buyer@example.com","full_name":"Buyer","password":"safe-password-123"}).json()
    product=client.post("/api/v1/products/",json={"name":"Bottle","description":"Steel bottle","price":"500.00","stock":3,"image_url":""}).json()
    response=client.post("/api/v1/orders/",headers={"Authorization":f"Bearer {user['access_token']}"},
                         json={"items":[{"product_id":product["id"],"quantity":2}]})
    assert response.status_code == 201
    assert float(response.json()["total_amount"]) == 1000.0
    assert client.get("/api/v1/products/").json()[0]["stock"] == 1

def test_order_requires_auth(client):
    response=client.post("/api/v1/orders/",json={"items":[{"product_id":1,"quantity":1}]})
    assert response.status_code == 401
