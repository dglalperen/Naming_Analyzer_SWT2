import openai

def check_openai_key(api_key):
    openai.api_key = api_key
    try:
        # Versuchen Sie, die verfügbaren Modelle aufzulisten
        openai.Model.list()
        print("Der OpenAI-API-Schlüssel ist gültig.")
    except openai.OpenAIError:
        print("Der OpenAI-API-Schlüssel ist ungültig.")

# Ersetzen Sie 'Ihr-OpenAI-API-Schlüssel' durch Ihren tatsächlichen OpenAI-API-Schlüssel.
gpt4_key = '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'
check_openai_key(gpt4_key)
