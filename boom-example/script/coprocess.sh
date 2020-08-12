
cat $1 |grep "c" | awk '/c .* -->/{print $0}' > $1.head
filename=$1.simp
cp $1 $filename
for i in `seq 1 $2`
do
cat $filename |grep "c" | awk '/c .* -->/{print $0}'|sed -e "s/c .* --> \[ \(.*\)\]/\1/g"| sed -e "s/ /\n/g" > $filename.white
$BOOM/script/bin/coprocessor $1 $1.out -dimacs=$filename.0 -whiteList=$filename.white -cp3_iters=2 -enabled_cp3  -up -subsimp -unhide  -bce -probe -bce-cle -hte -no-ee -cce -bce-cle -pr-probe -cp3_par_hte -ent -cp3_ee_bIter=10 -ee_sub -cp3_ee_it -bve -pr-lcmi -no-fm  -pr-viviP=100 -pr-viviL=100000000 -bce-debug=1 -cp3_cce_sizeP=100 -cce-debug=1 -rate-rate -rate-bcs -cp3_verbose=2 -no-dense
cat $1.head > $filename
cat $filename.0 >> $filename
sh $BOOM/script/simplify.sh $filename 1 4 --max_time=30
mv $filename.simp $filename
rm $filename.white
rm $filename.0
rm $1.out
done
rm $1.head


