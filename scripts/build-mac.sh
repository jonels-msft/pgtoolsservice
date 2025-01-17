# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

#!/bin/bash

# Save the current directory and the script's directory, since build must be run from the project root
pwd=$(pwd)
dirname=$(dirname "$0")

# Back up the old PYTHONPATH so it can be restored later
old_pythonpath=$PYTHONPATH

# Build the program
cd "$dirname/.."
export PYTHONPATH=""
pip3 install -r requirements.txt
pyinstaller ossdbtoolsservice_main.spec

# Create folder pgsqltoolsservice in dist folder
mkdir -p "./dist/pgsqltoolsservice"

# Move the contents in the dist folder to pgsqltoolsservice folder
find "./dist" -maxdepth 1 -type f -exec mv {} "./dist/pgsqltoolsservice" \;

# Copy pg_exe folder to pgsqltoolsservice
cp -R "./ossdbtoolsservice/pg_exes" "./dist/pgsqltoolsservice/pg_exes"

# Restore the old PYTHONPATH and move back to the original directory
cd "$pwd"
export PYTHONPATH="$old_pythonpath"
