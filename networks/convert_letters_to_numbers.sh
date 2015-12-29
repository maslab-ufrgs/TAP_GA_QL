count=1
echo $1
for i in {A..Z}
do
    sed -i "s/$i/$count/g" $1
    count=$[count+1]
    echo $count
done
