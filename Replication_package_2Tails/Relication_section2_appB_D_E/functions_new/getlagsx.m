function [L,aic,sic,hic]=getlagsx(data,maxlag,choice,exo,dummy)

N=cols(data);

%select lag length
sic=zeros(maxlag,1);
aic=zeros(maxlag,1);
hic=aic;
for i=1:maxlag
    Y=data;
    
    L=i;
    
    
X=[];
for j=1:L
X=[X lag0(data,j) ];
end
if exo
    size(dummy)
    EXO=[ones(rows(X),1) (0:rows(X)-1)' (0:rows(X)-1)'.^2 dummy]; 
X=[X  EXO];
else
    EXO=ones(rows(X),1);
    
 X=[X EXO ];
 
end
EX=cols(EXO);
p=N*L+EX;
NN=N*p;

Y=Y(maxlag+1:end,:);
X=X(maxlag+1:end,:);
T=rows(data)-maxlag;
beta2=X\Y;
res=Y-X*beta2;
sigma=(res'*res)/(T);
detsigma=det(sigma);
lik=-T/2*(N*(1+log(2*pi))+log(detsigma));
%lik=-((T*N)/2)*(1+log(2*pi))-(T/2)*log(detsigma)
sic(i)=(-2*lik/T)+(NN*log(T))/T;
aic(i)=(-2*lik/T)+(2*NN)/T;
hic(i)=(-2*lik/T)+((2*NN)*log(log(T)))/T;
end
% sic
temp=1:maxlag;
if choice==1
 [trash,I]=min(aic);
 'aic'
elseif choice==2
   
[trash,I]=min(sic);
else
 [trash,I]=min(hic);   
 
end

L=temp(I);