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

tmp1 = 20:20:100;
for j = 1:5
    if j == 1
        namesx{j} = strcat('$P_{', num2str(j), '} \, ( \le ', num2str(tmp1(j)), ')$');
    else
        namesx{j} = strcat('$P_{', num2str(j), '} \, ( >', num2str(tmp1(j-1)), ' \, \le ', num2str(tmp1(j)), ')$');
    end
end

namesx{j+1}='Aggregate'

tmp=5:5:95;
for j=1:19
    namesz{j}=strcat('$\le',num2str(tmp(j)),'$');
end



figure(40)
id=[156 188 190 192 194 196];

HH=0:size(irfsavem,2)-1;

for j=1:length(id)
    subplot(2,6,j)
plotx99(HH',irfsavem(1:5,:,id(j))','r','r');
title(namesx{j},'interpreter','latex');
xlabel('months','interpreter','latex')
if j==1 
ylabel('percent','interpreter','latex')
end
end
subplot(2,6,[7:12])
h1=plotx99(1:19,squeeze(irfsavem(1:5,6,150:2:187))','b','b')
hold on
h2=plotx99(1:19,squeeze(irfsavem(1:5,12,150:2:187))','r','r')
title('Response of Wages across the Distribution','interpreter','latex')
legend([h1(1) h2(1)],{'6 mths', '2 years'})%,'2 years' })
ax=gca
ax.XTick=1:19;
ax.XTickLabel=namesz;
ax.TickLabelInterpreter='latex';

%print('.\upload\figure2','-dpdf','-bestfit')
% savefigure_pdf('.\upload\figure_w')

export_with_margin(gcf, fullfile(out_dir,'figure_wages.pdf'));
