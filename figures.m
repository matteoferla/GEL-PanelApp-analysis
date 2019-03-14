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