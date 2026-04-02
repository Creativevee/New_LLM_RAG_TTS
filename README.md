# Hexagon Labs Chatbot

A RAG-powered AI chatbot with Text-to-Speech. Upload a document and ask questions about it, or just chat with the AI directly.

## Features

- Chat with Qwen 2.5 7B via HuggingFace Inference
- Upload documents (PDF, TXT, DOCX, CSV, JSON, MD) for context-aware answers
- Text-to-Speech responses via Edge TTS
- Dark-themed chat UI

## Requirements

- Python 3.10+
- A free [HuggingFace](https://huggingface.co) account and API token

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/Creativevee/New_LLM_RAG_TTS.git
cd New_LLM_RAG_TTS
```

**2. Create a virtual environment and install dependencies**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

**3. Add your API key**

Create a `.env` file in the project root:
```
HF_TOKEN=your_huggingface_token_here
```

Get your token at: https://huggingface.co/settings/tokens

**4. Run the app**
```bash
python main.py
```

Open your browser at: [http://localhost:7860](http://localhost:7860)

## Usage

- Type any question in the chat box and press Enter or click Send
- To use a document: click **Choose File**, select a file, click **Upload**, then ask questions about it
- The bot will read back answers using voice automatically
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




# 🎓 Complete Guide: Training Your Own LLM & Integrating with Hexagon Labs

> **From raw data to deployed AI: A step-by-step guide to fine-tuning, uploading, and integrating your custom language model.**

---

## 📋 Table of Contents

1. [Overview: The Complete Pipeline](#-overview-the-complete-pipeline)
2. [Part 1: Training Your Custom Model](#-part-1-training-your-custom-model)
3. [Part 2: Uploading to Hugging Face Hub](#-part-2-uploading-to-hugging-face-hub)
4. [Part 3: Deploying to Hugging Face Spaces](#-part-3-deploying-to-hugging-face-spaces)
5. [Part 4: How Frontend & Backend Connect to Your Model](#-part-4-how-frontend--backend-connect-to-your-model)
6. [Part 5: Data Flow Deep Dive](#-part-5-data-flow-deep-dive)
7. [Troubleshooting & Best Practices](#-troubleshooting--best-practices)

---

## 🎯 Overview: The Complete Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    COMPLETE MODEL LIFECYCLE                              │
│                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐              │
│  │   TRAINING   │───▶│   UPLOAD     │───▶│   DEPLOY     │              │
│  │  (Local/Colab)│   │  (HF Hub)    │   │  (Spaces)    │              │
│  └──────────────┘    └──────────────┘    └──────────────┘              │
│         │                   │                   │                       │
│         │                   │                   ▼                       │
│         │                   │          ┌──────────────┐                │
│         │                   │          │  YOUR MODEL  │                │
│         │                   │          │  API Endpoint│                │
│         │                   │          └──────┬───────┘                │
│         │                   │                 │                        │
│         ▼                   ▼                 ▼                        │
│  ┌──────────────────────────────────────────────────────────┐          │
│  │              HEXAGON LABS APPLICATION                     │          │
│  │  ┌────────────┐    ┌────────────┐    ┌────────────┐     │          │
│  │  │  Frontend  │───▶│  Backend   │───▶│  Your Model │     │          │
│  │  │  Port 3000 │    │  Port 8888 │    │  (Cloud)   │     │          │
│  │  └────────────┘    └────────────┘    └────────────┘     │          │
│  └──────────────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────────────┘
```

### What You'll Learn

| Step | What You'll Do | Time Required | Cost |
|------|---------------|---------------|------|
| **1. Prepare Data** | Clean and format training data | 1-2 hours | Free |
| **2. Fine-tune Model** | Train on Google Colab or local GPU | 2-6 hours | Free-$10 |
| **3. Upload to HF** | Push model to Hugging Face Hub | 30 minutes | Free |
| **4. Deploy Space** | Create API endpoint on Spaces | 1 hour | Free (30 GPU hrs/mo) |
| **5. Integrate** | Connect to Hexagon Labs backend | 30 minutes | Free |

---

## 🧠 Part 1: Training Your Custom Model

### Why Fine-Tune Instead of Using Pre-trained?

| Pre-trained Model | Fine-tuned Model |
|------------------|------------------|
| ✅ General knowledge | ✅ **Domain-specific expertise** |
| ✅ Works out of the box | ✅ **Your writing style** |
| ❌ Generic responses | ✅ **Custom terminology** |
| ❌ May hallucinate | ✅ **Factual accuracy on your data** |

### Step 1.1: Prepare Your Training Data

#### Format: Instruction-Response Pairs

Your training data should be in **JSONL format** (one JSON object per line):

```jsonl
{"instruction": "What is Hexagon Labs?", "input": "", "output": "Hexagon Labs is a technology company specializing in AI and machine learning solutions..."}
{"instruction": "Who founded the company?", "input": "", "output": "The company was founded by a team of software engineers with expertise in..."}
{"instruction": "What services do they offer?", "input": "", "output": "Hexagon Labs offers web development, mobile apps, AI integration, and cloud solutions..."}
```

#### Create Your Dataset

```python
# save as: prepare_dataset.py
import json

# Your training data
training_data = [
    {
        "instruction": "What is Hexagon Labs?",
        "input": "",
        "output": "Hexagon Labs is a technology company specializing in AI and machine learning solutions. We build intelligent systems that help businesses automate processes and gain insights from their data."
    },
    {
        "instruction": "What programming languages do you use?",
        "input": "",
        "output": "We primarily use Python for AI/ML work, JavaScript for frontend development, and Java/Kotlin for mobile applications. We also work with SQL for databases and cloud technologies like AWS and GCP."
    },
    {
        "instruction": "How many team members are there?",
        "input": "",
        "output": "Hexagon Labs has 9 team members with expertise in HTML/CSS, Java, Kotlin, SQL, PHP, and Python. Each member brings unique skills to deliver comprehensive digital solutions."
    },
    # Add 100-1000+ more examples for good results
]

# Save as JSONL
with open("training_data.jsonl", "w") as f:
    for example in training_data:
        f.write(json.dumps(example) + "\n")

print(f"✅ Created training_data.jsonl with {len(training_data)} examples")
```

#### Dataset Requirements

| Requirement | Minimum | Recommended | Ideal |
|-------------|---------|-------------|-------|
| **Examples** | 50 | 200-500 | 1000+ |
| **Quality** | Clean text | Verified facts | Expert-reviewed |
| **Diversity** | 5+ topics | 20+ topics | 50+ topics |
| **Length** | 50 words/example | 100 words/example | 200+ words/example |

---

### Step 1.2: Choose Your Base Model

For Hexagon Labs, we used **TinyLlama-1.1B-Chat-v1.0** because:

| Model | Size | VRAM Needed | Training Time | Quality |
|-------|------|-------------|---------------|---------|
| **TinyLlama-1.1B** | 1.1B params | 8GB | 2-4 hours | ⭐⭐⭐⭐ |
| Mistral-7B | 7B params | 24GB | 8-12 hours | ⭐⭐⭐⭐⭐ |
| Llama-2-7B | 7B params | 24GB | 8-12 hours | ⭐⭐⭐⭐⭐ |
| Phi-2 | 2.7B params | 12GB | 4-6 hours | ⭐⭐⭐⭐ |

**For beginners**: Start with TinyLlama (free on Colab)
**For production**: Use Mistral-7B or Llama-2 (requires paid GPU)

---

### Step 1.3: Fine-Tune on Google Colab (FREE)

#### Create Colab Notebook

1.  Go to: https://colab.research.google.com/
2.  Click **"New Notebook"**
3.  Go to **Runtime** → **Change runtime type** → **GPU** (T4)
4.  Copy this complete training script:

```python
# ═══════════════════════════════════════════════════════════════════
# HEXAGON LABS - MODEL FINE-TUNING SCRIPT
# Fine-tune TinyLlama on your custom data
# ═══════════════════════════════════════════════════════════════════

# Step 1: Install dependencies
!pip install -q transformers datasets accelerate peft trl bitsandbytes
!pip install -q huggingface_hub

# Step 2: Login to Hugging Face
from huggingface_hub import login
login(token="hf_YOUR_TOKEN_HERE")  # Get from https://huggingface.co/settings/tokens

# Step 3: Load your training data
from datasets import load_dataset

dataset = load_dataset("json", data_files="training_data.jsonl", split="train")
print(f"✅ Loaded {len(dataset)} training examples")

# Step 4: Load base model and tokenizer
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    load_in_4bit=True,  # Quantization for memory efficiency
)

# Step 5: Configure LoRA (Parameter-Efficient Fine-Tuning)
peft_config = LoraConfig(
    lora_alpha=16,
    lora_dropout=0.1,
    r=64,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["k_proj", "q_proj", "v_proj", "o_proj", "gate_proj", "down_proj", "up_proj"]
)

model = get_peft_model(model, peft_config)
model.print_trainable_parameters()

# Step 6: Prepare data for training
def format_prompt(example):
    """Format instruction-response pairs for chat model"""
    text = f"""<s>[INST] {example['instruction']}
{example['input']} [/INST] {example['output']} </s>"""
    return {"text": text}

dataset = dataset.map(format_prompt)

# Step 7: Training arguments
training_args = TrainingArguments(
    output_dir="./hexagon-llm-finetuned",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch",
    optim="paged_adamw_8bit",
    warmup_ratio=0.03,
    lr_scheduler_type="constant",
)

# Step 8: Train!
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    dataset_text_field="text",
    tokenizer=tokenizer,
)

print("🚀 Starting training...")
trainer.train()

# Step 9: Save model
model.save_pretrained("./hexagon-llm-final")
tokenizer.save_pretrained("./hexagon-llm-final")

print("✅ Training complete! Model saved to ./hexagon-llm-final")
```

#### Training Process Explained

```
┌─────────────────────────────────────────────────────────┐
│                  FINE-TUNING PROCESS                     │
│                                                          │
│  1. Load Base Model (TinyLlama-1.1B)                    │
│         ↓                                                │
│  2. Apply LoRA Adapters (trainable layers)              │
│         ↓                                                │
│  3. Format Training Data (instruction + response)       │
│         ↓                                                │
│  4. Forward Pass (model predicts next token)            │
│         ↓                                                │
│  5. Calculate Loss (compare prediction to target)       │
│         ↓                                                │
│  6. Backward Pass (update LoRA weights)                 │
│         ↓                                                │
│  7. Repeat for 3 epochs                                 │
│         ↓                                                │
│  8. Save Fine-tuned Model                               │
└─────────────────────────────────────────────────────────┘
```

#### Expected Training Output

```
✅ Loaded 200 training examples
trainable params: 8,388,608 || all params: 1,100,000,000 || trainable%: 0.76%
🚀 Starting training...
Epoch 1/3: 100%|████████| 50/50 [00:45<00:00, 1.10it/s, loss=0.456]
Epoch 2/3: 100%|████████| 50/50 [00:44<00:00, 1.13it/s, loss=0.312]
Epoch 3/3: 100%|████████| 50/50 [00:43<00:00, 1.15it/s, loss=0.245]
✅ Training complete! Model saved to ./hexagon-llm-final
```

**Training Time**: ~2-3 hours on Colab T4 (free tier)
**VRAM Usage**: ~6GB (fits in free tier)

---

### Step 1.4: Test Your Fine-tuned Model

Before uploading, verify it works:

```python
# Test the fine-tuned model
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_path = "./hexagon-llm-final"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto")

def ask(question):
    prompt = f"<s>[INST] {question} [/INST]"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=256)
    return tokenizer.decode(outputs[0], skip_special_tokens=True).split("[/INST]")[-1].strip()

# Test
print(ask("What is Hexagon Labs?"))
print(ask("Who is Anriel?"))
```

**Expected**: Answers should reflect your training data!

---

## 📤 Part 2: Uploading to Hugging Face Hub

### Step 2.1: Create Model Repository

1.  Go to: https://huggingface.co/new
2.  Fill in:
    - **Owner**: Your username (e.g., `FAO0-k4mrthrohrnoai34u50u`)
    - **Model name**: `hexagon-llm-1.1b`
    - **License**: MIT (or your choice)
    - **Visibility**: Public (for demo) or Private
3.  Click **"Create model"**

### Step 2.2: Upload Model Files

#### Option A: Using Python Script (Recommended)

```python
# upload_model.py
from huggingface_hub import HfApi, login

# Login
login(token="hf_YOUR_TOKEN_HERE")  # Must have WRITE permissions

# Initialize API
api = HfApi()

# Your model directory
model_path = "./hexagon-llm-final"

# Upload to Hub
api.upload_folder(
    folder_path=model_path,
    repo_id="FAO0-k4mrthrohrnoai34u50u/hexagon-llm-1.1b",
    repo_type="model",
)

print("✅ Model uploaded successfully!")
print("🌐 View at: https://huggingface.co/FAO0-k4mrthrohrnoai34u50u/hexagon-llm-1.1b")
```

#### Option B: Using Git

```bash
# Clone your model repo
git lfs install
git clone https://huggingface.co/FAO0-k4mrthrohrnoai34u50u/hexagon-llm-1.1b
cd hexagon-llm-1.1b

# Copy model files
cp -r ~/path/to/hexagon-llm-final/* .

# Commit and push
git add .
git commit -m "Upload fine-tuned hexagon-llm-1.1b"
git push
```

### Step 2.3: Add Model Card (README.md)

Create a `README.md` in your model repo:

```markdown
---
license: mit
language:
- en
tags:
- text-generation
- fine-tuned
- hexagon-labs
---

# Hexagon LLM 1.1B

A fine-tuned version of TinyLlama-1.1B-Chat-v1.0, customized for Hexagon Labs Q&A.

## Model Details

- **Base Model**: TinyLlama/TinyLlama-1.1B-Chat-v1.0
- **Fine-tuned by**: Anriel
- **Training Data**: 200 instruction-response pairs about Hexagon Labs
- **Training Time**: ~3 hours on Google Colab T4
- **Parameter Efficient Fine-Tuning**: LoRA (r=64)

## Use Cases

- Answering questions about Hexagon Labs
- Company information Q&A
- Team member information
- Service descriptions

## How to Use

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("FAO0-k4mrthrohrnoai34u50u/hexagon-llm-1.1b")
model = AutoModelForCausalLM.from_pretrained("FAO0-k4mrthrohrnoai34u50u/hexagon-llm-1.1b")

prompt = "<s>[INST] What is Hexagon Labs? [/INST]"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=256)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Training Data Format

```jsonl
{"instruction": "What is Hexagon Labs?", "input": "", "output": "Hexagon Labs is..."}
```

## License

MIT License - Free for commercial and academic use.
```

### Step 2.4: Verify Upload

```bash
# Test download
python3 -c "
from transformers import AutoTokenizer, AutoModelForCausalLM
tokenizer = AutoTokenizer.from_pretrained('FAO0-k4mrthrohrnoai34u50u/hexagon-llm-1.1b')
model = AutoModelForCausalLM.from_pretrained('FAO0-k4mrthrohrnoai34u50u/hexagon-llm-1.1b')
print('✅ Model downloaded successfully!')
"
```

---

## 🚀 Part 3: Deploying to Hugging Face Spaces

### Why Deploy to Spaces?

| Local Model | Spaces Deployment |
|-------------|------------------|
| ❌ Requires user to download | ✅ Instant API access |
| ❌ Needs GPU/RAM on user machine | ✅ Cloud GPU (free 30 hrs/mo) |
| ❌ Slow on CPU | ✅ Fast inference |
| ❌ Version management difficult | ✅ Easy updates |

### Step 3.1: Create Space

1.  Go to: https://huggingface.co/spaces
2.  Click **"Create new Space"**
3.  Configure:
    - **Space name**: `RaccoonSpace` (or your choice)
    - **License**: MIT
    - **SDK**: **Gradio**
    - **Visibility**: Public
4.  Click **"Create Space"**

### Step 3.2: Create Space Application

In your Space, create `app.py`:

```python
# app.py (for HF Spaces)
import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load model (cached after first load)
MODEL_ID = "FAO0-k4mrthrohrnoai34u50u/hexagon-llm-1.1b"

print("🔧 Loading model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16,
    device_map="auto"
)
print("✅ Model loaded!")

def generate_answer(question: str, context: str = "") -> str:
    """Generate answer using fine-tuned model"""
    try:
        # Build prompt
        if context and context.strip():
            prompt = f"""<s>[INST] Answer based ONLY on context.

Context:
{context}

Question: {question}

Answer: [/INST]"""
        else:
            prompt = f"""<s>[INST] You are a helpful assistant.

Question: {question}

Answer: [/INST]"""

        # Generate
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.7,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
        
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Clean up
        if "[/INST]" in answer:
            answer = answer.split("[/INST]")[-1].strip()
        
        return answer if answer else "I couldn't generate an answer."
        
    except Exception as e:
        return f"Error: {str(e)[:200]}"

# Gradio UI
with gr.Blocks(title="Hexagon Labs Demo", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# ⬡ Hexagon Labs Demo\n### Powered by hexagon-llm-1.1b")
    
    with gr.Row():
        with gr.Column():
            question = gr.Textbox(label="Question", placeholder="What is Hexagon Labs?", lines=3)
            context = gr.Textbox(label="Context (Optional)", placeholder="Paste document context...", lines=5)
            submit = gr.Button("🚀 Generate Answer", variant="primary")
        with gr.Column():
            output = gr.Textbox(label="Answer", lines=10)
    
    submit.click(fn=generate_answer, inputs=[question, context], outputs=output)

demo.launch(server_name="0.0.0.0", server_port=7860)
```

### Step 3.3: Create requirements.txt

```
# requirements.txt (for HF Spaces)
gradio>=4.0.0
transformers>=4.37.0
torch>=2.1.0
accelerate>=0.25.0
```

### Step 3.4: Request GPU Upgrade

1.  In your Space, go to **Settings** tab
2.  Scroll to **"Hardware"**
3.  Click **"Upgrade to GPU"**
4.  Select **"NVIDIA T4"** (free 30 hours/month)
5.  Click **"Request Access"** (if first time)
6.  Wait for approval (24-48 hours)

### Step 3.5: Get Your Space API URL

Once deployed, your API endpoint will be:
```
https://fa00-k4mrthrohrnoai34u50u--raccoonspace.hf.space/run/generate_answer
```

**Note the double hyphen `--` between owner and space name!**

---

## 🔗 Part 4: How Frontend & Backend Connect to Your Model

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER INTERACTION                                 │
│                                                                          │
│  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐    │
│  │   Browser    │         │   Backend    │         │  HF Spaces   │    │
│  │  (Port 3000) │         │  (Port 8888) │         │   (Cloud)    │    │
│  │              │         │              │         │              │    │
│  │  1. User     │         │  3. Process  │         │  5. Model    │    │
│  │     types    │────────▶│     request  │────────▶│     inference│    │
│  │     question │  HTTP   │  4. Call     │  HTTP   │  6. Generate │    │
│  │              │  POST   │     Space API│  POST   │     answer   │    │
│  │              │         │              │         │              │    │
│  │  9. Play     │         │  7. Generate │         │  8. Return   │    │
│  │     audio    │◀────────│     TTS      │◀────────│     answer   │    │
│  │              │  HTTP   │  (Local)     │  JSON   │              │    │
│  └──────────────┘         └──────────────┘         └──────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

### Step 4.1: Backend Configuration (`.env`)

```bash
# .env
HF_API_TOKEN=hf_YOUR_TOKEN_HERE
SPACE_ID=FAO0-k4mrthrohrnoai34u50u/RaccoonSpace
SPACE_API_URL=https://fa00-k4mrthrohrnoai34u50u--raccoonspace.hf.space/run/generate_answer
APP_PORT=8888
```

### Step 4.2: Backend LLM Module (`backend/llm.py`)

```python
#!/usr/bin/env python3
"""Hexagon Labs - LLM Module (Calls HF Space API)"""

import os, logging, requests
from typing import List, Union, Dict

logger = logging.getLogger("llm")

# Your HF Space API endpoint
SPACE_API_URL = os.getenv(
    "SPACE_API_URL",
    "https://fa00-k4mrthrohrnoai34u50u--raccoonspace.hf.space/run/generate_answer"
)
HF_TOKEN = os.getenv("HF_API_TOKEN")

def generate_answer(question: str, chunks: List[Union[str, Dict]]) -> str:
    """Generate answer by calling your HF Space"""
    try:
        # Build context from retrieved chunks
        context_parts = []
        for c in chunks:
            if isinstance(c, dict):
                text = c.get("text", str(c))
                source = c.get("source", "unknown")
            else:
                text = str(c)
                source = "unknown"
            context_parts.append(f"[{source}] {text}")
        context = "\n\n".join(context_parts)
        
        # Call Space API (Gradio REST format)
        payload = {
            "data": [
                question,  # question parameter
                context    # context parameter  
            ]
        }
        
        headers = {"Content-Type": "application/json"}
        if HF_TOKEN:
            headers["Authorization"] = f"Bearer {HF_TOKEN}"
        
        logger.info(f"🤖 Calling Space API: {SPACE_API_URL}")
        
        response = requests.post(
            SPACE_API_URL,
            json=payload,
            headers=headers,
            timeout=120  # 2 minute timeout for inference
        )
        
        if response.status_code != 200:
            raise Exception(f"API error {response.status_code}: {response.text[:200]}")
        
        result = response.json()
        
        # Extract answer from Gradio response
        # Response format: {"data": ["answer text"], "duration": 0.5, ...}
        if "data" in result and len(result["data"]) > 0:
            answer = result["data"][0]
        else:
            answer = str(result)
        
        logger.info(f"✅ Answer from hexagon-llm-1.1b: {len(answer)} chars")
        return answer
        
    except Exception as e:
        logger.error(f"❌ Space API error: {e}")
        return f"Error connecting to model: {str(e)[:150]}"
```

### Step 4.3: Frontend API Calls (`frontend/script.js`)

```javascript
// frontend/script.js

const API_BASE = 'http://127.0.0.1:8888';

async function askQuestion(question) {
    try {
        // 1. Send question to backend
        const response = await fetch(`${API_BASE}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: question })
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        // 2. Get answer + audio URL from backend
        const data = await response.json();
        
        // 3. Display answer
        displayAnswer(data.answer, data.sources);
        
        // 4. Play audio if available
        if (data.audio_url) {
            playAudio(`${API_BASE}${data.audio_url}`);
        }
        
        return data;
        
    } catch (error) {
        console.error('Ask error:', error);
        displayError(error.message);
    }
}

