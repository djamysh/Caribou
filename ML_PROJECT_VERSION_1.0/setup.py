from Predictor.dirPath import get_dir_path
path = get_dir_path()

###################################
desktopfile = """
#!/usr/bin/env xdg-open
[Desktop Entry]
Version=1.0
Type=Application
Terminal=false
Icon[en_US]={}Images/appIcon.png
Name[en_US]=Predictor
Exec=python3 {}main.py
Comment[en_US]=Predicting activity efficiency before activity happen
Name=Predictor
Comment=Predicting activity efficiency before activity happen
Icon={}Images/appIcon.png
""".format(path,path,path)

print(desktopfile)
with open("/home/wasptheslimy/.local/share/applications/Predictor.desktop","w",encoding = "utf-8") as file:
    file.write(desktopfile)
####################################

