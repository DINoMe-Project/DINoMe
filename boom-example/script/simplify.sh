filename=$1
cp ${filename} ${filename}.simp 
filename=$1.simp
oldclause=$(wc -l $filename| awk '{print $1}')
oldclause=$((oldclause+0))
times=$2
times=$((times))
mult=$3
mult=$((mult))
for i in `seq 1 $times`
do

#  distill-cls
${CRYTPSAT}/build/cryptominisat5 -p1 --bva=1 --mult=$mult --comps=1 --memoutmult=500000 --keepsymbol=1 --distillto=100 --gates=1 --strcachemaxm=1000000 --probemaxm=1000 --terntimelim=1000 --substimelim=1000 --strstimelim=1000 --varelimto=1000 --distillmaxm=100 --eratio=100 $filename $filename --verb=1 --occirredmaxmb=10000 --occredmax=10000	--occredmaxmb=10000 --maxtime=500  
#--preschedule "occ-bva,occ-bve, scc-vrepl,distill-cls, sub-impl,occ-backw-sub-str, occ-clean-implicit, occ-backw-sub-str, occ-clean-implicit, occ-bve, occ-bva, occ-xor, must-renumber"
#"scc-vrepl, cache-clean, cache-tryboth,sub-impl,sub-str-cls-with-bin,  scc-vrepl, sub-impl,occ-backw-sub-str, occ-clean-implicit, occ-bve, occ-bva, occ-xor, str-impl, cache-clean, sub-str-cls-with-bin, scc-vrepl, sub-impl, str-impl, sub-impl, sub-str-cls-with-bin, occ-backw-sub-str, occ-bve, occ-bva, sub-str-cls-with-bin,str-impl, intree-probe, probe, sub-str-cls-with-bin,distill-cls, occ-backw-sub-str, occ-clean-implicit, occ-bve, occ-bva, occ-xor, must-renumber"
newclause=$(wc -l $filename | awk '{print $1}')
newclause=$((newclause+0))
ndiff=$((oldclause-newclause))
if [ $ndiff -lt 100 ]
then
	break
fi
#${CRYTPSAT}/build/cryptominisat5 -p1 --bva=0 --mult=$3 --comps=1 --memoutmult=500000 --keepsymbol=1 --distillto=10 --distillmaxm=200 --eratio=100 $filename $filename 
#"occ-backw-sub-str,occ-xor, occ-clean-implicit, occ-bve, occ-bva,,scc-vrepl, cache-clean, cache-tryboth,sub-str-cls-with-bin, sub-impl, intree-probe, probe, scc-vrepl, sub-impl,occ-backw-sub-str,occ-xor, occ-clean-implicit, occ-bve, occ-bva, str-impl, cache-clean,sub-str-cls-with-bin, scc-vrepl, sub-impl,str-impl, sub-impl,sub-str-cls-with-bin, occ-backw-sub-str, occ-bve, occ-bva, sub-str-cls-with-bin,renumber"
# "handle-comps,scc-vrepl, cache-clean, cache-tryboth,sub-impl, intree-probe, probe,sub-str-cls-with-bin, scc-vrepl, sub-impl,occ-backw-sub-str,occ-xor, occ-clean-implicit, occ-bve, occ-bva, str-impl, cache-clean,sub-str-cls-with-bin, scc-vrepl, sub-impl,str-impl, sub-impl,sub-str-cls-with-bin, occ-backw-sub-str, occ-bve,renumber" 
done
#
