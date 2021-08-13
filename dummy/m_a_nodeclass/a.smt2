(set-option :produce-models true)
(set-logic QF_BV)
(declare-fun secret () (_ BitVec 8))
(declare-fun other () (_ BitVec 8))
(declare-fun control() (_ BitVec 8))
(declare-fun observe () (_ BitVec 8))
(declare-fun declass () (_ BitVec 4))
(define-fun modcontrol () (_ BitVec 5) ((_ extract 4 0) control) )
(define-fun modsecret () (_ BitVec 5) ((_ extract 4 0) secret) )
(define-fun compcontrol () Bool (bvult modcontrol (_ bv16 5)) )
(define-fun compsecret () Bool (bvult modsecret (_ bv16 5)) )
(define-fun cond1 () Bool (and (not compcontrol) compsecret ))
(define-fun cond2 () Bool compcontrol)
(define-fun modother () (_ BitVec 4) (concat (_ bv0 1) ((_ extract 2 0) other) ))
(assert (= declass
                           ((_ extract 3 0) secret)));
(assert (= observe
                           (concat (_ bv0 4)  
                           (ite cond1 modother 
                           (ite cond2 (_ bv9 4) (_ bv10 4))) )));
(check-sat)
(exit)

