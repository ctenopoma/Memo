---
type: topic
title: ソフトウェア開発への生成AI・LLM適用（2025–2026）
aliases: [GenAI for Software Development, AI支援ソフトウェア開発研究, GenAI SE]
sources: [GenAI-SoftwareDev コレクション（arXiv 12本）]
updated: 2026-06-21
---

# ソフトウェア開発への生成AI・LLM適用（2025–2026）

生成AI・LLM をソフトウェア開発プロセス（コード生成、コードレビュー、エージェント型開発、コンパイラ最適化、要件・アーキテクチャ評価、開発者協働、セキュリティ）へ適用した最新研究（2025–2026年、arXiv オープンアクセス）の総括レポート。鵜林研究室の購読要論文（[[naoyasu-ubayashi]]）の代替として収集した `GenAI-SoftwareDev` コレクション 12 本を根拠とする。実証研究の総括としては [[empirical-software-engineering]]、コード生成の各論は [[llm-code-generation]]、DORA 実務調査は [[dora-ai-assisted-development]] を参照。

---

## 1. 研究動向の俯瞰

2025–2026 年の研究は、単発のコード生成から **「自律エージェントが実運用リポジトリで多ターン作業する」段階** へ重心が移っている。本コレクションの 12 本中 5 本がエージェント型開発を扱い（§2.1）、残りもコード生成の専門ドメイン化（§2.2）、人間-AI 協働の精緻化（§2.3）、品質・セキュリティの批判的評価（§2.4）に分布する。

通底するメッセージは2点に集約される。

1. **「モデルの賢さ」より「足場（scaffolding）」が成果を決める** — ガイダンスファイル（[[probe-refine-coding-agent]]）、エージェントハーネス（[[stamina-bench]]）、コンテキスト注入（[[context-engineering-multi-agent]]）、アーキテクチャ選択（[[capra-arch-feedback]]）といった周辺設計が、モデル規模以上に出力品質へ寄与する。
2. **ベンチマーク高スコア＝真の能力ではない** — 脆弱性検出（[[calibration-vuln-detect]]）や長期セッション耐久性（[[stamina-bench]]）では、見かけの高性能の裏に「理解なき調整」「数ターンでの崩壊」が潜むことが実証された。

---

## 2. サブテーマ別整理

### 2.1 エージェント型ソフトウェア開発（Agentic SE）

実リポジトリで計画・実装・テスト・PR 作成までを担う自律エージェントの設計と限界評価。

- [[phoenix-github-issue]] — 6 専門エージェント＋7 層の安全制御で GitHub イシューを自動解決。SWE-bench Lite で **75% oracle 解決率**、成功実行でリグレッションゼロ。ただし Planner の局所化制限（修正コードの配置パス誤り）が残る。
- [[probe-refine-coding-agent]] — 合成バグ修正プローブでリポジトリガイダンス（AGENTS.md 等）を反復改善。SWE-bench Verified で **33.0%**（ガイダンスなし 25.5% を上回る）。改善は精度向上ではなく**カバレッジ向上**（修正対象ファイルの特定支援）から来る。
- [[n-version-coding-agents]] — 古典的 N 版プログラミングをコーディングエージェントに適用。3 版多数決で平均失敗数を **387.44 → 130.99（約66%減）**。ただし共通モード故障（複数版の同時失敗）は依然残り、独立性仮定は完全には成立しない。
- [[stamina-bench]] — 100 ターン超のマルチターン耐久性ベンチマーク。**全モデルが 5〜6 ターン以内に失敗**。テストフィードバックの付与でパスターン数が最大 **12倍**、ハーネス差で最大 **6倍** の性能差。
- [[context-engineering-multi-agent]] — Elicit / NotebookLM / Claude Code を統合したコンテキスト工学ワークフロー。意図変換＋RAG＋専門サブエージェントで、大規模 Next.js コードベースへの生成精度を単一エージェントより改善。

> **共通知見:** エージェント単体の能力より、(a) テストフィードバックループ、(b) リポジトリ知識の供給、(c) 多様性・冗長性の確保 が信頼性を左右する。[[stamina-bench]] と [[probe-refine-coding-agent]] はいずれも「テスト／ガイダンスがある場合にのみ大きなステップ予算が活きる」と一致して報告している。

