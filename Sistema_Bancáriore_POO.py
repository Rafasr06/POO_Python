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
    def __init__(self, nome, cpf, email):
        self.nome = nome
        self.cpf = cpf
        self.email = email


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
        self.__transacoes.append(Transacao(tipo, valor))

    def listar_transacoes(self):
        if not self.__transacoes:
            print("Nenhuma transação.")
        for t in self.__transacoes:
            print(f"{t.tipo.value} - R$ {t.valor:.2f}")

    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            self.registrar_transacao(TipoTransacao.DEPOSITO, valor)

    def consultar_saldo(self):
        print(f"Saldo: R$ {self.__saldo:.2f}")

    @abstractmethod
    def sacar(self, valor):
        pass

    @abstractmethod
    def transferir(self, destino, valor):
        pass


class ContaCorrente(Conta):
    TAXA = 0.10

    def sacar(self, valor):
        total = valor * (1 + self.TAXA)
        if total <= self.get_saldo():
            self._set_saldo(self.get_saldo() - total)
            self.registrar_transacao(TipoTransacao.SAQUE, valor)

    def transferir(self, destino, valor):
        total = valor * (1 + self.TAXA)
        if total <= self.get_saldo():
            self._set_saldo(self.get_saldo() - total)
            destino.depositar(valor)
            self.registrar_transacao(
                TipoTransacao.TRANSFERENCIA, valor
            )


class ContaPoupanca(Conta):
    LIMITE = 500

    def sacar(self, valor):
        if valor <= self.get_saldo():
            self._set_saldo(self.get_saldo() - valor)
            self.registrar_transacao(TipoTransacao.SAQUE, valor)

    def transferir(self, destino, valor):
        if valor <= self.LIMITE and valor <= self.get_saldo():
            self._set_saldo(self.get_saldo() - valor)
            destino.depositar(valor)
            self.registrar_transacao(
                TipoTransacao.TRANSFERENCIA, valor
            )


cliente = Cliente("Rafael", "123", "rafael@email.com")
corrente = ContaCorrente(cliente)
poupanca = ContaPoupanca(cliente)

while True:# aqui é só a criação do menu interativo.
    print("\n1-Depositar")
    print("2-Sacar")
    print("3-Transferir")
    print("4-Consultar Transações")
    print("5-Consultar Saldo")
    print("0-Sair")

    op = input("Opção: ")

    if op == "1":
        conta = input("1-Corrente 2-Poupança: ")
        valor = float(input("Valor: "))
        (corrente if conta == "1" else poupanca).depositar(valor)

    elif op == "2":
        conta = input("1-Corrente 2-Poupança: ")
        valor = float(input("Valor: "))
        (corrente if conta == "1" else poupanca).sacar(valor)

    elif op == "3":
        print("1-Corrente -> Poupança")
        print("2-Poupança -> Corrente")
        tipo = input("Escolha: ")
        valor = float(input("Valor: "))

        if tipo == "1":
            corrente.transferir(poupanca, valor)
        elif tipo == "2":
            poupanca.transferir(corrente, valor)

    elif op == "4":
        print("\nConta Corrente")
        corrente.listar_transacoes()

        print("\nConta Poupança")
        poupanca.listar_transacoes()

    elif op == "5":
        print("\nConta Corrente")
        corrente.consultar_saldo()

        print("Conta Poupança")
        poupanca.consultar_saldo()

    elif op == "0":
        break

    else:
        print("Opção inválida!")