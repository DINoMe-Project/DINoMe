#!/bin/bash
basesmt2=boom-initall.smt2
model=sidechannel_random
nset=$1
nway=$2
nmem=$((nway*nset))
model=$3
nstate=$4
basecnf=s${nstate}.cnf
echo $nset, $model, $nstate
leak=0
if [ $# -gt 4 ]
then
observefile=$5
observe=$observefile
fi
if [ $# -gt 5 ]
then
leak=$6
if [ "$leak" = "1" ] 
then
observe=$observe"_leak$leak"
else
	leak=0
fi
else
	leak=0
fi
single_target=target_$observe.cnf
if [ -f $basecnf ]
then
	echo "$basecnf skip"
else
cp ../states/$basecnf ./
python $BOOM/script/match_def.py --mode=mark --model=$model --cnffile=$basecnf --nstate=$((nstate+1)) ../$basesmt2 --nset=$nset --leak=$leak --nway=$nway
fi
sh $BOOM/script/coprocess.sh s${nstate}.cnf.observe.cnf 1 1
cp $basecnf.observe.cnf.simp $basecnf.observe.cnf
markWays()
{
	nway_seq=$(echo "obase=2;$((nway-1))"| bc)
	waywidth=${#nway_seq}
	for way in `seq 0 $((nway-1))`
	do
		way_seq=$(printf "%.0${waywidth}d" $(echo "obase=2;$way"| bc))
		for idx in `seq 0 31`
		do
			idx=$((idx+way*32))
			printcmd=""
			for i in `seq 1 ${waywidth}`
			do
				start=$((i-1))
				if [ "${way_seq:start:i}" = "1" ]
				then 
					printcmd=$printcmd"print 0+\$(NF-$start),0;"
				else
					printcmd=$printcmd"print -\$(NF-$start),0;"
				fi
			done
			cmd="awk '/dcache.random_map_array_way\\[$idx\\]/{$printcmd}' $observe/$1"
			echo $cmd
			eval $cmd  >> $observe/$1
		done
	done

}
mkdir $observe

sh $BOOM/script/compose.sh ../observe/$observefile.cnf.init s${nstate}.cnf.observe.cnf 0 1 $observe 1
sh $BOOM/script/coprocess.sh $observe/s1.cnf 1 1
mv $observe/s1.cnf.simp $observe/s1.cnf
sh $BOOM/script/compose.sh ../observe/$observefile.cnf.final $observe/s1.cnf 1 2 $observe 1
cat $observe/s2.cnf | awk '!/c secret|c observe|c control|c other/{print }' > $observe/target.cnf
cp $observe/target.cnf $observe/target_shared.cnf
if [ "$model" = "sidechannel_random" ]
then
	cat $observe/s2.cnf |grep "c secret"|awk -v nmem=$nmem '{for (i=0;i<7-log(nmem)/log(2);i=i+1){print "-"$NF-i,0}} {print $NF-i,0}' >> $observe/target.cnf
	#cat $observe/s2.cnf |grep "c secret"|awk '{print $NF-2,0}{print "-"$NF-1,0}{print -$NF,0}' >> $observe/target.cnf
	markWays target.cnf
	markWays target_shared.cnf
	cat $observe/s2.cnf |grep "c secret"|awk -v nmem=$nmem '{for (i=0;i<(8-(log(nmem)/log(2)));i=i+1){print "-"$NF-i,0}}' >> $observe/target_shared.cnf
fi
if [ "$model" = "spectre" ]
then
cat $observe/target.cnf|grep tag_array | awk '{print $(NF-2),0}' >> $observe/target.cnf
cat $observe/target.cnf|grep tag_array | awk '{for (i=0;i<19;i=i+1)print -$(NF-3-i),0}' >> $observe/target.cnf
fi
if [ "$model" = "spectre" ] | [ "$model" = "spectreMemDelay" ]
then
	for i in `seq 32 64`
	do
		
		cat $observe/s2.cnf |grep "c cache_observe_$i "|awk '{print -$NF,0}' >> $observe/target.cnf
		cat $observe/s2.cnf |grep "c cache_observe_$i "|awk '{print -$NF,0}' >> $observe/target_shared.cnf
	done
fi
python $BOOM/script/match_def.py --mode=mark --model=$model --cnffile=$observe/target.cnf --nstate=$((nstate+1)) ../$basesmt2 --nset=$nset --model_observe_counter=1 --leak=$leak --nway=$nway
if [ "$model" = "sidechannel_random" ]
then
cat $observe/target.cnf.symbol.cnf |grep secret|awk '{print $1,$2,$3,$4,$5,$6,$7,$8"]"}' > $single_target
cat $observe/target.cnf.symbol.cnf | awk '!/c secret/{print }' >> $single_target
else
	cp $observe/target.cnf.symbol.cnf  $single_target 
fi
sed -i "s/initial_observe/observe/g" $single_target
mkdir inter-$observe
sh $BOOM/script/coprocess.sh $single_target 1 1
mv $single_target.simp $single_target
sh $BOOM/script/compose-copy.sh $single_target inter-$observe 2

python $BOOM/script/match_def.py --mode=mark --model=$model --cnffile=$observe/target_shared.cnf --nstate=$((nstate+1)) ../$basesmt2 --nset=$nset --model_observe_counter=1 --leak=$leak --nway=$nway


cat $observe/target_shared.cnf.symbol.cnf |grep secret|awk '{print $1,$2,$3,$4,$5,$6,$7,$8"]"}' > $single_target.shared
cat $observe/target_shared.cnf.symbol.cnf | awk '!/c secret/{print }' >> $single_target.shared
sed -i "s/initial_observe/observe/g" $single_target.shared
mkdir inter-shared-$observe
sh $BOOM/script/coprocess.sh $single_target.shared 1 1
mv $single_target.shared.simp $single_target.shared
sh $BOOM/script/compose-copy.sh $single_target.shared inter-shared-$observe 2
