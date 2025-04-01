section .text
global pangram
pangram:
	; rdi: source string
	xor r13, r13	; set bitset to 0
.L1
	movzx eax, byte [rdi]	; mov char in rdi to edx
	; if 65 < eax < 90 -> A-Z
	cmp eax, 65
	jl .notLetter 	; below 65 are non-letter
	cmp eax, 91
	jl .upper
	; 90 < c
	cmp eax, 97
	jl .notLetter ; between 90 and 97 are non-letters
	cmp eax, 122
	jg .notLetter ; higher than 122 are non-letters	
	jmp .lower
.upper
	add eax, 32	; make lower case
	jmp .lower
.lower
	sub eax, 97	; which bit to set e.g. 4th bit	
	mov cl, al 	; cl contains how much to shift the bit
	; shift with cl (lowest 8 bits of ecx)
	mov r12, 1
	shl r12d, cl	; shift the bit e.g. by 4
	or r13d, r12d	; set in bitset
	jmp .notLetter
.notLetter
	inc rdi		; increment to the next char
	movzx eax, byte [rdi]	; mov char in rdi to edx
	; compare only the least sign byte
	cmp eax, 0 	; check if next char is newline
	jne .L1		; if not loop continues
	cmp r13d, 0x03ffffff	; compare to full on bitset	
	je .True
	xor eax, eax
	ret
.True
	mov eax, 1
	ret
	
