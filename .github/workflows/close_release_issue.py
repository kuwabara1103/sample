#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import urllib.parse
import urllib.request
import re

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
BRANCH = os.environ.get('BRANCH')
PER_PAGE = 30


def create_request(url, data=None):
    req = urllib.request.Request(url, data)
    req.add_header('Authorization', f'token {GITHUB_TOKEN}')
    return req


def get_open_issues(page):
    url = f"https://api.github.com/repos/kuwabara1103/myapp/issues?state=open&page={page}&per_page={PER_PAGE}&labels=release"
    req = create_request(url)
    with urllib.request.urlopen(req) as res:
        issues = json.load(res)
        return issues

def get_release_issue_number():
    # ブランチ名からバージョン名を取り出す
    version_name = re.sub(r'^(release|hotfix)/', '', BRANCH)
    page = 0
    while True:
        issues = get_open_issues(page)
        for issue in issues:
            # PRは検索対象外
            if 'pull_request' in issue:
                continue
            # v6.0.5リリース または [Hotfix]v6.0.5リリース のような名前のIssueを見つける
            if re.match(f'(\[Hotfix\])?{version_name}リリース', issue['title']):
                return issue['number']
        # 次のページが無いならbreak
        if len(issues) != PER_PAGE:
            break
        page += 1


def close_issue(number):
    url = f"https://api.github.com/repos/kuwabara1103/myapp/issues/{number}"
    data = {
        "state": "close"
    }
    req = create_request(url, json.dumps(data).encode())
    urllib.request.urlopen(req)


release_issue_number = get_release_issue_number()
if release_issue_number is not None:
    close_issue(release_issue_number)
