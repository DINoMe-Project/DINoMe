width=$1
bitcnf=$width-bit.cnf

#cp noninterference.cnf.simp $bitcnf
cat noninterference.cnf.simp |grep secret |awk -v width=$width '{for (i=1;i<5;i++) {printf $i" "} for (i=5;i<5+width;i++) {printf $i+0" "} printf "]\n"}' > $bitcnf

awk '!/c secret/{print }' noninterference.cnf.simp >> $bitcnf
for i in `seq $width 7`
do
	pos=$((5+i))
	cat noninterference.cnf.simp |grep secret|awk -v k=$pos '{print -$k,0}' >> $bitcnf
	cat noninterference.cnf.simp |grep secret|awk -v k=$pos '{print -$k,0}' 
done
