import ollama

def callOllama(model: str, prompt: str) -> str:
    print(f"Ollama called with the given prompt: {prompt}")
    try:
        response = ollama.generate(
            model=model,
            prompt=prompt
        )
        print(f"Response received: {response.response}")
        return response.response
    except Exception as e:
        print(f'"error": {str(e)}')
        return {"error": str(e)}

if __name__ == "__main__":
    print("This is a.py")