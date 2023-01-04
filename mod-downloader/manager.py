from github import Github, GitRelease
import requests
# import re
# import tarfile
import os
from baselib import create_dir
import subprocess
from datetime import datetime
from sys import argv

__version__ = "0.0.1"
__created_at__ = datetime(2023, 1, 5)

git = Github('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')
repo = git.get_repo('joshika39/minecraft-mods')
# releases = repo.get_releases()
last_release = repo.get_latest_release()
fname = "mod-downloader.exe"

if last_release.created_at > __created_at__:
    create_dir('update')
    r = requests.get(f"https://github.com/joshika39/minecraft-mods/releases/download/{last_release.title}/{fname}", allow_redirects=True)
    # d = r.headers['content-disposition']
    # fname = re.findall("filename=(.+)", d)[0]
    # print(fname)
    open(os.path.join('update', fname), 'wb').write(r.content)
    open(os.path.join('update', 'data'), 'wb')

subprocess.run([os.path.join('update', fname), ''.join([a for a in argv if a.startswith("-")])])
