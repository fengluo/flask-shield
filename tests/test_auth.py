from ._base import BaseCase


class TestAuth(BaseCase):
    def test_login(self):
        response = self.client.open("/")
        print response.data
        assert response.data == 'index'

    def test_permission(self):
        response = self.client.post("/login")
        response = self.client.open("/edit")
        assert response._status_code == 403
