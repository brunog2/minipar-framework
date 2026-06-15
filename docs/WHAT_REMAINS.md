# O que ainda falta — pós-implementação conformidade técnica

**Data:** 8 de junho de 2026  
**Status:** Fases 1–7 do plano de conformidade **implementadas** no repositório.

---

## Implementado nesta entrega

| Fase | Entrega |
|------|---------|
| **0** | URLs GitHub unificadas, `scripts/e2e-smoke.sh` |
| **1** | `channels/socket_channel.py` — broker TCP, `s_channel`/`c_channel` |
| **2** | `exec_par` sem `Queue`; IPC via broker socket |
| **3** | Workers MiniPar, `14_distributed_menu.minipar`, coord IP:porta |
| **4** | `ms-semantic` → `semantic_full.py` + `SemanticAnalyzer` |
| **5** | `runtime/minipar_rt.c`, emissão PAR/canais em `c_codegen.py` |
| **6** | `GET /variants`, `GET /recommendations`, painel MS na UI |
| **7** | Documentação sincronizada + [`docs/VALIDATION.md`](VALIDATION.md) |

---

## Pendências operacionais (não código)

- [x] Rodar `./scripts/validate-all.sh` — **15/15 PASS** (8/jun/2026)
- [x] Compilar PDF local (`./scripts/build-pdf.sh`; artefatos no `.gitignore`)
- [x] `./scripts/clean.sh` — limpar LaTeX/dist/caches antes do push
- [ ] Upload opcional Overleaf (`./scripts/package-overleaf.sh` → `overleaf-report.zip`)
- [ ] Completar **nomes completos** na capa ([`docs/report-cover-info.tex`](report-cover-info.tex))
- [ ] Inserir **URL do vídeo** (opcional) na capa — testes E1--E12 passo a passo
- [ ] Ensaio oral [`BANCA_NARRATIVE.md`](./BANCA_NARRATIVE.md)

---

## Trabalho futuro (opcional)

- Codegen Rust/ARM com `minipar_rt`
- Hotspots formais lexer/parser (autômatos vs manual)
- Métricas formais de reuso (% LOC)
- `pytest` automatizado no CI
