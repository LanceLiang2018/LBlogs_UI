import requests
import random
import hashlib
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

    def decode_login_token(self, login_token):
        if len(login_token) != 68:
            return '0' * 32
        auth_mix = login_token[:32]
        order = login_token[32:64]

        orderd = []
        for i in range(0, len(order), 2):
            orderd.append({'num': int(order[i:i + 2], 16), 'key': i // 2})
        orderd.sort(key=lambda x: x['num'])
        auth = ''
        for i in orderd:
            auth = auth + "%02x" % (0xff - int(auth_mix[i['key'] * 2:i['key'] * 2 + 2], 16))
        return auth

    def make_token(self):
        salt = '%032x' % random.randint(0, 1 << (4 * 32))
        salted = hashlib.md5(("%s%s" % (self.auth, salt)).encode()).hexdigest()
        token = "%s%s%s" % (salted, salt, self.auth[:4])
        return token

    # With Auth
    def post(self, action: str, params: dict, files=None):
        params['action'] = action
        # params['auth'] = self.auth
        params['token'] = self.make_token()
        r = requests.post(self.API, data=params, files=files)
        if r.status_code != 200:
            return {'code': -1, 'message': "Server Error."}
        return r.json()

    def post_content(self, action: str, params: dict, files=None):
        params['action'] = action
        # params['auth'] = self.auth
        params['token'] = self.make_token()
        r = requests.post(self.API, data=params, files=files)
        if r.status_code != 200:
            return {'code': -1, 'message': "Server Error."}
        return r.content

    def login(self, username, password):
        result = self.post(self.LOGIN, {'username': username, 'password': password})
        if result['code'] != 0:
            print('登陆失败。', result['message'])
            return False
        # self.auth = result['data']['auth']['auth']
        token = result['data']['login_token']['login_token']
        self.auth = self.decode_login_token(token)
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
    _username = '%04x' % random.randint(0, 1 << (4 * 4))
    if not client.login(_username, ''):
        if not client.signup(_username, ''):
            exit(1)
        print('注册完成！')

    # with open('test.zip', 'rb') as f:
    #     zipdata = f.read()

    # print(client.publish(zipdata))

