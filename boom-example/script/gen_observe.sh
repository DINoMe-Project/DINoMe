nmem=$1
cachesize=$2
actualnmem=32
cache=$3
observe=observe-${nmem}mem.cnf
offset=$((cachesize/nmem))
echo $offset
if [ $nmem > $cachesize ]
then
	offset=1
fi
mkdir tmp
cp observe.cnf.simp.0 tmp/s1.cnf 
for i in `seq 1 $((nmem-1))`
do
	rm tmp_$i.cnf
	j=$((i*offset))
	name="observe.cnf.simp.$j"
	for k in `seq 0 15`
	do
		idx=$((j+k*actualnmem))
		cmd="awk '/c \\\\top.boom_tile.dcache.random_map_array.*\\[$idx\\] -->/{print}' $name"

	done
	awk '!/top.boom_tile.dcache.random_map_array_way/{print}' $name > tmp_$i.cnf
	mv tmp_$i.cnf $name
	sh $BOOM/script/compose.sh observe.cnf.simp.$j tmp/s$i.cnf $i $((i+1)) tmp 1
	sh $BOOM/script/coprocess.sh tmp/s$i.cnf 1 1
	cp tmp/s$i.cnf.simp tmp/s$i.cnf
done
cat tmp/s${nmem}.cnf |awk '!/c addr|c \\top.boom_tile.dcache.MaxPeriodFibonacciLFSR/{print }' > $observe
cp $observe $observe.original
sh $BOOM/script/preproc-eq.sh $observe 1
mv $observe.simp $observe

mv tmp tmp-mem-$nmem
line=$(cat $observe|grep cache_observe_way|wc -l|awk '{print $1+0}')
if [ $line -gt 1 ]
then
	if [ "$cache" == "" ||  "$cache" == "normal" ]
	then
		sh $BOOM/script/cache_observe/constrainWay.sh $observe c-$observe
		cp $observe $observe.original
		cp c-$observe $observe
	fi
fi
sh $BOOM/script/process_observe.sh $observe

