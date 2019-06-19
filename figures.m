histogram(tally.tally)
title('Frequency of genes in multiple panels')
xlim([0,31])
print('distro.png','-dpng','-r300')



%% list tally 
summary(listtally.mode)

%%
figure()
types = {'Monoallelic';'Biallelic';'X-Linked';'Unknown';'NA';'Both'};
r=0:0.05:1;
for ti=1:6
t=types{ti};
subplot(2,3,ti);
[pLI,~] = ksdensity(listtally.pLI(listtally.mode==t),r);
[pRec,~] = ksdensity(listtally.pRec(listtally.mode==t),r);
[pNull,~] = ksdensity(listtally.pNull(listtally.mode==t),r);
hold off
plot(r,pLI);
hold on;
plot(r,pRec);
plot(r,pNull);
ylim([0 5])
%% gca.YScale = 'log';
legend({'pLI','pRec','pNull'})
title(t);
xlabel('p-value')
ylabel('density')
end
suptitle('pLI distribution and PanelApp mode')
print('pLI.png','-dpng','-r300')


%%
histogram(GELmodelled.modelled(GELmodelled.modelled>0)*100,20)
xlabel('% length modelled (20 bins)')
ylabel('N protein in bin')
title('Distribution of the coverage of the models (48% protein)')
print('models.png','-dpng','-r300')


%%
confdex = [20, 614, 167, 237, 1190];
refdex = [32,1114,304,433,2500];
bar([confdex; refdex.*sum(confdex)/sum(refdex)]');
f = gca;
f.XTickLabel = {'None','Lowest','Low','High','Highest'};
xlabel('Confidence');
title('Clinical confidence of protein')
legend({'Uncharacterised structurally';'All protein (scaled)'},'location','northwest');
ylabel('N protein')
print('confidence.png','-dpng','-r300')

%%
figure;
subplot(1,2,1);
h = histogram2(tally.modelled(tally.len<1e4)*100,tally.len(tally.len<1e4));
h.FaceColor = 'flat';
h.NumBins = [20 20];
h.DisplayStyle = 'tile';
view(2)
c = colorbar;
c.Label.String = 'N protein in 20x20 bin';

xlabel('% modelled')
ylabel('AA length')
zlabel('N protein')
title('Size and % modelled')

subplot(1,2,2);
h = histogram2(tally.modelled(tally.len<1e3)*100,tally.len(tally.len<1e3));
h.FaceColor = 'flat';
h.NumBins = [20 20];
h.DisplayStyle = 'tile';
view(2)
c = colorbar;
c.Label.String = 'N protein in 20x20 bin';

xlabel('% modelled')
ylabel('AA length')
zlabel('N protein')
title('Size (under 1e3 AA) and % modelled')
print('size.png','-dpng','-r300')

%%
figure;
yyaxis left;
h1=histogram(tally.len(tally.modelled>0.8  & tally.len<1e3 & tally.len >10),10);
xlabel('AA length');
ylabel('Fraction  modelled in 20AA bin')
hold on
yyaxis right;
ylabel('Fraction unmodelled in 20AA bin')
h2=histogram(tally.len(tally.modelled==0  & tally.len<1e3  & tally.len >10),10);
h1.Normalization = 'probability';
h1.BinWidth = 20;
h2.Normalization = 'probability';
h2.BinWidth = 20;
legend({'Modelled','Unmodelled'})
print('sizedistro.png','-dpng','-r300')

%%
