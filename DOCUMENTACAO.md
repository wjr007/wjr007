# Perfil GitHub de Walteir Junior

## Estrutura

- `README.md`: conteúdo público exibido no perfil.
- `dark.svg` e `light.svg`: banners por tema do GitHub.
- `.github/workflows/snake.yml`: atualiza a animação de contribuições a cada 12 horas.
- `scripts/generate_profile_banner.py`: fonte reprodutível dos banners.

## Banner

O banner usa a foto atual do perfil apenas como entrada local, sem adicionar a foto original ao repositório. Para atualizar a arte, salve uma foto de retrato em `work/profile-assets/profile-avatar.png` e execute:

```powershell
python scripts/generate_profile_banner.py
```

Depois, publique os dois SVGs gerados na raiz do repositório.

## Configuração manual necessária

1. Em `wjr007/wjr007`, abra **Settings > Actions > General** e configure **Workflow permissions** como **Read and write permissions**. Isto permite ao workflow publicar os SVGs da snake no branch `output`.
2. Execute manualmente o workflow **Generate Snake Animation** uma vez e confirme que o branch `output` foi criado.
3. Para ativar cartões de estatísticas sem limite compartilhado, faça o deploy privado de `anuraghazra/github-readme-stats` no Vercel e salve o token apenas como `PAT_1` nas variáveis de ambiente do Vercel. Nunca faça commit do token. Depois substitua `YOUR_STATS_INSTANCE` no README pelo domínio do seu deploy.

## Segurança

Este repositório não contém tokens, chaves nem a foto-fonte. A única integração com privilégio de escrita é o `GITHUB_TOKEN` temporário fornecido pelo GitHub Actions ao workflow.

