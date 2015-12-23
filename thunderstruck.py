from ketumclib import FSElement

import string
import random
import os


class Password(object):
    def __init__(self, _file):
        self.file = _file
        self.name = _file.name
        self._password = None
        self.password = _file.content or None

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value or self.random_pass()

    @staticmethod
    def random_pass(pass_len=16):
        chars = string.printable.split(' ')[0]
        return ''.join(
            random.SystemRandom().choice(chars) for _ in range(pass_len))

    def save(self):
        self.file.content = self.password
        self.file.save_to_remote()

    def __repr__(self):
        return "<Password: %s>" % self.name


class Category(object):
    def __init__(self, directory):
        self.directory = directory
        self.name = directory.name.rstrip('/')

    def passwords(self):
        result_list = list()
        for _file in self.directory.ls(FSElement.FILE):
            result_list.append(Password(_file))
        return result_list

    def add_password(self, keychain_name, name, password=None):
        self.directory.touch(name)
        passwd_obj = Password(self, self.directory.cd(name))
        passwd_obj.password = password
        passwd_obj.save()

    def get_password(self, name):
        for password in self.passwords():
            if password.name == name:
                return password
        return None

    def destroy_password(self, name):
        self.get_password(name).file.rm()

    def __repr__(self):
        return "<Category: %s>" % self.name


class PasswordManager(object):
    def __init__(self, ketum_directory):
        self.ketum_directory = ketum_directory
        try:
            self.ts_root = ketum_directory.cd('.thunderstruck')
        except LookupError:
            self.build()

    def build(self):
        self.ketum_directory.mkdir('.thunderstruck')
        self.ts_root = self.ketum_directory.cd('.thunderstruck')

    def categories(self):
        result_list = list()
        for directory in self.ts_root.ls(FSElement.DIRECTORY):
            result_list.append(Category(directory))
        return result_list

    def get_category(self, name):
        for category in self.categories():
            if category.name == name:
                return category
        return None

    def new_category(self, name):
        self.ts_root.mkdir(name)

    def destroy_category(self, name):
        self.ts_root.cd(name).rm()

    def destroy(self):
        self.ts_root.rm()
        self.build()

    def __repr__(self):
        return "<PasswordManager: %s>" % self.ts_root.storage.fingerprint
