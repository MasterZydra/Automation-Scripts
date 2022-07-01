# Automation-Scripts
A collection of scripts for automation of repetitive tasks.

**Content**:
- [Azure DevOps](#azure-devops)
- [Git](#git)
- [Setup OS](#setup-os)

# Azure DevOps
- [`Dependabot.yml`](Azure%20DevOps/Dependabot.yml): This pipeline uses the dependabot-azure-devops Docker image from Tingle Software to run the Dependabot for the package manager *Composer*.
- [`Dependabot-with-Magento-Credentials.yml`](Azure%20DevOps/Dependabot-with-Magento-Credentials.yml): This pipeline uses the dependabot-azure-devops Docker image from Tingle Software to run the Dependabot for the package manager *Composer*. Additionally you can pass credentials so that the Dependabot can check for updates in the Magento repository.

# Git
- [`GravCommitUpdates.py`](Git/GravCommitUpdates.py): This script can be used to commit updates on Grav to the Git repository.
- [`IntelliJInitialCommit.py`](Git/IntelliJInitialCommit.py): This script can be used to do the initial commits of a new IntelliJ project.

# Setup OS
- [`SetupUbuntuDev`](SetupOS/SetupUbuntuDev.sh): This script can be used to install the programs to setup Ubuntu as environment for development. E.g. install git, VSCode, ...
