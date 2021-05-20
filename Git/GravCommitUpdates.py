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
    print('\n📁' + os.getcwd())
    output = getChangedFiles()
    plugins = getChangedPluginList(output)
    if len(plugins) == 0:
        print('  No changed plugins')
        return
    commitPluginChanges(plugins)
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
    return output

def getChangedPluginList(output: list[str]) -> list[str]:
    # Get changed plugin list
    plugins = []
    for o in output:
        if o.startswith('user/plugins'):
            plugin = o.replace('user/plugins/', '')
            plugin = plugin.split('/', 1)[0]
            plugins.append(plugin)
    return removeListDuplicates(plugins)

def commitPluginChanges(plugins: list[str]):
    for plugin in plugins:
        # Get current version of plugin
        with open('user/plugins/' + plugin + '/CHANGELOG.md') as f:
            pluginVersion = f.readline().replace('# ', '').replace('\n', '')
            if not pluginVersion.startswith('v') or not pluginVersion.count('.') == 2:
                print('Wrong version info: ' + pluginVersion)
                break

        # Add plugins files to staged list
        cmd = [ 'git', 'add', 'user/plugins/' + plugin]
        output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
        output = output.decode('utf-8')
        if output != '':
            print('Error adding plugin "' + plugin + '": ' + output)

        # Commit staged list
        output = gitCommit('Update plugin "' + plugin + '" to ' + pluginVersion)
        print(output)
        input("Check if commit message is correct")

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
