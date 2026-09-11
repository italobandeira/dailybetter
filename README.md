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
- `assets/`: fonte Nunito, carinhas e screenshots reais do app.

Somente HTML, Tailwind e JavaScript; nenhum framework de aplicação ou build é necessário. Também é possível abrir `index.html` diretamente no navegador, mantendo a pasta `assets` e `main.js` ao lado dele. O Tailwind 3.4.17 é carregado pelo CDN oficial, e GSAP/ScrollTrigger 3.12.7 pelo cdnjs; é necessária conexão para carregar essas bibliotecas. As interações funcionam mesmo se GSAP não carregar. A preferência de movimento reduzido desativa as animações.

O link para o Google Play usa o pacote `com.iflag.dailybetter_moodtrack`. A ficha deve estar publicada para esse destino estar disponível. O contato utiliza o endereço público da landing de referência: `iflagdev@gmail.com`. A página não coleta nem armazena os humores selecionados na demonstração.

Para hospedar, publique todo o conteúdo desta pasta. Não é preciso substituir `web/index.html`, que pertence ao projeto Flutter. A página foi criada localmente e não foi publicada automaticamente.
