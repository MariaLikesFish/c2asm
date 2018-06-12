section .data
section .bss
i resb 1
j resb 4
k resb 8
section .text
global main
main:
;Assignment:char
mov eax,1
mov [i],al
;Assignment:int,float
mov eax,1
mov [j],eax
;Return
mov eax,1
mov ebx,0
int 80h

