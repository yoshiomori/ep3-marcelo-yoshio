run:
	python3 ep3.py

init:
	cd experimento/arquivos/ && export PYTHONPATH=../../ && python3 cria_arquivos.py

sv:
	make init && cd ../ && export PYTHONPATH=../ && python3 experimento.py sistema_vazio

s10:
	make init && cd experimento; export PYTHONPATH=../ && python3 experimento.py sistema_10MB

s50:
	make init && cd experimento && export PYTHONPATH=../ && python3 experimento.py sistema_50MB
