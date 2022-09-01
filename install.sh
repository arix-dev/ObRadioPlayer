#!/bin/bash
pip install -r requirements.txt
sudo mkdir /opt/ObRadioPlayer
sudo chown ${USER}:${USER} /opt/ObRadioPlayer
cp -r * /opt/ObRadioPlayer/

cat > ~/.local/share/applications/ObRadioPlayer.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=ObRadioPlayer
Comment=Simple Radio Player
Exec=/opt/ObRadioPlayer/ObRadio.py
Icon=/opt/ObRadioPlayer/icon.png
Type=Application
Categories=AudioVideo;
EOF
