#!/usr/bin/bash
echo ""
echo "Changing directory to /opt"
echo ""
cd /opt

if [ -d /opt/Sunrise ]; then
    echo "Old directory has been found, and it has been deleted."
    sudo rm -rf /opt/Sunrise
fi
sudo git clone https://github.com/HOuadhour/Sunrise.git

echo "Adding the execute attribute of sunrise to the current user"
sudo chmod u+x /opt/Sunrise/sunrise.pyw
echo ""
echo "Creating a symlink of sunrise in /usr/local/bin"
echo ""
if [ -L /usr/local/bin/sunrise ]; then
    echo "Old symlink has been found, and it has been deleted."
    echo ""
    sudo rm -rf /usr/local/bin/sunrise
fi
sudo ln -s /opt/Sunrise/sunrise.pyw /usr/local/bin/sunrise
echo "Symlink has been created successfully."
echo ""
 
echo "Creating a desktop file."
echo ""
if [ -f $HOME/.local/share/applications/sunrise.desktop ]; then
    echo "Old desktop file has been found, and it has been deleted."
    echo ""
    rm -rf $HOME/.local/share/applications/sunrise.desktop
fi
cp /opt/Sunrise/sunrise.desktop $HOME/.local/share/applications/
echo "Adding the execute attribute of the file to the current user"
echo ""
chmod u+x $HOME/.local/share/applications/sunrise.desktop
