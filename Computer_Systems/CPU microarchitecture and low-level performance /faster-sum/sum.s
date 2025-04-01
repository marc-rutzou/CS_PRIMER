	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 14, 0	sdk_version 14, 4
	.globl	_sum                            ; -- Begin function sum
	.p2align	2
_sum:                                   ; @sum
	.cfi_startproc
; %bb.0:
	cmp	w1, #4
	b.lt	LBB0_3
; %bb.1:
	stp	d15, d14, [sp, #-64]!           ; 16-byte Folded Spill
	.cfi_def_cfa_offset 64
	stp	d13, d12, [sp, #16]             ; 16-byte Folded Spill
	stp	d11, d10, [sp, #32]             ; 16-byte Folded Spill
	stp	d9, d8, [sp, #48]               ; 16-byte Folded Spill
	.cfi_offset b8, -8
	.cfi_offset b9, -16
	.cfi_offset b10, -24
	.cfi_offset b11, -32
	.cfi_offset b12, -40
	.cfi_offset b13, -48
	.cfi_offset b14, -56
	.cfi_offset b15, -64
	sub	w8, w1, #3
	mov	w9, #4
	cmp	x8, #4
	csel	x9, x8, x9, hi
	sub	x9, x9, #1
	cmp	x9, #60
	b.hs	LBB0_4
; %bb.2:
	mov	x9, #0
	mov	w15, #0
	mov	w14, #0
	mov	w13, #0
	mov	w12, #0
	b	LBB0_7
LBB0_3:
	mov	w0, #0
	ret
LBB0_4:
	movi.2d	v0, #0000000000000000
	lsr	x9, x9, #2
	movi.2d	v1, #0000000000000000
	add	x10, x9, #1
	movi.2d	v2, #0000000000000000
	and	x11, x10, #0x7ffffffffffffff0
	movi.2d	v3, #0000000000000000
	lsl	x9, x11, #2
	movi.2d	v4, #0000000000000000
	add	x12, x0, #128
	movi.2d	v5, #0000000000000000
	mov	x13, x11
	movi.2d	v6, #0000000000000000
	movi.2d	v7, #0000000000000000
	movi.2d	v16, #0000000000000000
	movi.2d	v17, #0000000000000000
	movi.2d	v18, #0000000000000000
	movi.2d	v19, #0000000000000000
	movi.2d	v20, #0000000000000000
	movi.2d	v21, #0000000000000000
	movi.2d	v22, #0000000000000000
	movi.2d	v23, #0000000000000000
LBB0_5:                                 ; =>This Inner Loop Header: Depth=1
	sub	x14, x12, #128
	sub	x15, x12, #64
	ld4.4s	{ v24, v25, v26, v27 }, [x14]
	ld4.4s	{ v28, v29, v30, v31 }, [x15]
	mov	x14, x12
	ld4.4s	{ v8, v9, v10, v11 }, [x14], #64
	ld4.4s	{ v12, v13, v14, v15 }, [x14]
	add.4s	v20, v24, v20
	add.4s	v21, v28, v21
	add.4s	v22, v8, v22
	add.4s	v23, v12, v23
	add.4s	v16, v25, v16
	add.4s	v17, v29, v17
	add.4s	v18, v9, v18
	add.4s	v19, v13, v19
	add.4s	v4, v26, v4
	add.4s	v5, v30, v5
	add.4s	v6, v10, v6
	add.4s	v7, v14, v7
	add.4s	v0, v27, v0
	add.4s	v1, v31, v1
	add.4s	v2, v11, v2
	add.4s	v3, v15, v3
	add	x12, x12, #256
	subs	x13, x13, #16
	b.ne	LBB0_5
; %bb.6:
	add.4s	v20, v21, v20
	add.4s	v20, v22, v20
	add.4s	v20, v23, v20
	addv.4s	s20, v20
	fmov	w12, s20
	add.4s	v16, v17, v16
	add.4s	v16, v18, v16
	add.4s	v16, v19, v16
	addv.4s	s16, v16
	fmov	w13, s16
	add.4s	v4, v5, v4
	add.4s	v4, v6, v4
	add.4s	v4, v7, v4
	addv.4s	s4, v4
	fmov	w14, s4
	add.4s	v0, v1, v0
	add.4s	v0, v2, v0
	add.4s	v0, v3, v0
	addv.4s	s0, v0
	fmov	w15, s0
	cmp	x10, x11
	b.eq	LBB0_9
LBB0_7:
	add	x10, x0, x9, lsl #2
	add	x10, x10, #8
LBB0_8:                                 ; =>This Inner Loop Header: Depth=1
	ldp	w11, w16, [x10, #-8]
	add	w12, w11, w12
	add	w13, w16, w13
	ldp	w11, w16, [x10], #16
	add	w14, w11, w14
	add	w15, w16, w15
	add	x9, x9, #4
	cmp	x9, x8
	b.lo	LBB0_8
LBB0_9:
	add	w8, w13, w12
	add	w8, w8, w14
	add	w0, w8, w15
	ldp	d9, d8, [sp, #48]               ; 16-byte Folded Reload
	ldp	d11, d10, [sp, #32]             ; 16-byte Folded Reload
	ldp	d13, d12, [sp, #16]             ; 16-byte Folded Reload
	ldp	d15, d14, [sp], #64             ; 16-byte Folded Reload
	ret
	.cfi_endproc
                                        ; -- End function
.subsections_via_symbols
