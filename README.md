# Algoritmos

Listas de exercícios de Estruturas de Dados I.

## Lista 2 - Estruturas Lineares

O enunciado está em [`lista2/LISTA2_README.md`](lista2/LISTA2_README.md). Cada questão fica em um arquivo `lista2/questao_*.py`, e as estruturas base usadas por elas ficam em `lista2/pilha.py` e `lista2/fila.py`.

### Como executar os testes

Os testes unitários de todas as questões estão em `lista2/executa_testes.py`. É preciso Python 3.13 ou mais recente e nenhuma biblioteca externa.

```bash
python3 lista2/executa_testes.py              # todas as questões
python3 lista2/executa_testes.py 6 8          # somente as questões 6 e 8
python3 lista2/executa_testes.py base         # somente pilha.py e fila.py
python3 lista2/executa_testes.py -v           # um teste por linha
python3 lista2/executa_testes.py --resumo     # somente a tabela final
```

Ao final é impressa uma tabela com o número de testes, acertos, falhas e erros por questão. O comando termina com código 0 quando todos os testes passam e 1 quando há falha ou erro.

Os testes cobrem apenas o uso válido das estruturas: operações em estruturas vazias ou cheias não são testadas.
