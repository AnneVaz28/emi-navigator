
# EMI Navigator 2.0

Protótipo em Streamlit para transformar o EMI em uma camada de diagnóstico e apoio à decisão.

## Fluxo

Empresa → Questionário EMI → Cálculo → Diagnóstico → Forças/Dores → Gap → Prioridade → Roadmap → Reavaliação.

## Importante

O núcleo do EMI segue as seis dimensões:
- KNO — Conhecimento e Transferência
- INO — Inovação e Experimentação
- VAL — Criação e Captura de Valor
- FOM — Fomento e Financiamento
- INF — Infraestrutura
- POL — Políticas e Regulação

As camadas de importância, gap, prioridade e roadmap são extensões de protótipo e precisam de validação empírica antes de serem apresentadas como instrumento validado.

## Como executar

No terminal do VS Code:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
