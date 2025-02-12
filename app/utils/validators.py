def is_valid_document(document: str) -> bool:
    # Remove caracteres não numéricos
    digits = ''.join(filter(str.isdigit, document))
    return len(digits) in (11, 14)  # CPF tem 11 dígitos e CNPJ tem 14 dígitos
