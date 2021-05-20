#!/usr/bin/env python

"""
Author: David Hein

This script can be used to commit updates on Grav to the Git repository.

The following features are implemented:
- Sequencial processing of multiple Grav source code repos
- Creating a separate commit for each plugin with the version info in the
  commit message
- Pushing the commits in the end

Requirements:
- A Git repo must exist in the directory of the Grav source code
- Git must be usable via the terminal

Usage:
To add a folder to the script add a new block to the main function:
  os.chdir('/path/to/your/folder')
  commitGravUpdates()
"""

import subprocess
import os

# Configuration area
# ------------------
# Script will wait for user input to confirm pushing to remote
manualCheckBeforePush = True

def main():
    os.chdir('/my/path/to/grav/source/code')
    commitGravUpdates()

    os.chdir('/my/path/to/grav/source/code2')
    commitGravUpdates()

# Helper functions
# ----------------
def commitGravUpdates():
    push = False

    print('\n📁' + os.getcwd())
    changedFiles = getChangedFiles()

    # Commit all Grav system files
    gravSys = getGravSystemList(changedFiles)
    if len(gravSys) == 0:
        print('  No changes in Grav system')
    else:
        commitGravSystemChanges(gravSys)
        push = True

    # Commit all Grav plugins
    plugins = getChangedPluginList(changedFiles)
    if len(plugins) == 0:
        print('  No changes in plugins')
    else:
        commitPluginChanges(plugins)
        push = True
    
    if push:
        if manualCheckBeforePush:
            input("Check if commit message is correct")
        gitPush()

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

def getChangedPluginList(changedFiles: list[str]) -> list[str]:
    plugins = []
    for f in changedFiles:
        if f.startswith('user/plugins'):
            plugin = f.replace('user/plugins/', '')
            plugin = plugin.split('/', 1)[0]
            plugins.append(plugin)
    return removeListDuplicates(plugins)

def getGravSystemList(changedFiles: list[str]) -> list[str]:
    files = []
    for f in changedFiles:
        # Add system directories
        if f.startswith('vendor/') or f.startswith('system/'):
            files.append(f[:f.find('/')])
        # Add root files and config files
        if f.count('/') == 0 or f.startswith('user/config/'):
            files.append(f)
    return removeListDuplicates(files)

def getVersionNumber(path: str) -> str:
    with open(path + '/CHANGELOG.md') as f:
        firstLine = f.readline().replace('# ', '').replace('\n', '')
    if not firstLine.startswith('v') or not firstLine.count('.') == 2:
        print('Could not extract version info: ' + firstLine)
        return ''
    else:
        return firstLine

def commitGravSystemChanges(changedFiles: list[str]):
    for f in changedFiles:
        output = gitAdd(f)
        if output != '':
            print(output)
    
    # Get current version of plugin
    gravVersion = getVersionNumber('.')
    if gravVersion == '':
        return

    # Commit staged list
    output = gitCommit('Update Grav to ' + gravVersion)
    print(output)

def commitPluginChanges(plugins: list[str]):
    for plugin in plugins:
        # Get current version of plugin
        pluginVersion = getVersionNumber('user/plugins/' + plugin)
        if pluginVersion == '':
            break

        # Add plugins files to staged list
        output = gitAdd('user/plugins/' + plugin)
        if output != '':
            print(output)

        # Commit staged list
        output = gitCommit('Update plugin "' + plugin + '" to ' + pluginVersion)
        print(output)

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
