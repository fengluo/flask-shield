from ._header_base import HeaderCase


class TestHeaderAuth(HeaderCase):
    def test_unlogin_index(self):
        response = self.client.open("/")
        assert response._status_code == 401

    def test_login_index(self):
        response = self.client.post("/login", data=dict(
            name='foo'
        ))
        cookie = response.headers['Set-Cookie']

        response = self.client.get('/', headers={'Cookie': cookie})
        assert response._status_code == 200

    def test_permission(self):
        response = self.client.post("/login", data=dict(
            name='foo'
        ))
        cookie = response.headers['Set-Cookie']
        response = self.client.open("/edit", headers={'Cookie': cookie})
        assert response._status_code == 200
