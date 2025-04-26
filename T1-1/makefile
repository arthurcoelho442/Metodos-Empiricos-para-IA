all: compila executa

compila:
	gcc *.c -lm -o executavel > compilacao.txt

executa: 
	./executavel < arquivoentrada > arquivosaida 2>&1

clear:
	rm executavel arquivosaida