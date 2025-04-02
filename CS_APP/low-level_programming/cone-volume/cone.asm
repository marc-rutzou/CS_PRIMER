default rel

section .text
global volume
volume:
    mulss xmm0, xmm0
    mulss xmm0, xmm1
    mulss xmm0, [third]
    mulss xmm0, [pi]
 	ret

section .data
pi: dd 0x40491000
third: dd 0x3e998000 
