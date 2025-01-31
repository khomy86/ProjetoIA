# Previsão de Preços de Voos Utilizando Técnicas de Aprendizagem de Máquina

## Descrição
Este projeto implementa um sistema de previsão de preços de voos utilizando técnicas avançadas de aprendizagem máquina. O sistema utiliza diferentes modelos (Regressão Linear, Random Forest e XGBoost) para prever preços de passagens aéreas com base em diversos fatores como data do voo, companhia aérea, rota e antecedência da reserva.

## Estrutura do Projeto

O projeto contém os seguintes notebooks:
* `analise_dados.ipynb` - Análise exploratória detalhada dos dados
* `modeltreinadonoptimizado.ipynb` - Treino inicial dos modelos
* `modeloajustado.ipynb` - Versão otimizada dos modelos
* `prep_dados_treino.ipynb` - Preparação dos dados para treino

## Requisitos

Os notebooks foram desenvolvidos e testados no Google Colab com:
* Python 3.8+
* Principais bibliotecas:
  - pandas
  - numpy
  - scikit-learn
  - xgboost
  - matplotlib
  - seaborn

## Resultados
O modelo Random Forest alcançou os melhores resultados:
* MAE: 20,22€
* RMSE: 39,51€
* R²: 0,963

## Autores
* Zakhar Khom'yakivskyy – 30011355
* Ivanilson Braga – 30010789
* Ektiandro Elizabeth - 30011479

