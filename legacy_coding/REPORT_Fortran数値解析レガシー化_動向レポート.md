# 数値解析プログラム（Fortran）のレガシー化への打ち手 ― 動向レポート

作成日: 2026-06-22
対象: LLM Wiki トピック [[legacy-code-migration]] および配下 entity（LegacyCoding コレクション 24論文 + 研究提案REPORT）
位置づけ: 数値解析プログラム（Fortran）がレガシー化していることに対する**打ち手を検討するための意思決定材料**。
構成: ① 課題設定（等価性証明の必要性と、現実的に取り得る証明方法の調査結果）／② 打ち手の説明／③ 期待される効果。
原則: 記述は LLM Wiki に蓄積した論文事実に基づく。各節末に Wiki 上の根拠ページを示す。

---

## エグゼクティブサマリー

- **課題:** 数値解析 Fortran 資産は「保守人材の枯渇」「CPU 同質環境前提ゆえの GPU/ヘテロ環境への非対応」によりレガシー化している。Python 等への移行が打ち手だが、**移行後コードが旧コードと数値的に等価であることをどう保証するか**が最大の障壁。
- **核心的論点:** **完全な等価性の証明は原理的に不可能**である（後述の4つの理由）。したがって課題は「完全証明」ではなく「**どこまでの等価性を、どの証明手段で、どの信頼度で担保するか**」という工学的設計問題に置き換わる。
- **調査結果（現実的に取り得る証明方法）:** 6系統の手法が文献上で確立／実証されている。レガシー出力との許容差付き比較、差分テスト/差分ファジング、メタモルフィックテスト（物理不変量・対称性）、MMS（製造解法）、数値許容差の原理的設定、契約（中間仕様）ベース検証。**単独で完全を狙わず多層に重ねる**のが現実解。
- **打ち手:** (A) 生成前に言語非依存の中間仕様＝契約を立てる、(B) 生成＆検査＋フィードバックループで自己修復する、(C) 上記6系統を多層オラクルとして組み、矛盾点を人間レビューに上げる。
- **期待効果:** 専門家が数週間要した移植を数時間・数ドル規模へ（[[fortran-to-kokkos-agent]]）。加えて、**監査可能な等価性レポート**という成果物が規制・安全クリティカル領域の事業価値になる。

---

## 1. 課題設定

### 1.1 なぜ Fortran 数値解析プログラムは「いま」打ち手が要るのか

- **保守人材の枯渇。** Fortran・COBOL・PL/SQL に精通した技術者は減少し、習得コストが上昇し続けている。システムを書いた技術者の退職により資産が脆弱化する（[[legacy-code-migration]], [[agent-modernize-bsg]]）。
- **ハードウェア進化への非対応。** 科学計算 Fortran は均質 CPU 環境向けに最適化されてきたが、HPC は GPU 加速ヘテロジニアス環境へ移行している。Fortran は GPU ネイティブバインディングを欠き、移植が急務（[[fortran-to-kokkos-agent]]）。
- **手作業移行の超高コスト。** 手動の移植には高度な専門知識と多大な時間が必要（[[fortran-to-kokkos-agent]]）。レガシー移行一般でも、大規模事例は数年・数億ドル規模に達する（[[legacy-code-migration]]）。

→ つまり「動かし続ける」コストと「移行する」コストの両方が上がっており、**LLM による移行支援が現実的選択肢として浮上**している。

> 根拠: [[legacy-code-migration]], [[fortran-to-kokkos-agent]], [[agent-modernize-bsg]]

### 1.2 移行の核心課題 ―― 等価性を証明する必要性

数値解析プログラムの移行が一般的な業務システム移行と決定的に異なるのは、**「動けばよい」では済まない**点にある。

- **直接（ワンショット）翻訳は信頼できない。** LLM 翻訳の正答率は 2.1〜47.3%、翻訳の最大 77.8% がコンパイル不能か誤結果（[[intent-preserving-pipeline]] 引用）。
- **「コンパイル・実行できる ≠ 振る舞いが等価」。** 構文的に正しい翻訳が、エッジケース処理・検証ロジック・制約を**サイレントに破壊**しうる（[[agent-modernize-bsg]] の中心主張）。数値計算ではこれが「静かな数値誤差」として現れ、発見が遅れるほど被害が大きい。
- **安全・規制要件。** 規制産業（医療機器・金融・通信等）では、移行物が旧物と同じ振る舞いをすることの**追跡可能な証拠（等価性レポート）**が事業価値になる（[[legacy-code-migration]], [[mms-elastostatic-fem]] は FDA 文脈）。

