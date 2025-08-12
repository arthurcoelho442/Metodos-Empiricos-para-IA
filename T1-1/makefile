all: arquivoentrada main compila executa

arquivoentrada:
	echo "" > arquivoentrada

main:
	echo "#include <stdio.h>" > main.c
	echo "" >> main.c
	echo "int main(int argc, char *argv[]){" >> main.c
	echo "    printf(\"Hello World!\");" >> main.c
	echo "    return 0;" >> main.c
	echo "}" >> main.c

compila:
	gcc *.c -lm -o executavel > compilacao.txt

executa: 
	./executavel < arquivoentrada > arquivosaida 2>&1

clear:
	rm -f executavel arquivosaida