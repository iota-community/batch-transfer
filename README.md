IOTA Batch Transaction Sender
===============================

This script allows you to distribute IOTA tokens to multiple newly generated addresses/seeds.
Define the amount of seeds, the amount of funds and the batch size yourself. This is great for
creating promotional vouchers or gifts with IOTA tokens. 

It waits between every batch/bundle until it is confirmed before it continues with the next one.
It will output a CSV file containing all newly generated seeds and addresses.

You will need to have a node that accepts remote POW, you might run into rate limits on public nodes.

Use at your own risk! Make sure you backup your seeds.csv file if the transfers succeeded so you won't overwrite it on a next run.


Installation
-------------

1. Install the dependancies using `pip install -r requirements.txt` (doing this in a virtual environment is recommended)
2. Execute `python batch_transfer.py --help` to see the available options
3. Execute `python batch_transfer.py` with the given arguments to start the process

Example
-------

Say we got a seed with 2Mi on it, and we want to send these funds to 200 new addresses with 10Ki each. To do this we execute the script like this:

`python batch_transfer.py --seed 9OCEOTY9TRYKLABTXKITTEGNP9EA9YLVGBJTMONAHPYNWJXDVNLJCOKGGVWBHXVWYZJGSYVT9OCAIXAIE --node  https://nodes.thetangle.org --amount_per_seed=10000 --amount_of_seeds=200 --batch_size=25 --tag=GIFT --message="Greetings from Dave"`

This will create 8 bundles with 25 transfers of 10ki each and a `seeds.csv` file containing the seed, address and value, for example:

```
Seed,Address,Iota
QA9GHDLHKSDGHHTMRDGIQFLNMVVLDIPGOMQHMCTTZEUBBHLPFQECPQKBAUVXAXW9DPKMJWVITUGFDRRWJ,CHWYH9BKCDSFNCPCRTHECIMVSRVZZLVNMGNOUEPAFWPPGGVQ9XZMQZJEDRBVJRUEQJOUJPQEFDZC9CGND,10000
OKIGPN9EDOXERTHFOGMHBAKXCGMVPYD9VBXF9ZURYPHKFENLQ9LKXAVDJCWG9SWIIUYTOCH9OZ9HFZLVG,VG9ASJBKITGRBGBMUATLOFQGGYFQGINIDQCISBPNOLNIOXHZVSKSSTPL9JEWLWCXGVMH9KGBCJW9FLZBA,10000
WTCMGWCNJAPMXCKVRLEBOSU9OLOLMSEKPU9G9KVXEMXBKWSMSDTCAZASUUACQGUHJ9RUUUSBBJFZGVQVM,CRKXSAJFRZIXPHRMFAQGNWFJAKGPCZDWQLBAQKVIJXAAXGWKMELGKXATVHMLICBDEJBLDEJLWDCUZRUX9,10000
PLHSKABHWV9AURJVSNKGFNOVYPORPAMJBEYUMNKDMLPHHYF9WNIQRDUN9X9OMZEDDFOIWYOMCAAXMYKTH,JJTVZWLSSDYCMFRKGMKTILGBUSGSYSFZUGEZZCLTNJZLUVAXTDQOFZLEUDFLRXYYL9FGOOOTCGQOHSTXW,10000
...
```
