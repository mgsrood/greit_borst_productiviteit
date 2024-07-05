@echo off
:: Verander naar de directory van je Git repository
cd /d D:\greit\klanten\borst_bloembollen\productiviteitsmeting

:: Voeg alle wijzigingen toe
git add .

:: Maak een timestamp voor de commit message
for /f "tokens=1-5 delims=/:. " %%d in ('echo %date% %time%') do set timestamp=%%d-%%e-%%f_%%g-%%h-%%i

:: Commit de wijzigingen met de timestamp als message
git commit -m "Commit on %timestamp%"

:: Push de wijzigingen naar de remote repository
git push origin main

pause
