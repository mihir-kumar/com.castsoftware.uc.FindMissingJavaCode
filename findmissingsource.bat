@echo off
set python_abs_path="C:\Program Files\CAST\8.2\ThirdParty\Python34\python.exe"

@echo Python Path found....

set kb_name="findsource_local"
set app_name="FindMissingSource"


%python_abs_path% %CD%\exex_missng_src.py %kb_name% %app_name%

echo Done pleas check the report under Lisa folder.
pause
