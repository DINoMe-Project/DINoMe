model=sidechannel_random
nsets=$1
nways=$2
model=$3
nstate=$4
cachecycle=$4
observe=observe_16mem
if [ $# -eq 5 ]
then
observe=$5
fi
	if [ -f boom-initall.smt2 ]; then
		echo "finished yosys"
	else
		yosys boom.ys
	fi
	if [ -f cache_trans.smt2.cnf ]; then
		echo "finish cnf gen"
	else
		sh $BOOM/script/cache_observe/boom.sh 
		sh $BOOM/script/boom-trans.sh boom-initall.smt2 cache 
	fi
	if [ -f states-cache/s$cachecycle.cnf  ]; then
		echo "finich cache states"
	else
		sh $BOOM/script/generate_cnf.sh $model cache boom-initall.smt2 $nsets $nways $cachecycle
	fi
	if [ -f observe/observe.cnf ]
	then
		echo "finished observe gen"
	else
		if [ $model == "sidechannel_random" ]
		then
		mkdir observe
		cd observe
		$BOOM/script/cache_observe/observe_cmd.sh $nsets $nways
		cd ..
	fi
	fi
if [ 1 -eq 0 ]
then
	if [ -f boom-test.smt2 ]; then
	echo "finished boom test generation"
else
	cp boom-initall.smt2.original boom-test.smt2
	$BOOM/script/cache_observe/cleanclockreset.sh boom-test.smt2
fi
if [ -f test_trans.smt2.cnf ]; then
	echo "finished test transformation"
else
	sh $BOOM/script/boom-trans.sh boom-test.smt2 test
fi

if [ -f states/s$nstate.cnf  ]; then
	echo "finish test states"
else
	sh $BOOM/script/generate_cnf.sh $model test boom-test.smt2 $nsets $nways $nstate
fi
fi
if [ 1 -eq 0 ]
then
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
				if [ ${way_seq:$start:$i} = "1" ]
				then
					printcmd=$printcmd"print 0+\$(NF-$start),0;"
				else
					printcmd=$printcmd"print -\$(NF-$start),0;"
				fi
			done
			cmd="awk '/dcache.random_map_array_way\\[$idx\\]/{$printcmd}' $initfile"
			echo $cmd
			eval $cmd  >> $initfile 
		done
	done
fi
mkdir s$nstate
cd s$nstate
 $BOOM/script/cache_observe/add_cache_ob.sh $nsets $nways $model $nstate $observe
