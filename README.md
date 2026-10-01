# Landing page do DailyBetter

Landing page estática em português, inspirada na estrutura comercial da landing do BetterDay e adaptada à identidade visual do DailyBetter.

## Visualizar localmente

Na raiz do projeto:

```powershell
python -m http.server 4173 --directory landing
```

Abra `http://localhost:4173/`.

## Estrutura

- `index.html`: conteúdo em português, layout em Tailwind e metadados de compartilhamento.
- `main.js`: menu móvel, demonstração de humor, troca de tema da prévia, galeria e animações GSAP.
- `contact.html` + `contact.css`: página de contato do desenvolvedor (usa também `legal.css`).
- `privacy.html`, `terms.html` e `legal.css`: documentos legais.
- `assets/`: fonte Nunito, carinhas e screenshots reais do app.
- `blog/` + `blog.css`: blog em português (índice e artigos).
- `en/`: versão em inglês (en-US) de todas as páginas, incluindo `en/blog/`.
- `sitemap.xml` e `robots.txt`: SEO. Cada página declara `canonical` e `hreflang` (pt-BR, en, x-default).

## Idiomas

O português fica na raiz e o inglês em `en/`, com os mesmos nomes de arquivo (exceto os slugs dos artigos). Toda página tem o botão PT/EN no cabeçalho e o link no rodapé. Os textos interativos da home (demonstração de humor, troca de tema, menu) ficam em atributos `data-*` no HTML, então `main.js` serve aos dois idiomas. Ao alterar um texto, altere as duas versões.

## Blog

Os artigos são HTML estático gerado por `tools/build_blog.py` (Python 3, sem dependências). Para publicar um novo artigo:

1. Adicione o conteúdo em `tools/posts.py` (versões `pt` e `en`, slug, data e corpo em HTML).
2. Na raiz do projeto, rode `python tools/build_blog.py`.
3. O script recria os índices do blog, os artigos, `sitemap.xml` e `robots.txt`.

O cabeçalho e o rodapé das páginas internas vêm de `tools/site_chrome.py`. Depois de publicar, envie o `sitemap.xml` no Google Search Console.

Somente HTML, Tailwind e JavaScript; nenhum framework de aplicação ou build é necessário. Também é possível abrir `index.html` diretamente no navegador, mantendo a pasta `assets` e `main.js` ao lado dele. O Tailwind 3.4.17 é carregado pelo CDN oficial, e GSAP/ScrollTrigger 3.12.7 pelo cdnjs; é necessária conexão para carregar essas bibliotecas. As interações funcionam mesmo se GSAP não carregar. A preferência de movimento reduzido desativa as animações.

O link para o Google Play usa o pacote `com.iflag.dailybetter_mood_tracker`. A ficha deve estar publicada para esse destino estar disponível. O contato utiliza o endereço público da landing de referência: `iflagdev@gmail.com`. A página não coleta nem armazena os humores selecionados na demonstração.

Para hospedar, publique todo o conteúdo desta pasta. Não é preciso substituir `web/index.html`, que pertence ao projeto Flutter. A página foi criada localmente e não foi publicada automaticamente.
