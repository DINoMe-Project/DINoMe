mode=$3
for i in `seq $2 -1 $1`
do
	if [ -f  $i.count.inter.count ]
	then
			python $BOOM/script/process_count.py $i.count.inter.count $mode | awk '!/invalid/{print $0}'
	fi
done

