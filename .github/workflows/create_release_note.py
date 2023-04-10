import os
import sys
import argparse
import releaser

# GitHub Personal Access Tokenを環境変数から取得する
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
BRANCH = os.environ.get('BRANCH')

if GITHUB_TOKEN is None:
    print('Error: Set the GITHUB_TOKEN environment variable.')
    sys.exit(1)

# 引数の解析
parser = argparse.ArgumentParser(description='Create a GitHub Release from a tag.')
parser.add_argument('tag_name', metavar='TAG_NAME', help='The name of the tag to create a release for.')
parser.add_argument('--description', metavar='DESCRIPTION', help='The description of the release.')
args = parser.parse_args()

# リリースの作成
release = releaser.create_release('owner/repo', args.tag_name, GITHUB_TOKEN, body=args.description)

if release is None:
    print('Error: Failed to create the release.')
    sys.exit(1)

print('Created a GitHub Release:', release['html_url'])
