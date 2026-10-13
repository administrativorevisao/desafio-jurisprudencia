# 1 Ano em 7 Dias — Dias 01 a 04 na plataforma

Produto do JurisClub (Revisão Ensino Jurídico): atualização jurisprudencial para procuradorias em 7 dias. Esta pasta reúne a versão digital dos Dias 01 a 04.

## Conteúdo

| Pasta | O que tem |
|---|---|
| `telas/` | Telas do protótipo: `Dia01` a `Dia04` e `SelosDigitais` (sistema de selos adotado) |
| `dados/` | Material de cada dia em JSON (temas, selos, tese, tópicos, quadros de lei) e, no Dia 01, o caderno de questões |
| `scripts/` | Conversores dos arquivos do Pedagógico (.docx ou .html) para JSON e gerador das telas |
| `assets/` | Logo do 1 Ano em 7 Dias e logo do Revisão |
| `midia/` | Vídeo curto com a jornada do aluno nos Dias 01 a 04 |

## Os dias

| Dia | Disciplina | Temas | Questões |
|---|---|---|---|
| 01 | Direito Administrativo (2026) | 7 | 10 (com gabarito e comentários) |
| 02 | Direito Administrativo (demais anos) | 9 | em breve |
| 03 | Direito Civil e Empresarial (2026) | 8 | em breve |
| 04 | Direito Civil e Direito Empresarial | 10 | em breve |

## Como a tela funciona

- **Material do dia:** temas na lateral com selos; tese no quadro do caderno; tópicos ("O assunto antes do julgamento", "Conclusão" etc.) que abrem e fecham; quadros de lei no formato do material original.
- **Caderno de questões:** o aluno responde, vê a correta, os comentários, as alternativas comentadas e o gabarito; filtros por tema e assunto; cada questão leva de volta ao tema no material.
- **Navegação:** botões "Dia 01" a "Dia 07" no topo; dias sem caderno mostram "em breve".

## Gerar os dados

```bash
pip install python-docx
python scripts/parse_1ano7dias.py "Dia 01 - Direito Administrativo.docx" "Dia 01 - Caderno de Questões.docx" dados/dia01.json
```

O material pode vir em `.docx` ou em `.html` exportado do Word.
