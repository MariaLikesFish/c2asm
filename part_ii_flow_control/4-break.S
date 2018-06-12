section .bss
a resb 4
i resb 4
sum resb 4
section .text
global _start
_start:
_7_5_start:
mov eax, 2
mov ecx, 1
cmp ecx, ecx
mov eax, 0
sete al
cmp eax, 1
jne _7_5_branch
jmp _7_5_end
jmp _7_5_end
_7_5_branch:
_9_10_start:
mov eax, 2
mov ecx, 1
cmp ecx, ecx
mov eax, 0
setge al
cmp eax, 1
jne _9_10_branch
mov eax,1
mov [a],eax
jmp _9_10_end
_9_10_branch:
mov eax,2
mov [a],eax
_9_10_end:
_7_5_end:
mov eax,7
mov [i],eax
mov eax, [i]
mov ecx, 0
cmp ecx, ecx
mov eax, 0
setg al
cmp eax, 0
je _15_5_end
jmp _15_5_start
_15_5_start:
jmp _15_5_end
_15_5_branch:
mov eax, [i]
mov ecx, 0
cmp ecx, ecx
mov eax, 0
setg al
cmp eax, 0
je _15_5_end
jmp _15_5_start
_15_5_end:
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
je _19_5_end
jmp _19_5_start
_19_5_start:
jmp _19_5_end
_19_5_branch:
mov eax,[i]
add eax,1
mov [i], eax
mov eax, [i]
mov ecx, 7
cmp ecx, ecx
mov eax, 0
setl al
cmp eax, 0
je _19_5_end
jmp _19_5_start
_19_5_end:
mov eax, 1
mov ebx, 0
int 80h

