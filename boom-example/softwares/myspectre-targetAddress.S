main:
	//lui	a3,%hi(array1_size)
	//lw	a4,%lo(array1_size)(a3)
	// a4 = array1_size
	li a4, 16
	li a1, 0x33
	// a3= secret val
	li a3, 0x44
	//sll t1, t1,6
	lui t1, 0x2000
	add s1, t1, 0x20
	sll t1, s1, 6
	add t3, t1, a1
	sb a3, 0(t3)
	lui t2, 0x80000
	//lbu	a5,0x33(t1)
	// array1: 0x80000800 - 0x80001000
	//long-delayed instructions
	li	a5,1001
	li	a2,1000
	//	add t1, t1,a4
	li  t3,0x3ff
//	lbu	a5,33(t1)
	li a3, 1
	mul	a4,a4,a5
	remuw	a5,a4,a2
	mul	a4,a4,a5
	remuw	a5,a4,a2
	bleu	a5,a1,.L2
	add t1,t1,a1
	lbu	a5,0x0(t1)
	sll	a5,a5,6
	and a5,a5,t3
	add	a5,t2,a5
	lbu	a4,0(a5)
.L2:
	j .L2

