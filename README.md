# DIGNIDADE EM AÇÃO R01

Plataforma digital de apoio às ações sociais do Instituto Pelo Bem.

## Funcionalidades da R01
- Página inicial do projeto
- Detalhes do projeto
- Cadastro de voluntários
- Registro de doações
- Tela de sucesso
- Painel simples com listagem de voluntários e doações

## Tecnologias
- Python
- Flask
- Supabase
- HTML + CSS

## Como rodar localmente
```bash
pip install -r requirements.txt
python app.py
```

Acesse:
```bash
http://127.0.0.1:5000
```

## Deploy no Render
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
