<!-- sweeper（sinoda1114/ci-standard）が配布した骨格。自由に編集してよい（sweeper は無いときに置くだけで、以後は触らない） -->
# AGENTS.md — AI エージェント向けプロジェクト指示

Claude Code / Codex / Cursor 共通の入口です。運用ルールの詳細は作者のグローバル設定にあり、
ここには他ツールでも守れる最小限の要約と、このリポ固有の値だけを置きます。
この骨格より前からある指示ファイル（`CLAUDE.md` `.cursorrules` 等）に固有の内容がある場合は、そちらを正とします（この骨格は後から自動で置かれたものです。同時に置かれた骨格の `CLAUDE.md` はこのファイルを指すだけです）。

## 運用ルール（要約）

- 既定ブランチ（`origin/HEAD`。多くは main）に直接 commit / push しない。`feat|fix|chore/<topic>` ブランチ → PR → squash マージ。
- ブランチは `git fetch origin` の後に既定ブランチ（`origin/HEAD`）起点で切る。並行作業は 1 エージェント = 1 worktree。
- push 前にレビューを通す（Claude Code は `/ai-review`）。High があれば push しない。
- CI がある場合は緑になってからマージする。デプロイがある場合は git 駆動（既定ブランチへのマージ = 本番）で、手動デプロイしない。
- タスクと PR の状態は GitHub（Issue / Project / `gh pr view`）を正とし、記憶で語らない。
- テスト先行（TDD）。検証は AI 自身が実行して PASS / FAIL を示す。
- lockfile をコミットし、依存は lockfile どおりに入れる（`npm ci` / `pnpm install --frozen-lockfile` / `uv sync --frozen` 等）。秘密情報をログ・出力・コミットに出さない。

## このプロジェクト固有の値（TODO: 埋める）

| 項目 | 値 |
|---|---|
| 目的 | |
| 技術スタック | |
| デプロイ先 / 本番 URL | |
| タスク管理（Project 板） | |
