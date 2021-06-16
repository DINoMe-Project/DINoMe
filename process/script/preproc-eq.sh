input=$1
output=$1.simp
ncycle=$2
ncycle=$((ncycle))
for i in `seq 1 $ncycle`
do 
awk '/c .* -->/{print $0}' $input > $output
#
#$BOOM/script/bin/preproc_linux -cpu-lim=50  -vivification -iterate=2 $input >> $output
clsize=$(wc -l $input | awk '{print $1}')
echo "clsize="$clsize
maxs=1000
if [ $clsize -gt $maxs ];then
	echo hi""
	$BOOM/script/bin/preproc_linux -cpu-lim=50 -vivification  -eliminateLit -litImplied -iterate=1 $input >> $output
	#$BOOM/script/bin/preproc_linux -vivification   -iterate=2 $input >> $output
	solve=$(tail -n 3 $output |grep "Solved")
else
	solve="solved"
fi
if [ "$solve" = "" ]
then
	echo "solve=null"
	sh $BOOM/script/simplify.sh $output 1 1
	mv $output.simp $output
else
	echo "solved"
	sh $BOOM/script/simplify.sh $1 1 1
	break
fi
input=$1.tmp
cp $output $input
done
