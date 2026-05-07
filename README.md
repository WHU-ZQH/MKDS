# MKDS

This is the official repository for the paper:

> **MKDS: Multi-source Knowledge-Driven Data Synthesis Framework for Effective Domain Adaptation of Large Language Models**

Domain-specific instruction tuning (IT) is a common approach to unleash the power of large language models (LLMs) in specialized applications, e.g. medical question answering (QA). The effectiveness of domain-specific IT highly relies on high-quality instruction corpora, which are usually limited because of the high cost and time-consuming data annotation. Hence, data synthesis (DS) via LLMs has emerged as an essential paradigm. However, current DS methods often struggle to generate professional, high-quality and diverse domain-specific IT data, especially for the Chinese medical domain. Thus, we propose a simple yet effective multi-source knowledge-driven DS (MKDS) framework to generate additional desired IT data. The principle of MKDS is to instruct proprietary LLMs to fully use rich and professional knowledge from multi-source knowledge bases. Accordingly, we designed a high-quality synthetic IT dataset tailored for the Chinese medical domain (MK-MedInstruct), comprising over 187K instruction-response pairs. To verify the effectiveness of this dataset, we used it to fine-tune two cutting-edge LLMs: LLaMA-3-8B-Instruct and Qwen-2.5-7B-Instruct. Extensive results on various medical benchmarks, encompassing multiple-choice and long-form medical QA, demonstrate that our models outperform baseline models by a large margin.

## Directory Structure

```
MKDS/
├── data/
│   ├── ours/
│   │   ├── segment.json          # Raw medical knowledge graph
│   │   └── MMK-Instruct.json     # Final synthesized SFT dataset
│   ├── baselines/                # Baseline datasets for comparison experiments
│   │   ├── CMB-train_convert.json
│   │   ├── medmcqa-train-instruction-dataset_convert.json
│   │   ├── medqa-train-instruction-dataset_convert.json
│   │   ├── aquilamed-instruct_convert.json
│   │   ├── DISC-Med-SFT_released.json
│   │   ├── Huatuo26M_Lite.json
│   │   └── Chinese_medical_dialogue_data.json
│   └── dataset_info.json         # LLaMA-Factory dataset registry
├── huggingface/                  # Local pre-trained model weights
│   ├── Meta-Llama-3.1-8B-Instruct/
│   └── Qwen2.5-7B-Instruct/
├── scripts/                      # Training launch scripts
└── src/                          # Data generation code
    ├── api.py                    # LLM API wrappers (ERNIE / GPT)
    ├── prompt_template.py        # All prompt templates
    ├── prepare_data.py           # Step 1: KG cleaning and flattening
    ├── get_llm_knowledge.py      # Step 2: LLM web retrieval
    ├── check_consistency.py      # Step 3: Dual-source consistency validation and merging
    ├── generate_sft_data.py      # Step 4: Multi-task SFT sample generation
    ├── format_data.py            # Step 5: Convert to training format
    └── score_sample.py           # Step 6: Data quality scoring
```

## Data Generation Pipeline

The pipeline chains 6 scripts, producing intermediate files `step1`–`step8`:

```
segment.json
    │
    ▼ prepare_data.py
step3-random.jsonl  (one record per medical entity, contains graph_knowledge)
    │
    ▼ get_llm_knowledge.py  (ERNIE + web search)
step4.jsonl  (adds retrieval_knowledge field)
    │
    ▼ check_consistency.py  (ERNIE dual-source merging)
step5.jsonl  (adds knowledge field, marked with ### 整合结果)
    │
    ▼ generate_sft_data.py  (randomly assigns 1 of 6 task types, ERNIE generates JSON samples)
step6.jsonl  (adds task_type / data fields)
    │
    ▼ format_data.py
step7.json   (alpaca format: instruction / input / output / history)
    │
    ▼ score_sample.py  (ERNIE scoring: accuracy + relevance, 1–5)
step8.jsonl  (adds score field)
```

The 6 generated task types: Named Entity Recognition (NER), Text Classification, Relation Extraction, Medical QA, Multiple Choice (MCQ), and Multi-turn Dialogue.

### Setup

Before running any LLM-dependent script, configure API keys in `src/api.py`:

- `ernie()`: Replace the `Authorization` Bearer token with a valid Baidu Qianfan API key.
- `gpt()`: Replace `api_key` with a valid OpenAI-compatible service key.

### Commands

```bash
# Step 1: Clean KG data, outputs data/ours/step1–3 files
# Note: paths inside the script use Windows backslashes; change to forward slashes on macOS/Linux
python src/prepare_data.py

# Step 2: Web retrieval (-s/-e control start/end index for batch processing)
python src/get_llm_knowledge.py \
    -i data/ours/step3-random.jsonl \
    -o step4.jsonl \
    -s 0 -e 1000

# Step 3: Dual-source consistency validation and merging
python src/check_consistency.py -i step4.jsonl -o step5.jsonl

# Step 4: Generate multi-task SFT samples
python src/generate_sft_data.py -i step5.jsonl -o step6.jsonl

# Step 5: Convert to LLaMA-Factory alpaca format
python src/format_data.py -i step6.jsonl -o step7.json

# Step 6: Quality scoring
python src/score_sample.py -i step7.json -o step8.jsonl
```

Steps 2–4 and 6 write in append mode, so interrupted runs can be safely resumed. Each LLM call retries up to 3 times on failure.

## Model Training

Training is based on [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory). Datasets are registered in `data/dataset_info.json`.

| Script | Dataset Combination | Description |
|--------|--------------------|----|
| `llama3_1_8b_it_mmk.sh` | CMB + medmcqa + medqa + **mmk** | With MKDS synthesized data (main experiment) |
| `llama3_1_8b_it.sh` | CMB + medmcqa + medqa | Baseline (no synthesized data) |
| `llama3_1_8b_it_aquila.sh` | + aquilamedrt | Ablation: replace with AquilaMed |
| `llama3_1_8b_it_disc.sh` | + DISC | Ablation: replace with DISC-Med-SFT |
| `llama3_1_8b_it_dialogue.sh` | + Chinese_medical_dialogue | Ablation: replace with Chinese medical dialogue |
| `llama3_1_8b_it_huatuo.sh` | + Huatuo | Ablation: replace with Huatuo26M |

```bash
bash scripts/llama3_1_8b_it_mmk.sh
```

Training hyperparameters: LoRA fine-tuning, FP16, cosine LR scheduler, learning rate 1e-4, batch size 8, sequence length 1024, 1 epoch.

> **Note**: `--model_name_or_path` and `--dataset_dir` in the training scripts use `/workspace/MKDS/...` paths. Update these to match your environment.

## Citation

```bibtex
@article{zhong2026mkds,
  title={MKDS: Multi-source Knowledge-Driven Data Synthesis Framework for Effective Domain Adaptation of Large Language Models},
  author={Zhong, Qihuang and Gong, Jinzhao and Zhu, Ke and Liao, Fei and Liu, Juhua and Du, Bo},
  journal={arXiv preprint},
  year={2026}
}
```
