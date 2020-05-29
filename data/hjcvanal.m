close all
clear all
labels=importdata('NiTiAl_Crystallized_hjhand.csv')
for x=1:54
    cv=importdata(sprintf('asdc_data_%03d.csv',x))
    c=cv.data(996:1992,2)
    V=cv.data(996:1992,3)
    si=csaps(V,c,.999999,V,sqrt(abs(c)));
    yyaxis left
    plot(V,log10(c))
    hold on
    plot(V,log10(si))
    hold off
    yyaxis right
    plot(V(2:end),diff(log10(si)))
    [garb ocppos(x)]=min(c);
    ylim([-.01 .01])
    
    pause
end
%% main comparison
figure()
hold on

%     cv=importdata(sprintf('asdc_data_%03d.csv',52))
%     c=cv.data(996:1992,2)
%     V=cv.data(996:1992,3)
%     plot(V,log10(c),'DisplayName','exp. 52,glass,Ni_{21.8}Ti_{29.6}Al_{48.6}')
    
    
    cv=importdata(sprintf('asdc_data_%03d.csv',10))
    c=cv.data(996:1992,2);
    V=cv.data(996:1992,3);
    [arg minchan]=min(abs(c));
    ocp=V(minchan);
    plot(V-ocp,log10(c),'DisplayName','exp. 10,glass (.45),Ni_{21.3}Ti_{35.6}Al_{43.1}')
    
    cv=importdata(sprintf('asdc_data_%03d.csv',17))
    c=cv.data(996:1992,2)
    V=cv.data(996:1992,3)
        [arg minchan]=min(abs(c));
    ocp=V(minchan);
    plot(V-ocp,log10(c),'DisplayName','exp. 17,xtal(.34),Ni_{26.5}Ti_{28.5}Al_{45.0}')
    
        cv=importdata(sprintf('asdc_data_%03d.csv',29))
    c=cv.data(996:1992,2)
    V=cv.data(996:1992,3)
        [arg minchan]=min(abs(c));
    ocp=V(minchan);
    plot(V-ocp,log10(c),'DisplayName','exp. 29,xtal(.31),Ni_{17.5}Ti_{36.2}Al_{46.3}')
 box on
 legend('Location','Best')
 
 %% Aluminum rich
figure()
hold on

    cv=importdata(sprintf('asdc_data_%03d.csv',43))
    c=cv.data(996:1992,2)
    V=cv.data(996:1992,3)
    plot(V,log10(c),'DisplayName','exp. 52,xtal(.04),Ni_{20.9}Ti_{16.5}Al_{62.6}')
    
    
    cv=importdata(sprintf('asdc_data_%03d.csv',47))
    c=cv.data(996:1992,2)
    V=cv.data(996:1992,3)
    plot(V,log10(c),'DisplayName','exp. 10,glass (.48),Ni_{17.3}Ti_{20.1}Al_{62.6}')
    
    cv=importdata(sprintf('asdc_data_%03d.csv',51))
    c=cv.data(996:1992,2)
    V=cv.data(996:1992,3)
    plot(V,log10(c),'DisplayName','exp. 17,xtal(.04),Ni_{21.7}Ti_{20.2}Al_{58.3}')
    
 box on
 legend('Location','Best')
 


 
 
 %% old data vs new data
 figure()
 hold on
cv=importdata(sprintf('asdc_data_%03d.csv',17))
    c=cv.data(996:1992,2)
    V=cv.data(996:1992,3)
        [arg minchan]=min(abs(c));
    ocp=V(minchan);
    plot(V-ocp,log10(c),'DisplayName','exp. 17,xtal(.34),Ni_{26.5}Ti_{28.5}Al_{45.0}')
    
    cv=importdata('G:\Shared drives\643-04\NiTiAl-HTE\data\k20-v2-cvs\cv_0109.csv')
    c=cv.data(1116:2112,2)
    logi=cv.data(1116:2112,7)
    V=cv.data(1116:2112,3)
        [arg minchan]=min(abs(c));
    ocp=V(minchan);
    plot(V-ocp,log10(c),'DisplayName','exp. 109,glass(.48),Ni_{30.1}Ti_{29.1}Al_{40.8}')
    plot(V-ocp,logi)
     box on
 legend()