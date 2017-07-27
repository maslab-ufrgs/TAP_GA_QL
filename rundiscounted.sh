#SF
python route_choice.py -et 7 -f ../network-files/Bar-GeraTNTP/SiouxFalls.net -k 4 -group 100 -d 0.9 -g 100 -io 2  &
python route_choice.py -et 8 -f ../network-files/Bar-GeraTNTP/SiouxFalls.net -k 4 -group 100 -d 0.9 -g 100 -ws 10 20 50 -io 2 &

#OW
#python route_choice.py -et 7 -f ../network-files/OW.net -k 8 -r 30 -d 0.8 0.9 0.95 0.99 -g 100 &
#python route_choice.py -et 8 -f ../network-files/OW.net -k 8 -r 30 -d 0.8 0.9 0.95 0.99 -g 100 -ws 10 20 50 &




