---
type: topic
aliases: [Legacy Code Migration, レガシーコード等価移行, Legacy Modernization]
sources: [LegacyCoding/REPORT_レガシーコード等価移行_研究提案.md, LegacyCoding/2605.17535_AgentModernize_JA.md, LegacyCoding/*.pdf]
updated: 2026-06-21
---

# レガシーコード等価移行 — 研究領域の総括

LLM を使ってレガシーコード（COBOL, Fortran, PL/SQL, C 等）を現代言語（Java, Python, Rust, C++, Kokkos 等）に**振る舞い等価性を保証しながら移行**する研究領域。2025〜2026年にかけて大量の論文が発表されている新興フィールド。

## 事業的背景（論文に記載された事実）

- COBOL, Fortran, PL/SQL に精通した技術者は減少し、習得コストが上昇（[[agent-modernize-bsg]], [[plsql-to-java-case-study]]）
- Commonwealth Bank of Australia は COBOL→Java 移行に約5年・約7.5億ドルを投資
- 米連邦政府のレガシーは稼働30〜60年に及ぶ
- 科学計算 Fortran は GPU ヘテロ環境への対応が急務（[[fortran-to-kokkos-agent]]）
- 規制産業（通信・金融・医療）はビジネスルール台帳・等価性レポートという**監査証跡**を必要とする

## 技術的課題

### 直接翻訳は信頼できない
- LLM 翻訳の正答率は 2.1〜47.3%（[[intent-preserving-pipeline]] 引用）
- 翻訳の最大 77.8% がコンパイル不能か誤結果
- **「コンパイル・実行できる ≠ 振る舞いが等価」**（[[agent-modernize-bsg]] の中心主張）

### 等価性検証が難しい
- テストスイートは不完全 → 偽の等価・偽の非等価（[[match-fix-agent]]）
- 評価パイプライン自体の不備 → 偽の失敗（[[beyond-translation-accuracy]]）
- 数値計算では「ビット完全一致」が基準になれない（[[fortran-to-cpp-llm]]）

### API統合・フレームワーク適合
- 生成コードが本番フレームワーク・API に統合できないと実用にならない（[[legacy-translate-api-aware]]）

## 収束する解決パターン（3つの打ち手）

### A: 生成前の中間仕様（contract-first / glass-box）

| 手法 | 中間表現 | 特徴 |
|-----|---------|------|
| [[agent-modernize-bsg]] | Behavioral Specification Graph (BSG) | 事前/事後/不変条件付き有向グラフ |
| [[intent-preserving-pipeline]] | 言語中立アルゴリズム | I/O 契約・数値規則・ループ境界 |
| [[babel-coder]] | NL 仕様 | テストで精緻化 |

### B: 生成＆検査 + フィードバックループ（自己修復）

| 手法 | 検査方法 | フィードバック先 |
|-----|---------|----------------|
| [[c-to-rust-feedback-loops]] | Rust コンパイラ + 差分ファジング | LLM 再プロンプト |
| [[fortran-to-kokkos-agent]] | 実行・テスト | 専門エージェント |
| [[agent-modernize-bsg]] | 差分トレース解析 | Transformer（的を絞った修正） |
| [[legacy-translate-api-aware]] | コンパイラ + API 提案 | Refinement Agent |

### C: 等価性検証・修復の独立強化

| 手法 | 特徴 |
|-----|------|
| [[match-fix-agent]] | 言語非依存 LLM ベース等価性検証&修復 |
| [[beyond-translation-accuracy]] | 評価標準の健全化（偽陰性の除去） |
| [[human-ai-partnership-code-migration]] | 人間の Director/Reviewer 役割設計 |

## 主要な定量結果

| 論文 | 主要指標 | 値 |
|-----|---------|---|
| [[migration-bench]] | pass@1（Java 移行） | 53〜72% |
| [[legacy-translate-api-aware]] | コンパイル可 / テスト通過 | 45.6% / 30.9% (+8%/+3%) |
| [[agent-modernize-bsg]] | 振る舞い等価率 (BER) | 9.4〜19.4%（Full AM） |
| [[match-fix-agent]] | 等価判定出力率 / 修復成功率 | 99.2% / 50.6% |
| [[intent-preserving-pipeline]] | 正答率向上 | 67.7%→78.5% (+10.8pt) |
| [[babel-coder]] | 平均正答率 | 94.16% |
| [[fortran-to-kokkos-agent]] | 完走率（GPT-5） | 全カーネル完走 |

## 研究ギャップ（未充足・差別化ポイント）

1. **物理/普遍知見をオラクルにする × LLM 移行 = 「橋渡し未統合」**  
   MT/MR・MMS・コード検証は確立済み（[[metamorphic-testing-oracle-problem]], [[mms-elastostatic-fem]]）だが、LLM マイグレーションの等価性オラクルとして統合した研究はない。

2. **Python ターゲットが手薄**  
   C++/Kokkos/Java/Rust が中心。NumPy/SciPy 等の数値意味論差・浮動小数点規則を正面から扱う研究は空白。

3. **数値許容差の原理的設定**  
   Fortran→C++ は「4桁丸め」と経験的（[[fortran-to-cpp-llm]]）。理論的許容差設定（[[scisw-test-frameworks-precision]]）との橋渡しが未実施。

4. **中間仕様の数値拡張**  
   BSG・言語中立仕様に物理単位・保存則・許容誤差を第一級で組み込む設計の提案余地がある。

## 普遍知見オラクルの先行技術群

| 技術 | 文献 | オラクルとして使う「普遍知見」 |
|-----|------|------------------------------|
| Metamorphic Testing (MT) | [[metamorphic-testing-oracle-problem]], [[metamorphic-relation-generation-sota]] | 物理対称性・スケール則・保存則 |
| 海洋モデル MT | [[metamorphic-testing-ocean-models]] | 既知の物理的対称性 |
| 因果テスト | [[causal-testing-framework]] | 因果効果（Causal Inference） |
| MT × LLM 修復 | [[metamorphic-testing-llm-program-repair]] | 意味等価変換の MR |
| MMS (製造解法) | [[mms-elastostatic-fem]], [[mms-swift-hohenberg]] | 解析解・収束次数 |
| 精度軸テスト | [[scisw-test-frameworks-precision]] | 期待精度・許容差 |
| 証明→コード変換 | [[scientific-texts-to-verifiable-code]] | 論文中の形式証明 |

## 周辺研究

- [[ttrace-distributed-training]] — 分散学習のサイレントバグ検出（数値許容差設定の方法論的ヒント）
- [[survey-code-agents]] — コード LLM の全体像サーベイ

## 関連 Topics

- [[genai-for-software-development]] — LLM × ソフトウェア開発（既存トピック）
- [[ml-system-quality-and-testing]] — ML/DNN システムの品質・テスト

## 出典

- LegacyCoding/REPORT_レガシーコード等価移行_研究提案.md (全体)
- LegacyCoding/2605.17535_AgentModernize_JA.md (AgentModernize 詳細)
- LegacyCoding/各PDF（上記 entity ページ参照）
