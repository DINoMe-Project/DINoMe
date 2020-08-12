.text
main:
// data : 0x80000200 - 0x80000800
// insts: 0x80000000 - 0x80000200
	li a0, 0
	li a1, 4
	lui s0, 0x2000
.L1:
	sll t0, a0, 6
	add a0, a0, 1
	add s1, s0, t0
	sll s1, s1, 6
// secret base address 0x80000600 - 0x80000800
// public  address 0x80000400 - 0x80000600
	lbu	a2, 0(s1)
	blt a0, a1, .L1
.L2:
	j	.L2 
/*
	.section .data.offset, "w"
offset: 
	.byte 0x88

	.section .data.size, "w"
size:
	.byte 32
	.section .data.secret, "w"
// assume 0< secret <8: 8*2^6 = 0x200
secret:
	.byte 6
	*/


