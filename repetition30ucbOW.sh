python route_choice.py -et 5 -k 8 -f ../network-files/OW.net -io 1 -r 30
python route_choice.py -et 7 -k 8 -f ../network-files/OW.net -io 1 -r 30 -d 0.8
python route_choice.py -et 7 -k 8 -f ../network-files/OW.net -io 1 -r 30 -d 0.95
python route_choice.py -et 7 -k 8 -f ../network-files/OW.net -io 1 -r 30 -d 0.99
python route_choice.py -et 8 -k 8 -f ../network-files/OW.net -io 1 -r 30 -d 0.99 -ws 10
python route_choice.py -et 8 -k 8 -f ../network-files/OW.net -io 1 -r 30 -d 0.99 -ws 20
python route_choice.py -et 8 -k 8 -f ../network-files/OW.net -io 1 -r 30 -d 0.99 -ws 50
python route_choice.py -et 6 -k 8 -f ../network-files/OW.net -r 30
python route_choice.py -et 9 -k 8 -f ../network-files/OW.net -r 30 -epl 0.01
python route_choice.py -et 9 -k 8 -f ../network-files/OW.net -r 30 -epl 0.1
python route_choice.py -et 1 -k 8 -f ../network-files/OW.net -r 30 -a 0.5 0.8 0.9 -d 0.9 0.95

