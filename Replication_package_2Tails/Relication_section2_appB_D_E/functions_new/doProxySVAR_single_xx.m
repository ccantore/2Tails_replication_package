function VAR = doProxySVAR_single_xx(VAR)





% VAR.bet=[X ones(length(VAR.m),1)]\Y; 
% VAR.res = Y-[X ones(length(X),1)]*VAR.bet;
tmp=packr([VAR.m1 VAR.res]);
 VAR.T = size(tmp,1);
VAR.n=size(VAR.res,2);
VAR.m=tmp(:,1);
VAR.res1=tmp(:,2:end);
VAR.T1=size(VAR.res1,1);
VAR.Sigma = VAR.Sigma;%(VAR.res'*VAR.res)/(VAR.T-VAR.n*VAR.p-1);
      
% Identification
%%%%%%%%%%%%%%%%%

Phib = [ones(length(VAR.m),1) VAR.m]\VAR.res1;
Phib = Phib(2:end,:);
Phib11  = Phib(1:VAR.k,1:VAR.k);
Phib21  = Phib(1:VAR.k,VAR.k+1:VAR.n);
b21ib11 = (Phib11\Phib21)';
Sig11   = VAR.Sigma(1:VAR.k,1:VAR.k);
Sig21   = VAR.Sigma(VAR.k+1:VAR.n,1:VAR.k);
Sig22   = VAR.Sigma(VAR.k+1:VAR.n,VAR.k+1:VAR.n);
ZZp     = b21ib11*Sig11*b21ib11'-(Sig21*b21ib11'+b21ib11*Sig21')+Sig22;
b12b12p = (Sig21- b21ib11*Sig11)'*(ZZp\(Sig21- b21ib11*Sig11));
b11b11p = Sig11-b12b12p;
b11 = sqrt(b11b11p);
VAR.b1 = [b11; b21ib11*b11];

%Reliability
%  Sigmm = VAR.m'*VAR.m/VAR.T;
ED    = eye(VAR.k)*sum(sum(VAR.m,2)~=0)/VAR.T;
mu1   = VAR.m'*VAR.res1(:,1:VAR.k)/VAR.T;
 % PhiPhip = mu1*inv(b11b11p)*mu1';
 % VAR.RM    = inv(Sigmm)*PhiPhip*inv(ED)
Bi = [1/b11+(Sig21-Sig11*b21ib11)'*inv(ZZp)/b11*b21ib11 -(Sig21-Sig11*b21ib11)'*inv(ZZp)/b11];
VAR.et = (Bi*VAR.resx')';

PHI = mu1/b11;
GAM = inv(ED)*PHI;
E  = GAM*VAR.et(sum(VAR.m,2)~=0);
V  = VAR.m(sum(VAR.m,2)~=0)-E;
VAR.RM = inv(E'*E+V'*V)*E'*E;





