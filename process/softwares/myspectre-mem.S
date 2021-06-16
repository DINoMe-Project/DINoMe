main:
	//lui	a3,%hi(array1_size)
	//lw	a4,%lo(array1_size)(a3)
	// a4 = array1_size
	li a1, 0x33
	lui t2, 0x80000
	//sll t1, t1,6
	lui t1, 0x2000
	add s1, t1, 0x20
	sll t1, s1, 6
	add t5, t1, 0x300
	//lbu	a5,0x33(t1)
	// array1: 0x80000800 - 0x80001000
	//long-delayed instructions
	//	add t1, t1,a4
	li  t3,0x7ff
//	lbu	a5,33(t1)
	lbu a5, 0(t5)
	bleu	a5,a1,.L2
	add t1,t1,a1
	lbu	a5,0x0(t1)
	sll	a5,a5,6
	and a5,a5,t3
	add	a5,t2,a5
	lbu	a4,0(a5)
.L2:
	j .L2

