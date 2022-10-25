Write-Host "Creating an executable"

pyinstaller app.py --onefile -F

Move-Item "dist/app.exe" ""

Remove-Item "app.spec"
Remove-Item "build/" -Recurse
Remove-Item "dist/"
