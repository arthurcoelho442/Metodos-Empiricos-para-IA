# Variáveis
URL_DADOS = http://200.137.66.21/tjsp/law-tjsp/decisoesTJSP.tar.gz
ARQUIVO_ZIP = decisoesTJSP.tar.gz
DIRETORIO_DADOS = decisoesTJSP

# Alvos
all: executa

executa: install descompacta_dados
	@echo "Executando o script..."
	python3 build_index.py

compila:
	@echo "Python não precisa de compilação" > compilacao.txt

install:
	@echo "Instalando dependências com pip..."
	pip install -r requirements.txt

download_dados:
	@echo "Baixando o arquivo de dados..."
	wget -N $(URL_DADOS)

descompacta_dados: download_dados
	@echo "Descompactando o arquivo de dados..."
	tar -xzf $(ARQUIVO_ZIP)

clear:
	@echo "Limpando arquivos gerados..."
	rm -rf compilacao.txt $(ARQUIVO_ZIP) $(DIRETORIO_DADOS) json_pages docs_mapping.csv