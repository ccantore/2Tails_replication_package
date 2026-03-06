function [out,out1]=getbeta(xs,xn)
out=[];
out1=[];
for i=1:cols(xs)
%   ytemp=xn(:,i);
%   xtemp=[xs(:,i) ones(rows(xs),1)];
 tmp=[xn(:,i) xs(:,i)];
  tmp=packr(tmp);
  ytemp=tmp(:,1);
  xtemp=[tmp(:,2) ones(rows(tmp),1)];
  bn=xtemp\ytemp;
  out=[out;bn(1)];
out1=[out1;bn(2)];
end
  