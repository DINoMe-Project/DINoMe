/playpen/ziqiao/2project/stp-cm/build/stp -r --disable-simplifications --output-CNF $1
cp name_cnf.txt $1.cnf
cat output_0.cnf >> $1.cnf
sh $BOOM/script/simp.sh $1.cnf 1 1 
