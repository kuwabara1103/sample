import json
import os
import urllib.parse
import urllib.request

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
BRANCH = os.environ.get('BRANCH')
PER_PAGE = 100

def create_request(url, data=None):
    req = urllib.request.Request(url, data)
    req.add_header('Authorization', f'token {GITHUB_TOKEN}')
    return req

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def get_open_issues(page):
    url = f"https://api.github.com/repos/kuwabara1103/myapp/issues?state=open&page={page}&per_page={PER_PAGE}"
    req = create_request(url)
    with urllib.request.urlopen(req) as res:
        issues = json.load(res)
        return issues

def get_release_issue():
    # リリースブランチ名からバージョン名を取り出す
    version_name = remove_prefix(BRANCH, 'release/')
    page = 0
    while True:
        issues = get_open_issues(page)
        for issue in issues:
            # v6.0.5リリースのような名前のIssueを見つける
            if issue['title'] == f'{version_name}リリース':
                return issue
        # 次のページが無いならbreak
        if len(issues) != PER_PAGE:
            break
        page += 1

release_issue = get_release_issue()
if release_issue is not None:
    issue_body = release_issue['body']
    release_note = issue_body
    print(f"::set-output name=release_note::{release_note}")