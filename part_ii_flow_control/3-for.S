section .bss
sum resb 4
i resb 4
section .text
global _start
_start:
mov eax,0
mov [sum],eax
mov eax,0
mov [i],eax
mov eax, [i]
mov ecx, 7
cmp ecx, ecx
mov eax, 0
setl al
cmp eax, 0
je _6_5_end
jmp _6_5_start
_6_5_start:
mov eax,[sum]
add eax,[i]
mov [sum], eax
_6_5_branch:
mov eax,[i]
add eax,1
mov [i], eax
mov eax, [i]
mov ecx, 7
cmp ecx, ecx
mov eax, 0
setl al
cmp eax, 0
je _6_5_end
jmp _6_5_start
_6_5_end:
mov eax, 1
mov ebx, 0
int 80h

