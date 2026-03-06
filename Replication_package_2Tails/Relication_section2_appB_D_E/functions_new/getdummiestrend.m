function [yd,xd,b0,s0,S,Tstar]=getdummiestrend(LAMDAPEVIEWS,TAUPEVIEWS,EPSILONPEVIEWS,Y,L,ex)
N=cols(Y);
EX=ex;
lamdaP=LAMDAPEVIEWS;  %This controls the tightness of the priors on the first lag
tauP=TAUPEVIEWS;  % this controls the tightness of the priors on sum of coefficients
epsilonP=EPSILONPEVIEWS;  % this controls tightness of the prior on the constant
muP=mean(Y)';
sigmaP=zeros(N,1);
deltaP=zeros(N,1);
for i=1:N
    ytemp=Y(:,i);
    xtemp=[lag0(ytemp,1) ones(rows(ytemp),1)];
    ytemp=ytemp(2:end,:);
    xtemp=xtemp(2:end,:);
    btemp=xtemp\ytemp;
    etemp=ytemp-xtemp*btemp;
    stemp=etemp'*etemp/(rows(ytemp)-cols(xtemp));
    if btemp(1)>1;
        btemp(1)=1;
    end
    deltaP(i)=btemp(1);
    sigmaP(i)=sqrt(stemp);
end

%dummy data to implement priors see http://ideas.repec.org/p/ecb/ecbwps/20080966.html
[yd,xd] = create_dummiestrendxx(lamdaP,tauP,deltaP,epsilonP,L,muP,sigmaP,N,EX);
b0=vec(xd\yd);
  b01=reshape(b0,N*L+EX,N);

 e0=yd-xd*b01;
S=e0'*e0;
Tstar=rows(yd)-cols(xd);
  s0=kron(S,pinv(xd'*xd));
