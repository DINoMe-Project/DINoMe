(set-logic QF_BV)
(declare-fun secret () (_ BitVec 8))
(declare-fun other () (_ BitVec 8))
(declare-fun control() (_ BitVec 8))
(declare-fun observe () (_ BitVec 8))
(declare-fun declass () (_ BitVec 4))
(assert (= declass
                           ((_ extract 3 0) secret)));
(assert (= observe
                           (bvand (bvand secret control)  (_ bv47 8) ) ));
(check-sat)
(exit)
