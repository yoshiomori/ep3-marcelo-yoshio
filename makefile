run:
	python3 ep3.py

init: experimento/arquivos/arquivo1MB experimento/arquivos/arquivo10MB experimento/arquivos/arquivo30MB experimento/arquivos/sistema_vazio experimento/arquivos/sistema_10MB experimento/arquivos/sistema50MB
	cd experimento/arquivos/;export PYTHONPATH=../../; python3 cria_arquivos.py

sv:
	make init; cd experimento; export PYTHONPATH=../; python3 experimento.py sistema_vazio

s10:
	make init; cd experimento; export PYTHONPATH=../; python3 experimento.py sistema_10MB

s50:
	make init; cd experimento; export PYTHONPATH=../; python3 experimento.py sistema_50MB
