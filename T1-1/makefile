all: compila arquivoentrada executa

compila:
	gcc *.c -lm -o executavel > compilacao.txt

arquivoentrada:
	echo "" > arquivoentrada

executa: 
	./executavel < arquivoentrada > arquivosaida 2>&1

clear:
	rm executavel arquivoentrada arquivosaida compilacao.txt