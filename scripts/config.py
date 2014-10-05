#set these up in your google account
import getpass
import os.path

class Credential:
    def __init__(self, prompt='Username:', secret=False):
        self.prompt = prompt
        self.secret = secret
        self.filename = '.' + prompt
        if os.path.exists(prompt):
            self.value = open(self.filename).read()
        else:
            self.value = None
    def __repr__(self):
        if self.value is None:
            if self.secret:
                self.value = getpass.getpass(self.prompt)
            else:
                self.value = raw_input(self.prompt)
                open(self.filename, 'w').write(self.value)
        return self.value
    def __str__(self):
        return self.__repr__()

username = Credential(prompt="AppSpecificPassword:")
password = Credential(prompt='Password:', secret=True)
gmailUser = username
gmailPassword = password

SIGN_ME_IN = True
