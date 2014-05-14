#set these up in your google account
import getpass
import os.path

class Credential:
    def __init__(self, name='password', hidden=True):
        self.name = name
        self.prompt = self.name + ': '
        if not os.path.exists(self.name):
            if hidden:
                self.value = getpass.getpass(self.prompt)
            else:
                self.value = raw_input(self.prompt)
            open(self.name, 'wb').write(self.value)
        else:
            self.value = open(self.name).read().strip()
    def __str__(self):
        return self.value

    def reset(self):
        if os.path.exists(self.name):
            os.unlink(self.name)
            self.value = open(self.name).read()

def Credential__test__():
    p = Credential('password')
    q = Credential('password')
    assert p == q
    p.reset()

if False:
    username = Credential('username', hidden=False)
    password = Credential('password')
    gmailUser = username
    gmailPassword = password
else:
    username = 'XXXXXXXX@gmail.com'
    password = 'YYYYYYYY'
    gmailUser = 'ZZZZ@gmail.com'
    gmailPassword = 'QQQQQQQ'
