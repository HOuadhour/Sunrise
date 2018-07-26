#!/usr/bin/bash

echo "\nChanging directoy to $HOME/.cache"
cd $HOME/.cache
git clone https://github.com/HOuadhour/Sunrise.git

echo "\nCreating a symlink of sunrise in /usr/local/bin"
until sudo ln -s $HOME/.cache/Sunrise/sunrise.pyw /usr/local/bin/sunrise
do
    echo "Please check your password, Try again"
done
echo "\nSymlink has been created successfully."

echo "\nCreating a desktop file."
cp $HOME/.cache/Sunrise/sunrise.desktop $HOME/.local/share/applications/
echo "\nAdding the execute attribute of the file to the current user"
chmod u+x $HOME/.local/share/applications/sunrise.desktop


