---
type: topic
aliases: [LLMコード生成, Code Generation, GPT-4o]
sources: [sources/ubayashi-bibliography-2024plus.md, sources/2026_SolidityCodeGen_LLM.pdf, sources/2026_AutoPass_CompilerTuning.pdf, sources/2026_CoRaCommit_MessageGen.pdf, sources/2025_ContextEngineering_MultiAgent.pdf]
updated: 2026-06-21
---

# LLMによるコード生成

LLM（GPT-4o等）を用いたコード生成と、入力表現（フローチャート画像など）が生成品質に与える影響の研究。2026年以降は専門ドメイン（Solidity）、コンパイラ最適化、コミットメッセージ生成、マルチエージェント協調など多様なサブテーマが発展。

## 関連論文（鵜林ラボ）
- [[flowchart-image-code-generation]] — プログラムフローチャート画像がGPT-4oのコード生成に与える影響
- [[carla-llm-scenario]] — 要件からの実行スクリプト生成（要件工学と横断）

## 関連論文（GenAI-SoftwareDev 2026）
- [[solidity-codegen-llm]] — SolidityBench: リポジトリレベルのスマートコントラクト生成。SFTがプロンプティングより有効
- [[autopass-compiler-tuning]] — コンパイラ最適化へのLLMエージェント適用（LLVM -O3超え）
- [[coracommit-message-gen]] — RAGベースのコミットメッセージ生成VS Code拡張
- [[context-engineering-multi-agent]] — 意図変換+RAG+マルチエージェントのコンテキスト工学ワークフロー

## 関連トピック
- [[llm-requirements-engineering]]
- [[genai-for-software-development]]

## 関連研究（arXiv・外部）
[[flowchart-image-code-generation]] と直接対応する、図・フローチャートからのコード生成研究。
- Flow2Code: Evaluating Large Language Models for Flowchart-based Code Generation Capability — [arXiv:2506.02073](https://arxiv.org/abs/2506.02073) (2025) ※フローチャート→コード生成、最も近い先行研究
- Unified Modeling Language Code Generation from Diagram Images Using Multimodal LLMs — [arXiv:2503.12293](https://arxiv.org/abs/2503.12293) (2025)
- Assessing GPT-4-Vision's Capabilities in UML-Based Code Generation — [arXiv:2404.14370](https://arxiv.org/abs/2404.14370) (2024)
- Towards Making Flowchart Images Machine Interpretable — [arXiv:2501.17441](https://arxiv.org/abs/2501.17441) (2025)

## 出典
- sources/ubayashi-bibliography-2024plus.md
- sources/2026_SolidityCodeGen_LLM.pdf (arXiv:2606.19988)
- sources/2026_AutoPass_CompilerTuning.pdf (arXiv:2606.20373)
- sources/2026_CoRaCommit_MessageGen.pdf (arXiv:2606.19814)
- sources/2025_ContextEngineering_MultiAgent.pdf (arXiv:2508.08322)
- arXiv 検索（2026-06-20、2026-06-21更新）