→ ゆえに移行の合否は**等価性の証明可否**にかかる。これが本レポートの中心課題である。

> 根拠: [[intent-preserving-pipeline]], [[agent-modernize-bsg]], [[legacy-code-migration]]

### 1.3 なぜ「完全な等価性の証明」は不可能か（4つの理由）

調査の結論として、**新旧プログラムの完全な等価性を証明することは原理的・現実的に不可能**である。理由は文献上次の4点に整理できる。

1. **形式的等価性検証はスケールしない。** 形式的プログラム等価性（二分化・トレース等価・観察的等価）は理論的根拠を与えるが、**実世界システムではしばしば困難**で、実務家は軽量代替（差分テスト・メタモルフィックテスト）に頼る（[[agent-modernize-bsg]] 関連研究）。実際、等価性検証ツールは言語ペア専用実装に閉じがちで（ALPHATRANS 10,859行、OXIDIZER 19,052行）、言語ペア数が二乗で増えるためスケールしない（[[match-fix-agent]]）。
2. **浮動小数点ゆえ「ビット完全一致」を基準にできない。** 数値出力は `0.00000000` vs `0.0`、`832040` vs `832040.0` のような表記差・丸め差が必然的に生じ、完全一致比較が機能しない（[[fortran-to-cpp-llm]]）。そもそも何をもって「同じ」とするかに許容差の定義が要る。
3. **テストスイートは不完全。** ユニットテストは重要入力を欠いて**偽の等価**を生み、ファジングは無効入力で**偽の非等価**を生む（[[match-fix-agent]]）。テストによる等価性は「反証されなかった」以上を意味しない。
4. **オラクル問題。** 数値シミュレーションでは「正解出力」が存在しない／定義できないことが多い（[[metamorphic-testing-oracle-problem]]）。さらに、レガシー出力自体を正解（オラクル）として使う場合、**レガシー独自ロジックが生む数値誤差を「正解」として固定してしまう**危険がある。メタモルフィック関係を使っても「初期出力が誤りでも後続出力が許容変動内なら検出できない」という限界がある（[[metamorphic-testing-ocean-models]]）。

→ **したがって課題は「完全証明」から「現実的な部分証明の積み上げ」へと再定義される。** 「どの等価性を、どの手段で、どの信頼度で保証し、保証できない領域を人間レビューにどう上げるか」が設計問題になる。

> 根拠: [[agent-modernize-bsg]], [[match-fix-agent]], [[fortran-to-cpp-llm]], [[metamorphic-testing-oracle-problem]], [[metamorphic-testing-ocean-models]]

### 1.4 現実的に取り得る証明方法の調査結果

完全証明が不可能である以上、現実的に取り得るのは**「部分的な等価性を担保する複数の検証手段」**である。Wiki に蓄積した文献から、確立／実証済みの6系統を整理する。

#### (1) レガシー出力との許容差付き比較
旧コードの出力を**許容差つきの「正解」とみなして**新コードの出力と比較する。Fortran→C++ では、出力をトークン化 → float 変換 → **小数4桁丸め** → Jaro-Winkler 類似度で比較する手法を導入（[[fortran-to-cpp-llm]]）。
- **保証範囲:** 与えた入力集合に対する出力の近さ。**前提:** レガシー出力が正しいこと。**限界:** §1.3-4 の通り、レガシー独自の数値誤差ごと固定してしまう。許容差「4桁」は経験的で原理的根拠が弱い。

#### (2) 差分テスト / 差分ファジング
新旧（または参照実装と対象）を同じ入力で実行し出力を突き合わせる。C→Rust では振る舞い等価性を**差分ファジング**で自動検査し、失敗時に LLM へ再プロンプト（[[c-to-rust-feedback-loops]]）。分散学習デバッグの TTrace は中間テンソルを参照実装と照合する差分テストの先例（[[ttrace-distributed-training]]）。
- **保証範囲:** ファザーが探索した入力域での一致。**限界:** 入力空間網羅は不可能。ファジングは無効入力で偽の非等価を生む（[[match-fix-agent]]）。

