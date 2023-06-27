# Steam Games Price Classification

## Descrição do problema

Para uma empresa de vendas é importante saber os principais fatores detrás do preço de um videogame pois, essa informação pode ajudar os consumidores a tomar decisões de compra mais informadas. Também podem avaliar melhor se o preço é razoável e se o jogo vale o investimento. Além de ajudar organizar inventarios e fazer forecasting no futuro.

Em segundo lugar, entender os fatores por trás do preço de um jogo também pode fornecer insights sobre a indústria de jogos como um todo. Isso pode ajudar indivíduos interessados em trabalhar na indústria a entender melhor os vários custos e fluxos de receita envolvidos no desenvolvimento e publicação de jogos.

Em terceiro lugar, pode ajudar as empresas a tomar decisões mais estratégicas sobre como precificar seus jogos. Ao analisar os custos e fatores de demanda envolvidos na definição de preços de um jogo, as empresas podem tomar decisões mais informadas sobre como precificar seus produtos e como alocar seus recursos.

No geral, entender os fatores por trás do preço de um jogo é importante tanto para consumidores, profissionais da indústria e empresas. Isso pode ajudar a promover transparência na indústria, apoiar a tomada de decisões informadas e facilitar o crescimento e sucesso da indústria de jogos como um todo.

## Objetivo do projeto

A empresa precisa entender quais os principais fatores detrás de 3 categorias de videojogos, videojogos baratos e/ou economicos, videojogos estándar e videojogos AAA e/ou caros. Por isso o projeto têm como meta entender o perfil de cada um desses jogos e treinar um algoritmo de Machine Learning capaz de classificar nessas três clases (Barato, Estándar, Caro).

Um projeto de classificação multi-classe é utilizado quando a variável de saída (ou variável alvo) possui três ou mais possíveis resultados. O objetivo é treinar um modelo capaz de aprender padrões a partir dos dados de entrada e utilizar esses padrões para prever a classe correta para novos dados não vistos. O sucesso de um projeto de classificação multi-classe é medido pela sua capacidade de prever com precisão a classe correta para novos dados não vistos. A precisão do modelo pode ser melhorada selecionando recursos apropriados, ajustando hiperparâmetros e selecionando o algoritmo de aprendizado de máquina apropriado.

## Processo de tomada de decisão.

A data precisou de uma transformação desde o ínicio para adaptar aos requisitos da empresa, esta transformação foi convertir o target númerico (Preço do jogo) para um target categorico (Jogo Barato, Jogo de preço estandar, Jogo Caro), tal que:

- **Barato:** Aqueles jogos com preço de R$0 até R$49
- **Estandar:** Aqueles jogos com preço de R$50 até R$149
- **Caro:** Aqueles jogos com preço de R$150 ou mais.

Com esta transformação consegui descubrir e entender o primeiro desafio do projeto. O balance das classes do target.

