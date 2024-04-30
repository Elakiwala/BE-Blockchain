from hashlib import sha256
import time
import random
from txOutput import TxOutputs
from txInputs import TxInputs
from datetime import datetime

class Transactions:
    def __init__(self, comment):
        self.timestamp = datetime.now()
        self.nb_inputs = 0
        self.lst_inputs = []  # une ou plusieurs UTXO
        self.nb_outputs = 0
        self.lst_outputs = []  # limité à trois sorties : la tx+reward+change
        # les adresses sont dans les scripts
        self.comment = comment

    def print_trans(self):
        print("Nb inputs:", self.nb_inputs)
        print("Nb outputs:", self.nb_outputs)
        print("Inputs list:")
        for tx_input in self.lst_inputs:
            tx_input.print_input()
        print()
        print("Outputs list:")
        for tx_output in self.lst_outputs:
            tx_output.print_output()
        print("Comments:", self.comment)

    def coinbase_tx(self, reward, user):
        lock_script = [
            "<tx sign " + user + ">",
            "<pubKey " + user + ">",
            "DUP",
            "HASH"
        ]
        out_tx = TxOutputs(0, "0", lock_script, reward)
        self.lst_outputs.append(out_tx)
        self.nb_inputs = len(self.lst_inputs)
        self.nb_outputs = len(self.lst_outputs)

    def lock_script(self, user):
        lock_script = [
            "<tx sign " + user + ">",
            "<pubKey " + user + ">",
            "DUP",
            "HASH"
        ]
        return lock_script

    def fees(self):
        input_amount = sum(tx_input.amount for tx_input in self.lst_inputs)
        output_amount = sum(tx_output.amount for tx_output in self.lst_outputs)
        return input_amount - output_amount

    def market_tx(self, utxo_list, user, dest, amount, fee_rate):
        unlock_script = ["H(<pubKey " + user + ">)", "EQ", "VER"]
        lock_script = self.lock_script(dest)

        lock_script_change = self.lock_script(user)
        lst_utxo_in = []
        hash_source_tx = ""
        change = 0
        fees = 0
        in_amount = 0
        global_in_amount = 0
        hauteur = 0

        fees = amount * fee_rate // 100
        for utxo in utxo_list:
            if utxo.verify(unlock_script):
                global_in_amount += utxo.amount
                lst_utxo_in.append(utxo)
                if global_in_amount >= amount + fees:
                    break

        change = global_in_amount - amount - fees
        for utxo in lst_utxo_in:
            hash_source_tx = utxo.hash
            in_amount = utxo.montant
            tx_input = TxInputs(hash_source_tx, hauteur, 0, in_amount, len(unlock_script), unlock_script, "market tx")
            self.lst_inputs.append(tx_input)
            utxo_list.remove(utxo)

        out_change = TxOutputs(1, "0", lock_script_change, change)
        out_change.hash = out_change.calculate_hash()
        out_tx = TxOutputs(0, "0", lock_script, amount)

        self.lst_outputs.extend([out_tx, out_change])
        self.nb_inputs = len(self.lst_inputs)
        self.nb_outputs = len(self.lst_outputs)

        utxo_list.extend([out_tx, out_change])
        return utxo_list

    def stringify(self):
        return str(self.timestamp) + str(self.nb_inputs) + str(self.lst_inputs) + str(self.nb_outputs) + str(self.lst_outputs) + self.comment

