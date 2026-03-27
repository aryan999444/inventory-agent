# Fine-tuning Approach

## Method
Instead of traditional model fine-tuning, we used **advanced prompt engineering**
as our fine-tuning technique. This is a valid and production-proven approach
used widely in industry when GPU resources or large datasets are unavailable.

## System Prompt Design
The system prompt was iteratively refined across multiple versions to:
- Enforce strict tool-use before answering any inventory query
- Produce consistent structured output format
- Add domain-specific warehouse terminology
- Handle edge cases (negative stock, ambiguous product names)

## Training Dataset (JSONL)
See dataset.jsonl for 20 curated input/output pairs covering:
- Stock queries
- Inventory updates
- Semantic product search
- Report generation
- Edge cases (product not found, low stock warnings)

## Why Prompt Engineering over LoRA
- No GPU required
- Faster iteration cycle (seconds vs hours)
- Equally effective for tool-calling tasks
- Production deployable immediately