#!/bin/bash
# demo_knowledge_update.sh
# Demonstrates RAG-based "up-training" competency

echo "=============================================="
echo "  RAG Knowledge Update Demo"
echo "=============================================="
echo ""

# Step 1: Ask question BEFORE adding new knowledge
echo "🔍 Step 1: Ask question BEFORE knowledge update"
echo "Question: What is Hexagon Lab?"
echo ""
curl -s -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Hexagon Lab?"}' | python3 -m json.tool | grep -A 5 '"answer"'
echo ""
echo "⚠️  Expected: 'I don't have enough information' or similar"
echo ""
read -p "Press Enter to continue..."
echo ""

# Step 2: Add new document with knowledge
echo "📝 Step 2: Adding new knowledge document..."
echo "Creating: data/raw_docs/hexagon_lab.txt"
mkdir -p data/raw_docs
cat > data/raw_docs/hexagon_lab.txt << 'EOF'
Hexagon Lab is a research division focused on AI safety and multimodal systems.
The lab specializes in combining LLMs with Text-to-Speech technology for accessible AI interfaces.
Founded in 2024, Hexagon Lab aims to reduce AI hallucination through RAG-based architectures.
EOF
echo "✅ Document created successfully"
echo ""
read -p "Press Enter to continue..."
echo ""

# Step 3: Re-index knowledge base
echo "🔄 Step 3: Re-indexing knowledge base (up-training)..."
curl -s -X POST http://localhost:8000/update-knowledge | python3 -m json.tool
echo ""
read -p "Press Enter to continue..."
echo ""

# Step 4: Ask same question AFTER update
echo "🔍 Step 4: Ask SAME question AFTER knowledge update"
echo "Question: What is Hexagon Lab?"
echo ""
curl -s -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Hexagon Lab?"}' | python3 -m json.tool | grep -A 5 '"answer"'
echo ""
echo "✅ Expected: Answer now includes information about Hexagon Lab"
echo ""
echo "=============================================="
echo "  Demo Complete!"
echo "=============================================="