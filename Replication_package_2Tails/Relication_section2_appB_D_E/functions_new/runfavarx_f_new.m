function [irfsavem,irfsavec,irfsavecc,irfsave,rmsave,fvsavem]=...
    runfavarx_f_new(D_data,J,spec)


fieldsx=fieldnames(spec);
for j=1:length(fieldsx)
    cmnd=strcat(fieldsx{j},'=','spec.',fieldsx{j},';');
    eval(cmnd);
    
end

if ~exist('do_fv','var')
do_fv=false;
end

data1=D_data.data1;
m_t=D_data.m_t;
names=D_data.names;
Z=D_data.Z;
%Factor estimation
data0=data1;
dataD=data0-lag0(data0,1);
dataD=dataD(2:end,:);
[dataD,md,sd]=standardise(dataD);
Z=Z(2:end,:);
m_t=m_t(2:end);%
data0=data0(2:end,:);


% opt.disp = 0;
% [loadings, ~] = eigs(cov(dataD), Nfact,'LM',opt);
[~,loadings]=ML_efactors2(dataD,Nfact,2);
%non-stationary factors
if detrend_all==0
JJ=BL_TestLinearTrend2(diff(data0));
if exist('over_write','var') && exist('over_write_val','var')
JJ(over_write)=over_write_val;
end
JJ=JJ==1;
else
 JJ=ones(cols(data0),1)==1;
end

if detrend_Z==0
 JJ1=BL_TestLinearTrend2(diff(Z));
elseif detrend_Z==10
    JJ1=0;
else
    JJ1=1;
end

dataS=detrend(data0,'constant'); %demean
dataS(:,JJ)=detrend(data0(:,JJ));
data00=detrend(data0,'constant'); %demean;
data00(:,JJ)=detrend(data0(:,JJ));

dataS=dataS./sd;
[betamat,cmat]=getbeta(dataS,data00);%scaling factors to convert IRFs into original data units
%pmat=dataS*loadings;
pmat=dataS*loadings/cols(dataS);                                                               % BLL Factors

%Z
if JJ1==1
ZS=detrend(Z);
Z00=detrend(Z);
else
ZS=Z;
Z00=Z;
end
ZS=standardise(ZS);
[betamatz,cmatz]=getbeta(ZS,Z00);%scaling factors to convert IRFs into original data units
betamat=[betamatz betamat'];

fload=blkdiag(1,loadings);


data=[ZS pmat];
if fix_L==1
 L=max_L;
else
[L,aic,sic,hic]=getlagsx(data,max_L,1,0,[]);
end
%%%
% 
disp(sprintf('BAI NG Criteria'));
rmax=max_fact;
DEMEAN=1;
disp(sprintf('T= %d N= %d',size(dataD)));
for i=1:2
  disp([nbpiid(dataD,rmax,i,DEMEAN)   nbplog(dataD,rmax,i,DEMEAN)]);
end

%%%


maxtrys=50; %try maxdraws to obtain stable draw/A0
EX=1;  %number of exogenous regressors (constant)
idx=BURN+1:SKIP:REPS;
fsize=length(idx);
N=cols(data);
NN=cols(data1)+1;
disp_=1000; %display every disp_ iters
%prepare data
Y=data;
dat0=Y;
X=prepare(Y,L);
Y=Y(L+1:end,1:N);
X=X(L+1:end,:);%intercept at end
M=(m_t(L+1:end,:));
T=rows(X);
%priors for VAR coefficients
if exist('taup','var')
    TAUP=taup;
else
TAUP=10*LAMDAP;
end
EPSILONP=1/10000;
[yd,xd,b0,s0,S0b,T0]=getdummiestrend(LAMDAP,TAUP,EPSILONP,Y,L,EX);
if LAMDAP==inf
    yd=[];
    xd=[];
    T0=0;
end
Y0=[Y;yd];
X0=[X;xd];

 %conditional mean of the VAR coefficients
 mstar=X0\Y0;  %ols on the appended data
sigma_tilda=(Y0-X0*mstar)'*(Y0-X0*mstar);
mstar=vec(mstar);
xx=X0'*X0;
ixx=xx\eye(cols(xx));  %inv(X0'X0) to be used later in the Gibbs sampling algorithm
beta0=mstar;

  
  save(strcat('priors_',num2str(J)))

%storage
irfsave=zeros(fsize,Horz,NN);
fvsave=irfsave;
rmsave=zeros(fsize,2);
tic;
gibbs1=1;
gibbs=1;
%for gibbs=1:REPS
while gibbs1<=fsize
    
      %step1: Draw sigma
    sigma=iwishrnd(sigma_tilda,2+rows(Y0)-cols(X0)); %Td+T+2-K
    %step 2: Sample VAR coefficients
    [ beta2,PROBLEM] =...
        getcoef2( mstar,sigma,ixx,maxtrys,N,L,EX,CHECK );
    if PROBLEM
        beta2=beta0;
    else
        beta0=beta2;
    end
 
     beta3=reshape(beta2,N*L+EX,N);

    
    
    if rem(gibbs,disp_)==0
    clc
    fprintf('-----------%s \n','');

fprintf('Iteration Number= %s \n', num2str(gibbs));
fprintf('Draws= %s \n', num2str(gibbs1));

fprintf('-----------%s \n','');
     end
    
if gibbs>BURN
   
   if sum(gibbs==idx)>0
       
       
   %calculate A0 matrix using Mertens and Ravn approach
VAR1.k=1;
resid=Y-X*beta3;
tmp=packr([ M resid]);
proxy=tmp(:,1:VAR1.k);
innovations=tmp(:,VAR1.k+1:end);
VAR1.resx=resid;
VAR1.m1=proxy;
VAR1.res=innovations;
VAR1.Sigma=sigma;
VAR1 = doProxySVAR_single_xx(VAR1);
res=ProxySVARidentification(innovations',1,proxy);
fstat=res.fstat;


A0x=zeros(N,N);
tmp=VAR1.b1';
A0x(1:VAR1.k,:)=tmp;
shocks=VAR1.et;
 
    shock=zeros(1,N);
    shock(1)=1;
    imp=irfsimx(beta3,N,L,A0x,shock,Horz+L,EX);
 irf=(imp*fload(:,1:N)'.*repmat(betamat,Horz,1));


if do_fv
A0c=chol(sigma);
mse=0;
for jj=1:N
 shock=zeros(1,N);
    shock(1)=1;
    impx=irfsimx(beta3,N,L,A0c,shock,Horz+L,EX);
 irfx=(impx*fload(:,1:N)'.*repmat(betamat,Horz,1));
 mse=mse+cumsum(irfx.^2);
end
fv=cumsum(irf.^2)./mse;
fvsave(gibbs1,:,:)=fv*100;
end
    irf1=irf./irf(1,1);   
   irfsave(gibbs1,:,:)=irf1;
   
rmsave(gibbs1,:)=[VAR1.RM fstat];
   gibbs1=gibbs1+1;
   end
   end

  

gibbs=gibbs+1;
end

irfsavec=prctile(cummean(irfsave,2),[50 16 84]);
irfsavecc=prctile(cumsum(irfsave,2),[50 16 84]);
irfsavem=prctile(irfsave,[50 16 84 5 95]);
if do_fv
fvsavem=prctile(fvsave,[50 16 84 5 95]);
else
fvsavem=[];
end