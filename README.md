# Biblioteca para Renderização de Grafos Dinamicamente

Esta biblioteca foi desenvolvida para renderizar grafos dinamicamente com seu próprio compilador. Com ela, você pode facilmente criar e conectar pontos para representar grafos de forma visual.

## Como usar

1. **Definindo o padrão de conexão:**
   Vá para o arquivo principal (`main`) e defina o seu padrão de conexão no texto fornecido.

2. **Criando pontos:**
   Para criar um ponto, utilize o seguinte formato:

```
Pn(x,y)
```

Onde:
- `n` é o número do ponto.
- `(x,y)` são as coordenadas do ponto no plano.

3. **Declarando Singletons:**  
Para declarar vértices sozinhos, basta adicioná-lo sem conexões como no
exemplo:

```
Pn(x,y)
```

4. **Conectando pontos:**
Para conectar dois pontos, utilize o seguinte formato:

```
P1(x1,y1) operador_de_conexão P2(x2,y2)
```

Onde:
- `P1(x1,y1)` e `P2(x2,y2)` são os pontos que você deseja conectar.
- `conexão` é o tipo de conexão entre os pontos. As conexões disponíveis são:
  - `->` para conexão direcionada de `P1` para `P2`.
  - `<-` para conexão direcionada de `P2` para `P1`.
  - `-` para conexão não direcionada entre `P1` e `P2`.
  - `<->` para conexão bidirecional entre `P1` e `P2`.

**Nota:** As coordenadas que o compiler utilizará serão sempre as últimas a serem declaradas

5. **Conectando Singletons:**  
Para conectar vértices em loop, basta conectá-lo nele mesmo como no
exemplo:

```
P1(x1,y1) operador_de_conexão P1(x1,y1)
```
6. **Reutilizando pontos:**
Se desejar reutilizar um ponto, basta redeclará-lo conforme descrito no primeiro passo. Exemplo:

```
P1(x1,y1) operador_de_conexão **P2(x2,y2)**
**P2(x2,y2)** operador_de_conexão P3(x3,y3)
```



```bibtex
@software{drayan2024,
  authors = {Drayan S. and Lucchin, Lucca and Nogueira, Matheus G. P. and Geremias, Lucas G. N. and Joel and Antunes, Pedro L. and Zambão, João V.},
  title = {TinyGraph},
  year = {2024},
  university = {Pontifícia Universidade Católica do Paraná - PUCPR}
}
