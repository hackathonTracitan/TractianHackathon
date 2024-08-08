generate_specification_prompt = """
    Você é um assistente especializado em engenharia de máquinas. 
    Eu tenho uma consulta sobre a seguinte máquina: {query}.
    Aqui está uma lista de informações e resultados obtidos na interet, que podem ou não estar relacionados com a máquina em questão:
    
    {results}
    
    Com base nessas informações, você pode gerar as especificações detalhadas para essa máquina?
"""