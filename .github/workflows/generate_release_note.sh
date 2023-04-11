#!/bin/bash

# get latest release tag
TAG=$(git describe --tags --abbrev=0)

# generate release note
git log --pretty=format:'- %s [View on GitHub](https://github.com/your-username/your-repo/commit/%H)' ${TAG}..HEAD > release_note.txt
