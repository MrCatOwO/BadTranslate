pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}
pip freeze > requirements.txt