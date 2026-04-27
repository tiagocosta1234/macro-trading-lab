# 📈 Yield Sentinel

Este é o meu primeiro passo no mundo do Quant Trading. Em vez de ficar só pela teoria, decidi construir uma ferramenta que me ajudasse a perceber o que se passa realmente com o "preço do dinheiro".

### Porquê este projeto?
Inspirado pelo Gary Stevenson, percebi que a **Curva de Rendimentos (Yield Curve)** é o gráfico mais importante do mundo. Quando ela inverte (o spread 10Y-2Y fica negativo), o mercado está a dizer-nos que algo vai correr mal na economia. 

Este script monitoriza esse sinal em tempo real para eu não ter de ir ver ao site da Bloomberg todos os dias.

### O que é que isto faz?
- Saca os dados das taxas de juro de 2 e 10 anos (EUA) via `yfinance`.
- Calcula o diferencial (Spread) para ver se estamos em território de recessão.
- Gera um gráfico limpo para análise visual rápida.

### Como correr
Se tiveres Python instalado, é só fazer:
1. `pip install yfinance pandas matplotlib`
2. `python sentinel.py`

### O que vem a seguir?
- Adicionar o spread de crédito da Zona Euro (Portugal vs Alemanha).
- Criar alertas no terminal quando o spread mudar bruscamente.