
## 概要
VLM（Vision-Language Model）のファインチューニングにおいて、画像の特定部分（Region）に対する推論やドメイン知識の注入に焦点を当てた研究は、近年非常に活発です。

一般的なVLMは画像全体を一枚のパッチとして処理する傾向があり、細かな部分の分析や専門的な評価（医療画像や精密機器の欠陥検知など）には不向きな場合があります。これを解決するための主なアプローチを、最新の論文とともに整理しました。

## 1. リージョンレベルの理解（Region-based Tuning）
画像全体ではなく、特定の関心領域（RoI: Region of Interest）を明示的に扱う手法です。

### GPT4RoI: GPT4RoI: Instruction Tuning Large Language Model on Region-of-Interest
- 手法: ユーザーが指定した矩形領域（Bounding Box）をプロンプトとして受け取り、その領域内の特徴量を抽出してLLMに入力します。
- 特徴: 特定の部位に「名前」や「属性」を割り当てるだけでなく、その部分が「何をしているか」といった複雑な推論を可能にします。

### RegionGPT: RegionGPT: Towards Region Understanding Vision Language Model
手法: 領域記述の複雑さを解消するため、領域レベルの指示チューニングを行い、詳細な領域理解を実現しています。

## 2. 視覚的プロンプティング（Visual Prompting）
画像そのものに「印」をつけたり、補助的な視覚情報を加えることで、モデルの注意を特定の場所に向けさせる手法です。

### ControlMLLM / ControlMLLM++: Test-Time Computing for Referring Multimodal Large Language Models / ControlMLLM: Training-Free Visual Prompt Learning for Multimodal Large Language Models
手法: 学習済みVLMを凍結したまま、学習可能な「視覚的プロンプト」を注入することで、テスト時に特定の領域に対する推論精度を高めます。

### Explicit Visual Prompts: Guiding Medical Vision-Language Models with Explicit Visual Prompts: Framework Design and Comprehensive Exploration of Prompt Variations
ドメイン応用: 特に医療ドメインにおいて、医師が注目する特定の病変部位を強調するためのプロンプト設計を提案しています。

## 3. ドメイン知識の注入（Domain-Specific Adaptation）
特定のドメイン（医療、工業、サッカー、リモートセンシング等）に特化した知識を効率的に注入する手法です。

### Keep the General, Inject the Specific: Keep the General, Inject the Specific: Structured Dialogue Fine-Tuning for Knowledge Injection without Catastrophic Forgetting
手法: 壊滅的忘却（Catastrophic Forgetting）を防ぎつつ、構造化されたダイアログを用いて専門知識を注入します。

### CropVLM: CropVLM: Learning to Zoom for Fine-Grained Vision-Language Perception
手法: 「ズーム」の概念を学習に取り入れ、ドキュメント解析やテキスト認識など、細かい解像度が必要なタスクに対応します。