function playAudio(url) {
    const audio = new Audio(url);
    audio.play();
}
```

### Step 4.4: Complete Request/Response Flow

#### Request Flow

```
1. User types: "What is Hexagon Labs?"
         ↓
2. Frontend sends POST to /ask
   {
     "question": "What is Hexagon Labs?"
   }
         ↓
3. Backend receives request
         ↓
4. Backend queries ChromaDB for relevant chunks
         ↓
5. Backend calls Space API with context
   POST https://fa00-k4mrthrohrnoai34u50u--raccoonspace.hf.space/run/generate_answer
   {
     "data": [
       "What is Hexagon Labs?",
       "[Source: TestforHexagon.txt] Hexagon Labs is a technology company..."
     ]
   }
         ↓
6. Space runs inference on hexagon-llm-1.1b
         ↓
7. Space returns answer
   {
     "data": ["Hexagon Labs is a technology company specializing in..."],
     "duration": 2.3
   }
         ↓
8. Backend generates TTS audio (local Piper)
         ↓
9. Backend returns to frontend
   {
     "answer": "Hexagon Labs is a technology company...",
     "sources": [...],
     "audio_url": "/audio/answer_20260331_194027.wav"
   }
         ↓
10. Frontend displays answer + plays audio
```

#### Response Timeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        REQUEST TIMELINE                                  │
│                                                                          │
│  0s    │ User clicks "Ask"                                              │
│  0.1s  │ Frontend sends HTTP POST to backend                            │
│  0.2s  │ Backend queries ChromaDB (local, ~100ms)                       │
│  0.3s  │ Backend calls Space API                                        │
│  0.5s  │ Space receives request                                         │
│  0.5-2.5s │ Model inference (GPU, ~2 seconds)                          │
│  2.6s  │ Space returns answer                                           │
│  2.7s  │ Backend generates TTS (local, ~1 second)                       │
│  3.7s  │ Backend returns response to frontend                           │
│  3.8s  │ Frontend displays answer + plays audio                         │
│                                                                          │
│  TOTAL: ~3-4 seconds from click to answer                               │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Part 5: Data Flow Deep Dive

### Complete Data Transformation Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     DATA TRANSFORMATION PIPELINE                        │
│                                                                          │
│  USER INPUT                                                             │
│  "What is Hexagon Labs?"                                                │
│         │                                                               │
│         ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  FRONTEND (JavaScript)                                           │   │
│  │  - Captures user input                                           │   │
│  │  - Validates question                                            │   │
│  │  - Sends JSON: {"question": "..."}                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│         │                                                               │
│         ▼ HTTP POST /ask                                                │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  BACKEND (FastAPI)                                               │   │
│  │  1. Receive JSON request                                         │   │
│  │  2. Validate question (length, content)                          │   │
│  │  3. Embed question with sentence-transformers                    │   │
│  │     Input: "What is Hexagon Labs?"                               │   │
│  │     Output: [0.123, -0.456, 0.789, ...] (384 dimensions)        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│         │                                                               │
│         ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  CHROMADB (Vector Search)                                        │   │
│  │  1. Compare question embedding to document embeddings            │   │
│  │  2. Return top-3 most similar chunks                             │   │
│  │  3. Include metadata (source, score)                             │   │
│  │                                                                  │   │
│  │  Output:                                                         │   │
│  │  [                                                               │   │
│  │    {"text": "Hexagon Labs is...", "source": "doc.txt",          │   │
│  │     "score": 0.89},                                              │   │
│  │    {"text": "The company was...", "source": "doc.txt",          │   │
│  │     "score": 0.76}                                               │   │
│  │  ]                                                               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│         │                                                               │
│         ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  PROMPT CONSTRUCTION                                             │   │
│  │                                                                  │   │
│  │  Input:                                                          │   │
│  │  - Question: "What is Hexagon Labs?"                            │   │
│  │  - Chunks: [chunk1, chunk2, chunk3]                             │   │
│  │                                                                  │   │
│  │  Output (formatted for model):                                   │   │
│  │  <s>[INST] Answer based ONLY on context.                        │   │
│  │                                                                  │   │
│  │  Context:                                                        │   │
│  │  [Source: doc.txt] Hexagon Labs is...                           │   │
│  │  [Source: doc.txt] The company was...                           │   │
│  │                                                                  │   │
│  │  Question: What is Hexagon Labs?                                │   │
│  │                                                                  │   │
│  │  Answer: [/INST]                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│         │                                                               │
│         ▼ HTTP POST to Space API                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  HF SPACES (hexagon-llm-1.1b)                                    │   │
│  │                                                                  │   │
│  │  1. Receive prompt                                               │   │
│  │  2. Tokenize: Convert text to token IDs                          │   │
│  │     "What" → 1234, "is" → 567, "Hexagon" → 890, ...             │   │
│  │  3. Forward pass through model layers                            │   │
│  │     - Embedding layer                                           │   │
│  │     - 22 transformer layers                                     │   │
│  │     - Output layer                                              │   │
│  │  4. Generate tokens autoregressively                             │   │
│  │     Token 1: "Hexagon" (probability: 0.92)                       │   │
│  │     Token 2: " " (probability: 0.98)                             │   │
│  │     Token 3: "Labs" (probability: 0.89)                          │   │
│  │     ... (continue until EOS token)                               │   │
│  │  5. Decode tokens to text                                        │   │
│  │     [1234, 567, 890, ...] → "Hexagon Labs is..."                │   │
│  │                                                                  │   │
│  │  Output:                                                         │   │
│  │  {"data": ["Hexagon Labs is a technology company..."]}          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│         │                                                               │
│         ▼ JSON Response                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  BACKEND (Response Processing)                                   │   │
│  │                                                                  │   │
│  │  1. Parse JSON response                                          │   │
│  │  2. Extract answer text                                          │   │
│  │  3. Clean up (remove special tokens, trim)                       │   │
│  │  4. Pass to TTS module                                           │   │
│  │                                                                  │   │
│  │  TTS Processing:                                                 │   │
│  │  1. Call Piper CLI: piper -m model.onnx -f output.wav           │   │
│  │  2. Input: "Hexagon Labs is a technology company..."            │   │
│  │  3. Piper converts text → phonemes → audio waveform             │   │
│  │  4. Output: WAV file (22050 Hz, 16-bit, mono)                   │   │
│  │                                                                  │   │
│  │  Final Response:                                                 │   │
│  │  {                                                               │   │
│  │    "answer": "Hexagon Labs is a technology company...",         │   │
│  │    "sources": [...],                                             │   │
│  │    "audio_url": "/audio/answer_20260331_194027.wav"             │   │
│  │  }                                                               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│         │                                                               │
│         ▼ HTTP Response                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  FRONTEND (Display)                                              │   │
│  │                                                                  │   │
│  │  1. Receive JSON response                                        │   │
│  │  2. Display answer in chat UI                                    │   │
│  │  3. Display source citations                                     │   │
│  │  4. Create Audio element with audio_url                          │   │
│  │  5. Auto-play audio                                              │   │
│  │  6. Show "Play Again" button                                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│         │                                                               │
│         ▼                                                               │
│  USER HEARS ANSWER + SEES RESPONSE                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

### Token Flow Example

```
Original Text:
"What is Hexagon Labs?"

