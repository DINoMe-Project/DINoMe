outfile=$2
nstate=$3
outtrans=${outfile}_trans.smt2
#outtrans_reset=${outfile}_trans_reset.smt2
outinit=${outfile}_init.smt2
outall=${outfile}_all.smt2
basesmt=$1
#sed -i "s/(define-fun |TestHarness_t|/(define-fun prev_cache_observe  ((state |TestHarness_s|)) Bool (= ((_ extract 81403 81403) state) #b1))\n(define-fun cache_observe ((state |TestHarness_s|)) Bool (ite (not (prev_cache_observe state)) false (= (|TestHarness#20499| state) #b0) ))\n(define-fun |TestHarness_t|/g" $basesmt
sed -i "/auto_init ; \\reset/d" $basesmt
sed -i "/auto_init ; \\clock/d" $basesmt
echo "(set-option :produce-models true)\n(set-logic QF_BV)" > ${outtrans}
cat $1 >> ${outtrans}
echo "(declare-fun s0 () |TestHarness_s|)
(declare-fun s1 () |TestHarness_s|)
(assert (|TestHarness_t| s0 s1))
(assert (not  (|TestHarness_n reset| s1)))
(assert (not  (|TestHarness_n reset| s0)))
(check-sat)
(get-model)
(exit)" >> ${outtrans}

echo "(set-option :produce-models true)\n(set-logic QF_BV)" > ${outall}
cat $1 >> ${outall}
echo "(declare-fun s0 () |TestHarness_s|)
(assert (|TestHarness_i| s0))
(assert (|TestHarness_n reset| s0))">> ${outall}
for cycle in `seq 1 $nstate`
do
echo "(declare-fun s$cycle () |TestHarness_s|)
(assert (|TestHarness_t| s$((cycle-1)) s$cycle))
(assert (not  (|TestHarness_n reset| s$cycle)))" >>${outall}
done
if false
then
echo "(set-option :produce-models true)\n(set-logic QF_BV)" > ${outtrans_reset}
cat $1 >> ${outtrans_reset}
echo "(declare-fun s0 () |TestHarness_s|)
(declare-fun s1 () |TestHarness_s|)
(assert (|TestHarness_t| s0 s1))
(assert  (|TestHarness_n reset| s0))
(assert (not  (|TestHarness_n reset| s1)))
(check-sat)
(get-model)
(exit)" >> ${outtrans_reset}
fi
echo "(set-option :produce-models true)\n(set-logic QF_BV)" > ${outinit}
cat $1 >> ${outinit}
echo "(declare-fun s0 () |TestHarness_s|)
(declare-fun s1 () |TestHarness_s|)
(declare-fun s2 () |TestHarness_s|)
(assert (|TestHarness_i| s0))
(assert (|TestHarness_n reset| s0))
(assert (|TestHarness_t| s0 s1))
(assert (|TestHarness_t| s1 s2))
(assert (not  (|TestHarness_n reset| s1)))
(assert (not  (|TestHarness_n reset| s2)))
(check-sat)
(get-model)
(exit)" >> ${outinit}
yices-smt2 --dimacs=${outall}.cnf ${outall} &
p1=$!
yices-smt2 --dimacs=${outinit}.cnf ${outinit} & 
p2=$!
yices-smt2 --dimacs=${outtrans}.cnf ${outtrans} &
p3=$!
wait $p1
wait $p2
wait $p3

#yices-smt2 --dimacs=${outtrans_reset}.cnf ${outtrans_reset}
