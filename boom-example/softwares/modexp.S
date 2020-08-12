	.file	"modexp.c"
	.text
	.align	2
	.globl	modexp
	.type	modexp, @function
modexp:
	mulw	a5,a0,a0
	add	sp,sp,-144
	add	t0,sp,16
	li	a7,0
	li	t1,0
	li	a4,0
	li	a6,0
	li	t3,1
	li	t2,32
	remw	a0,a0,a2
	remw	a5,a5,a2
	sw	a0,4(sp)
	mulw	a5,a5,a0
	remw	a5,a5,a2
	sw	a5,12(sp)
	j	.L6
.L23:
	beq	t1,t3,.L2
	beqz	a0,.L3
	li	t1,1
.L4:
	addw	a6,a6,1
	add	t0,t0,4
	beq	a6,t2,.L5
.L6:
	sraw	a0,a1,a6
	and	a3,a0,1
	sllw	a3,a3,t1
	sll	a5,a7,2
	addw	a4,a4,a3
	add	a3,sp,144
	add	a5,a3,a5
	sw	zero,0(t0)
	bnez	a4,.L23
.L2:
	sw	a4,-128(a5)
	addw	a7,a7,1
	beqz	a0,.L5
	li	t1,0
	li	a4,0
	j	.L4
.L3:
	sll	a7,a7,2
	add	a3,sp,144
	add	a7,a3,a7
	sw	a4,-128(a7)
.L5:
	add	a4,sp,144
	add	a1,sp,12
	li	a0,1
.L9:
	mulw	a0,a0,a0
	lw	a3,0(a4)
	add	a6,sp,144
	add	a4,a4,-4
	sll	a5,a3,2
	add	a5,a6,a5
	remw	a0,a0,a2
	beqz	a3,.L8
	lw	a5,-144(a5)
	mulw	a0,a0,a5
	remw	a0,a0,a2
.L8:
	bne	a4,a1,.L9
	add	sp,sp,144
	jr	ra
	.size	modexp, .-modexp
	.ident	"GCC: (GNU) 5.2.0"
