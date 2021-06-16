smt2file=boom-initall.smt2
if [ ! -f $smt2file.original ]
then
cp $smt2file $smt2file.original
else
	cp $smt2file.original $smt2file
fi
nway=$(cat $smt2file |grep top.boom_tile.dcache.s2_tag_match_way |grep "define-fun"|grep extract| awk '{print $7+0}')
echo "nway="$nway
s2tag_match_way="|TestHarness_n top.boom_tile.dcache.s2_tag_match_way_0|"
nBits=$(head -n 10 $smt2file|grep "(define-sort |TestHarness_s| ()" | awk '{print $NF+0}')
echo $s2tag_match_way
sed -i -e "s/_ BitVec $nBits/_ BitVec $((nBits+1+nway))/g" $smt2file
s2hit=$(cat $smt2file |grep top.boom_tile.dcache.s2_hit_0 | awk '{print $2}')
if [ "$nway" -gt "1" ]
then
sed -i -e "s/(define-fun |TestHarness_i|/(define-fun prev_cache_observe  ((state |TestHarness_s|)) Bool (= ((_ extract $nBits $nBits) state) #b1))\n(define-fun cache_observe ((state |TestHarness_s|)) Bool (ite (not (prev_cache_observe state)) false (= ($s2hit state) #b1) ))\n (define-fun prev_cache_way  ((state |TestHarness_s|)) (_ BitVec $nway) ((_ extract $((nBits+nway)) $((nBits+1))) state) )\n (define-fun cache_way ((state |TestHarness_s|)) (_ BitVec $nway) (ite (not (= (prev_cache_way state) (_ bv0 $nway))) (prev_cache_way state)  ($s2tag_match_way state) ))\n(define-fun |TestHarness_i|/g" -e "s/(define-fun |TestHarness_i| ((state |TestHarness_s|)) Bool (and/(define-fun |TestHarness_i| ((state |TestHarness_s|)) Bool (and\n (prev_cache_observe state)/g" -e "s/)) ; end of module TestHarness/(= (cache_observe state) (prev_cache_observe next_state)) ; auto_init\n (= (cache_way state) (prev_cache_way next_state)) ; auto_init\n )) ; end of module TestHarness/g" $smt2file

else

sed -i -e "s/(define-fun |TestHarness_i|/(define-fun prev_cache_observe  ((state |TestHarness_s|)) Bool (= ((_ extract $nBits $nBits) state) #b1))\n(define-fun cache_observe ((state |TestHarness_s|)) Bool (ite (not (prev_cache_observe state)) false (= ($s2hit state) #b1) ))\n (define-fun |TestHarness_i|/g" -e "s/(define-fun |TestHarness_i| ((state |TestHarness_s|)) Bool (and/(define-fun |TestHarness_i| ((state |TestHarness_s|)) Bool (and\n (prev_cache_observe state)/g" -e "s/)) ; end of module TestHarness/(= (cache_observe state) (prev_cache_observe next_state)) ; auto_init\n  )) ; end of module TestHarness/g" $smt2file
fi
line=$(grep -n "; auto_init ; " $smt2file|grep "clock"|head -n1| 
	awk '{print $1+0}')
awk -v line=$line 'NR == line {print ";"$0} NR!=line {print} ' $smt2file > $smt2file.new
mv $smt2file.new $smt2file
line=$(grep -n "; auto_init ; " $smt2file|grep "reset"|head -n1| awk '{print $1+0}')
awk -v line=$line 'NR == line {print ";"$0} NR!=line {print} ' $smt2file > $smt2file.new
mv $smt2file.new $smt2file