### 2.2 コード生成（専門ドメインと低レイヤー）

汎用コード生成から、ドメイン制約の強い領域・低レイヤー領域への展開。

- [[autopass-compiler-tuning]] — LLM エージェントがコンパイラ内部状態（IR・最適化状態）と実行時証拠を参照してコンパイラ性能をチューニング。LLVM -O3 比で x86-64 **1.043倍**／ARM64 **1.117倍**。訓練不要（推論のみ）。
- [[solidity-codegen-llm]] — リポジトリレベル Solidity 生成のベンチマーク SolidityBench（**5,470 件**）。汎用コードモデルは専門ドメインで顕著に性能低下し、**教師あり微調整（SFT）** がドメイン固有制約の内面化に最も有効。プロンプティングのみでは限界。
- [[capra-arch-feedback]] — ソフトウェアアーキテクチャ成果物の評価を自動化するマルチエージェント。決定論的エビデンスアンカリングでハルシネーションを抑制し、基準充足率 **88.8%**。ただし主観評価には人間監視が不可欠。
- [[coracommit-message-gen]] — 類似コミット例の検索（RAG）と並列 LLM 呼び出しでコミットメッセージ生成を改善する VS Code 拡張。BLEU/CIDEr/METEOR/ROUGE-L で既存拡張を上回る。

> **共通知見:** 専門ドメイン（スマートコントラクト、コンパイラ、アーキテクチャ）では「汎用 LLM をそのまま使う」だけでは不十分で、微調整・内部証拠アクセス・例示検索といった**ドメイン適応**が決定的。[[solidity-codegen-llm]] の SFT 優位は、[[calibration-vuln-detect]] の「ファインチューニングは出力分布を変えるが推論は変えない」という指摘と緊張関係にある（§3 参照）。

### 2.3 開発者生産性・人間-AI 協働

ツールの性能ではなく、人間側の使い方・個人差・上流要因に着目した実証研究。

- [[prompt-quality-pull-request]] — プロンプト構造の3次元（Context / Specificity / Verification）が PR の下流アウトカムに与える**段階依存的**影響を 265 件で分析。Specificity・Context は実行可能コード生成に、Verification はコード採用に強く関連。
- [[developer-copilot-interaction]] — 27 人の開発者調査で Copilot Chat との **5 インタラクションモード**と **10 の基礎ニーズ**を特定。問題解決スタイル・経験・性別による認知多様性を既存ツールが十分支援していないと指摘。
- [[coracommit-message-gen]] — ユーザーフィードバック駆動で LLM を動的推薦する点で、人間-AI 協働の実用ツールとしても位置づけられる（§2.2 と重複）。

> **共通知見:** AI 支援の成否は「プロンプト品質」「個人の認知スタイル」という人間側因子に強く依存する。これは [[dora-2025-state-of-ai]] の「AI は増幅器（[[ai-as-amplifier]]）」——既存の能力差を拡大する——という大規模調査の結論とも整合する。

### 2.4 セキュリティ・品質の批判的評価

- [[calibration-vuln-detect]] — 834 件の Linux カーネルサンプル＋厳格な時間分割（CWE-Trace）で、LLM の脆弱性検出が**真の推論ではなくパターンマッチング**であることを診断。ファインチューニングは出力閾値を変えるが決定方策は変えない（「理解なき調整」）。データ汚染も測定可能な優位を与えない。

> **共通知見:** ベンチマークスコアの改善を「能力の獲得」と解釈する危険性への警鐘。評価設計（時間分割・診断指標 DFI/HDD・多ターン化）の重要性を示す。

---

## 3. 対立する主張・未解決の課題

