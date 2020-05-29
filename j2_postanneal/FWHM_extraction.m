close all
clear all
skip=[78 79]
bad=[]
for x=1:177

    
    xrd=importdata(sprintf('j2_postanneal-%03d_exported.dat',x-1))
    q=xrd.data(:,1);
    inten=xrd.data(:,2);
    xtal(x)=max(inten);
    if max(inten)<50
        fwhm(x)=NaN
        bad=[bad x]
        continue
    end
    si=csaps(q,inten,.9999995,q,(inten).^2)
    figure(1)
    plot(q,inten)
    hold on
    plot(q,si)
     figure(3)
    plot(q,inten)
    hold on
    plot(q,si)
    xlim([1 4])
%     figure();plot(inten)
    bkrgn=[200:800 1500:1800]
    hold on
    pback=polyfit(q(bkrgn),inten(bkrgn),4)
    bkgnd=polyval(pback,q)
    plot(q,bkgnd)
    sig=si-bkgnd;
    hold off
    figure(2)
    title('x')
    plot(q,sig)
    xlim([1.5 4])
    
    peak=find_peak(q(800:1500),sig(800:1500),'thresh',.50)
    vline(peak.com)
    vline(peak.xl)
    vline(peak.xr)
    fwhm(x)=peak.fwhm
    cen(x)=peak.com
  
%     pause(1)
end
%%


map=importdata('177pointmapbadorder.txt')
x=map.data(:,1);
y=map.data(:,2);
[xi,yi]=meshgrid(-38:.1:38,-38:.1:38);
    zi = griddata(x,y,fwhm,xi,yi);
    contourf(xi,yi,zi,20)
    xlabel('Distance (mm)')
    ylabel('Distance (mm)')
    colorbar
    axis square
    colormap jet
    shading interp
    hold on
    plot(x,y,'kx')
    %%
    output=[x y fwhm'];
outtab=array2table(output,'VariableNames',{'x' 'y' matlab.lang.makeValidName('fwhm(IA)')})
writetable(outtab,'j2_fwhm.csv')