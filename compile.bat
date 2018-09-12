del /f /q \dist\*.*
pyinstaller --clean --upx-dir "upx393w" --noconsole --onefile --icon=icons\icon.ico "RAT.py"
del /f /q *.spec
