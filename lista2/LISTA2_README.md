**Lista de Exercícios \- Curso de Estruturas de Dados I (em C/C++)** 

**Prof. Igor Machado Coelho \- Tópico: Estruturas Lineares** 

**Observação:** os exercícios devem ser feitos em C/C++ (ou similar\!). Foque mais na lógica do que em erros básicos de programação e SEMPRE discuta a proposta do algoritmo (não quero apenas código\!). Sempre analise a complexidade assintótica dos métodos implementados. 

1\. Considere um tipo chamado Deque, que inclui manipulação de dois extremos em uma estrutura linear (como se operasse como Pilha e Fila simultaneamente).   
template\<typename Agregado, typename Tipo\> 

concept DequeTAD \= requires(Agregado a, Tipo t) { 

// requer operação de consulta ao elemento 'inicio' 

{ a.inicio() }; 

// requer operação de consulta ao elemento 'fim' 

{ a.fim() }; 

// requer operação 'insereInicio' sobre tipo 't' 

{ a.insereInicio(t) }; 

// requer operação 'insereFim' sobre tipo 't' 

{ a.insereFim(t) }; 

// requer operação 'removeInicio' e retorna tipo 't' 

{ a.removeInicio() }; 

// requer operação 'removeFim' e retorna tipo 't' 

{ a.removeFim() }; 

}; 

1.a) Satisfaça as seguintes operações de um DequeTAD para o tipo ‘char’, utilizando uma estrutura Sequencial OU uma estrutura encadeada:   
struct Deque { 

// implementar métodos propostos no TAD Deque 

}; 

static\_assert(DequeTAD\<Deque, char\>); // testa se Deque está correto 

1.b) Implemente uma estrutura PilhaDeque para tipo ‘char’, utilizando somente um Deque como armazenamento interno e mais espaço auxiliar constante:   
struct PilhaDeque{ 

Deque d; // Deque para ‘char’ (veja exercício anterior) 

// SOMENTE espaço auxiliar CONSTANTE aqui (nenhum vetor, lista, etc) // implementar métodos do TAD Pilha 

}; 

static\_assert(DequeTAD\<Deque, char\>); // testa se Deque está correto static\_assert(PilhaTAD\<PilhaDeque, char\>); // testa se Pilha está correta 

1.c) Implemente uma estrutura FilaDeque para tipo ‘char’, utilizando somente um Deque como armazenamento interno e mais espaço auxiliar constante:   
struct FilaDeque { 

Deque d; // Deque para ‘char’ (veja exercício anterior) 

// SOMENTE espaço auxiliar CONSTANTE aqui (nenhum vetor, lista, etc) // implementar métodos do TAD Fila 

}; 

static\_assert(DequeTAD\<Deque, char\>); // testa se Deque está correto static\_assert(FilaTAD\<FilaDeque, char\>); // testa se Fila está correta  
2\) Implemente uma estrutura que satisfaz o TAD Pilha para o tipo ‘char’ e somente utiliza duas Filas como armazenamento interno (mais espaço constante):   
\#include\<queue\> // Fila genérica em C++ (ou import std) 

struct Pilha2F{ 

std::queue\<char\> f1; // Fila para ‘char’ 

std::queue\<char\> f2; // Fila para ‘char’ 

// SOMENTE espaço auxiliar CONSTANTE aqui (nenhum vetor, lista, etc) // implementar métodos do TAD Pilha 

}; 

static\_assert(PilhaTAD\<Pilha2F, char\>); // testa se Pilha está correta 

3\) Implemente uma estrutura que satisfaz o TAD Fila para o tipo ‘char’ e somente utiliza duas Pilhas como armazenamento interno (mais espaço constante):   
\#include\<stack\> // Pilha genérica em C++ (ou import std) 

struct Fila2P{ 

std::stack\<char\> p1; // Pilha para ‘char’ 

std::stack\<char\> p2; // Pilha para ‘char’ 

// SOMENTE espaço auxiliar CONSTANTE aqui (nenhum vetor, lista, etc) // implementar métodos do TAD Fila 

}; 

static\_assert(FilaTAD\<Fila2P, char\>); // testa se Fila está correta 

4\) Escreva um algoritmo que dada uma pilha padrão P externa passada como parâmetro, inverte o conteúdo de P. Somente utilize as estruturas extras permitidas como armazenamento externo(mais espaço constante) 

a) Uma Fila 

void inverte(std::stack\<char\>\* p) { 

std::queue\<char\> f; // somente essa fila e mais espaço auxiliar constante } 

b) Duas Pilhas 

