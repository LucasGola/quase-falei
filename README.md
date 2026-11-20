# Quase Falei

Jogo de adivinhação em equipe para jogar em um celular passado de mão em mão. Quem explica tem que fazer o próprio time adivinhar a palavra da carta sem falar nenhuma das 5 palavras proibidas.

É um arquivo HTML só, sem instalação, sem servidor e sem internet depois de aberto.

## Como jogar

1. Configure os dois times (nome, cor e, se quiser, os jogadores), o tempo da rodada e quantas rodadas cada time joga (ou ∞).
2. Os times se alternam. Em cada rodada, quem explica segura o celular e o time tenta adivinhar.
3. Para cada carta, arraste:

| Gesto | Significa | Ponto para |
|---|---|---|
| → direita | Acertou | o time da vez |
| ← esquerda | Falou uma palavra proibida | o time adversário |
| ↑ ou ↓ | Pular | ninguém |

- **Pulo:** só 1 por rodada. A carta pulada volta para o baralho.
- **Tempo esgotado:** a carta que estava na mão volta para o baralho, sem ponto.
- **Desfazer:** volta a última ação da rodada, para corrigir um arraste errado.
- Cartas acertadas ou com falta saem do baralho e não voltam na mesma sessão.
- A sessão termina quando as rodadas acabam, quando o baralho acaba ou quando alguém toca em **Encerrar sessão**.

Se você fechar o jogo no meio, a sessão fica salva no navegador e aparece **Continuar sessão** quando você abrir de novo.

## Como abrir

Abra o `index.html` num navegador. No celular, use o Chrome ou o Firefox. Os visualizadores de arquivo de apps como Drive e WhatsApp podem não rodar o jogo.

## Cartas

As cartas ficam na planilha `cartas.xlsx`:

- coluna **A**: título da carta
- coluna **B**: as 5 palavras proibidas, separadas por vírgula
- a primeira linha é o cabeçalho

Depois de alterar a planilha, rode:

```
python atualizar_cartas.py
```

O script copia as cartas para dentro do `index.html`, entre os marcadores `/*CARTAS-INICIO*/` e `/*CARTAS-FIM*/`. Ele não grava nada se alguma linha não tiver exatamente 5 palavras ou se houver título repetido, e diz qual linha corrigir. Precisa só do Python 3, sem bibliotecas extras.

Não edite a lista de cartas direto no `index.html`: ela é sobrescrita na próxima vez que o script rodar.

## Arquivos

| Arquivo | O que é |
|---|---|
| `index.html` | O jogo inteiro (HTML, CSS, JS e as cartas) |
| `cartas.xlsx` | A lista de cartas, que é a fonte de verdade |
| `atualizar_cartas.py` | Copia as cartas da planilha para o jogo |
