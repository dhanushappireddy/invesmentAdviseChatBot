import ollama

def callOllama(model: str, prompt: str) -> str:
    response = ollama.generate(
        model=model,
        prompt=prompt
    )
    return response.response
if __name__ == "__main__":
    print("This is a.py")