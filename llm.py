from transformers import pipeline

generator = pipeline("text-generation", model="distilgpt2")


def generate_llm_response(prompt):
    response = generator(prompt, max_length=100, num_return_sequences=1, truncation=True)
    generated_text = response[0]['generated_text']
    return generated_text


qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")


def get_factual_answer(question, context):
    result = qa_pipeline(question=question, context=context)
    return result['answer']