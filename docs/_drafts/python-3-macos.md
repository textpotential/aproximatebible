---
layout: post
title:  "Installing Python 3 on macOS"
date:   2020-04-11 10:04:25
---

## Install xcode command line tools

1. Open Terminal 
2. Type `xcode-select --install` and hit `return`
3. When dialog box appears for command line tools, click Install

## Install Homebrew package manager

1. Go to the [Homebrew Install page](https://brew.sh/#install)
2. Copy the first command on the page and paste into terminal on your Mac and click `return`

## Install python 3 with homebrew

1. `$ brew install python`
2. Onxce install is complete, run `$ python3`
3. Confirm that version (first line in python console) has something like `Python 3.x.x`
4. Exit python with `>>> exit()`

## Make python 3 default for your user

1. Open Terminal
2. `$ vim ~/.profile`
3. `i` for insert mode
4. copy `export PATH="/usr/local/opt/python/libexec/bin:$PATH"` and past into terminal
5. hit `escape` to exit insert mode
6. type `:wq` to write these changes and exit file
7. exit terminal and start a new terminal session
8. `$ python` should now run the python3 version you just installed with Homebrew
