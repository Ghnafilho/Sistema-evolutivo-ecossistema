# Sistema-evolutivo-ecossistema
Esse repositório contém códigos de um sistema evolutivo que tenta recriar um ecossistema real, o código atual apresenta 3 versões
## Descrição
Esse projeto foi desenvolvido com o intuito de ser o projeto final proposto por Eduardo do Valle Simões na disciplina Sistemas Evolutivos aplicados à robótica, ele foi feito na linguagem python, que mesmo não sendo a mais indicada para construir um algoritmo evolutivo, apresenta boas opções de inteface gráfica, com as quais apresentamos maior domínio. O código foi pensado com a ideia de simular um ecossistema que contém os seguintes itens:
### 5 diferentes espécies sendo elas:
#### Uma espécie de peixe que se alimenta de microorganismos aquáticos, que não estão incluídos no sistema, logo, é dado como se o peixe comesse a todo momento;
#### Uma espécie de herbívoros que se alimentam exclusivamente da vegetação dada no código por árvores;
#### Uma espécie de Carnívoros que se alimentam exclusivamente dos herbívoros;
#### Uma espécie de Carnívoros que se alimentam exclusivamente dos peixes ou uma espécie de Onívaros que comem peixes, herbívoros e vegetação, sendo essas duas versões do código;
#### Uma espécie de Mosquito que se alimenta de cadáveres; 
### 3 ambientes possíveis para os animais viverem, sendo eles: 
#### Água;
#### Deserto;
#### Floresta;

## Como funciona o código?
O código funciona da seginte maneira: primeiramente é criado o ambiente, caso seja de desejo do operador, ele pode modificar as estruturas como quiser; após essa fase, ele irá adicionar ao cenário os animais, que cada espécie apresenta uma vida e energia específica e uma variável fome, que cresce quando o animal fica sem comer. 
As variáveis aleatórias são: A posição inicial do animal, e um vetor de movimentos que consome a energia do ser vivo; 
Caso um predador encontre a sua presa, ele automaticamente a devora e a partir disso, sua fome zera e ele recupera energia; 
Caso sua fome atinja o valor de 20 ele começa a perder vida; 
Caso ele fique parado ele recupera energia; 



## As três versões:
O código atual apresenta 3 versões:
A primeira é mais visual, utiliza a espécie de carnívoros que se alimentam exclusivamente de peixes e imprime na tela todas as rodadas de movimentos dos animais de todas as gerações;
As outras duas apresentam somente as rodadas da última geração escolhida e uma versão é com o onívaro e outra com o carnívoro de peixes.


## Vídeo do projeto:



## Colaboradores: 
Gustavo Henrique Nogueira de Andrade Filho
Caio
