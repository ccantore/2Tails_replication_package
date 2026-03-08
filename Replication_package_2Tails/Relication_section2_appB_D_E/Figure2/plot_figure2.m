clear
close all

this_dir = fileparts(mfilename('fullpath'));
addpath(fullfile(this_dir,'..','functions_new'), '-begin');
addpath(genpath(fullfile(this_dir,'..','data','functions')), '-end');

load(fullfile(this_dir,'..','Figure1','priors_1.mat'))
load(fullfile(this_dir,'..','Figure1','results.mat'))

out_dir = fullfile(this_dir,'..','Output');
if ~exist(out_dir,'dir')
    mkdir(out_dir);
end

for j=1:5
    namesx{j}=strcat('$P_{',num2str(j),'}$');
end
tmp=5:5:95;
for j=1:19
    namesz{j}=strcat('$\le',num2str(tmp(j)),'$');
end


fig = figure(40);
id=[157 189:2:195];

HH=0:size(irfsavem,2)-1;

for j=1:length(id)
    subplot(2,5,j)
plotx99(HH',irfsavem(1:5,:,id(j))','r','r');
title(namesx{j},'interpreter','latex');
xlabel('months','interpreter','latex')
if j==1 
ylabel('percent','interpreter','latex')
end
end
subplot(2,5,[6:10])
h1=plotx99(1:19,squeeze(irfsavem(1:5,6,151:2:188))','b','b')
hold on
h2=plotx99(1:19,squeeze(irfsavem(1:5,24,151:2:188))','r','r')
ylabel('percent','interpreter','latex')

%hold on
%h3=plotx99(1:19,squeeze(irfsavem(1:5,24,151:2:188))','b','b')
title('Response of the Distribution of hours','interpreter','latex')
legend([h1(1) h2(1)],{'6 months', '2 years'})%,'2 years' })
ax=gca
ax.XTick=1:19;
ax.XTickLabel=namesz;
ax.TickLabelInterpreter='latex';


% x0=50;
% y0=1000;
% width=1000;
% height=1000;
% set(gcf,'position',[x0,y0,width,height])
% 
% %print('.\upload\figure2','-dpdf','-bestfit')
% savefigure_pdf('.\upload\figure2')

export_with_margin(fig, fullfile(out_dir,'figure2_6.pdf'));
