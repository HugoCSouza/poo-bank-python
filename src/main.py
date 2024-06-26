from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty
import datetime
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
    def __init__(self, numero: int, cliente: PessoaFisica, agencia: str, limite: float = 500, limite_saques: int  = 3) -> None:
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
    
    def __str__(self) -> str:
        return f""" 
                Agência: {self._agencia}
                Nº da conta: {self._numero}
                Titular: {self._cliente._nome}"""
                
class Historico:
    def __init__(self) -> None:
        self._transacoes = []
    
    @property    
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao: Transacao):
        self._transacoes.append(
            {
                "Tipo": transacao.__class__.__name__,
                "Valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )
        
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
            
class Deposito(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

