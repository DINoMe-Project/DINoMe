nsets=$1
nways=$2
cache=$3
nways=$(cat ../boom-initall.smt2 |grep top.boom_tile.dcache.s2_tag_match_way |grep "define-fun"|grep extract| awk '{print $7+0}')
statefile=s42
cp ../states/$statefile.cnf $statefile.cnf
nway_seq=$(echo "obase=2;$((nways-1))"| bc)
waywidth=${#nway_seq}
observe=observe.cnf
if [ "$nways" -gt "1" ]
then
echo "c cache_observe_way_0 --> ["$(cat $statefile.cnf |grep "$statefile"|awk -v nways=$nways '{for(i=0;i<nways;i=i+1){print $(NF-i)+0}}')"]" > $observe
else
	nways=0
fi
echo "c cache_observe_0 --> ["$(cat $statefile.cnf |grep "$statefile"|awk -v nways=$nways '{print $(NF-nways)+0}')"]" >> $observe
cat $statefile.cnf |awk '/random/{print }' >> $observe
cat $statefile.cnf |awk '/icache/{print }' >> $observe
cat $statefile.cnf | awk '/tag_array/{print}' >> $observe
cat $statefile.cnf |awk '!/-->/{print }' >> $observe
#cat $observe|grep tag_array | awk '{print $(NF-2),0}' >> $observe
#cat $observe|grep tag_array | awk '{for (i=0;i<8;i=i+1)print -$(NF-3-i),0}' >> $observe
if 0
then
	if [ "$nways" -gt "1" ]
	then
		cat $statefile.cnf |grep "$statefile"|awk -v nways=$nways '{for(i=0;i<nways;i=i+1)for(j=i+1;j<nways;j=j+1){printf "%d %d 0\n",-$(NF-i)+0,-$(NF-j)+0}}{print "c next"}{for(i=0;i<nways;i=i+1){printf "%d ",$(NF-i)+0}}{printf "0\n"}' >> $observe
	fi
fi
sh $BOOM/script/simplify.sh $observe 1 10
mkdir tmp
python $BOOM/script/gen_observe.py observe.cnf.simp --addr_len=5 --nsets=$nsets --nways=$nways
if 0
then
	x=$((33-nsets))
cp observe.cnf.simp.0 tmp/s1.cnf.simp
cat tmp/s${x}.cnf.simp |awk '!/c addr|c \\top.boom_tile.dcache.MaxPeriodFibonacciLFSR/{print }' > observe_4.cnf
sh $BOOM/script/process_observe.sh observe_4.cnf
mkdir tmp-4
mv tmp/* tmp-4/
sh $BOOM/script/process_observe.sh observe_4.cnf
mkdir tmp
python $BOOM/script/gen_observe.py observe.cnf.simp --addr_len=5 --nsets=$nsets --nways=$nways --all=1
cat tmp/s32.cnf.simp |awk '!/c addr|c \\top.boom_tile.dcache.MaxPeriodFibonacciLFSR/{print }' > observe_32.cnf
sh $BOOM/script/process_observe.sh observe_32.cnf
mkdir tmp-32

mv tmp/* tmp-32

sh $BOOM/script/gen_observe.sh
mv tmp tmp-mem4
python $BOOM/script/gen_observe.py observe.cnf.simp --addr_len=6 --nsets=$nsets --nways=$nways --all=1
cat tmp/s64.cnf.simp |awk '!/c addr|c \\top.boom_tile.dcache.MaxPeriodFibonacciLFSR/{print }' > observe_64.cnf
sh $BOOM/script/process_observe.sh observe_64.cnf
mkdir tmp-64
mv tmp/* tmp-64
fi
for i in  16  
do
	sh $BOOM/script/gen_observe.sh $i $((nsets*nways)) $cache
done





