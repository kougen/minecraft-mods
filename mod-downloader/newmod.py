

import os

from baselib import construct_name

from json_service import JsonService
from verions import Version
from selection_picker_joshika39 import *

class Mod():
    depend_on = []  # type: list['Mod']
    preferred_version = Version.VS_1_16_5
    domain: str
    file_name: str
    depend_on_str: list[str]
    state: str
    name: str

    def __str__(self):
        deps = ""
        for mod in self.depend_on_str:
            deps += f'{mod} '
        deps = deps[:-1]
        deps = deps[:100] + (deps[100:] and '..')
        return colorize(f"{self.name}{GRAY} - ({self.state}) - {YELLOW}({deps})", GREEN)

    def details(self) -> str:
        return f"Mod: {self.name}\n-> {self.category}\n-> {self.filename}\n-> {self.link}\n" + 10 * '-' + '\n'

    def __init__(self, m_id: str, read_path: str, write_path: str, category: str):
        self.mod_id = m_id
        self.read_service = JsonService(read_path)
        self.write_service = JsonService(write_path)
        self.category = category
        self.domain = self.read_service.read(f'{self.mod_id}/domain')
        self.file_name = self.read_service.read(f'{self.mod_id}/filename')
        self.depend_on_str = self.read_service.read(f'{self.mod_id}/depend_on')
        self.state = self.read_service.read(f'{self.mod_id}/state') 

    def setup(self, domain: str, file_name: str, depend_on_str: list[str], state: str):
       self.domain = domain
       self.file_name = file_name
       self.depend_on_str = depend_on_str
       self.state = state
       self.name = construct_name(self.file_name)

    def serializable_attrs(self):
        props = {
            'domain': self.domain, 
            'filename': self.file_name,
            'depend_on': self.depend_on_str,
            'state': self.state,
            'version': self.preferred_version.name
        }
        return props

    def save(self):
        self.write_service.write(self.mod_id, self.serializable_attrs())
