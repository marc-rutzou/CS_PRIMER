section .text
global sum_to_n
sum_to_n:
	mov rax, 0	; init the sum
	mov rsi, 0	; init the counter
.L1
	add rax, rsi	
	inc rsi
	cmp rsi, rdi	; continue loop if rsi <= rdi
	jle .L1
	ret
