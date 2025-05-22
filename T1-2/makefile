all: compila executa

compila:
	@echo "Python não precisa de compilação" > compilacao.txt

executa:
	python3 model.py < arquivoentrada > arquivosaida 2>&1

clear:
	rm -f arquivosaida compilacao.txt model model.hpp
