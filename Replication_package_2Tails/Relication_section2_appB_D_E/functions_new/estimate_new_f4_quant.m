clear
close all
addpath('..\..\functions\')

%estimation sample
begdate='01-Jan-1985';
enddate='01-Dec-2019';
TR=timerange(begdate,enddate);
fname='..\data\data_QUANT1';
load(fname);
data_table=data_table(TR,:);
Z_table=Z_table(TR,:);
M_table=M_table(TR,:);
out.data1=data_table.Variables;
out.Z=Z_table.Variables;
out.m_t=M_table.Variables;
out.names=names_big;



spec.Nfact=9;
spec.REPS=21000;  %replications
spec.BURN=1000; %burn-in
spec.SKIP=2;  %iterations skipped
spec.Horz=60;
spec.max_L=12;
spec.fix_L=1;
spec.LAMDAP=0.1;
spec.max_fact=20;
spec.CHECK=0;
spec.detrend_all=0;
spec.detrend_Z=0;
spec.over_write=[129 130 ];
spec.over_write_val=[0 0 ];



[irfsavem,irfsavec,irfsavecc,irfsave]=runfavarx_f_new(out,1,spec);

save('results','irfsavem','irfsavec','irfsavecc','out','irfsave','spec')

