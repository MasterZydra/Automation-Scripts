#!/usr/bin/env python3

"""
Author: David Hein

This script can be used to do the initial commits of a new IntelliJ project.

The following files will be commited:
- Git Ignore
- IntelliJ project folder
- Gradle files

Requirements:
- A Git repo must exist in the directory of the Grav source code
- Git must be usable via the terminal

Usage:
To add a folder to the script add a new block to the main function:
    os.chdir('/my/path/to/grav/source/code')
    commitIntelliJProject()
"""

import subprocess
import os

def main():
    os.chdir('/my/path/to/grav/source/code')
    commitIntelliJProject()

# Helper functions
# ----------------
def commitIntelliJProject():
    print('\n📁' + os.getcwd())
    changedFiles = getChangedFiles()

    addAndCommit(changedFiles, '.gitignore', 'Add gitignore')
    addAndCommit(changedFiles, '.idea/', 'Add IntelliJ project')
    
    addGradle(changedFiles)

def addGradle(changedFiles: list[str]):
    commit = False
    for f in changedFiles:
        if f in ['gradle/', 'gradlew.bat', 'settings.gradle', 'build.gradle', 'gradlew']:
            gitAdd(f)
            commit = True
    
    if commit:
        gitCommit('Add gradle')
        print('Add gradle')
    

def addAndCommit(changedFiles: list[str], file: str, message: str):
    try:
        if changedFiles.index(file) > -1:
            gitAdd(file)
            gitCommit(message)
            print(message)
    except ValueError:
        print(file + ' not found')

def getChangedFiles() -> list[str]:
    cmd = [ 'git', 'status', '-s']
    output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
    output = output.decode('utf-8').split('\n')

    # Remove first characters to get only the file names
    for i in range(len(output)):
        output[i] = output[i][3:]

    # Remove empty string entry
    if output[len(output) - 1] == '':
        output.pop(len(output) - 1)
    return removeListDuplicates(output)

def gitAdd(file: str) -> str:
    cmd = [ 'git', 'add', file]
    output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
    output = output.decode('utf-8')
    if output != '':
        return 'Error adding "' + file + '": ' + output
    else:
        return output

def gitCommit(message: str) -> str:
    cmd = [ 'git', 'commit', '-m', message]
    output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
    output = output.decode('utf-8')
    return output

def gitPush():
    cmd = [ 'git', 'push']
    output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
    output = output.decode('utf-8')
    print(output)

def removeListDuplicates(l: list) -> list:
    return list(dict.fromkeys(l))

if __name__=="__main__":
   main()
