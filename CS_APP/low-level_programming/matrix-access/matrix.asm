section .text
global index
index:
	; rdi: matrix
	; esi: rows
	; edx: cols
	; ecx: rindex
	; r8d: cindex

	imul ecx, edx		; row idx = row idx * max rows	3i
	imul ecx, 4		; row idx = row idx * sizeof(int) 12
	add rdi, rcx		; A = Xa + 12i
	imul r8, 4		; j = j * 4
	add rdi, r8		; A = Xa + 12i + 4j
	mov rax, [rdi]
	ret
