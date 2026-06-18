import torch

def generate_agent_vote(text, persona, dynamic_context, model, tokenizer):
    system_prompt = f"{persona}\n{dynamic_context}\nClassify the following text as 0 (Benign), 1 (IT Support), or 2 (Malicious). Only output the single digit."
    
    chat = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ]
    
    formatted = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
    
    # THE FIX: Automatically detect hardware (GPU vs CPU)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    inputs = tokenizer([formatted], return_tensors="pt").to(device)
    
    with torch.no_grad():
        output_ids = model.generate(inputs.input_ids, max_new_tokens=2, temperature=0.0, do_sample=False)
    
    raw_output = tokenizer.decode(output_ids[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
    
    for char in raw_output:
        if char in ['0', '1', '2']:
            return int(char)
    return -1