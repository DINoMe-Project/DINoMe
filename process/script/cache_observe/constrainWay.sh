input=$1
output=$2
cat $input |grep random > $output
cat $input |grep cache_observe_way >> $output
cat $input | awk '!/-->/{print}' >> $output
cat $input| awk '/cache_observe_[0-9]* /{for(i=5;i<=NF;i=i+1){print $i+0,0}}' >> $output
sh $BOOM/script/simplify.sh $output
mv $output.simp $output.tmp
sh $BOOM/script/compose-light.sh $output.tmp $input 0 1 ./ 1
mv s1.cnf $output