#### (3) メタモルフィックテスト（MT）/ メタモルフィック関係（MR）
正解データなしに、**プログラムが満たすべき性質（物理対称性・スケール則・保存則等の不変量）**で出力を検証する。オラクル問題への主要技術として確立（[[metamorphic-testing-oracle-problem]]）。海洋モデルでは**既知の物理的対称性を MR にして、同一モデルの2実装を突き合わせる**（＝移行の等価性検証と構造が酷似）（[[metamorphic-testing-ocean-models]]）。LLM のコードタスクにも適用例がある（[[metamorphic-relation-generation-sota]]）。
- **保証範囲:** レガシー出力に依存せず、物理/数学的に「あるべき関係」を満たすか。**限界:** 初期出力自体の誤りは検出できない場合がある（[[metamorphic-testing-ocean-models]]）。MR の網羅性は保証されない。

#### (4) MMS（Method of Manufactured Solutions／製造解法）
解析的に既知の解を**先に構成**し、そこから逆算したソース項を入れて、コードがその解に収束するかを検証する。**正解データ無しに、製造解という普遍的構成でコードの正しさを定量検証**できる（[[mms-elastostatic-fem]]）。収束次数解析は**軽微なコーディング誤りに感度を持つ**（[[mms-elastostatic-fem]]）。Lyapunov 汎関数の単調減少など**物理不変量を検証オラクル**にする例もある（[[mms-swift-hohenberg]]）。FDA（規制産業）での適用例がある点も、安全クリティカルな数値解析資産に近い。
- **保証範囲:** 数値スキームの正しさ・収束次数（＝離散化が正しく実装されているか）。**限界:** 「製造解」を作れる問題クラスに限る。業務固有ロジックそのものの等価性は別途要検証。

#### (5) 数値許容差の原理的設定
許容差を経験則でなく**数学的解析に基づいて設定**し、バグ誘発誤差と正常な丸め誤差を区別する。TTrace は分散学習で「数学的解析に基づく許容差ガイドライン」を提案（[[ttrace-distributed-training]]）。科学ソフト開発を「期待精度」軸で体系化した方法論もある（[[scisw-test-frameworks-precision]]）。
- **保証範囲:** (1)(2) の比較における「合否しきい値」の妥当性。**限界:** 問題依存で一般式化は途上。

#### (6) 契約（中間仕様）ベースの検証
コード生成前に**事前/事後条件・不変条件**を明示した中間表現を立て、生成コードがそれを満たすか検証する。AgentModernize の Behavioral Specification Graph（BSG）は「LLM が理解した内容」と「生成する内容」の間に**人間が点検できる信頼境界（glass box）**を置き、仕様からテストオラクルを生成する（[[agent-modernize-bsg]]）。Intent-Preserving は I/O 契約・**数値規則**・ループ境界を言語中立に固定（[[intent-preserving-pipeline]]）。
- **保証範囲:** 明示した契約条項の保存。**限界:** 暗黙ルールを契約化し損ねれば漏れる。AgentModernize ではボトルネックは抽出でなく**コード生成側**にあった（BER 9.4〜19.4%）。

#### 調査結果のまとめ（証明手段の俯瞰）

| 証明手段 | 何を保証するか | 前提 | 主な限界 | 根拠 |
|---|---|---|---|---|
| (1) 許容差付き出力比較 | 入力集合上の出力一致 | レガシー出力が正しい | 旧誤差ごと固定／許容差が経験的 | [[fortran-to-cpp-llm]] |
| (2) 差分テスト/ファジング | 探索入力域の一致 | 参照実装あり | 入力網羅不可／偽の非等価 | [[c-to-rust-feedback-loops]], [[ttrace-distributed-training]] |
| (3) メタモルフィックテスト | 物理/数学的不変量の充足 | MR を定義できる | 初期誤り未検出／網羅性なし | [[metamorphic-testing-oracle-problem]], [[metamorphic-testing-ocean-models]] |
| (4) MMS（製造解法） | 数値スキームの正しさ・収束次数 | 製造解を作れる | 業務ロジック等価は別途 | [[mms-elastostatic-fem]], [[mms-swift-hohenberg]] |
| (5) 数値許容差の原理化 | 合否しきい値の妥当性 | 誤差解析が可能 | 一般式化は途上 | [[ttrace-distributed-training]], [[scisw-test-frameworks-precision]] |
| (6) 契約ベース検証 | 明示契約条項の保存 | 仕様を抽出できる | 暗黙ルール漏れ／生成側がボトルネック | [[agent-modernize-bsg]], [[intent-preserving-pipeline]] |

