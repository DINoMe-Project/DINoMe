start=0
domain="victim"
rm map.txt
echo "s 0 4 secret" >> map.txt
echo "salt 0 4 secretalt" >> map.txt
for i in `seq 0 31`
do
	for way in `seq 0 1`
	do
		echo "I $start 3 ${domain}Map_${i}_${way}" >> map.txt
		start=$((start+3))
	done
done
start=$((start+16))
domain='attack'
for i in `seq 0 31`
do
	for way in `seq 0 1`
	do
		echo "I $start 3 ${domain}Map_${i}_${way}">> map.txt
		start=$((start+3))
	done
done