![Target balance](https://raw.githubusercontent.com/liamarguedas/steam-games-price/main/Summary-Charts/target-balance.png)


É possível ver que a grande maioria de jogos estavam na classe Barato, pelo qual não seria um grande problema classificar a mesma. Porém podemos ver que a classe Caro contêm menos de 100 jogos (Menos do 10% do dataset) o qual dificulta a classificação. Por isso meu foco ficou em criar uma classificação funcional, para fazer isso eficientemente a solução devia ter:

- Diminuir erros de classificação de Baratos como Caros e vice-versa, distribuindo assim a maioria da margem de erro na classificação de Baratos como Estandar, Caros como Estandar ou vice-versa em ambos casos.

- Ser fácil de implementar

- Ter um custo beneficio eficiente e dentro do orçamento da empresa.

- Replicavél na produção.

Para realizar uma implantação dessa forma foi necessário realizar a exploração de cada atributo junto com nosso target e entender a relação entre eles, no gráfico a seguir podemos ver a correlação dos atributos e Preço do jogo (Na sua forma continua):

![Preço correlations](https://raw.githubusercontent.com/liamarguedas/steam-games-price/main/Summary-Charts/target-correlations.png)

Podemos ver logo que o Score do Metacritic e o ano de lançamento são atributos sumamente importantes para determinar o preço de um jogo, ao analisar os lançamentos dos jogos podemos perceber o seguinte:


![Lançamento de jogos](https://raw.githubusercontent.com/liamarguedas/steam-games-price/main/Summary-Charts/Jogos-por-ano-e-preco.png)

No dataset são tratados os jogos mais jogos (Top Games), podemos perceber que a grande maioria de jogos são dos ultimos 3 anos (2020, 2021, 2022) o qual descreve muito bem o preço, pois, jogos antigos serão mais baratos que jogos lançados recentemente. Por isso no gráfico de ano vs. preço é possível ver uma relação linear crescente (Tirando certos outliers dos anos 2011, 2012, 2013)

Na analise exploratoria foi encontrado também uma relação bastante particular, as resenhas dos Curator (Pode se considerar um Curator como Influencer do gaming) junto com as resenhas dos usuários normais. Ao gráficar essa relação encontramos: 

![Relação linear reviews](https://raw.githubusercontent.com/liamarguedas/steam-games-price/main/Summary-Charts/relacao-linear-reviews.png)

Com o aumento das resenhas de usuários as resenhas de  Curator também apresentaba um aumento. É fácil de explicar tal relação, pois, usualmente Curators fazem resenhas de jogos mais populares, por isso, tais jogos jogos populares tem milhares de resenhas de usuários. 


Também foi curioso entender as estadisticas da Steam e compreender que a grande maioria de jogos no Top são de Um jogador, além de outros atributos, tais que:

![Features](https://raw.githubusercontent.com/liamarguedas/steam-games-price/main/Summary-Charts/jogos-features.png)

Como parte do resumo minha tarefa foi trazer algumas das descubertas mais importantes na analise exploratoria, porém eu recomendo ler o projeto inteiro para se familiarizar com a data e realmente comprender que descreve e como descreve nosso target. Pode ler o projeto inteiro fazendo [click aqui](https://github.com/liamarguedas/steam-games-price/blob/main/Steam-Games-Price-pt-br.ipynb).

### Perfil Target

Depois do analise exploratorio, descobrimos o prefil ideal para classificar cada jogo, perfil que se resume em:

**Barato:**

- É de Um Jogador
- Tem armazenamento na SteamCloud.
- É mais velho que as classe Barato e Caro
- Tem menos atualizações que as outras classes
- Tem menos reviews que os jogos Caros porém mais que os jogos Estandar.
- Tem um Ranking PEGI mais familiar
- Tem piores MetacritictScore que as outras clases
- Tem menos idiomas disponíveis
- Tem menos conquistas na Steam
- Tem menos CuratorReviews que os jogos Caros porém mais que os jogos Estandar.

**Caro:**

- É de Um Jogador
- Alguns tem JxJ on-line
- Tem compatibilidade com controle
- Tem Legendas
- Tem Cartas Colecionáveis Steam
- É mais novo que as outras classes.
- Tem atualizações com mais frequência do que as outras classes.
- Tem mais reviews que as outras classes.
- Tem um Ranking PEGI dirigido mais para adultos.
- Tem melhor MetacriticScore que as outras classes.
- Tem mais idiomas disponíveis.
- Tem mais conquistas na Steam
- Tem mais CuratorReviews

**Estandar:**
- É de Um Jogador
- Tem compatibilidade com controle
- Tem armazenamento na SteamCloud
- Mais velho que os jogos Caros porém mais novo do que os jogos Baratos.
- Mais reviews que os jogos Baratos porém menso que os jogos Caros.
- Maior Ranking PEGI que os jogos Baratos porém menor que os jogos Caros.
- Melhor MetacriticScore que os jogos Baratos porém pior que os jogos Caros.
- Mais idiomas disponíveis que os jogos Baratos porém menos que os jogos Caros.
- Mais conquistas na Steam que os jogos Baratos porém menos que os jogos Caros.
- Menos CuratorReviews que ambas classes.

Com estes insights somos capaces de tomar uma decisão para classificar um jogo na loja, resolvendo assim o problema. Porém é sabiamos que era muito trabalho manual, trabalho de comparativa e provavelmente de muitas pessoas. Por isso era escencial treinar um algorithmo de classificação para automatizar todo esse trabalho que o pessoal da loja deveria fazer. 

Para tomar uma decisão eficiente foram utilizadas variedade de metricas para a seleção de um algorithmo capaz de efetuar uma classificação precisa. Tais metricas foram:

**ROC AUC**

O score ROC AUC nos diz o quão eficiente o modelo é. Quanto maior o AUC, melhor é o desempenho do modelo em distinguir entre as classes positivas e negativas. Um score AUC de 1 significa que o classificador pode distinguir perfeitamente entre todos os pontos das classes Positiva e Negativa.

**Accuracy**

Número de previsões corretas feitas pelo modelo dividido pelo número total de previsões. É útil quando as classes alvo estão bem equilibradas.

**Recall**

O recall é a razão tp / (tp + fn) onde tp é o número de verdadeiros positivos e fn é o número de falsos negativos. O recall é, intuitivamente, a capacidade do classificador de encontrar todos as amostras positivas.

**Precisão**

A precisão é a razão tp / (tp + fp) onde tp é o número de verdadeiros positivos e fp é o número de falsos positivos. A precisão é, intuitivamente, a capacidade do classificador de não rotular uma amostra negativa como positiva.

**F1-score**

O score F-beta pode ser interpretado como a média harmônica ponderada da precisão e recall, onde um score F-beta alcança seu melhor valor em 1 e pior score em 0. O score F-beta pondera o recall mais do que a precisão por um fator de beta. beta == 1.0 significa que o recall e precisão têm igual importância.

### Importância das métricas

A gente têm um problema de classificação unbalanceada, por esse motivo, temos que escolher eficientemente quais metricas são as melhores para nosso modelos classificar corretamente as classes. Existem 3 possíveis casos:

1. Quando a classe positiva é menor e a habilidade de detectar corretamente amostras positivas é nosso foco principal (a detecção correta de exemplos negativos é menos importante para o problema), devemos usar a precisão e o recall.

2. Quando queremos dar peso igual à habilidade de prever todas as classes, devemos olhar para a curva ROC (ROC curve).

3. Quando a classe positiva é maior, provavelmente devemos usar as métricas ROC porque a precisão e o recall refletiriam principalmente a capacidade de previsão da classe positiva e não da classe negativa, que naturalmente será mais difícil de detectar devido ao menor número de amostras. Se a classe negativa (a minoria, neste caso) for mais importante, podemos trocar os rótulos e usar precisão e recall.

No problema apresentado para nós, podemos confirmar que encaixa no ponto 2, então nosso foco deve estar nas seguintes métricas:

 - ROC Curve (ROC AUC)

Mesmo assim eu dei bastante importância ao recall de cada classe, utilizando o classification report. Para complementar estas metricas, precisavamos de um referencia. Por isso utilizamos o ZeroR value e Random Rate Classifier para entender qual seria o pior cenario do nosso modelo. Tais baseline scores apresentaram os seguintes resultados:

- **Random Rate Classifier:** 0.4966030135580001
- **ZeroR value:** 0.6318622174381054

Mas o que significam estes scores? Funcionam para entender que nosso modelo tem que obter uma performance maior do que 0.63 para ser efetivo, de outro jeito o modelo não funcionaria de forma correta e teremos que voltar no projeto para achar outra solução ou tentar diferentes transformações. É bom ter um ponto de referencia antes de treinar um modelo.

### Seleção de modelo

Ao trabalharmos com um problema de classificação multi-classe, resolvimos treinar os seguintes modelos:

- k-Nearest Neighbors.
- Naive Bayes.
- Random Forest.
- Gradient Boosting.
- AdaBoostClassifier.

Após o treinamento utilizando validação cruzada, obtemos os seguintes resultados:

![Model Performance](https://raw.githubusercontent.com/liamarguedas/steam-games-price/main/Summary-Charts/Model-statistics.png)

Depois de 5 CV, podemos perceber que os 2 modelos a serem considerados foram RandomForest e GradientBoosting, o qual leva para a decisão final.

## Final Decision

Para solucionar o problema, resolvi utilizar GradientBoosting, pois apresentou uma melhor variação de metricas depois da validação cruzada e outros testes efetuados no projeto. Sabendo o modelo a ser usado, eu comecei com a otimização de parametros para encontrar que parametros do modelo afetam o score na data de treinamento. Os resultados encontrados foram os seguintes:

![Parametros](https://raw.githubusercontent.com/liamarguedas/steam-games-price/main/Summary-Charts/otimiza%C3%A7%C3%A3o-parametros.png)

Podemos enxergar que:

- O score aumenta junto com o valor de learning rate, sendo o melhor 0.15.
- Menor o max_depth melhor o score, sendo o melhor 4.5.
- Menor o min_samples_leaf melhor o score, mas parece que os melhores resultados ficaram em 0.10
- Maior o min_samples split, melhor o score, sendo o melhor 0.36.
- maior o subsample, melhor o socre, sendo o melhor 0.95.

Sabendo o que melhor e piora o score do GradientBoost foi treinando novamente otimizando parametros e conseguimos uma melhora importante na classe Caro (Lembrando que era a classe com menos observações na data), tal que:

**GradientBoosting SEM otimização de parametros**

![GBNoOpt](https://raw.githubusercontent.com/liamarguedas/steam-games-price/main/Summary-Charts/gradient-boost-performance-sem-otimizacao.png)

**GradientBoosting COM otimização de parametros**

![GBOpt](https://raw.githubusercontent.com/liamarguedas/steam-games-price/main/Summary-Charts/gradient-boost-performance-otimizado.png)

## Implantação em produção

Criando um modelo simples, liviano e de fácil manutenção. Seria um poco fora da linha criar uma implantação exagerada, não precisamos um serviço web para o deployment, então a melhor forma de implatação é usando batch prediction. No caso as abordagens abaixo podem ser usadas para implementar previsões em lote:

- A maneira mais simples é escrever um programa em Python e agendá-lo usando o Cron, mas requer esforço adicional para introduzir funcionalidades de validação, auditoria e monitoramento. No entanto, hoje em dia temos muitas ferramentas/abordagens que podem tornar essa tarefa mais simples.

- Escrevendo um job de lote do Spark e agendando-o no yarn e introduzindo logging para monitoramento e funcionalidades de retry.

- Usando ferramentas como Perfect e Airflow que fornecem capacidades de interface de usuário para agendar, monitorar e alertar notificações em caso de falhas.

- Plataformas como Kubeflow, MLFlow e Amazon Sagemaker também fornecem capacidades de implantação e agendamento em lote.

Eu resolvi utilizar Spark para colocar o modelo em produção. Tal que:

![alt text](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*o60YlwFt3wnXlEQ4RuKWqw.png)

## Os resultados do projeto são perfeitos?

Não. Continuamos tendo uma margem de erro bastante grande, o qual não é ideal para um problema de classificação. Porém nós sabiamos disso desde o inicio e nosso objetivo final foi atingido, no caso, reduzir aqueles jogos Caros classificados como Baratos e vice-versa.

## Por que o performance não é ideal?

O modelo confunde muito jogos Estandar com jogos Baratos, de fato uma solução muito eficiente para este problema é conversar com o cliente para tirar essa classe "Estandar" e nós focarmos em classificar Baratos e Caros, onde teriamos um problema bastante diferente. Onde seria necessário realizar outros cortes de buckets e analisar novas estrategias. Sempre adaptando o projeto às necessidades do cliente, 
