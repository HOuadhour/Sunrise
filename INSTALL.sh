#!/usr/bin/bash
echo ""
echo "Changing directoy to $HOME/.cache"
echo ""
cd $HOME/.cache

if [ -d $HOME/.cache/Sunrise ]; then
    echo "Old directory has been found, and it has been deleted."
    rm -rf $HOME/.cache/Sunrise 
fi
git clone https://github.com/HOuadhour/Sunrise.git

echo ""
echo "Creating a symlink of sunrise in /usr/local/bin"
echo ""
if [ -L /usr/local/bin/sunrise ]; then
    echo "Old symlink has been found, and it has been deleted."
    echo ""
    sudo rm -rf /usr/local/bin/sunrise
fi
sudo ln -s $HOME/.cache/Sunrise/sunrise.pyw /usr/local/bin/sunrise
echo "Symlink has been created successfully."
echo ""
 
echo "Creating a desktop file."
echo ""
if [ -f $HOME/.local/share/applications/sunrise.desktop ]; then
    echo "Old desktop file has been found, and it has been deleted."
    echo ""
    sudo rm -rf $HOME/.local/share/applications/sunrise.desktop
fi
cp $HOME/.cache/Sunrise/sunrise.desktop $HOME/.local/share/applications/
echo "Adding the execute attribute of the file to the current user"
echo ""
chmod u+x $HOME/.local/share/applications/sunrise.desktop

