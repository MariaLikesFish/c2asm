section .bss
a resb 4
section .text
global _start
_start:
_4_5_start:
mov eax, 2
mov ecx, 1
cmp ecx, ecx
mov eax, 0
sete al
cmp eax, 1
jne _4_5_branch
mov eax,0
mov [a],eax
jmp _4_5_end
_4_5_branch:
_6_10_start:
mov eax, 2
mov ecx, 1
cmp ecx, ecx
mov eax, 0
setge al
cmp eax, 1
jne _6_10_branch
mov eax,1
mov [a],eax
jmp _6_10_end
_6_10_branch:
mov eax,2
mov [a],eax
_6_10_end:
_4_5_end:
mov eax, 1
mov ebx, 0
int 80h

