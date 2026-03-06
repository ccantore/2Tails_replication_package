% BL_TestLinearTrend - test if there is a linear trend
% 
% J=BL_TestLinearTrend(y)
% 
% J=variables that need to be detrended
%
% In order to choose whether or not to de-trend a variable we apply the following procedure: 
% 	let $m_i$ be the sample mean of $\Delta y_{it}$, 
% 	$\gamma_{i}(j)$ be the auto-covariance of order $j$ of $\Delta y_{it}$, 
% 	and $\bar{\gamma}_i=\sqrt{\frac{1}{T}\sum_{j=-J}^J \gamma_i(j)}$, 
% 	then if  $\frac{|m_i|}{\bar{\gamma}_i}\ge 1.96$ we estimate $a_i$ and $b_i$ 
% 	from an OLS regression of $y_{it}$ on a constant and a time trend, 
% 	whereas if $\frac{|m_i|}{\bar{\gamma}_i}< 1.96$ we set $\wh{a}_i=m_i$ and $\wh{b}_i=0$.
% 

% Matteo Luciani (matteoluciani@yahoo.it)

function [J, J2]=BL_TestLinearTrend2(y)
[T,N]=size(y);
my=mean(y);                                                                 % Sample mean
K=round(sqrt(T)); K1=round(T^.6);                                           % number of lags for which we compute the autocorrelation
gamma=NaN(K1+1,N);                                                          % preallocates
for ii=1:N
    for jj=0:K1                                                             % take some extra cov just in case 
        x1=y(jj+1:end,ii); 
        xx1=x1-mean(x1);
        x2=y(1:end-jj,ii);
        xx2=x2-mean(x2);
        gamma(jj+1,ii)=(xx1'*xx2)/(T-jj-1);                                 % autocovariance
        clear x1 x2
    end    
end

for kk=1:K; NW(kk,1)=1-kk/(K+1); end

gammaS=gamma(1,:)+sum(2*gamma(2:K+1,:).*repmat(NW,1,N));  

gammabar= sqrt(gammaS/T);                                                   % standard deviation sample mean
J=(abs(my)./gammabar)>=1.96;

b=0.5*log(T);
J2=(abs(my)./gammabar)>=abs(b);                           % with Bonferroni correction

J=J';J2=J2';
