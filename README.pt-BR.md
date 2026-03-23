# Nati's Recipes

<div align="center">

![Mockup do site](nati-recipe.png)

![Versão](https://img.shields.io/badge/version-1.0.0-blue?style=for-the-badge)
![Licença](https://img.shields.io/badge/licen%C3%A7a-Non--Commercial-red?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MkDocs](https://img.shields.io/badge/MkDocs-Material-526CFE?style=for-the-badge&logo=materialformkdocs&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-Automation-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)

</div>

[To read in English, click here!](./README.md)

## Sobre o Projeto

Nati's Recipes é um site que criei para organizar as receitas da minha namorada (Natalia), separadas por país de origem. O conteúdo é escrito em Markdown e o site é gerado com **MkDocs + Material Theme**, hospedado via **Discloud** com rebuild automático a cada push. Para facilitar a adição de novas receitas, existe um fluxo de automação completo no **n8n**: basta preencher um formulário e o fluxo normaliza o título, gera o slug, monta o arquivo `.md` com o template padrão, posiciona na pasta correta e faz o commit automaticamente no repositório.

## Features

| Recurso | Descrição |
|---|---|
| **Catálogo por país** | Receitas organizadas em pastas por origem (`brazil/`, `france/`, `fusion/`, etc.), com navegação automática pelo plugin `awesome-pages`. |
| **Template padronizado** | Cada receita segue um layout consistente com imagem, ingredientes (admonition), utensílios, informações e modo de preparo. |
| **Tema customizado** | Material Theme com paleta de cores personalizada, suporte a modo escuro/claro e CSS próprio para imagens de receitas. |
| **Busca integrada** | Plugin de busca com sugestão e destaque de termos diretamente no site. |
| **Adição via formulário** | Formulário externo conectado ao n8n. Nenhum arquivo precisa ser criado manualmente. |
| **Automação n8n** | Fluxo completo que recebe o formulário, normaliza dados, gera slug, monta o `.md`, posiciona o arquivo e faz commit no repositório. |
| **Deploy automático** | A cada push, o Discloud reinicia o container, o `app.py` roda `mkdocs build` e serve o site estático via Flask na porta 8080. |
| **Rebuild no boot** | O servidor Flask sempre executa `mkdocs build` ao iniciar, garantindo que o conteúdo mais recente esteja disponível sem etapa manual. |

## Arquitetura

O `app.py` é o entry point: ao iniciar, executa `mkdocs build` para gerar o site estático na pasta `site/` e sobe um servidor Flask que serve os arquivos gerados. O conteúdo vive em `docs/` organizado por país e o plugin `awesome-pages` monta a navegação automaticamente a partir da estrutura de pastas. O `mkdocs.yml` centraliza tema, plugins, extensões Markdown e a URL do formulário n8n exposta como botão "Add Recipe" no header do site.

## Tecnologias Utilizadas

- **[MkDocs](https://www.mkdocs.org/)** - gerador de site estático a partir de arquivos Markdown; toda a navegação, busca e build são gerenciados por ele.
- **[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)** - tema com paleta customizável, modo escuro/claro, admonitions e extensões avançadas de Markdown.
- **[mkdocs-awesome-pages-plugin](https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin)** - gera a navegação lateral automaticamente a partir da estrutura de pastas, sem precisar listar páginas no `mkdocs.yml`.
- **[Flask](https://flask.palletsprojects.com/)** - servidor leve que serve os arquivos estáticos gerados pelo MkDocs e lida com roteamento de paths no ambiente Discloud.
- **[n8n](https://n8n.io/)** - plataforma de automação que processa o formulário de receitas, gera os arquivos e realiza o commit no repositório.
- **[Discloud](https://discloudbot.com/)** - hospedagem do container Python com reinício automático a cada push no repositório.

## Estrutura de Pastas

```
natis-recipes/
│
├── app.py                  # Entry point: build do MkDocs + servidor Flask
├── mkdocs.yml              # Configuração do site (tema, plugins, extensões)
├── requirements.txt        # Dependências Python
├── discloud.config         # Configuração do deploy (Discloud)
│
├── n8n/
│   └── workflow.json       # Fluxo de automação para adição de receitas
│
└── docs/
    ├── images/             # Imagens das receitas
    ├── stylesheets/        # CSS customizado (tema e imagens)
    │
    ├── brazil/             # Receitas brasileiras
    ├── france/             # Receitas francesas
    ├── fusion/             # Receitas fusion / internacionais
    ├── asia/               # Receitas asiáticas
    ├── cuba/               # Receitas cubanas
    ├── germany/            # Receitas alemãs
    └── greece/             # Receitas gregas
```

## Como Adicionar Receitas

### Via formulário (método principal)

Acesse o formulário disponível no botão **"Add Recipe"** no header do site ou diretamente via n8n. O fluxo cuida de tudo automaticamente:

1. Normalização do título e geração do slug
2. Criação do arquivo `.md` com o template padrão
3. Posicionamento na pasta correta por país
4. Processamento da imagem (se enviada)
5. Commit automático no repositório e deploy automático no Discloud

### Via arquivo manual

Crie um arquivo `.md` em `docs/<pais>/<slug-da-receita>.md` seguindo o template:

```markdown
![Nome da Receita](../images/slug-da-receita.jpg){ .recipe-img }

!!! abstract "Ingredientes"
    - item 1
    - item 2

!!! tip "Utensílios"
    - item

!!! info "Informações"
    **Custo:** $
    **Tempo de preparo:** X min
    **Rendimento:** X porções

## Modo de Preparo

1. Passo 1
2. Passo 2
```

## Fluxo n8n

O fluxo em `n8n/workflow.json` processa as submissões do formulário:

1. Recebe os dados do formulário (título, país, ingredientes, modo de preparo, imagem)
2. Normaliza o título e gera o slug (`minúsculas-com-hífens`)
3. Monta o conteúdo Markdown com o template padrão
4. Posiciona o arquivo na pasta correta dentro de `docs/`
5. Faz commit e push no repositório e o Discloud detecta o push e reconstrói o site

## Licença

Distribuído sob licença não comercial personalizada. Você pode usar, copiar e modificar este projeto para fins pessoais e não comerciais, desde que mantenha os créditos ao autor original. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">
  Desenvolvido por <a href="https://giovannitavares.com">Giovanni Tavares</a>
</div>
