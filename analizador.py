class Parser:
    def __init__(self, input_expr):
        self.input_expr = input_expr.replace(" ", "")  # Remove espacos em branco
        self.index = 0
        self.path = []  # Para registrar o caminho da recursao
        self.current_chain = []  # Para construir a cadeia analisada

    def current_token(self):
        return self.input_expr[self.index] if self.index < len(self.input_expr) else None

    def match(self, token):
        if self.current_token() == token:
            self.current_chain.append(token)
            self.index += 1
            return True
        return False

    def log(self, rule, new_chain):
        # Registra a producao no caminho da recursao
        self.path.append(f"{rule: <10} {''.join(new_chain)}")

    def parse_I(self):
        self.log("I -> S", ["S"])
        return self.parse_S()

    def parse_S(self):
        self.log("S -> TK", self.current_chain + ["T", "K"])
        if self.parse_T():
            return self.parse_K()
        return False

    def parse_K(self):
        if self.match('+'):
            self.log("K -> +TK", self.current_chain + ["T", "K"])
            if self.parse_T():
                return self.parse_K()
            return False
        elif self.match('-'):
            self.log("K -> -TK", self.current_chain + ["T", "K"])
            if self.parse_T():
                return self.parse_K()
            return False
        self.log("K -> e", self.current_chain)
        return True

    def parse_T(self):
        self.log("T -> FZ", self.current_chain + ["F", "Z"])
        if self.parse_F():
            return self.parse_Z()
        return False

    def parse_Z(self):
        if self.match('*'):
            self.log("Z -> *FZ", self.current_chain + ["F", "Z"])
            if self.parse_F():
                return self.parse_Z()
            return False
        elif self.match('/'):
            self.log("Z -> /FZ", self.current_chain + ["F", "Z"])
            if self.parse_F():
                return self.parse_Z()
            return False
        self.log("Z -> e", self.current_chain)
        return True

    def parse_F(self):
        if self.match('('):
            self.log("F -> (S)", self.current_chain + ["S", ")"])
            if self.parse_S() and self.match(')'):
                return True
            return False
        elif self.current_token() == '-':
            self.log("F -> -N", self.current_chain + ["N"])
            self.current_chain.append('-')
            self.index += 1
            return self.parse_N()
        else:
            self.log("F -> N", self.current_chain + ["N"])
            return self.parse_N()

    def parse_N(self):
        if self.current_token() and self.current_token() in '123456789':
            self.current_chain.append(self.current_token())
            self.log(f"N -> {self.current_token()}D", self.current_chain + ["D"])
            self.index += 1
            return self.parse_D()
        return False

    def parse_D(self):
        if self.current_token() and self.current_token() in '0123456789':
            self.current_chain.append(self.current_token())
            self.log(f"D -> {self.current_token()}D", self.current_chain + ["D"])
            self.index += 1
            return self.parse_D()
        self.log("D -> e", self.current_chain)
        return True

    def parse(self):
        self.path = []
        self.current_chain = []
        result = self.parse_I() and self.index == len(self.input_expr)
        return result, self.path


# Funcao para processar cadeias de um arquivo
def process_file(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        lines = infile.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Identifica se a cadeia e esperada como aceita ou rejeitada
            expected = line[:2]
            expression = line[2:].strip()

            parser = Parser(expression)
            accepted, recursion_path = parser.parse()

            # Verifica o resultado
            result = "Cadeia aceita" if accepted else "Cadeia rejeitada"
            expected_result = "Aceita" if expected == "A:" else "Rejeitada"

            # Registra os resultados no arquivo de saida
            outfile.write(f"Expressao: {expression}\n")
            outfile.write(f"Esperado: {expected_result} | Resultado: {result}\n")
            outfile.write("Caminho da recursao e formacao da cadeia:\n")
            for step in recursion_path:
                outfile.write(f"{step}\n")
            outfile.write("\n")


# Arquivo de entrada e saida
input_file = "exemplos.txt"  # Insira aqui o nome do arquivo de entrada
output_file = "resultado.txt"  # Insira aqui o nome do arquivo de saida

# Processa o arquivo
process_file(input_file, output_file)

print(f"Processamento concluido. Verifique o arquivo {output_file} para os resultados.")
