import requests
import io


class LBlogsClient:
    def __init__(self):
        # self.API = "http://lanceliang2018.xyz:5000/v1/api"
        self.API = "http://127.0.0.1:5000/v1/api"
        self.LOGIN = 'login'
        self.SIGNUP = 'signup'
        self.UPLOAD = 'upload'
        self.GET_FILES = 'get_files'
        self.GET_USER = 'get_user'
        self.SET_USER = 'set_user'
        self.PUBLISH = 'publish'

        self.username = ''
        self.auth = ''

    # With Auth
    def post(self, action: str, params: dict, files=None):
        params['action'] = action
        params['auth'] = self.auth
        r = requests.post(self.API, data=params, files=files)
        if r.status_code != 200:
            return {'code': -1, 'message': "Server Error."}
        return r.json()

    def post_content(self, action: str, params: dict, files=None):
        params['action'] = action
        params['auth'] = self.auth
        r = requests.post(self.API, data=params, files=files)
        if r.status_code != 200:
            return {'code': -1, 'message': "Server Error."}
        return r.content

    def login(self, username, password):
        result = self.post(self.LOGIN, {'username': username, 'password': password})
        if result['code'] != 0:
            print('登陆失败。', result['message'])
            return False
        self.auth = result['data']['auth']['auth']
        return True

    def signup(self, username, password, email='lanceliang2018@163.com'):
        result = self.post(self.SIGNUP, {'username': username, 'password': password, 'email': email})
        if result['code'] != 0:
            print('注册失败。', result['message'])
            return False
        return True

    def publish(self, zipdata: bytes):
        files = {'zipfile': io.BytesIO(zipdata)}
        result = self.post(self.PUBLISH, {}, files=files)
        if not result['code'] == 0:
            print(result)
            return False
        return True


if __name__ == '__main__':
    client = LBlogsClient()
    if not client.login('Tony', ''):
        if not client.signup('Tony', ''):
            exit(1)

    with open('test.zip', 'rb') as f:
        zipdata = f.read()

    print(client.publish(zipdata))

