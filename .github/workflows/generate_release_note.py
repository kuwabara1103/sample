import json
import os
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

def get_release_issue():
    # ブランチ名からバージョン名を取り出す
    version_name = re.sub(r'^(release|hotfix)/', '', BRANCH)
    print(f"version_name: {version_name}")  # ログを追加
    page = 0
    while True:
        issues = get_open_issues(page)
        for issue in issues:
            print(f"issue: {issue['title']}")  # ログを追加
            # v6.0.5リリース または [Hotfix]v6.0.5リリース のような名前のIssueを見つける
            if re.match(f'(\[Hotfix\])?{version_name}リリース', issue['title']):
                return issue
        # 次のページが無いならbreak
        if len(issues) != PER_PAGE:
            break
        page += 1

print("Getting release issue...")  # ログを追加
release_issue = get_release_issue()
if release_issue is not None:
    print(f"Release issue found: {release_issue}")  # ログを追加
    issue_body = release_issue['body']

    # ```で囲まれている文言のみ抽出する
    pattern = r"```([\s\S]*?)```"
    extracted_release_note = re.search(pattern, issue_body).group(1)

    # 各エスケープ文字を適切に変換し、JSON文字列に適した形式にする
    formatted_release_note = extracted_release_note.replace('\r', '').replace('\n', '\\n').replace('\t', '\\t').replace('"', '\\"')
    print(f"Formatted release note: {formatted_release_note}")  # ログを追加
    print(formatted_release_note, end='') # 出力の末尾に改行文字が追加されないようにする
else:
    print("Release issue not found")  # ログを追加
    exit(1)
