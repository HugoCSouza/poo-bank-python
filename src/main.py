class Cliente:
    def __init__(self, endereco: str) -> None:
        self._endereco = endereco
        self._contas = []
        
    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta: Conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento) -> None:
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
    
class Conta:
    def __init__(self, numero: int, cliente: Cliente, agencia: str) -> None:
        self._saldo = 0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()
    
    @property    
    def saldo(self):
        return self._saldo
    
    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int) -> Conta:
        return cls(numero, cliente)
    
    def sacar(self, valor):
        saldo = self.saldo
        permissao = valor > saldo
        
        if valor < 0:
            print(f'{"-"*10} Valor de saque menor que R$ 0,00 {"-"*10}')
            return False
        elif not permissao:
            print(f'{"-"*10} Saldo Insuficiente! {"-"*10}')
        else:
            print(f"{'-'*10} Saque Realizado com sucesso {'-'*10}"
                  f"\t Saldo atual: R$ {self.saldo:.2f}")
        return permissao

    def depositar(self, valor):
        permissao = valor > 0
        if permissao:
            self._saldo += valor
            print(f"{'-'*10} Depósito realizado! {'-'*10}")
        else:
            print(f"{'-'*10} Valor abaixo que R$ 0,00 {'-'*10}")
        return permissao
    
class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: Cliente, agencia: str, limite: float = 500, limite_saques: int  = 3) -> None:
        super().__init__(numero, cliente, agencia)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor: float):
        numero_saques = len(transacao for transacao in self.historico.transacoes
                            if transacao["tipo"] == Saque.__name__)
        
        if valor > self._limite:
            print(f'{"-"*10} Valor do saque excede o limite! {"-"*10}')
        elif numero_saques > self._limite_saques:
            print(f'{"-"*10} Limite de saques foi atingido! {"-"*10}')
        else:
            return super().sacar(valor)
        return False