> **結論（§1.4）:** いずれの手段も単独では完全を保証しない。**(1)(2) はレガシー出力を基準にした「相対的等価」、(3)(4) は物理/数学知見を基準にした「絶対的妥当性」を担保する**。両者は補完関係にあり、**多層に重ねること**が現実的な証明戦略になる。特に (3)(4) は「レガシー出力をオラクルにできない」課題への直接の解になりうる。

> 根拠: 上表の各ページ、および総括 [[legacy-code-migration]]（研究ギャップ §1〜4）

---

## 2. 打ち手

文献群を貫く収束パターンは3つ。これを数値解析 Fortran 移行に当てはめる。

### 打ち手A ― 生成前に「契約（中間仕様）」を立てる（contract-first / glass-box）
直接翻訳せず、**言語非依存の中間表現を先に確定**してから目的言語コードを生成する。
- 事前/事後条件・不変条件・**数値規則・I/O 契約・ループ境界**を明示（[[agent-modernize-bsg]] の BSG、[[intent-preserving-pipeline]] の言語中立アルゴリズム）。
- 数値解析向けには、この契約に**物理単位・保存則・許容誤差を第一級で組み込み、人間が承認**する拡張が有効（[[legacy-code-migration]] 研究ギャップ4）。
- 効用: 「LLM が理解した内容」を人間が点検できる**信頼境界**になり、規制産業の監査証跡にもなる。

### 打ち手B ― 生成＆検査＋フィードバックループで自己修復する
生成物をコンパイル/実行/差分で自動検査し、失敗時に LLM へ再プロンプトして反復修復する。
- C→Rust・Fortran→Kokkos・AgentModernize が独立に「翻訳・検証・コンパイル・実行・テスト・デバッグ・最適化」のエージェント分業へ収束（[[c-to-rust-feedback-loops]], [[fortran-to-kokkos-agent]], [[agent-modernize-bsg]]）。
- **重要知見:** フィードバックループはオプションでなく必須。「アーキテクチャとモデルが協働する ― どちらか一方では不十分」（[[c-to-rust-feedback-loops]], [[agent-modernize-bsg]]）。フィードバック無しでは振る舞い等価率が 0% に落ちる例もある（[[agent-modernize-bsg]]）。

### 打ち手C ― 等価性検証を「多層オラクル」として組み、矛盾を人間に上げる
§1.4 の6系統を**単独でなく重ねて**配置する。数値解析向けの推奨構成:
- **第1層（相対的等価）:** レガシー出力との許容差付き比較（[[fortran-to-cpp-llm]]）＋差分ファジング（[[c-to-rust-feedback-loops]]）。許容差は数学的解析に基づき設定（[[ttrace-distributed-training]], [[scisw-test-frameworks-precision]]）。
- **第2層（絶対的妥当性）:** メタモルフィック関係（物理対称性・保存則）（[[metamorphic-testing-oracle-problem]], [[metamorphic-testing-ocean-models]]）＋ MMS による収束次数検証（[[mms-elastostatic-fem]], [[mms-swift-hohenberg]]）。
- **検証の汎用化:** 言語ペア専用実装の限界は、LLM ベースの言語非依存検証で突破しうる（[[match-fix-agent]]）。
- **健全な評価:** 失敗の相当数は翻訳誤りでなく評価環境の不備（コンパイルフラグ欠落等）由来の**偽陰性**。構成情報を明示した再現可能な評価を設計する（[[beyond-translation-accuracy]]）。
- **人間の役割:** 第1層と第2層が**衝突する箇所**こそ「レガシー独自の数値誤差」候補として人間レビューに上げ、要件再構築の承認点とする。人間は Director/Reviewer として残る（[[human-ai-partnership-code-migration]]）。

