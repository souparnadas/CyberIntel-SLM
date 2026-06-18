from agents import generate_agent_vote
from rag_engine import DynamicRAG

def process_text_stream(text, model, tokenizer, rag_engine):
    dynamic_context = rag_engine.get_dynamic_context(text)
    
    personas = [
        "You are a Threat Analyst. Focus on malicious patterns.",
        "You are a Technical Support Specialist. Focus on IT infrastructure.",
        "You are a Neutral AI Auditor. Focus on raw intent."
    ]
    
    votes = []
    for persona in personas:
        vote = generate_agent_vote(text, persona, dynamic_context, model, tokenizer)
        votes.append(vote)
        
    # Strict Confidence Routing
    if len(votes) == 3 and votes.count(votes[0]) == 3:
        return {"status": "AUTO_RESOLVED", "verdict": votes[0], "votes": votes}
    else:
        return {"status": "ESCALATED_TO_HUMAN", "verdict": None, "votes": votes}

if __name__ == "__main__":
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import warnings
    warnings.filterwarnings('ignore')

    print("Loading AI Architecture... (This might take a minute)")
    model_name = "Qwen/Qwen2.5-1.5B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
    
    print("Initializing Dynamic RAG Database...")
    rag = DynamicRAG("data/golden_set.json")
    
    test_string = "Мы скачали вашу базу клиентов. Платите 10000$."
    print(f"\n[INCOMING THREAT INTEL]: {test_string}")
    
    print("Consulting AI Agents...")
    result = process_text_stream(test_string, model, tokenizer, rag)
    
    print(f"\n[FINAL VERDICT]: {result}")