import ollama


MODEL = "llama3.2:latest"


def generate_recommendations(prompt):

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.2,
            "num_predict": 250
        },
        keep_alive="10m"
    )

    return response["message"]["content"]