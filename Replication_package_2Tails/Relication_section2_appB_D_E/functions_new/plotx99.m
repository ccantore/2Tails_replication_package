function hh1=plotx99(t,y,varargin)

if isempty(varargin)
    colr='r';
    colr1=[1 0.2 0.2];
else
    colr=varargin{1};
    colr1=varargin{2};
end

mm=y(:,1);
cu=y(:,2);
cl=y(:,3);
chck=0;
if cols(y)>3
    chck=1;
   cu1=y(:,4);
cl1=y(:,5);
end
if rows(t)==1
h=t;
else
h=t';
end
h=h';
chck
if chck==1
   
plotConfidenceBandsBlue(h,[cl1 cl mm cu1 cu],colr);   
else
plotConfidenceBandsBlue(h,[cl mm cu],colr)   
end
hold on
plot(h,[cl cu],'color',colr1);
hold on
hh1=plot(h,mm,colr,'LineWidth',1.5); %median IRF
axis tight

hold on;
zz=zeros(size(y,1),1);
plot(h,zz,'k-','LineWidth',2);  %zero line
axis tight





