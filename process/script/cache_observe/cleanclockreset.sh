smt2file=$1
line=$(grep -n "; auto_init ; " $smt2file|grep "clock"|head -n1| awk '{print $1+0}')
awk -v line=$line 'NR == line {print ";"$0} NR!=line {print} ' $smt2file > $smt2file.new
mv $smt2file.new $smt2file
line=$(grep -n "; auto_init ; " $smt2file|grep "reset"|head -n1| awk '{print $1+0}')
awk -v line=$line 'NR == line {print ";"$0} NR!=line {print} ' $smt2file > $smt2file.new
mv $smt2file.new $smt2file
