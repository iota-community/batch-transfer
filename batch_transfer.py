"""
This application generates a CSV file with seeds and addresses and will evenly distribute the funds of the main seed over these addresses.
"""
from argparse import ArgumentParser
from sys import argv
import csv
from time import sleep
from random import choice
from iota.adapter.wrappers import RoutingWrapper

from iota import (
  __version__,
  Address,
  Iota,
  ProposedTransaction,
  Tag,
  TryteString,
)

from iota.crypto.addresses import AddressGenerator

from six import text_type

def batch_transfer(filename, node_uri, seed, amount_of_seeds=100, amount_per_seed=10000, batch_size=25, depth=3, tag='GIFT', message='', pow_node_uri=None):
    needed_funds = amount_of_seeds * amount_per_seed
    print('You are about to spend %s iota spread out over %s addresses.' % (needed_funds, amount_of_seeds))
    print('Checking your seeds balance...')
    
    if pow_node_uri:
        router = RoutingWrapper(node_uri)
        router.add_route('attachToTangle', pow_node_uri)
        api = Iota(router, seed)
    else:
        api = Iota(node_uri, seed)

    inputs = api.get_inputs()
    balance = inputs['totalBalance']

    if balance < needed_funds:
        print("You don't have enough funds available on your SEED, please make sure your seed has at least %si available!" % needed_funds)
        return

    print('You have enough available to transfer the %si, Generating %d seeds and addresses now...' % (needed_funds, amount_of_seeds))
    
    seedlist = []
    for i in range(amount_of_seeds):
        random_seed = ''.join([choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ9') for x in range(81)])
        gen = AddressGenerator(random_seed)
        new_addr = gen.get_addresses(0, 1, 2)[0]
        seedlist.append((random_seed, new_addr))
        print('.', sep='', end='', flush=True)

    print('\n')
    
    with open(filename, 'w') as fh:
        writer = csv.writer(fh)
        writer.writerow(['Seed', 'Address', 'Iota'])

        for gseed, gaddr in seedlist:
            writer.writerow([gseed, gaddr, amount_per_seed])

    print('All seeds and addresses are now available in %s!' % filename)

    amount_of_bundles = (amount_of_seeds // batch_size) + 1

    if amount_of_seeds % batch_size == 0:
        amount_of_bundles -= 1

    print('We will generate and send %d bundles containing %d transactions per bundle max, this can take a while...' % (amount_of_bundles, batch_size))
    
    from_addr = None
    for i in range(amount_of_bundles):
        sliced = seedlist[i*batch_size:(i+1)*batch_size]
        print('Starting transfer of bundle %d containing %d seeds...' % (i+1, len(sliced)))
        
        transfers = []
        for gseed, gaddr in sliced:
            transfers.append(
                ProposedTransaction(
                    address=gaddr,
                    value=amount_per_seed,
                    tag=Tag(tag),
                    message=TryteString.from_string(message),
                )
            )


        bundle = api.send_transfer(
            depth=depth,
            transfers=transfers
        )

        for tx in bundle['bundle'].transactions:
            if tx.current_index == tx.last_index:
                print('Remainder:', tx.current_index, tx.address, tx.value)
                from_addr = tx.address
                
                if amount_per_seed == 0:
                    continue

                print('Waiting for the TX to confirm and the remainder address (%s) to fill...' % tx.address)
                while True:
                    balances = api.get_balances([tx.address], 100)
                    if balances['balances'][0] > 0:
                        break
                    else:
                        print('...', sep='', end='', flush=True)

                    sleep(5)

                print('\n')

        print('Transfer complete.')

    print('All done!')

if __name__ == '__main__':
    parser = ArgumentParser(
        description=__doc__,
        epilog='PyOTA v{version}'.format(version=__version__),
    )
    
    parser.add_argument(
        '--filename',
        type=text_type,
        default='seeds.csv',
        help='filename of the CSV file to write all seeds/addresses to',
    )

    parser.add_argument(
        '--seed',
        type=text_type,
        required=True,
        default='',
        help='Main seed with enough funds to transfer to all the addresses to generate',
    )

    parser.add_argument(
        '--depth',
        type=int,
        default=3,
        help=
        'Depth at which to attach the bundle.'
        '(defaults to 3).',
    )

    parser.add_argument(
        '--message',
        type=text_type,
        default='Hello World!',
        help=
        'Transfer message.'
        '(defaults to Hello World!).',
    )

    parser.add_argument(
        '--tag',
        type=text_type,
        default=b'EXAMPLE',
        help=
        'Transfer tag'
        '(defaults to EXAMPLE).',
    )

    parser.add_argument(
        '--node_uri',
        type=text_type,
        default='http://localhost:14265/',
        help=
        'URI of the node to connect to.'
        '(defaults to http://localhost:14265/).',
    )
    
    parser.add_argument(
        '--pow_node_uri',
        type=text_type,
        default=None,
        help=
        'URI of the node to connect to.'
        '(defaults to http://localhost:14265/).',
    )

    parser.add_argument(
        '--amount_of_seeds',
        type=int,
        default=100,
        help=
        'Amount of seeds to generate'
        '(defaults to 100).',
    )
    
    parser.add_argument(
        '--amount_per_seed',
        type=int,
        default=10000,
        help=
        'Amount of iota to send per generated seed'
        '(defaults to 10000).',
    )
    
    parser.add_argument(
        '--batch_size',
        type=int,
        default=25,
        help=
        'Amount of transactions per bundle'
        '(defaults to 25).',
    )

    batch_transfer(**vars(parser.parse_args(argv[1:])))


