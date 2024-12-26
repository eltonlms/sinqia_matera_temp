# Repositório para a trasnformação dos arquivos de movimento contábil por produto.

1. Para o correto funcionamento é necessário que o Python esteja instalado no computador na versão 3.9 ou superior.

[Python](https://www.python.org/)

2. Este script utiliza bibliotecas adicionais, é necessários instalá-las através do comando:
```bash
pip install -r requirements.txt
```

3. Mover o arquivo de resumo de momevimento contábil para o diretório **input**.

4. Executar o comando abaixo, substituindo o nome do arquivo pelo `nome_do_arquivo` que será lido:

*Exemplo:*

*python matera_transform.py Resumo_de_movimento_contabil_por_produto__sintetico_26_12_2024_11_13.xlsx*
```bash
python matera_transform.py <nome_do_arquivo>
```

5. Após a execução o arquivo csv é criado no diretório **output**, com o nome `modelo_de_importacao_sinqia_matera.csv`, 
se já existir um arquivo com este nome no diretório **output**, o script sobrescreverá o arquivo existente.