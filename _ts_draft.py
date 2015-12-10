class Password(object):
    def __init__(self, name, passwd=None):
        self.name = name

    def passwd(self):
        pass

    def destroy(self):
        pass

class PasswordManager(object):
    def __init__(self, ketum_directory):
        self.ts_root = ketum_directory

    def list_passwords(self):
        pass

    def destroy_password_manager(self):
        pass

    def add_password(self, password_obj):
        pass