- **ファインチューニング vs. 「理解なき調整」** — [[solidity-codegen-llm]] は SFT がドメイン制約の内面化に最も有効と結論する一方、[[calibration-vuln-detect]] は SFT が真の推論を生まず出力分布の調整に留まると指摘。両者はタスク（生成 vs. 判定）が異なるが、「微調整は何を学習しているのか」は未解決。
- **エージェントの信頼性の壁** — [[phoenix-github-issue]] の高解決率は oracle/小規模サブセット、[[stamina-bench]] は実運用的多ターンで全モデルが早期崩壊。短期ベンチでの成功が長期セッションの信頼性を保証しない。
- **足場依存の代償** — ガイダンス（[[probe-refine-coding-agent]]）・冗長化（[[n-version-coding-agents]]）・コンテキスト工学（[[context-engineering-multi-agent]]）はいずれも有効だが、構築・運用コストと再現性（小サンプル・単一モデル族での評価が多い）が課題。
- **評価の外的妥当性** — [[capra-arch-feedback]]（10 件）、[[context-engineering-multi-agent]]（質的評価）など、サンプル規模・モデル多様性が限定的な予備評価が多い。
- **時期的偏り** — 本コレクションは 2026 年 6 月の cs.SE 投稿が 11 本を占め、2025 年は 1 本（[[context-engineering-multi-agent]]）のみ。2025 年通年の動向把握には SWE-bench 系・Copilot 影響研究の追加収集が必要（[[index]] 補強候補）。

---

## 4. 関連 Topic

- [[llm-code-generation]] — コード生成手法の各論
- [[empirical-software-engineering]] — 実証的 SE 研究の方法・知見
- [[llm-requirements-engineering]] — 要件工学への LLM 適用（[[capra-arch-feedback]] が隣接）
- [[ai-assurance-and-security]] — AI システムの保証・セキュリティ（[[calibration-vuln-detect]] が隣接）
- [[dora-ai-assisted-development]] — DORA による実務・組織レベルの大規模調査

---

## 出典

| エンティティ | arXiv | 原本（正本リポジトリ） |
| --- | --- | --- |
| [[prompt-quality-pull-request]] | [2606.19644](https://arxiv.org/abs/2606.19644) | GenAI-SoftwareDev/pdf/2026_PromptQuality_PullRequest.pdf |
| [[phoenix-github-issue]] | [2606.20243](https://arxiv.org/abs/2606.20243) | GenAI-SoftwareDev/pdf/2026_Phoenix_GitHubIssue.pdf |
| [[probe-refine-coding-agent]] | [2606.20512](https://arxiv.org/abs/2606.20512) | GenAI-SoftwareDev/pdf/2026_ProbeRefine_CodingAgent.pdf |
| [[n-version-coding-agents]] | [2606.20158](https://arxiv.org/abs/2606.20158) | GenAI-SoftwareDev/pdf/2026_NVersion_CodingAgents.pdf |
| [[coracommit-message-gen]] | [2606.19814](https://arxiv.org/abs/2606.19814) | GenAI-SoftwareDev/pdf/2026_CoRaCommit_MessageGen.pdf |
| [[calibration-vuln-detect]] | [2606.20502](https://arxiv.org/abs/2606.20502) | GenAI-SoftwareDev/pdf/2026_CalibrationVulnDetect.pdf |
| [[stamina-bench]] | [2606.19613](https://arxiv.org/abs/2606.19613) | GenAI-SoftwareDev/pdf/2026_StaminaBench_CodingAgent.pdf |
| [[developer-copilot-interaction]] | [2606.19216](https://arxiv.org/abs/2606.19216) | GenAI-SoftwareDev/pdf/2026_DeveloperCopilot_Interaction.pdf |
| [[autopass-compiler-tuning]] | [2606.20373](https://arxiv.org/abs/2606.20373) | GenAI-SoftwareDev/pdf/2026_AutoPass_CompilerTuning.pdf |
| [[solidity-codegen-llm]] | [2606.19988](https://arxiv.org/abs/2606.19988) | GenAI-SoftwareDev/pdf/2026_SolidityCodeGen_LLM.pdf |
| [[capra-arch-feedback]] | [2606.18976](https://arxiv.org/abs/2606.18976) | GenAI-SoftwareDev/pdf/2026_CAPRA_ArchFeedback.pdf |
| [[context-engineering-multi-agent]] | [2508.08322](https://arxiv.org/abs/2508.08322) | GenAI-SoftwareDev/pdf/2025_ContextEngineering_MultiAgent.pdf |

> 原本の正本: `C:\work_space\Paper\GenAI-SoftwareDev\` / 収集台帳: `GenAI-SoftwareDev/README.md`（取得日 2026-06-21）
