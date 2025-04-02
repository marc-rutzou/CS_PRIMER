section .text
global binary_convert
binary_convert:
    xor eax, eax 
.loop:
    movzx ecx, byte [rdi]   ; put most sign bit in ecx
    cmp ecx, 0              ; end of input str
    je .end
    shl eax, 1              ; n <<= 1
    sub ecx, '0'            ; c -= '0' 
    add eax, ecx            ; n += c
    add rdi, 1              ; on to next char
    jmp .loop
.end
    ret

	
