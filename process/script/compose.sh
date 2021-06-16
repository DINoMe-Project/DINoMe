echo "
$CRYTPSAT/build/cmsat5-compose/compose --keepsymbol=1 --init=$2 --cycles=$4 --start_cycle=$3 --memoutmult=50000000 --composedfile=compose.cnf  --simplify_interval=$6  $1 --out=$5 --compsvar=10000000 --compslimit=500000 --mult=80 --bva=1 --distillto=10000 --distillmaxm=2000  simp.cnf"
start=$3
finish=$4
finish=$((finish+0))
transfile=$1
outdir=$5
step=1
tmp_start=$((start+0))
tmp_finish=$((start+step))
initfile=$2

echo "
$CRYTPSAT/build/cmsat5-compose/compose --keepsymbol=1 --init=$2 --cycles=$4 --start_cycle=$3 --memoutmult=50000000 --composedfile=compose.cnf  --simplify_interval=$6  $1 --out=$5 --compsvar=10000000 --compslimit=500000 --mult=80 --bva=1 --distillto=10000 --distillmaxm=2000  simp.cnf"

$CRYTPSAT/build/cmsat5-compose/compose --keepsymbol=1 --init=$2 --cycles=$4 --start_cycle=$3 --memoutmult=50000000 --composedfile=compose.cnf  --simplify_interval=$6  $1 --out=$5 --compsvar=10000000 --compslimit=500000 --mult=80 --bva=1 --distillto=10000 --distillmaxm=2000  simp.cnf
# --preschedule="scc-vrepl, cache-clean, cache-tryboth,sub-impl,sub-str-cls-with-bin, scc-vrepl,occ-backw-sub-str,occ-xor, occ-clean-implicit, occ-bve, occ-bva,occ-ternary-res, cl-consolidate,scc-vrepl, cache-clean, cache-tryboth,sub-str-cls-with-bin, sub-impl, intree-probe, probe, scc-vrepl, sub-impl,occ-backw-sub-str,occ-xor, occ-clean-implicit, occ-bve, occ-bva,occ-ternary-res, cl-consolidate, str-impl, cache-clean,sub-str-cls-with-bin, scc-vrepl, sub-impl,str-impl, sub-impl,sub-str-cls-with-bin, occ-backw-sub-str, occ-bve, sub-str-cls-with-bin,probe,scc-vrepl,sub-impl,renumber" 
#--schedule="scc-vrepl, cache-clean, cache-tryboth,sub-impl, sub-str-cls-with-bin, scc-vrepl, sub-impl,occ-backw-sub-str,occ-xor, occ-clean-implicit, occ-bve, occ-bva, str-impl, cache-clean,sub-str-cls-with-bin, scc-vrepl, sub-impl,str-impl, sub-impl,sub-str-cls-with-bin, occ-backw-sub-str, occ-bve"
