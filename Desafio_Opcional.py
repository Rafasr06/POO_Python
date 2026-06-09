from abc import ABC, abstractmethod
from enum import Enum
from typing import List


class TipoTransacao(Enum):
    DEPOSITO = "Depósito"
    SAQUE = "Saque"
    TRANSFERENCIA = "Transferência"


class Transacao:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor


class Cliente:
    def __init__(
        self,
        nome,
        cpf,
        email,
        usuario,
        senha
    ):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.usuario = usuario
        self.senha = senha


class Conta(ABC):
    contador = 0

    def __init__(self, titular):
        Conta.contador += 1

        self.__numero = Conta.contador
        self.__saldo = 0.0
        self.__titular = titular
        self.__transacoes: List[Transacao] = []

    def get_saldo(self):
        return self.__saldo

    def _set_saldo(self, saldo):
        self.__saldo = saldo

    def registrar_transacao(self, tipo, valor):
        self.__transacoes.append(
            Transacao(tipo, valor)
        )

    def listar_transacoes(self):
        if not self.__transacoes:
            print("Nenhuma transação.")
            return

        for t in self.__transacoes:
            print(
                f"{t.tipo.value} - "
                f"R$ {t.valor:.2f}"
            )

    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor

            self.registrar_transacao(
                TipoTransacao.DEPOSITO,
                valor
            )

    def consultar_saldo(self):
        print(
            f"Saldo: "
            f"R$ {self.__saldo:.2f}"
        )

    @abstractmethod
    def sacar(self, valor):
        pass

    @abstractmethod
    def transferir(
        self,
        destino,
        valor
    ):
        pass


class ContaCorrente(Conta):
    TAXA = 0.10

    def sacar(self, valor):

        total = valor * (1 + self.TAXA)

        if total <= self.get_saldo():

            self._set_saldo(
                self.get_saldo() - total
            )

            self.registrar_transacao(
                TipoTransacao.SAQUE,
                valor
            )

        else:
            print("Saldo insuficiente.")

    def transferir(
        self,
        destino,
        valor
    ):

        total = valor * (1 + self.TAXA)

        if total <= self.get_saldo():

            self._set_saldo(
                self.get_saldo() - total
            )

            destino.depositar(valor)

            self.registrar_transacao(
                TipoTransacao.TRANSFERENCIA,
                valor
            )

        else:
            print("Saldo insuficiente.")


class ContaPoupanca(Conta):
    LIMITE = 500

    def sacar(self, valor):

        if valor <= self.get_saldo():

            self._set_saldo(
                self.get_saldo() - valor
            )

            self.registrar_transacao(
                TipoTransacao.SAQUE,
                valor
            )

        else:
            print("Saldo insuficiente.")

    def transferir(
        self,
        destino,
        valor
    ):

        if valor > self.LIMITE:
            print(
                "Limite máximo "
                "de R$500."
            )
            return

        if valor <= self.get_saldo():

            self._set_saldo(
                self.get_saldo() - valor
            )

            destino.depositar(valor)

            self.registrar_transacao(
                TipoTransacao.TRANSFERENCIA,
                valor
            )

        else:
            print("Saldo insuficiente.")


def login(cliente):

    usuario = input("Usuário: ")
    senha = input("Senha: ")

    return (
        usuario == cliente.usuario
        and senha == cliente.senha
    )


cliente = Cliente(
    "Rafael",
    "12345678900",
    "rafael@email.com",
    "rafael",
    "123"
)

corrente = ContaCorrente(cliente)
poupanca = ContaPoupanca(cliente)

if not login(cliente):
    print("Login inválido.")
    exit()

print("\n1 - Conta Corrente")
print("2 - Conta Poupança")

op = input("Escolha a conta: ")

if op == "1":
    conta = corrente
elif op == "2":
    conta = poupanca
else:
    print("Conta inválida.")
    exit()

while True:

    print("\n1 - Depositar")
    print("2 - Sacar")
    print("3 - Consultar Transações")
    print("4 - Consultar Saldo")
    print("0 - Sair")

    opcao = input("Opção: ")

    if opcao == "1":

        valor = float(
            input("Valor: ")
        )

        conta.depositar(valor)

    elif opcao == "2":

        valor = float(
            input("Valor: ")
        )

        conta.sacar(valor)

    elif opcao == "3":

        conta.listar_transacoes()

    elif opcao == "4":

        conta.consultar_saldo()

    elif opcao == "0":

        print("Encerrando...")
        break

    else:

        print("Opção inválida.")