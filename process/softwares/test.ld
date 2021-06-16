/*======================================================================*/
/* Proxy kernel linker script                                           */
/*======================================================================*/
/* This is the linker script used when building the proxy kernel. */

/*----------------------------------------------------------------------*/
/* Setup                                                                */
/*----------------------------------------------------------------------*/

/* The OUTPUT_ARCH command specifies the machine architecture where the
   argument is one of the names used in the BFD library. More
   specifically one of the entires in bfd/cpu-mips.c */

OUTPUT_ARCH( "riscv" )
ENTRY(_start)
/*----------------------------------------------------------------------*/
/* Sections                                                             */
/*----------------------------------------------------------------------*/
ENTRY(main)

SECTIONS
{
  /* text: test code section */
 /* . = 0x200;*/
 /* text: test code section */
  . = 0x80000000;
  .text.main : { *(.text.main) } 
  . = 0x80000200;
  .data.offset : { *(.data.offset) }
  . = 0x80000310;
  .data.size : { *(.data.size0) }
  . = 0x80000688;
  .data.secret : { *(.data.secret0) } 
}

