global main
main:
;BinaryOp:add
mov eax,6
add eax,4
;BinaryOp:sub
mov eax,6
sub eax,4
;BinaryOp:mul
mov eax,6
mov ecx,4
imul ecx,eax;ecx
;BinaryOp:div
mov ecx,4
mov eax,6
cdq
idiv ecx;eax
;BinaryOp:mod
mov ecx,4
mov eax,6
cdq
idiv ecx;eax;edx
;Return
mov eax,1
mov ebx,0
int 80h