↓ Tokenization (tokenizer converts to IDs)
Tokens: [1, 5765, 338, 47234, 8901, 2]
        │  │     │    │      │     │
        │  │     │    │      │     └─ </s> (end token)
        │  │     │    │      └─ "Labs"
        │  │     │    └─ "Hexagon"
        │  │     └─ "is"
        │  └─ "What"
        └─ <s> (start token)

↓ Model Processing (22 transformer layers)
Layer 1:  Contextual embeddings
Layer 2:  Attention patterns
...
Layer 22: Final representations

↓ Generation (autoregressive)
Step 1: Predict next token → "Hexagon" (ID: 47234)
Step 2: Predict next token → " " (ID: 338)
Step 3: Predict next token → "Labs" (ID: 8901)
Step 4: Predict next token → " is" (ID: 5765)
...
Step N: Predict EOS token → Stop

↓ Detokenization (IDs back to text)
[47234, 338, 8901, 5765, ...] → "Hexagon Labs is a technology company..."
```

---

## 🐛 Troubleshooting & Best Practices

### Common Training Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| **Out of Memory** | Batch size too large | Reduce `per_device_train_batch_size` to 2 or 1 |
| **Model doesn't learn** | Learning rate too high | Reduce to 1e-5 or 5e-5 |
| **Overfitting** | Too many epochs | Reduce to 2 epochs, add dropout |
| **Garbage output** | Bad training data | Clean and verify your JSONL format |
| **Slow training** | No GPU acceleration | Enable `fp16=True` and `device_map="auto"` |

### Common Deployment Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| **Space 404** | Wrong URL format | Use double hyphen: `owner--space.hf.space` |
| **Model still loading** | First inference on CPU | Wait 5-10 min or upgrade to GPU |
| **API timeout** | Inference too slow | Increase timeout to 120s in `llm.py` |
| **Authentication failed** | Invalid token | Regenerate token with correct permissions |

### Best Practices

#### For Training
1.  **Start small**: 50-100 examples first, then scale
2.  **Validate data**: Check for typos, inconsistencies
3.  **Use LoRA**: Much faster than full fine-tuning
4.  **Monitor loss**: Should decrease each epoch
5.  **Test before upload**: Verify model works locally first

#### For Deployment
1.  **Request GPU early**: Approval takes 24-48 hours
2.  **Use caching**: Model loads once, then stays warm
3.  **Add health checks**: Monitor Space status
4.  **Implement fallbacks**: Handle API failures gracefully
5.  **Log everything**: Debug issues faster

#### For Integration
1.  **Use environment variables**: Never hardcode tokens
2.  **Add retries**: Network calls can fail
3.  **Show loading states**: Users need feedback
4.  **Cache responses**: Reduce API calls for repeated questions
5.  **Test end-to-end**: Verify full flow before demo

---

## 🎓 Summary: Your Complete Journey

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    COMPLETE PROJECT TIMELINE                             │
│                                                                          │
│  Week 1: Training                                                        │
│  ├─ Day 1-2: Prepare training data (200+ examples)                      │
│  ├─ Day 3: Set up Colab, start training                                 │
│  └─ Day 4-5: Test fine-tuned model locally                              │
│                                                                          │
│  Week 2: Deployment                                                      │
│  ├─ Day 1: Upload model to Hugging Face Hub                             │
│  ├─ Day 2: Create Space, deploy app                                     │
│  ├─ Day 3: Request GPU upgrade                                          │
│  └─ Day 4-5: Wait for approval, test API                                │
│                                                                          │
│  Week 3: Integration                                                     │
│  ├─ Day 1: Update backend llm.py with Space API                         │
│  ├─ Day 2: Test end-to-end flow                                         │
│  ├─ Day 3: Fix any issues                                               │
│  └─ Day 4-5: Polish UI, prepare demo                                    │
│                                                                          │
│  TOTAL: ~3 weeks from zero to production-ready                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### What You've Built

✅ **Custom fine-tuned LLM** trained on your data  
✅ **Cloud deployment** with free GPU access  
✅ **Production backend** with RAG + TTS  
✅ **Professional frontend** with real-time updates  
✅ **Complete documentation** for future maintenance  

### Next Steps

1.  **Add more training data** → Improve model quality
2.  **Experiment with models** → Try Mistral-7B for better results
3.  **Add more features** → Multi-turn conversations, file uploads
4.  **Deploy to production** → Use paid endpoints for reliability
5.  **Share your work** → Portfolio, GitHub, blog post

---

> **You now have a complete, production-ready AI system with your own custom model!** 🎉⬡🤖

*Ready to train your own model? Start with the Colab script in Part 1!* 🚀
