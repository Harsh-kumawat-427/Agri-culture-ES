@echo off
title AgriCulture - Expert System Desktop Form
echo =======================================================
echo  🌱 AgriCulture Expert System Desktop GUI Form
echo =======================================================
cd /d "%~dp0"
python crop_expert_system/app.py --gui
pause

