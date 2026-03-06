function [ beta,PROBLEM] = getcoef2( mstar,sigma,ixx,MAXTRYS,N,L,EX,CHECK )
PROBLEM=0;
%
vstar=kron(sigma,ixx);
cvstar=chol(vstar);
if CHECK==0
    beta=mstar+(randn(1,N*(N*L+EX))*cvstar)';
else


check=-1;
tryx=1;
   while check<0 && tryx<MAXTRYS
beta=mstar+(randn(1,N*(N*L+EX))*cvstar)';

CH=stability1(beta,N,L,EX);
    if CH==0
    check=10;
    else
      tryx=tryx+1;
    end
   end
   if CH>0
       PROBLEM=1;
   end
   


end

