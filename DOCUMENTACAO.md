# Perfil GitHub de Walteir Junior

## Estrutura e publicação

- `README.md`: apresentação pública, habilidades por área, projetos e contribuição.
- `dark.svg` e `light.svg`: banners com foto pública do perfil incorporada ao SVG, tipografia e movimento.
- `scripts/generate_profile_banner.mjs`: fonte atual dos banners, usando apenas módulos nativos do Node.js.
- `scripts/generate_profile_banner.py`: gerador do experimento antigo, preservado como histórico; não é usado pelo README atual.
- `.github/workflows/snake.yml`: gera a cobrinha a cada 12 horas, em pushes para main ou por execução manual.

O GitHub publica o README de `wjr007/wjr007` no perfil de mesmo nome. Não há servidor ou dependência de instalação para exibir o perfil.

## Design e movimento

Paleta escura: fundo `#0B1623`, texto `#EFF8FA`, secundário `#9BB1C2`, ciano `#55DDE0`, verde-água `#7AE2C3`. O banner claro utiliza fundo `#F3F8FA` com texto e acentos escuros.

O retrato tem deslocamento vertical suave; um arco gira lentamente. As três habilidades do rodapé aparecem em sequência uma vez, permanecendo legíveis. O CSS do banner desativa esses movimentos com `prefers-reduced-motion: reduce`. A animação da cobrinha é produzida pelo gerador externo e não herda esse controle.

O README mantém nome, formação, habilidades e links como texto independente das imagens. Não usa JavaScript nem CSS na página do GitHub; o movimento fica dentro dos SVGs. A seleção do banner claro/escuro usa `picture`.

## Alterações rápidas

Edite textos, projetos e contatos em `README.md`. Para editar o banner, altere `renderBanner` no gerador e execute na raiz:

```sh
node scripts/generate_profile_banner.mjs
```

Isso atualiza os dois SVGs da raiz. A foto pública atual do GitHub está incorporada como PNG no SVG. O gerador não baixa fotos nem precisa de Pillow; o arquivo de origem não foi retocado.

Para mudar as cores da cobrinha, edite `color_snake` e os cinco valores de `color_dots` no workflow. A primeira cor representa ausência de contribuição; as seguintes representam intensidade crescente. Os SVGs gerados são publicados no branch `output`.

## Serviços e diagnóstico

Os ícones usam skillicons.dev; as estatísticas recolhidas em um bloco expansível usam github-readme-stats.shion.dev. São serviços externos e podem falhar. Textos e links continuam utilizáveis sem eles.

Se o banner não refletir a última versão, confira os SVGs em main e recarregue o perfil; o cache de imagens do GitHub pode atrasar a atualização.

Se a cobrinha não atualizar, confira o workflow **Generate Snake Animation** em Actions e os arquivos do branch output. O workflow declara `contents: write` para publicar os arquivos com o token temporário do GitHub. Não adicione tokens pessoais ao README ou ao repositório; políticas da organização podem limitar Actions.

## Verificação e histórico

- Reorganizada a leitura: apresentação → conhecimentos → projetos → contribuições → contato.
- Incorporada a foto pública do perfil com novo banner e entrada sequencial de habilidades.
- Substituída a paleta roxa da cobrinha por azul, ciano e verde-água.
- Mantidas as informações de graduação e aprendizado, sem afirmar senioridade ou proficiência não comprovada.

## GIF pixel art

O GIF indicado pelo proprietário aparece abaixo do banner e ocupa a largura disponível do README. Usa a URL pública permanente de user-images.githubusercontent.com, verificada com resposta HTTP 200 e tipo image/gif. O link privado temporário com JWT não foi incluído no repositório. A animação mostra uma cena pixel art de programação. O GIF é hospedado externamente, não foi editado e não oferece controle de redução de movimento; pode ser removido pelo bloco de imagem correspondente no README.
