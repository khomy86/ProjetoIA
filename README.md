# ProjetoIA

Vou ajudar a criar um README.md bem estruturado para o projeto do GitHub.



```markdown
# Previsão de Preços de Voos usando Aprendizagem Máquina

## Descrição do Projeto

Este projeto implementa um sistema avançado de previsão de preços de voos utilizando técnicas de aprendizagem máquina. O sistema combina dois modelos complementares - XGBoost e Redes Neuronais Profundas - para prever preços de passagens aéreas com alta precisão.

## Principais Características

- Implementação de modelo XGBoost com otimização GPU
- Arquitetura de Rede Neuronal Profunda com múltiplas camadas
- Pré-processamento robusto de dados
- Normalização e codificação avançada de características
- Sistema de treino com validação cruzada
- Métricas de avaliação abrangentes

## Requisitos

- Python 3.8+
- PyTorch
- XGBoost
- NVIDIA GPU (recomendado)
- Bibliotecas adicionais listadas em `requirements.txt`

## Instalação

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install --upgrade xgboost
pip install -r requirements.txt
```

## Estrutura do Projeto

```
├── data/
│   └── Clean_Dataset.csv
├── models/
│   ├── neural_network.py
│   └── xgboost_model.py
├── utils/
│   └── preprocessing.py
├── main.py
└── README.md
```

## Características do Modelo

### Pré-processamento
- Normalização de dados numéricos
- Codificação de variáveis categóricas
- Transformação logarítmica de preços
- Mapeamento de períodos temporais
- Tratamento de valores ausentes

### Arquitetura da Rede Neuronal
- 3 camadas ocultas (256, 128, 64 neurónios)
- Normalização por lotes
- Função de ativação LeakyReLU
- Dropout para regularização
- Otimizador AdamW

### Configuração XGBoost
- Otimização GPU
- Early stopping
- Hiperparâmetros otimizados
- Validação cruzada

## Resultados

O sistema alcançou resultados excecionais na previsão de preços:

### XGBoost
- RMSE: 40,65€
- MAE: 21,64€
- R² Score: 0,9740

### Rede Neuronal
- RMSE: 47,54€
- MAE: 25,79€
- R² Score: 0,9645

## Utilização

1. Prepare o conjunto de dados:
```python
df = pd.read_csv('data/Clean_Dataset.csv')
```

2. Execute o pipeline completo:
```python
python main.py
```

## Metodologia

O projeto segue uma metodologia rigorosa que inclui:
1. Análise exploratória de dados
2. Pré-processamento robusto
3. Treino de modelos com validação cruzada
4. Avaliação comparativa de performance
5. Otimização de hiperparâmetros


## Autores

Zakhar Khom'yakivskyy - 30011355
Ivanilson Braga - 30010789
Ektiandro Elizabeth - 30011479


