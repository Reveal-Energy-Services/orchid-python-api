#! /usr/bin/bash

# Identify all changes
echo 'Before'
grep '\\\\path\\\\to' *.ipynb

# Make the changes
echo
echo 'Editing in-place'
sed --in-place 's/\\\\path\\\\to/C:\\\\src/' *.ipynb

# Ensure all changes are correct
echo
echo 'After'
grep 'C:\\\\src' *.ipynb


