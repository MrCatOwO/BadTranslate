.\.venv\Scripts\Activate.ps1
python.exe -m pip install --upgrade pip
pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}
pip freeze > requirements.txt