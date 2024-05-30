from functools import wraps


def check_none(func):

    """
        DECORADOR QUE VERIFICA SE HÁ ALGUM VALOR NÃO
        NONE EM UMA LISTA ANTES DE CHAMAR A FUNÇÃO DECORADA.

        SE TODOS OS VALORES NA LISTA FOREM NONE,
        A FUNÇÃO NÃO SERÁ CHAMADA E RETORNARÁ NONE.

        # Arguments
            func                - Required: Função a ser decorada.
                                            O primeiro parâmetro da função
                                            deve ser uma lista sobre a
                                            qual a verificação será realizada (Function)

        # Returns:
            wrapper             - Required: A função wrapper que executa
                                            a verificação e então, se apropriado,
                                            chama a função decorada (Function)

        # Example:
            @check_none
            def process_list(values):
                # Função que realiza alguma operação sobre 'values', que é uma lista.
                return sum(values)  # Exemplo de operação.

            print(process_list([1, 2, 3]))  # Saída: 6
            print(process_list([None, None]))  # Saída: None
    """

    @wraps(func)
    def wrapper(values):
        # VERIFICA SE HÁ ALGUM VALOR NÃO NONE NA LISTA
        if any(x is not None for x in values):
            return func(values)
        else:
            return None

    return wrapper