void inverte(std::stack\<char\>\* p) { 

std::stack\<char\> p1; // primeira pilha auxiliar 

std::stack\<char\> p2; // segunda pilha auxiliar 

// mais espaço auxiliar constante 

} 

c) Uma Pilha 

void inverte(std::stack\<char\>\* p) { 

std::stack\<char\> p1; // uma pilha auxiliar 

// mais espaço auxiliar constante 

} 

5\) Escreva um algoritmo em que dada uma fila padrão F externa passada como parâmetro, inverte o conteúdo de F. Somente utilize as estruturas extras permitidas como armazenamento externo (mais espaço constante) 

a) Uma Pilha 

void inverte(std::queue\<char\>\* f) { 

std::stack\<char\> p; // somente essa pilha e mais espaço auxiliar constante } 

b) Duas Filas 

void inverte(std::queue\<char\>\* f) { 

std::queue\<char\> f1; // primeira fila auxiliar 

std::queue\<char\> f2; // segunda fila auxiliar 

// mais espaço auxiliar constante 

}  
6\) Criar uma implementação do TAD Pilha para o tipo ‘int’, chamada PilhaMin, que oferece os métodos do TAD (em tempos constantes) e também o método obterMinimo(), que retorna o menor elemento da pilha. O método obterMinimo() também deve operar em tempo constante. 

struct PilhaMin { 

// incluir variáveis necessárias 

int topo(); 

int desempilha(); 

void empilha(int t); 

int obterMinimo(); 

// mais métodos auxiliares 

} 

static\_assert(PilhaTAD\<PilhaMin, int\>); //testa se PilhaMin está de acordo com o TAD 

7\) Exercícios em notação polonesa reversa. 

7.a) Escreva um algoritmo que executa uma conta em expressão polonesa reversa para N variáveis (A, B, C …). Considere no máximo N variáveis entre 1 e 7\. Exemplo: 

Entrada: 5 

3 

3 

2 

1 

1 

“AB+CED/-\*” 

Saída: \-4 

Explicação: A=3 B=3 C=2 D=1 E=1, expressão “33+211/-\*”, ou seja 3+3=6 1/1=1 2-6=-4 

7.b) Escreva um algoritmo que converte uma expressão aritmética parentizada usando as 4 operações para a expressão correspondente em notação polonesa reversa. 

Exemplo: 

Entrada: “((A+B)\*(C-(F/D)))” 

Saída: “AB+CFD/-\*” 

// ‘expressao’ eh um string terminado em ‘\\0’, com tamanho N (sem contar o \\0) // ‘saida\_polonesa’ eh um string com capacidade máxima N 

void polonesa(char expressao\[\], int N, char saida\_polonesa\[\]) { 

// escreva o resultado no string ‘saida\_polonesa’ 

} 

8\) Considere o TAD chamado PegaEntreMaiores com a seguinte especificação: 

template\<typename Agregado, typename Tipo\> 

concept PegaEntreMaioresTAD \= requires(Agregado a, Tipo t) { 

// requer operação 'insere' sobre tipo 't' 

{ a.insere(t) }; 

// requer operação de retornar o maior elemento 

{ a.maior() }; 

// requer operação de retornar o segundo maior elemento 

{ a.segundomaior() }; 

// requer operação de retornar o k-esimo maior elemento 

{ a.kmaior(int) }; 

// requer operação tamanho, ou seja, numero total de elementos 

{ a.tamanho() }; 

};  
Implemente um TAD PegaEntreMaiores para o tipo caractere, com as seguintes estratégias: 

8.a) utilize um vetor não-ordenado para armazenar os valores internamente (analise as complexidades das operações\!) 

8.b) utilize um algoritmo de ordenação pouco eficiente (Selection Sort, Bubble Sort, Insertion Sort, …) para manter o vetor ordenado (analise as complexidades das operações\!) 

8.c) utilize um algoritmo de ordenação eficiente (Quick Sort, Merge Sort, Heap Sort, …) para manter o vetor ordenado (analise as complexidades das operações\!) 8.d) utilize o algoritmo clássico QuickSelect em sua implementação. (analise as complexidades das operações\!) 

***BONUS:** implemente as quatro versões do TAD no computador e marque os tempos computacionais para valores de N=10, 100, 1000, 10000, 100000 e N=1000000. O tempo esperado condiz com a complexidade analítica?* 

9\) Considere um TAD Saco padrão com suas operações adiciona, itera, busca e remove. Implemente um TAD SacoVaiEVem, que além do iterador comum de itera(), implementa o método iteravolta() como um iterador reverso que percorre o TAD na ordem contrária do iterador padrão do método itera() (ou seja, do fim para o começo).