import argparse
import math
def main_random_full(args):
    nsets=args.nsets
    nways=args.nways
    f=open(args.file,"w+")
    lognset=math.log(nsets,2)
    masks="(_ bv0 64)"
    tagsize=28# 32-> 23, 16->24, 8 -> 25, 4 -> 26, 2 ->26, 1 ->27
    if nsets==1:
        tagsize=27

    f.write("(declare-fun tag_array () (_ BitVec %d))\n"%(tagsize*nways*nsets))
    f.write("(set-option :produce-models true)\n(set-logic QF_BV)\n")
    f.write("(declare-fun observe_counter () (_ BitVec 64))\n")
    for set_idx in range(0,nsets):
        f.write("(define-fun tag_array_%d ()  (_ BitVec %d) ((_ extract %d %d) tag_array)) \n"%(set_idx,tagsize*nways,(set_idx+1)*tagsize*nways-1,set_idx*tagsize*nways))
        for i in range(0,nways):
            read="read_%d_%d"%(set_idx,i)
            tag="tag_%d_%d"%(set_idx,i)
            read_attack="readAttack_%d_%d"%(set_idx,i)
            mask="mask_%d_%d"%(set_idx,i)
            base=i*tagsize
            f.write("(define-fun %s ()  (_ BitVec %d) ((_ extract %d %d) tag_array_%d))\n"%(tag,tagsize-2,base+tagsize-3,base,set_idx))
            f.write("(define-fun %s () Bool (not (= ((_ extract %d %d) tag_array_%d) #b00)))\n"%(read,base+tagsize-1, base+tagsize-2,set_idx))
            f.write("(define-fun %s () Bool (and %s (= ((_ extract 2 0) %s) (_ bv%d 3)) ) )\n"%(read_attack,read,tag,set_idx))
            f.write("(define-fun %s () (_ BitVec 64) (bvand observe_counter (bvshl (_ bv1 64) (concat (_ bv0 %d) ((_ extract %d 0) %s) ))))\n"%(mask,64-tagsize+3,tagsize-4,tag))
            f.write("(assert (= ((_ extract %d %d) %s) (ite %s #b1 #b0)))\n"%(tagsize-3,tagsize-3,tag,read))
            f.write("(assert (xor (= %s (_ bv0 64)) %s))\n"%(mask,read_attack))

            f.write("(assert (= ( (_ extract %d %d) %s) (_ bv0 19)))\n"%(tagsize-4,tagsize-4-18,tag))
            masks="(bvor %s %s)"%(masks,mask)
    f.write("(assert (= observe_counter %s))\n"%(masks))
    f.write("(check-sat)\n")
    f.close()


def main_random(args):
    nsets=args.nsets
    nways=args.nways
    f=open(args.file,"w+")
    lognset=math.log(nsets,2)
    masks="(_ bv0 64)"
    tagsize=28# 32-> 23, 16->24, 8 -> 25, 4 -> 26, 2 ->26, 1 ->27
    if nsets==1:
        tagsize=27
    f.write("(set-option :produce-models true)\n(set-logic QF_BV)\n")
    f.write("(declare-fun tag_array ()  (_ BitVec %d))\n"%(tagsize*nways))
    f.write("(declare-fun observe_counter () (_ BitVec 64))\n")
    for i in range(0,nways):
        base=i*tagsize

        f.write("(define-fun tag%d ()  (_ BitVec %d) ((_ extract %d %d) tag_array))\n"%(i,tagsize-2,base+tagsize-3,base))
        f.write("(define-fun read%d () Bool (not (= ((_ extract %d %d) tag_array) #b00)))\n"%(i,base+tagsize-1, base+tagsize-2))
        f.write("(define-fun readAttack%d () Bool (and read%d (= ((_ extract %d 0) tag%d) (_ bv0 %d)) ) )\n"%(i,i,lognset-1,i,lognset))
        

        f.write("(define-fun mask%d () (_ BitVec 64) (bvand observe_counter (bvshl (_ bv1 64) (concat (_ bv0 %d) (concat ((_ extract %d %d) tag%d) (_ bv0 %d))))))\n"%(i,64-tagsize+3,tagsize-4,lognset,i,lognset))
        f.write("(assert (= ((_ extract %d %d) tag%d) (ite read%d #b1 #b0)))\n"%(tagsize-3,tagsize-3,i,i))
        f.write("(assert (xor (= mask%d (_ bv0 64)) readAttack%d))\n"%(i,i))

        f.write("(assert (= ( (_ extract %d %d)tag%d) (_ bv0 19)))\n"%(tagsize-4,tagsize-4-18,i))
        masks="(bvor %s mask%d)"%(masks,i)

    f.write("(assert (= observe_counter %s))\n"%(masks))
    f.write("(check-sat)\n")
    f.close()


def main_original(args):
    nsets=args.nsets
    nways=args.nways
    f=open(args.file,"w+")
    lognset=math.log(nsets,2)
    masks="(_ bv0 64)"
    tagsize=28-lognset# 32-> 23, 16->24, 8 -> 25, 4 -> 26, 2 ->26, 1 ->27
    if nsets==1:
        tagsize=27
    f.write("(set-option :produce-models true)\n(set-logic QF_BV)\n")
    f.write("(declare-fun tag_array ()  (_ BitVec %d))\n"%(tagsize*nways))
    f.write("(declare-fun observe_counter () (_ BitVec 64))\n")
    for i in range(0,nways):
        base=i*tagsize
        f.write("(define-fun read%d () Bool (not (= ((_ extract %d %d) tag_array) #b00)))\n"%(i,base+tagsize-1, base+tagsize-2))
        f.write("(define-fun tag%d ()  (_ BitVec %d) ((_ extract %d %d) tag_array))\n"%(i,tagsize-2,base+tagsize-3,base))

        if nsets==1:
            f.write("(define-fun mask%d () (_ BitVec 64) (bvand observe_counter (bvshl (_ bv1 64) (concat (_ bv0 %d) (tag%d)))))\n"%(i,64-tagsize-lognset+2,i))
            f.write("(assert (xor (= mask%d (_ bv0 64)) read%d))\n"%(i,i))
        else:
            f.write("(define-fun mask%d () (_ BitVec 64) (bvand observe_counter (bvshl (_ bv1 64) (concat (_ bv0 %d) (concat ((_ extract %d 0) tag%d) (_ bv0 %d))))))\n"%(i,64-tagsize+3-lognset,tagsize-4,i,lognset))
        f.write("(assert (= ((_ extract %d %d) tag%d) (ite read%d #b1 #b0)))\n"%(tagsize-3,tagsize-3,i,i))
        f.write("(assert (xor (= mask%d (_ bv0 64)) read%d))\n"%(i,i))

        f.write("(assert (= ( (_ extract %d %d)tag%d) (_ bv0 19)))\n"%(tagsize-4,tagsize-4-18,i))
        masks="(bvor %s mask%d)"%(masks,i)

    f.write("(assert (= observe_counter %s))\n"%(masks))
    f.write("(check-sat)\n")
    f.close()

def main(args):
    if "random" in args.model:
        main_random(args)
    elif "random-full" in args.model:
        main_random_full(args)
    else:
        main_original(args)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='match symbol')
    parser.add_argument('file',metavar='files',type=str,help='smt file '
    'generated from yosys tool')
    parser.add_argument('--nsets',type=int,default=8,help='#nset')
    parser.add_argument('--nways',type=int,default=4,help='#nset')
    parser.add_argument('--model',type=str,default="cache",help='model')
    args=parser.parse_args()
    main(args)
