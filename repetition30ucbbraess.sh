python route_choice.py -et 5 -k 3 -f ../network-files/Braess\ graphs/Braess_1_4200_10_c1.net -io 1 -r 30
python route_choice.py -et 7 -k 3 -f ../network-files/Braess\ graphs/Braess_1_4200_10_c1.net -io 1 -r 30 -d 0.99
python route_choice.py -et 7 -k 3 -f ../network-files/Braess\ graphs/Braess_1_4200_10_c1.net -io 1 -r 30 -d 0.8
python route_choice.py -et 8 -k 3 -f ../network-files/Braess\ graphs/Braess_1_4200_10_c1.net -io 1 -r 30 -d 0.9 -ws 10
python route_choice.py -et 8 -k 3 -f ../network-files/Braess\ graphs/Braess_1_4200_10_c1.net -io 1 -r 30 -d 0.9 -ws 50 
python route_choice.py -et 6 -k 3 -f ../network-files/Braess\ graphs/Braess_1_4200_10_c1.net -r 30
python route_choice.py -et 1 -k 3 -f ../network-files/Braess\ graphs/Braess_1_4200_10_c1.net -r 30 -a 0.8 0.9 -d 0.99 0.9
python route_choice.py -et 9 -k 3 -f ../network-files/Braess\ graphs/Braess_1_4200_10_c1.net -r 30 -epl 0.2 -ws 102 
python route_choice.py -et 9 -k 3 -f ../network-files/Braess\ graphs/Braess_1_4200_10_c1.net -r 30 -epl 0.1 -ws 102 


python route_choice.py -et 10 -k 3 -f ../network-files/Braess\ graphs/Braess_1_4200_10_c1.net -r 30 -epl 0.01 -pf 0.001 -d 0.99 0.9 -ws 102 

