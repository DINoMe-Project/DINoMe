	.file	"modexp.c"
	.text
	.align	2
	.globl	modexp
	.type	modexp, @function
modexp:
	li sp, 0x2000000
	add sp, sp, 0x20
	sll sp, sp, 6
	li  a0,1 // a
	li a2, 3 // p 
	li a3, 4 // D[i]
	// return a= b^d % p
//	add a4, sp, 100 // address for D[i] 
.L9:
	mulw	a0,a0,a0
	remw	a0,a0,a2
	sll	a5,a3,2
	add	a5,sp,a5
	beqz	a3,.L8
	lw	a5,0(a5)
	mulw	a0,a0,a5
	remw	a0,a0,a2
.L8:
	j	.L8
	.size	modexp, .-modexp
	.ident	"GCC: (GNU) 5.2.0"
