# Gerador de Assinatura de E-mail — SCI-AGRO

Ferramenta interna para os colaboradores da SCI-AGRO gerarem a própria assinatura de e-mail, seguindo o padrão visual oficial da marca.

## Como usar

Abra o arquivo **`index.html`** direto no navegador (funciona offline, sem precisar instalar nada). Preencha seus dados, ajuste a foto se quiser, confira a pré-visualização e exporte:

- **Baixar assinatura em PNG** — gera uma imagem em alta resolução pronta pra usar como assinatura em qualquer cliente de e-mail (é só colar a imagem).
- **Gerar código HTML da assinatura** — gera o código HTML para colar na opção "Editar em HTML" das configurações de assinatura do Gmail, Outlook, etc. A foto (ou a logo da SCI-AGRO, quando não há foto) já vêm embutidas no próprio código.

Se ninguém escolher uma foto, a logo da SCI-AGRO aparece automaticamente no lugar dela.

## Hospedar online (opcional)

Como é um arquivo único e autocontido, dá pra publicar este repositório com o **GitHub Pages** (Settings → Pages → Deploy from branch → `main` / `root`) e distribuir um link direto para o time, sem precisar mandar o arquivo por e-mail toda vez.

## Estrutura do repositório

```
index.html          → a ferramenta pronta para uso (é o único arquivo necessário para usar ou hospedar)
source/              → código-fonte para manutenção futura
  build3.py           → script Python que gera o index.html
  html2canvas.js       → biblioteca usada para exportar a assinatura em PNG
  ai/                  → assets extraídos da arte original (.ai) usados pelo build: logo em base64, caminhos SVG, etc.
```

Para gerar o `index.html` novamente a partir do código-fonte (por exemplo, depois de editar `build3.py`):

```bash
cd source
python3 build3.py
```

Isso recria `index.html` na pasta `source/` — é só mover o arquivo gerado para a raiz do repositório.

## Sobre o design

O layout, as cores e os ícones seguem exatamente a arte original em vetor (`.ai`) da identidade visual da SCI-AGRO, incluindo o recorte em formato de onda característico do cartão.