> 根拠: [[agent-modernize-bsg]], [[intent-preserving-pipeline]], [[c-to-rust-feedback-loops]], [[fortran-to-kokkos-agent]], [[match-fix-agent]], [[beyond-translation-accuracy]], [[human-ai-partnership-code-migration]] と §1.4 の各手段

---

## 3. 期待される効果

- **移行コストの劇的削減。** かつて専門家が数週間・高コストで行った Fortran→Kokkos 移植を、有償 LLM で**数時間・数ドル・人手介在なしに**実現できると報告されている（[[fortran-to-kokkos-agent]]）。フィードバックループ付きパイプラインは、予算モデルでも非ゼロの振る舞い等価を達成する唯一の経路（[[agent-modernize-bsg]]）。
- **「サイレントな数値破壊」の早期検出。** 多層オラクル（特に MT/MMS による絶対的妥当性チェック）により、構文的には正しいが数値的に誤った翻訳を、本番障害化する前に検出できる（[[agent-modernize-bsg]], [[mms-elastostatic-fem]]）。
- **監査可能な等価性レポートという成果物。** 契約（中間仕様）＋等価性レポートは、単発プロンプト方式が提供できない**追跡可能な監査証跡**になり、規制・安全クリティカル領域（医療機器・金融・原子力等）での事業価値になる（[[agent-modernize-bsg]], [[mms-elastostatic-fem]]）。
- **ハードウェア進化への追随と性能向上。** GPU ヘテロ環境向け移植により次世代スパコンへのアクセスが広がり、場合により**旧 Fortran ベースラインを超える最適化コード**が得られる（[[fortran-to-kokkos-agent]]）。
- **モデル依存性の低減。** フィードバックループを組むことでモデル間の性能差が縮小し、特定の高価モデルに固定されにくくなる（[[c-to-rust-feedback-loops]]）。

### 効果の限界（過大評価への注意）
- 振る舞い等価率の絶対値は依然 modest（Full 構成で平均一桁〜十数%）で、ボトルネックは抽出でなく**コード生成側**（[[agent-modernize-bsg]]）。
- 評価シナリオは数百行規模が中心で、実レガシーは桁違いに大きい（階層化・分割統治が工学課題）（[[agent-modernize-bsg]]）。
- OSS モデルは産業要件に未達のことが多い（[[fortran-to-kokkos-agent]]）。
- 評価標準自体が未成熟で偽陰性が混入する（[[beyond-translation-accuracy]]）。

→ ゆえに本打ち手は「全自動の置換」ではなく「**人間承認ゲート付きの強力な支援**」として導入するのが現実的。

> 根拠: [[fortran-to-kokkos-agent]], [[agent-modernize-bsg]], [[c-to-rust-feedback-loops]], [[mms-elastostatic-fem]], [[beyond-translation-accuracy]]

---

## 付録: 根拠とした LLM Wiki ページ

- トピック総括: [[legacy-code-migration]]
- Fortran 数値計算移行: [[fortran-to-cpp-llm]], [[fortran-to-kokkos-agent]]
- 契約／中間仕様: [[agent-modernize-bsg]], [[intent-preserving-pipeline]]
- フィードバックループ／差分検証: [[c-to-rust-feedback-loops]], [[match-fix-agent]], [[ttrace-distributed-training]]
- 評価の健全化／人間の役割: [[beyond-translation-accuracy]], [[human-ai-partnership-code-migration]]
- 普遍知見オラクル（証明方法の核）: [[metamorphic-testing-oracle-problem]], [[metamorphic-testing-ocean-models]], [[metamorphic-relation-generation-sota]], [[mms-elastostatic-fem]], [[mms-swift-hohenberg]], [[scisw-test-frameworks-precision]]

原本 PDF の正本パスは `C:\work_space\Paper\LegacyCoding\*.pdf`、Wiki 側の対応は `source-map.json` の `LegacyCoding_collection`（origin）を参照。

---

*本レポートは LLM Wiki（compile-first RAG）に ingest 済みの LegacyCoding コレクションを根拠に、Query 原則（Wiki 内の事実のみ・出典明示）で作成した。ingest 自体は 2026-06-21 に完了済み（冪等性チェックにより再取り込みは不要）。*
