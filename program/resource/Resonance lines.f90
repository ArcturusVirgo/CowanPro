program Resonance
  parameter(m=180000,n=2000,delta=-0)
  real wavelength(m),gf(m),specen(m),fwhm(m),wfwhm(m),lj,&
    aversum,averintensity,average,wspecen(m),fwspecen(m),lowk(m),highk(m),&
    wave(n),intensity(n),fwhmnew(m),wavenew(m),newwspecen(m),&
    intensitynew(m),tt,emin,emax,cross(n),ss,flowk(m),fwhmgauss,&
    fhighk(m),fjt(m),fjtp(m),ffjtp(m),ffjt(m),lowenergy(m),&
    flowenergy(m),minimum,crossb(n),population(m),uu,ffwhm(m),newfjt(m),newfjtp(m)

  emin=49
  emax=250
  Te=25
  fwhmgauss=0.27

  ! open(10,file="Jenergy-fwhm.dat",status="old")
  open(11,file="spectra.dat",status="old")
  ! open(11,file="test 1- 5.txt",status="old")
  ! open(18,file="test 1- 5.dat",sta tus="unknown")
  ! open(15,file="tt",status="unknown")
  ! open(16,file="out.dat",status="unknown")
  open(17,file="gauss.dat",status="unknown")
  open(18,file="cross-NP.dat",status="unknown")
  open(19,file="cross-P.dat",status="unknown")


  i=0
30 i=i+1
  read(11,*,end=40) lowenergy(i),&
    wspecen(i),wavelength(i),gf(i),lowk(i),highk(i),fjt(i),fjtp(i)
  goto 30
40 continue
  trans=i-1

  minimum=lowenergy(1)
  do j=2,trans
    if (minimum .gt. lowenergy(j)) then
      minimum=lowenergy(j)
      lj=fjt(i)
    end if
  end do

  do k=1,trans
    wfwhm(k)=fwhmgauss
  end do

  mm=0
  do 100 i=1,trans
    if(abs(wavelength(i)).gt. emin .and. abs(wavelength(i)).lt.emax)then
      mm=mm+1
      wavenew(mm)=abs(1239.85/(1239.85/wavelength(i)-delta))
      intensitynew(mm)=abs(gf(i))
      fwhmnew(mm)=wfwhm(i)*2
      flowk(mm)=lowk(i)
      fhighk(mm)=highk(i)
      newfjtp(mm)=fjtp(i)
      newfjt(mm)=fjt(i)
      fwspecen(mm)=wspecen(i)
      flowenergy(mm)=lowenergy(i)
    end if
100 continue

! consider the Boltzman contribution
  do i=1,mm
    if(flowenergy(i)>fwspecen(i))then
      newwspecen(i)=flowenergy(i)
      ffjtp(mm)=newfjt(i)
    else
      newwspecen(i)=fwspecen(i)
      ffjtp(mm)=newfjtp(i)
    end if

    population(i)=(2*ffjtp(i)+1)*exp(-abs(newwspecen(i)-minimum)*0.124/Te)/(2*lj+1)

    write(15,"(f10.4)") population(i)
  end do

  do i=1,n
    wave(i)=emin+(emax-emin)*i/n
    intensity(i)=0
    cross(i)=0
    crossb(i)=0
  enddo

  do i=1,n
    tt=0
    ss=0
    uu=0
    do j=1,mm
      tt=tt+intensitynew(j)/sqrt(2*3.14158)&
        &/fwhmgauss*2.355*exp(-2.355**2*(wavenew(j)-wave(i))**2&
        &/fwhmgauss**2/2)

      ss=ss+(intensitynew(j)/(2*ffjtp(j)+1))*fwhmnew(j)/&
        &(2*3.1415928*(((wavenew(j)-wave(i))**2+fwhmnew(j)**2/4)))

      uu=uu+(intensitynew(j)*population(j)/(2*ffjtp(j)+1))*&
        &fwhmnew(j)/(2*3.1415928*(((wavenew(j)-wave(i))**2+&
        &fwhmnew(j)**2/4)))

    end do
    intensity(i)=tt
    cross(i)=ss
    crossb(i)=uu
    write(6,*)  i,crossb(i),cross(i),intensity(i)
  end do



  do i=1,n
    if(intensity(i).lt.0.00001 ) then
      intensity(i)=0
    end if
    write(17,*) 1239.85/wave(i), intensity(i)
  end do

  do i=1,n
    if(cross(i).lt.0.00001 ) then
      cross(i)=0
    endif
    write(18,*) 1239.85/wave(i), cross(i)
  enddo


  do i=1,n
    if(crossb(i).lt.0.00001 ) then
      crossb(i)=0
    endif
    write(19,*) 1239.85/wave(i), crossb(i)
  enddo

end
