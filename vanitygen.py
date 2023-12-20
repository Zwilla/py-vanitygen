# -*- coding: utf-8 -*-
#
#    coineva vanitygen.py
#    Copyright (C) 2016 February 
#    1200 Web Development
#    http://1200wd.com/
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
from bitcoin import *
import timeit
import random
import multiprocessing

from cryptos import fast_multiply, pubkey_to_address, encode_privkey

from lib.pybitcointools.cryptos import G

bitcoinAddress = '12XqeqZRVkBDgmPLVY4ZC6Y4ruUUEug8Fx'
filenameFound = bitcoinAddress + ".txt"


def writeFoundDatas(filename, address, pk):
    with open(filename, 'a') as result:
        resultToWrite = "Address: {}  PK: {}\n".format(address, pk)
        result.write(resultToWrite)


def address_search(pipeout, search_for=bitcoinAddress):
    global filenameFound
    global bitcoinAddress
    privkey = random.randrange(2 ** 256)
    address = ''
    count = 0
    start = timeit.default_timer()

    # os.write(pipeout, "Searching for %s (pid %s)" % (search_for, os.getpid()))

    while search_for not in address:
        privkey += 1
        pubkey_point = fast_multiply(G, privkey)
        address = pubkey_to_address(pubkey_point)
        count += 1
        if not count % 1000:
            print("Searched {} in {} seconds ".format(count, timeit.default_timer() - start))

    HexPrivKey = encode_privkey(privkey, 'hex')
    print("Found address {} in {} seconds ".format(address, timeit.default_timer() - start))
    print("Private key HEX {}".format(HexPrivKey))
    writeFoundDatas(filenameFound, bitcoinAddress, HexPrivKey)


def main():
    # processors = multiprocessing.cpu_count()
    # processors = 2
    # print("You have %d processors so starting %d threads" % (processors, processors))
    # for i in range(processors):

    pipein, pipeout = os.pipe()
    address_search(pipeout)

    print('Main process exiting')


main()
