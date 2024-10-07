#!/bin/bash

# Start Ollama in the background.
/bin/ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

echo "🔴 Retrieve Qwen model..."
ollama pull qwen2:0.5b
echo "🟢 Done!"

# Wait for Ollama process to finish.
wait $pid