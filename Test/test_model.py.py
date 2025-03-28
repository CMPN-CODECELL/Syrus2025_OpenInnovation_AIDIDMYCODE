import torch
from transformers import BertTokenizer, BertForSequenceClassification
from pathlib import Path

# 1. Load model with error handling
try:
    MODEL_PATH = Path(r"F:\modelllll\legal_bert_finetuned")
    tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
    model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
    model.eval()
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Failed to load model: {str(e)}")
    exit()

# 2. Improved classification with threshold adjustment
def analyze_question(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    
    probs = torch.softmax(outputs.logits, dim=1)[0]
    legal_prob = probs[1].item()  # Probability it's a legal question
    
    # Adjusted threshold (originally 0.5, now 0.3 to reduce false negatives)
    is_legal = legal_prob > 0.3  
    
    return {
        "is_legal": is_legal,
        "confidence": legal_prob,
        "raw_probs": probs.tolist()
    }

# 3. Enhanced testing
print("\n🦉 Legal Bot Tester - Type 'quit' to exit\n")
while True:
    prompt = input("Your question: ").strip()
    if prompt.lower() == 'quit':
        break
    
    result = analyze_question(prompt)
    print(f"\n🔍 Analysis for: '{prompt}'")
    print(f"   Legal probability: {result['confidence']:.1%}")
    print(f"   Raw probabilities: [Non-legal: {result['raw_probs'][0]:.1%}, Legal: {result['raw_probs'][1]:.1%}]")
    
    if result["is_legal"]:
        print("✅ VERDICT: Legal question")
        if "divorce" in prompt.lower():
            print("💡 Suggested steps:\n1. File a petition in family court\n2. Serve your spouse\n3. Attend mediation")
        elif "tenant" in prompt.lower():
            print("💡 Suggested steps:\n1. Review your lease\n2. Document issues\n3. Send written notice")
    else:
        print("❌ VERDICT: Not a legal question")
        print("💡 Try rephrasing like:\n- 'What are the legal steps for divorce?'\n- 'Can a landlord evict without cause?'")
    
    print("-" * 50)