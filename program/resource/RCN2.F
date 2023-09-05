      program rcn2
c     program rcn2(in2,tape10=in2,out2,tape9=out2,
c    1  tape2n,tape2=tape2n,out2ing,tape11=out2ing,tape31,tape32)
c
c     this program copyright 1980 by los alamos national laboratory
c          and the u.s. government.  the program may be freely
c          distributed gratis anywhere in the world, but may not be sold.
c
c
c          this program reads radial wavefunctions from tape (or disk)
c               unit number 2 prepared by program rcn or hf, and (using
c               input option g5inp) calculates configuration-interaction
c               parameters (rk) and radial electric multipole integrals,
c               scales the energy-level parameter values (fk, gk, zeta,
c               and rk), and punches complete input card decks for
c               program rcg mod 5, 6, 7, 8, or 9.
c          option to include overlap integrals of spectator electrons
c               in computed configuration-interaction and electric-
c               multipole integrals added at the zeeman laboratory,
c               december 1987.
c
c          this version, easily adaptable to the vax 8200,
c               made at lund university march 1988,
c                    modified at lanl august-december 1988.
c
      implicit real*8 (a-h,o-z)
      parameter (kbgks=41,kcase=50,km=1801,ko=20)
      parameter (kco=100,kp=kco+1)
      dimension pa(km),pb(km),pc(km),pd(km),calsq(5)
c
      common nlz(4),subr0,subr,ncfg(2),mmin,ncdes,nkk(4),l(4),
     1  m,iexch,iz1,idum0,overlp,x(km),dummy(km,7)
c
      common/c1/fact(5),ifact(5),idummy2,dummy2(20)
      common/c3/icon,isli,idip,ic,icn(2),nconfn(2),nc0,icase,
     1  nsconf(3,2),del(kco),idipp,iovfact,ovfact
      common/cp/p(km,4),wnl(2),rm1(km),rmkp1(km)
      common/lcm1/nt2(ko),lt2(ko),wt2(ko),ncspvs,idum2,vpar(50),
     1  nconf,iz,z,ion,irel,hxid,c,mesh,idb,exf,corrf,kut,npar
      common/lcm1a/nlbcd
      common/lcm1b/nnlz(ko),nkkk(ko),ee(ko),ee8,r(km),ru(km),
     1  pnl(km,ko),npnl
      common/genosc/igen,nbigks,rj,bigks(kbgks),ibk
      character dh*80,option*28,nlh(4)*3,ha*3,hb*3,hc*3,hd*3,ha1*3,
     1  hb1*3,he*3,nlbcd(ko)*8,nlht(8)*3,nlb(8,kco)*3,kst(kcase,2)*3
      character*6 conf(3),cst(kcase,6),conf1(3),conf2(3),
     1  cf1(kp),cf2(kp),cf3(kp)
      common/cdh/dh,option,nlh,ha1,hb1,he,nlht,nlb,kst,
     1  conf,cst,conf1,conf2,cf1,cf2,cf3
      equivalence (p,pa),(p(1,2),pb),(p(1,3),pc),(p(1,4),pd),
     1  (l(1),la),(l(2),lb),(l(3),lc),(l(4),ld),
     2  (nlh(1),ha),(nlh(2),hb),(nlh(3),hc),(nlh(4),hd)
      character*20 inf
c
      data (calsq(i),i=1,5)/3hdip,3hove,3hsli,3hzet,3hg5i/
c
c          open files
c               (set iii=0 to name files interactively, for vax)
c               (set iii=1 to use standard file names, for vax)
c               (set iii>1 and uncomment program card at
c                     start of program for cray and cdc computers)
c
      iii=1
      if (iii.eq.1) go to 50
      if (iii.gt.1) go to 100
c
      write(6,*) '  input file name  '
      read(5,11) inf
   11 format(a)
      open(10,file=inf,status='old')
      write(6,*) '  output file name  '
      read(5,11) inf
      open(9,file=inf,status='unknown')
      write(6,*) '  give file name for wavefunc. file '
      read(5,11) inf
      open(2,file=inf,status='old',form='unformatted')
      write(6,*) '  give file name for rcg input file '
      read(5,11) inf
      open(11,file=inf,status='unknown')
      go to 55
c
c          use these open statements for standard file names
c               (set iii=1 on statement above)
c
   50 open(10,file='in2',status='old')
      open(9,file='out2',status='unknown')
      open(2,file='tape2n',status='old',form='unformatted')
      open(11,file='out2ing',status='unknown')
   55 open(31,status='scratch',form='unformatted')
      open(32,status='scratch',form='unformatted')
      open(100,file='test.dat',status='unknown')
c
  100 rewind 2
      ic=2
      icn(1)=2
      icn(2)=2
      nconf=99
      nconfn(1)=99
      nconfn(2)=99
      subr0=0.0
      p(1,1)=-99.0
c
  200 read (10,19) dh
   19 format (a)
c     decode (3,20,dh) subr
      read (dh,20) subr
   20 format (a3)
      if (subr.eq.calsq(5)) go to 800
c     decode (45,21,dh) subr,iz1,ncfg(1),ncfg(2),ha,hb,hc,hd,mmin
      read (dh,21) subr,iz1,ncfg(1),ncfg(2),ha,hb,hc,hd,mmin
   21 format (a3,4x,i3,2i5, 4(2x,a3), i5)
      if (iz1.lt.0) write (11,22)
   22 format (5h   -1)
      if(iz1.lt.0) stop '(normal exit)'
      do 300 i=1,5
      if(subr.eq.calsq(i)) go to (500,550,600,700,800) i
  300 continue
      go to 200
  500 call dip
      go to 200
  550 call over
      go to 200
  600 call sli2
      go to 200
  700 call zeta2
      go to 200
  800 call g5inp
      write (9,80)
   80 format (//15h0finished g5inp/)
      go to 200
      end
      subroutine over
c
c          evaluate overlap integrals
c
      implicit real*8 (a-h,o-z)
      parameter (kbgks=41,kcase=50,km=1801,ko=20)
      parameter (kco=100,kp=kco+1)
      dimension pa(km),pb(km),pc(km),pd(km)
c
      common nlz(4),subr0,subr,ncfg(2),mmin,ncdes,nkk(4),l(4),
     1  m,iexch,iz1,idum0,overlp,x(km),absovr,frac
c
      common/c3/icon,isli,idip,ic,icn(2),nconfn(2),nc0,icase,
     1  nsconf(3,2),del(kco),idipp,iovfact,ovfact
      common/cp/p(km,4),wnl(2),rm1(km),rmkp1(km)
      common/lcm1/nt2(ko),lt2(ko),wt2(ko),ncspvs,idum2,vpar(50),
     1  nconf,iz,z,ion,irel,hxid,c,mesh,idb,exf,corrf,kut,npar
      common/lcm1a/nlbcd
      common/lcm1b/nnlz(ko),nkkk(ko),ee(ko),ee8,r(km),ru(km),
     1  pnl(km,ko),npnl
      character dh*80,option*28,nlh(4)*3,ha*3,hb*3,hc*3,hd*3,ha1*3,
     1  hb1*3,he*3,nlbcd(ko)*8,nlht(8)*3,nlb(8,kco)*3,kst(kcase,2)*3
      character*6 conf(3),cst(kcase,6),conf1(3),conf2(3),
     1  cf1(kp),cf2(kp),cf3(kp)
      common/cdh/dh,option,nlh,ha1,hb1,he,nlht,nlb,kst,
     1  conf,cst,conf1,conf2,cf1,cf2,cf3
      equivalence (p,pa),(p(1,2),pb),(p(1,3),pc),(p(1,4),pd),
     1  (l(1),la),(l(2),lb),(l(3),lc),(l(4),ld),
     2  (nlh(1),ha),(nlh(2),hb),(nlh(3),hc),(nlh(4),hd)
c
      k=1
      if (subr) 100,105,100
  100 if (subr.eq.subr0) go to 150
  101 write (9,10)
   10 format (1h1)
  105 subr0=subr
      if (isli.gt.0) go to 200
      write (9,11)
   11 format (1h0//15h  z  kut       ,9x,5hconf1,17x,5hconf2,15x,
     1  16hoverlap integral,11x,8hfraction/17h --- ---         ,
     2  22h-------------------   ,23h-------------------    ,
     3  24h------------------------,7x,8h--------/)
      go to 200
c
  150 if (ncfg(1).ne.nconfn(k).or.ha.ne.ha1) go to 200
      if (iovfact.gt.2) go to 200
      n=2
      go to 251
c
c          read wavefunctions from tape ic and select those desired
c
  200 n=1
      iz0=iz1
      ha1=ha
      if (isli.gt.0) go to 205
      write (9,20)
   20 format (1h )
  205 ic=icn(n)
      if (ic.gt.30) k=ic-30
      if (ncfg(n).eq.nconf) go to 220
      if (ncfg(n)-nconfn(k)) 210,210,211
c     if (ncfg(n)-nconfn(k)) 210,206,211
c 206 backspace ic
c     go to 211
  210 rewind ic
  211 read (ic) nt2,lt2,wt2,ncspvs,vpar,conf,nconf,iz,z,
     1  ion,irel,hxid,mesh,c,idb,exf,corrf,kut,npar,
     2  nlbcd,nnlz,nkkk,ee,ee8,npnl,r,ru, ((pnl(i,m),i=1,km),m=1,npnl)
      if (nconf.ne.ncfg(n)) go to 211
      nconfn(k)=nconf
c
  220 if (n.gt.1) go to 223
  221 do 222 i=1,3
  222 conf1(i)=conf(i)
      go to 225
  223 do 224 i=1,3
  224 conf2(i)=conf(i)
  225 do 226 m=1,ncspvs
      if (nlbcd(m)(1:3).eq.nlh(n)) go to 230
  226 continue
      go to 1000
c
  230 nkk(n)=nkkk(m)
      nlz(n)=nnlz(m)
      wnl(n)=wt2(m)
      l(n)=nnlz(m)-100*(nnlz(m)/100)
      j=m+npnl-ncspvs
      if (j.le.0) go to 1000
      if (nlh(1).eq.nlh(2).and.nnlz(m).ge.9900) go to 260
      do 231 i=1,mesh
  231 p(i,n)=pnl(i,j)
c
  250 n=n+1
  251 if (n-2) 200,205,300
c          set overlp=1.0 for continuum electrons
  260 overlp=1.0
      absovr=1.0
      go to 400
c
c          begin integration loop
c
  300 nf=-1
      overlp=0.0
      absovr=0.0
      imax=min0(nkk(1),nkk(2))
      do 399 i=1,imax
      if (nf) 340,350,360
  340 eras=1.5
      if (i-1) 342,341,342
  341 eras=1.0
      go to 344
  342 if (i-imax) 344,343,344
  343 eras=0.5
  344 eras=pa(i)*pb(i)*eras
      overlp=(overlp+eras)*0.5
      absovr=(absovr+abs(eras))*0.5
      nf=0
      nocyc=40
      if (i.ge.idb) nocyc=imax-i
      go to 399
c
  350 eras=pa(i)*pb(i)
      eras=eras+eras
      overlp=overlp+eras
      absovr=absovr+abs(eras)
      nf=1
      nocyc=nocyc-2
      if (nocyc) 399,351,399
  351 nf=-1
      go to 399
c
  360 eras=pa(i)*pb(i)
      overlp=overlp+eras
      absovr=absovr+abs(eras)
      nf=0
c
  399 continue
c
c          complete calculation of integral
c
  400 frac=overlp/absovr
      write(100,*) frac
      overlp=overlp*(r(imax)-r(imax-1))/0.75
      if (isli.gt.0) go to 450
  410 write (9,41) iz,kut,conf1,conf2,ha,hb,overlp,frac
   41 format (2i4,6x, 2(3x,3a6,1x), 5h    (,a3,1h/,a3,2h)=,f14.9,f15.6)
  450 return
c
 1000 write (9,1001) nlh(n),conf
 1001 format (//9h orbital ,a3, 23h not found for config  ,3a6)
      go to 450
c
      end
      subroutine zeta2
c
c          calculate spin-orbit configuration-interaction integrals
c
c
c
      implicit real*8 (a-h,o-z)
      parameter (kbgks=41,kcase=50,km=1801,ko=20)
      parameter (kco=100,kp=kco+1)
      dimension pa(km),pb(km),pc(km),pd(km)
c
      common nlz(4),subr0,subr,ncfg(2),mmin,ncdes,nkk(4),l(4),
     1  m,iexch,iz1,idum0,overlp,x(km),drudr(km),deru(km),
     2  v(km),zei(km),zeta,zetak
c
      common/c1/fact(5),ifact(5),idummy2,dummy2(20)
      common/c3/icon,isli,idip,ic,icn(2),nconfn(2),nc0,icase,
     1  nsconf(3,2),del(kco),idipp,iovfact,ovfact
      common/cp/p(km,4),wnl(2),rm1(km),rmkp1(km)
      common/lcm1/nt2(ko),lt2(ko),wt2(ko),ncspvs,idum2,vpar(50),
     1  nconf,iz,z,ion,irel,hxid,c,mesh,idb,exf,corrf,kut,npar
      common/lcm1a/nlbcd
      common/lcm1b/nnlz(ko),nkkk(ko),ee(ko),ee8,r(km),ru(km),
     1  pnl(km,ko),npnl
      character dh*80,option*28,nlh(4)*3,ha*3,hb*3,hc*3,hd*3,ha1*3,
     1  hb1*3,he*3,nlbcd(ko)*8,nlht(8)*3,nlb(8,kco)*3,kst(kcase,2)*3
      character*6 conf(3),cst(kcase,6),conf1(3),conf2(3),
     1  cf1(kp),cf2(kp),cf3(kp)
      common/cdh/dh,option,nlh,ha1,hb1,he,nlht,nlb,kst,
     1  conf,cst,conf1,conf2,cf1,cf2,cf3
      equivalence (p,pa),(p(1,2),pb),(p(1,3),pc),(p(1,4),pd),
     1  (l(1),la),(l(2),lb),(l(3),lc),(l(4),ld),
     2  (nlh(1),ha),(nlh(2),hb),(nlh(3),hc),(nlh(4),hd)
c
  111 if (subr-subr0) 114,113,114
  113 if (ncfg(2)-nconf) 114,150,114
  114 subr0=subr
      write (9,10)
   10 format (11h1rcn mod 35///)
c
c
c          read wavefunctions from tape ic and select those desired
c
  150 n=1
      k=1
  205 ic=icn(n)
      if (ic.gt.30) k=ic-30
      if (ncfg(n).eq.nconf) go to 220
      if (ncfg(n)-nconfn(k)) 210,210,211
c     if (ncfg(n)-nconfn(k)) 210,206,211
c 206 backspace ic
c     go to 211
  210 rewind ic
  211 read (ic) nt2,lt2,wt2,ncspvs,vpar,conf,nconf,iz,z,
     1  ion,irel,hxid,mesh,c,idb,exf,corrf,kut,npar,
     2  nlbcd,nnlz,nkkk,ee,ee8,npnl,r,ru, ((pnl(i,m),i=1,km),m=1,npnl)
      if (nconf.ne.ncfg(n)) go to 211
      nconfn(k)=nconf
c
  220 do 221 i=1,3
      conf1(i)=conf2(i)
  221 conf2(i)=conf(i)
c
      do 222 m=1,ncspvs
      if (nlbcd(m)(1:3).eq.nlh(n)) go to 225
  222 continue
      go to 1000
  225 nkk(n)=nkkk(m)
      nlz(n)=nnlz(m)
      l(n)=nnlz(m)-100*(nnlz(m)/100)
c
      n=n+1
      jj=m+npnl-ncspvs
      if (jj.le.0) go to 1000
      if (n.gt.2) go to 350
  230 do 231 i=1,mesh
  231 pa(i)=pnl(i,jj)
      go to 205
c
  350 write (9,35) conf1,conf2,iz,kut
   35 format ( 1h ,3a6,5x,3a6,6x,2hz=,i3,6x,4hkut=,i2///
     1  6x,32hnl   nl  zeta(ryd)    zeta(cm-1) )
c
c          calculate v and derivative of ru
c
  400 dr3=3.0*(r(2)-r(1))
      kkk=min0(nkk(1),nkk(2))
      nblock=kkk/40
      i=1
      do 420 nb=1,nblock
      do 410 j=1,10
      i=i+4
      drudr(i-3)=(-5.5*ru(i-3)+9.0*ru(i-2)-4.5*ru(i-1)+ru(i))/dr3
      drudr(i-2)=(-ru(i-3)-1.5*ru(i-2)+3.0*ru(i-1)-0.5*ru(i))/dr3
      drudr(i-1)=(0.5*ru(i-3)-3.0*ru(i-2)+1.5*ru(i-1)+ru(i))/dr3
  410 drudr(i)=(-ru(i-3)+4.5*ru(i-2)-9.0*ru(i-1)+5.5*ru(i))/dr3
      if (i.gt.idb) go to 420
      dr3=dr3+dr3
  420 continue
c
      twoz=z+z
      do 450 i=2,kkk
      v(i)=ru(i)/r(i)
  450 deru(i)=(drudr(i)-v(i))/(r(i)**2)
c
      do 520 i=2,kkk
      psq=pa(i)*pnl(i,jj)
  520 zei(i)=psq*deru(i)
c
c          integrate
c
      zei(1)=0.0
      xif=0.00125*c*5.0/288.0
      j=1
      s1z=0.0
  530 mm=8
      if (i.gt.idb) go to 531
      xif=xif+xif
  531 continue
      s2z=0.0
  532 s2z=s2z+19.0*(zei(j)+zei(j+5))+75.0*(zei(j+1)+zei(j+4))
     1       +50.0*(zei(j+2)+zei(j+3))
  533 j=j+5
      mm=mm-1
      if (mm) 534,534,532
  534 s1z=s1z+xif*s2z
      if (j-kkk) 530,535,535
  535 zeta=2.66246e-5*s1z
      zetak=zeta*109737.31
c
      write (9,70) ha,hb,zeta,zetak
   70 format (5x,a3,2x,a3,f11.5,f14.3////)
c
c
  900 return
c
 1000 write (9,1001) nlh(n),conf
 1001 format (//9h orbital ,a3, 23h not found for config  ,3a6)
       go to 900
      end
      subroutine dip
c
c          calculate electric dipole or quadrupole radial integrals
c
      implicit real*8 (a-h,o-z)
      parameter (kbgks=41,kcase=50,km=1801,ko=20)
      parameter (kco=100,kp=kco+1)
      dimension pa(km),pb(km),pc(km),pd(km)
c
      common nlz(4),subr0,subr,ncfg(2),mmin,ncdes,nkk(4),l(4),
     1  m,iexch,iz1,idum0,overlp,x(km),dipole,absdip,frac,
     2  reddip
c
      common/c2/ex(kp),stn(kp),wt(kp),gamma(kp),q(kp),
     1  q2(kp),pdipsc(kp),rrsc(kp,12),ncd,ncpd,nfirst,ncont1,ipwr
      common/c3/icon,isli,idip,ic,icn(2),nconfn(2),nc0,icase,
     1  nsconf(3,2),del(kco),idipp,iovfact,ovfact
      common/cp/p(km,4),wnl(2),rm1(km),rmkp1(km)
      common/lcm1/nt2(ko),lt2(ko),wt2(ko),ncspvs,idum2,vpar(50),
     1  nconf,iz,z,ion,irel,hxid,c,mesh,idb,exf,corrf,kut,npar
      common/lcm1a/nlbcd
      common/lcm1b/nnlz(ko),nkkk(ko),ee(ko),ee8,r(km),ru(km),
     1  pnl(km,ko),npnl
      common/lcm2/rdips(kbgks,kcase),st(kcase,5)
      common/genosc/igen,nbigks,rj,bigks(kbgks),ibk
      character dh*80,option*28,nlh(4)*3,ha*3,hb*3,hc*3,hd*3,ha1*3,
     1  hb1*3,he*3,nlbcd(ko)*8,nlht(8)*3,nlb(8,kco)*3,kst(kcase,2)*3
      character*6 conf(3),cst(kcase,6),conf1(3),conf2(3),
     1  cf1(kp),cf2(kp),cf3(kp)
      common/cdh/dh,option,nlh,ha1,hb1,he,nlht,nlb,kst,
     1  conf,cst,conf1,conf2,cf1,cf2,cf3
      equivalence (p,pa),(p(1,2),pb),(p(1,3),pc),(p(1,4),pd),
     1  (l(1),la),(l(2),lb),(l(3),lc),(l(4),ld),
     2  (nlh(1),ha),(nlh(2),hb),(nlh(3),hc),(nlh(4),hd)
c
      itest=1
  100 if (subr.eq.subr0) go to 150
  101 subr0=subr
      if (igen.le.8) write (9,10)
   10 format (1h1//19h  z  kut           ,7x,5hconf1,15x,5hconf2,8x,
     1  10hr integral,6x,22hreduced mupole element,7x,4hfrac,4x,
     2  8h ovfact ,12h  over   fr1/
     3  19h --- --- ---- ---- ,20h------------------- ,
     4  20h------------------- ,10h----------,3x,14h--------------,
     5  14h--------------,3x,6h------,2x, 9h---------,12h ----- -----/)
      go to 200
c
  150 if (ncfg(1).ne.ncfg1.or.ha.ne.ha1) go to 200
      n=2
      go to 251
c
c          read wavefunctions from tape ic and select those desired
c
  200 n=1
      ic=icn(1)
      ncfg1=ncfg(1)
      ha1=ha
      k=1
      write (9,20)
   20 format (1h )
  205 if (ic.gt.30) k=ic-30
      if (ncfg(n).eq.nconf) go to 220
      if (ncfg(n)-nconfn(k)) 210,210,211
c     if (ncfg(n)-nconfn(k)) 210,206,211
c 206 backspace ic
c     go to 211
  210 rewind ic
  211 read (ic) nt2,lt2,wt2,ncspvs,vpar,conf,nconf,iz,z,
     1  ion,irel,hxid,mesh,c,idb,exf,corrf,kut,npar,
     2  nlbcd,nnlz,nkkk,ee,ee8,npnl,r,ru, ((pnl(i,m),i=1,km),m=1,npnl)
      if (nconf.ne.ncfg(n)) go to 211
      nconfn(k)=nconf
c
  220 if (n.gt.1) go to 223
  221 do 222 i=1,3
  222 conf1(i)=conf(i)
      go to 225
  223 do 224 i=1,3
  224 conf2(i)=conf(i)
  225 if (mmin.lt.0) go to 250
      do 226 m=1,ncspvs
      if (nlbcd(m)(1:3).eq.nlh(n)) go to 230
  226 continue
      go to 1000
c
  230 nkk(n)=nkkk(m)
      nlz(n)=nnlz(m)
      wnl(n)=wt2(m)
      l(n)=nnlz(m)-100*(nnlz(m)/100)
      j=m+npnl-ncspvs
      if (j.le.0) go to 1000
      do 231 i=1,mesh
  231 p(i,n)=pnl(i,j)
c
  250 n=n+1
  251 ic=icn(2)
      if (n-2) 200,205,300
c
c          begin integration loop
c
  300 pwrt=2*ipwr+1
      pwrt=sqrt(pwrt)
      do 450 ibk=1,nbigks
      if (mmin.ge.0) go to 305
c
  500 ha='   '
      hb='   '
      ha1='   '
      dipole=0.0
      reddip=0.0
      frac=0.0
      sigsq=0.0
      overlp=0.0
      frac1=0.0
      go to 410
c
  305 dipole=0.0
      absdip=0.0
      rpwr=0.
      nf=-1
      overlp=0.0
      absovr=0.0
      imax=min0(nkk(1),nkk(2))
      do 399 i=1,imax
      rip=r(i)
      if (i.eq.1) go to 320
      rpwr=rip**ipwr
      if (igen.lt.5) go to 320
c          calculate sperical Bessel function
      bigk=bigks(ibk)
      bigk2=bigk**2
      call sbess(rip,itest,ipwr,bigk2,sz,szp)
      rpwr=pwrt*sz/(rip*bigk2)
c
  320 continue
      if (nf) 340,350,360
  340 eras=1.5
      if (i-1) 342,341,342
  341 eras=1.0
      go to 344
  342 if (i-imax) 344,343,344
  343 eras=0.5
  344 eras1=pa(i)*pb(i)*eras
      eras=rpwr*eras1
      dipole=(dipole+eras)*0.5
      absdip=(absdip+abs(eras))*0.5
      overlp=0.5*(overlp+eras1)
      absovr=0.5*(absovr+abs(eras1))
      nf=0
      nocyc=40
      if (i.ge.idb) nocyc=imax-i
      go to 399
c
  350 eras1=2.0*pa(i)*pb(i)
      eras=rpwr*eras1
      dipole=dipole+eras
      absdip=absdip+abs(eras)
      overlp=overlp+eras1
      absovr=absovr+abs(eras1)
      nf=1
      nocyc=nocyc-2
      if (nocyc) 399,351,399
  351 nf=-1
      go to 399
c
  360 eras1=pa(i)*pb(i)
      eras=rpwr*eras1
      dipole=dipole+eras
      absdip=absdip+abs(eras)
      overlp=overlp+eras1
      absovr=absovr+abs(eras1)
      nf=0
c
  399 continue
c
c          complete calculation of integral
c
  400 frac=dipole/absdip
      frac1=overlp/absovr
      dipole=dipole*(r(imax)-r(imax-1))/0.75
      overlp=overlp*(r(imax)-r(imax-1))/0.75
      if (ipwr.eq.0) dipole=dipole-overlp/bigk
      dipole=dipole*ovfact
      a=la
      b=lb
      c=ipwr
          zero=0.0
          temps=s3j(a,b,c,zero,zero)
      reddip=((-1.0)**la)*sqrt((2.0*a+1.0)*(2.0*b+1.0))
     1  *s3j(a,b,c,zero,zero)*dipole
      pdipsc(ncpd)=reddip
      lgr=max0(la,lb)
      flgr=lgr
      sigsq=dipole*dipole/(4.0*flgr*flgr-1.0)
  410 if (igen.lt.5) go to 420
      if ((igen.le.5.and.reddip.ne.0.0).or.(igen.le.8.and.ibk.eq.1))
     1  go to 420
      go to 430
  420 write (9,41) iz,kut,conf1,conf2,
     1  dipole,  ha,rj,ipwr,hb, reddip , frac, ovfact,overlp,frac1
   41 format (1x,2i3,11x,    2(1x,3a6,1x), f11.6, 3x, 1h(,a3,
     1  2h//,a1,i1,2h//,a3, 2h)=, f10.5, 3h a0, f9.4, f11.6,2f6.3)
  430 if (ncfg(2).ge.ncont1+nc0) reddip=0.0
      iover=100.4*overlp
      if1=100.4*frac1
      if (igen.ge.5) go to 440
      if (idip.ne.8) go to 432
      frac=1.0
      go to 435
  432 if (idip.lt.7) go to 435
      i=ncfg(2)-nc0
      reddip=del(i)*reddip
      if (idip.lt.9) frac=del(i)
      write (9,42) del(i),reddip
   42 format (30x,9h sqrtdel=,f10.4,38x,f10.5)
  435 if (frac.ge.0.0.and.frac.lt.9.99) go to 437
      write (11,43) conf1,conf2,reddip,ha,ipwr,hb,frac,hxid,iover,if1
   43 format (3a6,2x,3a6,f12.5,1h(,a3,3h//r,i1,2h//,a3,1h),f6.3,a2,2i4)
      go to 450
  437 write (11,44) conf1,conf2,reddip,ha,ipwr,hb,frac,hxid,iover,if1
!      write (100,44) conf1,conf2,reddip,ha,ipwr,hb,frac
   44 format (3a6,2x,3a6,f12.5,1h(,a3,3h//r,i1,2h//,a3,1h),f6.4,a2,2i4)
      go to 450
c          store results in Bessel-function case
  440 if (ibk.gt.1) go to 449
      icase=icase+1
      if (icase.gt.kcase) stop 44
      do 447 icf=1,3
      cst(icase,icf)=conf1(icf)
  447 cst(icase,icf+3)=conf2(icf)
      st(icase,1)=ipwr
      st(icase,2)=frac
      st(icase,3)=hxid
      st(icase,4)=iover
      st(icase,5)=if1
      kst(icase,1)=ha
      kst(icase,2)=hb
c
  449 rdips(ibk,icase)=reddip
  450 continue
      return
c
 1000 write (9,1001) nlh(n),conf
 1001 format (//9h orbital ,a3, 23h not found for config  ,3a6)
      return
c
      end
      subroutine sli2
c
c          calculate configuration-interaction coulomb integrals rk
c
      implicit real*8 (a-h,o-z)
      parameter (kbgks=41,kcase=50,km=1801,ko=20)
      parameter (kco=100,kp=kco+1)
      dimension pa(km),pb(km),pc(km),pd(km)
      save no
c
      common nlz(4),subr0,subr,ncfg(2),mmin,ncdes,nkk(4),l(4),
     1  m,iexch,iz1,idum0,overlp,x(km),
     2  xi(km),xj(km),xa(km),xb(km),f1(km),f2(km),rkp1(km)
      common/c1/fact(5),ifact(5),nrk,rkaysc(20)
      common/c2/ex(kp),stn(kp),wt(kp),gamma(kp),q(kp),
     1  q2(kp),pdipsc(kp),rrsc(kp,12),ncd,ncpd,nfirst,ncont1,ipwr
      common/c3/icon,isli,idip,ic,icn(2),nconfn(2),nc0,icase,
     1  nsconf(3,2),del(kco),idipp,iovfact,ovfact
      common/c4/irho,isig,irhop,isigp,n12,idum4,t0
      common/cp/p(km,4),wnl(2),rm1(km),rmkp1(km)
      common/lcm1/nt2(ko),lt2(ko),wt2(ko),ncspvs,idum2,vpar(50),
     1  nconf,iz,z,ion,irel,hxid,c,mesh,idb,exf,corrf,kut,npar
      common/lcm1a/nlbcd
      common/lcm1b/nnlz(ko),nkkk(ko),ee(ko),ee8,r(km),ru(km),
     1  pnl(km,ko),npnl
      common/lcm3/pe(km),wa1,wb1
      character dh*80,option*28,nlh(4)*3,ha*3,hb*3,hc*3,hd*3,ha1*3,
     1  hb1*3,he*3,nlbcd(ko)*8,nlht(8)*3,nlb(8,kco)*3,kst(kcase,2)*3
      character*6 conf(3),cst(kcase,6),conf1(3),conf2(3),
     1  cf1(kp),cf2(kp),cf3(kp)
      common/cdh/dh,option,nlh,ha1,hb1,he,nlht,nlb,kst,
     1  conf,cst,conf1,conf2,cf1,cf2,cf3
      equivalence (p,pa),(p(1,2),pb),(p(1,3),pc),(p(1,4),pd),
     1  (l(1),la),(l(2),lb),(l(3),lc),(l(4),ld),
     2  (nlh(1),ha),(nlh(2),hb),(nlh(3),hc),(nlh(4),hd)
c
      dimension k1(10,2),rryd(10,2),rkay(10,2),frac(10,2),eav(2),eps(2)
      dimension rr1(10,2,3),rk1(10,2,3),kk(4),ww(4),ncfgo(2),nn(4)
      equivalence (kk(1),ka),(kk(2),kb),(kk(3),kc),(kk(4),kd),
     1            (ww(1),wa),(ww(2),wb),(ww(3),wc),(ww(4),wd)
c
c
      if (p(1,1).eq.(-99.0)) ncfgo(1)=-7
      if (p(1,1).eq.(-99.0)) ncso=-7
      if (ncfg(1).ne.ncfgo(1).or.ncfg(2).ne.ncfgo(2)) itest=0
      ncs=1000*ncfg(1)+ncfg(2)
      if (isli.eq.0) go to 110
      write (9,95)
      go to 120
  110 write (9,10)
   10 format (11h1rcn mod 36//)
c          determine whether interaction is class 1b,7, or 8
c
  120 iclass=0
      la1=la
      lb1=lb
c
      do 125 i=1,4
c 125 decode (3,12,nlh(i)) l(i)
  125 read (nlh(i),12) l(i)
   12 format (2x,a1)
      if (ha.eq.hc) go to 150
      if (hb.eq.hd) go to 130
      if (hb.eq.hc.or.ha.eq.hd) go to 140
      go to 150
  130 if (la.ne.lc.or.hb(1:2).eq.'99') go to 150
      he=hb
      hb=ha
      ha=he
      he=hd
      hd=hc
      hc=he
      iclass=8
      if (ha.eq.hb.or.hc.eq.hd) iclass=1
      go to 148
  140 if (la.ne.ld.or.lb.ne.lc) go to 150
      iclass=7
      if (ha.eq.hd) go to 145
      he=hb
      hb=ha
      ha=he
      go to 148
  145 he=hd
      hd=hc
      hc=he
  148 n12=1
c
c          read wavefunctions from tape ic and select those desired
c
  150 if (ncfg(2).gt.ncfg(1)+1.and.iclaso.eq.7) n12=1
      n=n12
      npos=0
      if (n12.eq.2) npos=npos1
      la=la1
      lb=lb1
      wa=wa1
      wb=wb1
      eee=0.0
      if (n12.eq.2) eee=ee1
      call seconds(t1)
      iread=0
  151 if (ncfg(n12)-nconf) 160,220,170
  160 rewind ic
  170 read (ic) nt2,lt2,wt2,ncspvs,vpar,conf,nconf,iz,z,
     1  ion,irel,hxid,mesh,c,idb,exf,corrf,kut,npar,
     2  nlbcd,nnlz,nkkk,ee,ee8,npnl,r,ru, ((pnl(i,m),i=1,km),m=1,npnl)
      eav(n)=vpar(1)
      eps(n)=ee(ncspvs)
      iread=iread+1
      if (nconf.ne.ncfg(n)) go to 170
      k=1
      if (ic.gt.30) k=ic-30
      nconfn(k)=nconf
c
  220 do 221 i=1,3
      if (n12.eq.1) conf1(i)=conf2(i)
  221 conf2(i)=conf(i)
c
      do 229 j=1,2
      k=2*n-2+j
      do 222 m=1,ncspvs
      if (nlbcd(m)(1:3).eq.nlh(k)) go to 225
  222 continue
      go to 1000
  225 nkk(k)=nkkk(m)
      nlz(k)=nnlz(m)
      l(k)=nnlz(m)-100*(nnlz(m)/100)
      ww(k)=wt2(m)
      nn(k)=nt2(m)
      kk(k)=m
      ip=mesh
      jj=m+npnl-ncspvs
      if (jj.le.0) go to 1000
      do 226 i=1,ip
  226 p(i,k)=pnl(i,jj)
  229 continue
      m=kk(2*n)
      if (nt2(m).ge.99) npos=npos+1
      if (n.eq.1) npos1=npos
      eee=eee+0.5*ee(m)
      if (isli.le.0) write (9,22) ee(m),eee
   22 format (8h ee,eee=,2f10.5)
c
      n=n+1
      wa1=wa
      wb1=wb
      if (n.gt.2) go to 250
      ee1=eee
  230 if (ncfg(2)-nconf) 160,231,170
  231 hc=ha
      hd=hb
      go to 220
c
c          determine whether interaction is class 1a,6, or 11
c
  250 if (iclass.ne.0) go to 300
      if (ha.ne.hc) go to 300
      if (lb.ne.ld) go to 300
      if ((wb+wd).eq.2.0) iclass=11
      if (isig.ne.isigp) iclass=6
      if (ha.eq.hb.or.hc.eq.hd) iclass=1
c
c          set up k tables for direct (d) and exchange (e) integrals
c
  300 kdmin=max0(iabs(la-lc),iabs(lb-ld))
      kemin=max0(iabs(la-ld),iabs(lb-lc))
      kdmax=min0(la+lc, lb+ld)
      kemax=min0(la+ld, lb+lc)
      kmin=min0(kdmin,kemin)
      kmax=max0(kdmax,kemax)
      nokd=(kdmax-kdmin)/2+1
      noke=(kemax-kemin)/2+1
      nokmax=max0(nokd,noke)
      call seconds(t2)
c
c          calculate integration limits
c
      i1max=max0( min0(nkk(1),nkk(3)), min0(nkk(1),nkk(4)) )
      i2max=max0( min0(nkk(2),nkk(4)), min0(nkk(2),nkk(3)) )
      imax=max0(i1max,i2max)
c
c          calc pnl-products for direct or exchange case
c
  400 do 700 n1=1,2
      if (n1-1) 420,420,412
  412 do 415 i=1,imax
      f1(i)=pa(i)*pd(i)
  415 f2(i)=pb(i)*pc(i)
      k=kemin-2
      go to 500
  420 do 425 i=1,imax
      f1(i)=pa(i)*pc(i)
  425 f2(i)=pb(i)*pd(i)
      k=kdmin-2
c
c          calc for each value of k
c
  500 do 700 n=1,nokmax
      k1(n,n1)=0
  520 k=iabs(k+2)
      k1(n,n1)=k
c
      if (mmin.ge.0) go to 522
      a1=0.0
      b1=1.0
      iclass=0
      go to 650
  522 rkp1(1)=0.001
      rm1(1)=1.0/r(1)
      do 530 i=2,imax
      rm1(i)=1.0/r(i)
      if (n-1) 525,525,529
  525 rkp1(i)=r(i)
      if (k.eq.0) go to 530
  526 do 527 m=1,k
  527 rkp1(i)=rkp1(i)*r(i)
      go to 530
  529 rkp1(i)=rkp1(i)*(r(i)**2)
  530 rmkp1(i)=1.0/rkp1(i)
c
c          calc r1 integral
c
      xi(1)=0.0
      xj(1)=0.0
      xa(1)=0.0
      xb(1)=0.0
      a2=0.0
      b2=0.0
      ho12=r(2)/12.0
      ni=40
      do 550 i=3,i1max,2
      a0=a2
      b0=b2
      eras=8.0*f1(i-1)
      a1=eras*rkp1(i-1)*rm1(i-1)
      b1=eras*rmkp1(i-1)
      a2=f1(i)*rkp1(i)*rm1(i)
      b2=f1(i)*rmkp1(i)
      eras=ho12*(5.0*a0+a1-a2)
      xi(i-1)=xi(i-2)+eras
      xa(i-1)=xa(i-2)+abs(eras)
      eras=ho12*(5.0*b0+b1-b2)
      xj(i-1)=xj(i-2)+eras
      xb(i-1)=xb(i-2)+abs(eras)
      eras=ho12*(-a0+a1+5.0*a2)
      xi(i)=xi(i-1)+eras
      xa(i)=xa(i-1)+abs(eras)
      eras=ho12*(-b0+b1+5.0*b2)
      xj(i)=xj(i-1)+eras
      xb(i)=xb(i-1)+abs(eras)
      ni=ni-2
      if (ni) 540,540,550
  540 ho12=ho12+ho12
      ni=40
      if (i.ge.idb) ni=10000
  550 continue
c
      do 560 i=2,i1max
      eras=rkp1(i)*rm1(i)
      xi(i)=xi(i)*rmkp1(i)+(xj(i1max)-xj(i))*eras
  560 xa(i)=xa(i)*rmkp1(i)+(xb(i1max)-xb(i))*eras
      if (i2max-i1max) 600,600,569
  569 a0=xi(i1max)*rkp1(i1max)
      b0=xa(i1max)*rkp1(i1max)
      do 570 i=i1max,i2max
      xi(i)=a0*rmkp1(i)
  570 xa(i)=b0*rmkp1(i)
c
c          calc r2 integral
c
  600 a0=0.0
      b0=0.0
      a1=0.0
      b1=0.0
      ho3=r(2)/1.5
      ni=40
      do 620 i=3,i2max,2
      a2=f2(i)*xi(i)
      b2=abs(f2(i))*xa(i)
      eras=4.0*f2(i-1)
      a1=a1+ho3*(a0+eras*xi(i-1)+a2)
      b1=b1+ho3*(b0+abs(eras)*xa(i-1)+b2)
      xj(i)=a1
      a0=a2
      b0=b2
      ni=ni-2
      if (ni) 610,610,620
  610 ho3=ho3+ho3
      ni=40
      if (i.ge.idb) ni=10000
  620 continue
      if (npos.ne.2) go to 650
      amin=1.0e30
      amax=-1.0e30
      jn=0
      jx=0
      i=i2max+2
      ix=i2max/4
      do 630 j=1,ix
      i=i-2
      if (xj(i).le.amax) go to 622
      amax=xj(i)
      jx=jx+1
  622 if (xj(i).ge.amin) go to 624
      amin=xj(i)
      jn=jn+1
  624 if (xj(i).lt.amax.and.xj(i).gt.amin.and.jn.gt.3.and.jx.gt.3)
     1  go to 640
  630 continue
  640 a1=0.5*(amin+amax)
      if (isli.gt.0) go to 650
      write (9,8764) amin,amax,a1
 8764 format ( 3f15.6)
c
  650 frac(n,n1)=a1/b1
      rryd(n,n1)=a1
  700 rkay(n,n1)=a1*109737.31
c
c          output
c
      mminp1=max(mmin+1,1)
      do 890 n=1,nokmax
      do 890 n1=1,2
      rr1(n,n1,mminp1)=rryd(n,n1)
  890 rk1(n,n1,mminp1)=rkay(n,n1)
      if (isli.gt.0) go to 935
      if (mmin.gt.0) go to 930
  900 write (9,90) conf1,ncfg(1),iz,ion,exf,irel,conf2,ncfg(2),kut,
     1  corrf,iclass
   90 format (/23h0 slater integrals for   ,3a6,6x,6hnconf=,i2,
     1      14x,2hz=,i3,3x,4hion=,i2,5x,4hexf=,f5.3,11x,5hirel=,i2/
     2    23x,3a6,6x,6hnconf=,i2,22x,4hkut=,i2,3x,6hcorrf=,f5.3,
     3  10x,6hclass ,i2)
  905 if (ncfg(1)-ncfg(2)) 920,910,920
  910 write (9,91) ha,hb,ha,hb
   91 format (/1h0,8x,1hk,14x,3hfk(,a3,1h,,a3,1h),21x,4hfrac,
     1 9x,1hk,14x,3hgk(,a3,1h,,a3,1h),21x,4hfrac)
      go to 930
  920 write (9,92) ha,hb,hc,hd,ha,hb,hc,hd
   92 format (
     1  /1h0,8x,1hk,10x,4hrdk(,a3,1h,,a3,1h,,a3,1h,,a3,1h),16x,4hfrac,
     2       9x,1hk,10x,4hrek(,a3,1h,,a3,1h,,a3,1h,,a3,1h),16x,4hfrac)
  930 write (9,93)
   93 format (1h ,8x,43h-     -------------------------------------,
     1 8h   -----,9x,43h-     -------------------------------------,
     2 8h   -----//)
  935 if (isli.gt.1) go to 945
      if (isli.eq.1.and.iclass.ne.0.and.mmin.ge.0.and.mmin.lt.3)
     1  go to 945
      do 940 n=1,nokmax
  940 write (9,94) (k1(n,n1),rryd(n,n1),rkay(n,n1),
     1      frac(n,n1), n1=1,2)
   94 format (i10,f16.8,7h ryd  =,f14.4,5h cm-1,f8.3,
     1        i10,f16.8,7h ryd  =,f14.4,5h cm-1,f8.3)
      write (9,95)
   95 format (1h0)
c
  945 aa=0.0
      a=0.0
      if (iclass.eq.0) go to 980
      mmin=mmin+1
      go to (950,960,965,970), mmin
  950 do 951 i=1,ip
      pe(i)=pc(i)
  951 pc(i)=pa(i)
      go to 400
  960 do 962 i=1,ip
      pc(i)=pe(i)
      pe(i)=pa(i)
  962 pa(i)=pc(i)
      go to 400
  965 do 966 n=1,nokmax
      do 966 n1=1,2
      rryd(n,n1)=(rryd(n,n1)+rr1(n,n1,2))/2.0
  966 rkay(n,n1)=(rkay(n,n1)+rk1(n,n1,2))/2.0
      if (isli.gt.0) go to 935
      go to 930
  970 he=ha
      ha=hb
      hb=hd
      fla=la
      flb=lb
      hb=ha
      ha=he
      do 972 i=1,ip
  972 pa(i)=pe(i)
c
      b=(2.0*flb+1.0)/(4.0*flb+1.0)
      if (itest.ne.0) go to 975
      itest=7
      aa=0.0
      a=aa
  975 fk=kemin-2
      do 979 n=1,noke
      fk=fk+2.0
      if (iclass.eq.1) go to 976
      d=ww(1)
      c=d*rryd(n,2)
      if (iclass.eq.11) go to 1978
      go to 978
  976 n2=2
      n3=3
      if (ha.eq.hb) go to 977
      n2=3
      n3=2
  977 d=ww(n2)-1.0
      c=0.5*rr1(n,2,n3)
      if (n.gt.1) c=c+b*rr1(n,1,n2)
      c=c*d
  978 a=a+0.5*c*s3j0sq(fla,fk,flb)
 1978 continue
      if (isli.gt.0) go to 979
      write (9,96) d,c,fla,fk,flb,a,eee,overlp
   96 format (/8f10.5)
  979 continue
      rr1(1,1,1)=a/d
      aa=109.73731*aa/d
c
  980 m=0
      do 981 n1=1,2
      ncfgo(n1)=ncfg(n1)
      n2=n1
      if (iclass.eq.7) n2=3-n1
      do 981 n=1,noke
      m=m+1
  981 rkay(m,1)=109.73731*rr1(n,n2,1)
      n3=(2-n2)*noke+1
      m=1
      n=2*nokd
      if (ha.eq.hb.or.hc.eq.hd) n=nokd
      n1=n-m+1
      n2=5
      if (isli.lt.3) write (9,97) conf1(1),conf1(2),
     1      conf1(3),conf2(2),conf2(3),n1, (rkay(i,1),n2, i=m,n),ovfact
   97 format (/1h0,2a6,a4,1h-,a6,a4,4x,i2,5(f11.4,1x,i1)/7(f11.4,1x,i1))
      if (ncs.ne.ncso) no=0
c
c         this write statement included to cure an apparent compiler bug
            if (isli.gt.5) write (9,2356) ncso,ncs,no,m,n
 2356 format (' ncso,ncs,no,m,n=',5i5)
c
      do 982 i=m,n
      j=no+i
      rkaysc(j)=fact(5)*rkay(i,1)*ovfact
      if (ncd.ne.nfirst) go to 982
      rrsc(ncpd,j)=rkaysc(j)/109.73731
  982 continue
      n=n+no
      np1=n+1
      if (idipp.eq.5.and.eps(2).gt.0.0.and.abs(eav(1)-eav(2)).
     1  gt.0.01) np1=1
      if (idip.ne.6.or.(nn(2).lt.99.or.nn(4).lt.99)) go to 983
      np1=1
      if (eps(1).eq.eps(2).and.l(2).eq.l(4)) np1=no+1
  983 do 985 i=np1,20
  985 rkaysc(i)=0.0
      nrk=n
  990 no=n
      ncso=ncs
c
      call seconds(t3)
      t4=t2-t1
      t5=t3-t2
      t3=t3-t0
      write (9,9988) ncfg,iread,t4,t5,t3
 9988 format (3i5,2f10.3,f10.3,4h sec)
      iclaso=iclass
      if (iclass.eq.0.or.iclass.eq.6.or.iclass.eq.11) return
      nconf=1000
      ha='   '
      return
c
 1000 write (9,1001) nlh(k),conf
 1001 format (//9h orbital ,a3, 23h not found for config  ,3a6)
      ha='   '
      go to 990
c
      end
      subroutine g5inp
c
c          punch input for program rcg, mods 5 to 11 (but not 12)
c
      implicit real*8 (a-h,o-z)
      parameter (kbgks=41,kcase=50,km=1801,ko=20)
      parameter (kco=100,kp=kco+1)
      dimension norb(kp),n(25,kp),l(25,kp),iww(8),
     1  w(25,kp),nn(8,kco),ww(8,kco),lsymb(22),
     2  lb(8,kco),ll(8,kco),wwo(8,kco),lbo(8,kco),etot(kco),ee8nc(kco)
c
      common nlz(4),subr0,subr,ncfg(2),mmin,ncdes,
     1  jdum(8),idum(4),overlp,
     2  ix(8),fk(8,5),ze(8),fgk(8,8,5),kpar(50),ivpar(50)
      common/c1/fact(5),ifact(5),nrk,rkaysc(20)
      common/c2/ee(kp),stn(kp),wt(kp),gamma(kp),q(kp),
     1  q2(kp),pdipsc(kp),rrsc(kp,12),ncd,ncpd,nfirst,ncont1,ipwr
      common/c3/icon,isli,idip,ic,icn(2),nconfn(2),nc0,icase,
     1  nsconf(3,2),del(kco),idipp,iovfact,ovfact
      common/c4/irho,isig,irhop,isigp,n12,idum4,t0
      common/cp/p(km,4),wnl(2),rm1(km),rmkp1(km)
      common/lcm1/nt2(ko),lt2(ko),wt2(ko),ncspvs,idum2,vpar(50),
     1  nconf,iz,z,ion,irel,hxid,c,mesh,idb,exf,corrf,kut,npar
      common/lcm1a/nlbcd
      common/lcm1b/nnlz(ko),nkkk(ko),e(ko),ee8,r(km),ru(km),
     1  pnl(km,ko),npnl
      common/lcm2/rdips(kbgks,kcase),st(kcase,5)
      common/genosc/igen,nbigks,rj,bigks(kbgks),ibk
      character dh*80,option*28,nlh(4)*3,ha*3,hb*3,hc*3,hd*3,ha1*3,
     1  hb1*3,he*3,nlbcd(ko)*8,nlht(8)*3,nlb(8,kco)*3,kst(kcase,2)*3
      character*6 conf(3),cst(kcase,6),conf1(3),conf2(3),
     1  cf1(kp),cf2(kp),cf3(kp)
      character ha1t*3
      common/cdh/dh,option,nlh,ha1,hb1,he,nlht,nlb,kst,
     1  conf,cst,conf1,conf2,cf1,cf2,cf3
      equivalence (nlh(1),ha),(nlh(2),hb),(nlh(3),hc),(nlh(4),hd),
     1  (pnl,wwo),(pnl(1,4),lbo),(rdips,etot),(rdips(1,10),ee8nc)
c
      dimension eav(kp)
      data (lsymb(i),i=1,22)/1hs,1hp,1hd,1hf,1hg,1hh,1hi,1hk,1hl,1hm,
     1  1hn,1ho,1hq,1hr,1ht,1hu,1hv,1hw,1hx,1hy,1hz,1ha/
      data slin,dipn/3hsli,3hdip/
      data i2s,bcdr,bcdj/3h 2s,1hr,1hj/
c
c
c     kco=100
c     kp=kco+1
      call seconds(t0)
c 100 decode (80,10,dh) nck,iovfact,nocset,nsconf(3,1),nsconf(3,2),
c    1  eav11,iabg,
c    2  option,iquad,ifact,dmin,iprint,iengyd,ispecc,icon,isli,idip,alf
  100 read(dh,10) nck,iovfact,nocset,nsconf(3,1),nsconf(3,2),eav11,iabg,
     1  option,iquad,ifact,dmin,iprint,iengyd,ispecc,icon,isli,idip,alf
   10 format (5x,a2,i1,i2,i1,i2,f7.4,i1,a28,i1,5i2,2a5,2a1,3i1,f5.0)
c
c               check for generalised oscillator strength option
c                    and compute momentum transfer values
c
c     decode (18,11,option) nbigks,nenrgs,igen,irnq,irxq,irnd,irxd
      read (option,11) nbigks,nenrgs,igen,irnq,irxq,irnd,irxd
   11 format (1x,i3,i2,5x,5i1)
      if (igen.lt.5.and.iquad.gt.0) irnq=2
      irxq=max0(irxq,irnq)
      irnd=max0(irnd,1)
      irxd=max0(irxd,irnd)
      rj=bcdr
      if (igen.lt.5) nbigks=1
      if (igen.lt.5) go to 80
      if (nbigks.le.10) nbigks=kbgks
      if (nenrgs.le.0) nenrgs=21
      rj=bcdj
      option(1:8)='        '
      xmin=1.01
      if (icon.eq.1) xmin=1.1
      if (icon.gt.2) xmin=icon
      if (icon.eq.9) xmin=10.0
      icon=0
      xmax=100.0
      if (idip.eq.1) xmax=20.0
      if (idip.gt.1) xmax=100*idip
      if (idip.eq.9) xmax=1000.0
      idip=0
   80 nc0=0
      idipp=0
      if (idip.ne.5) go to 82
      idipp=5
      idip=9
   82 ncmax=kco
      nocset=-iabs(nocset)
      iabg=iabs(iabg)
      iquad=iabs(iquad)
      do 101 i=1,5
      if (ifact(i).eq.0.and.i.eq.2) ifact(i)=95
      if (ifact(i).eq.0) ifact(i)=85
      eras=ifact(i)
      if (eras.lt.1.5) eras=0.1
      fact(i)=0.01*eras
  101 if (ifact(i).eq.99) fact(i)=1.0
      if (icon.eq.0) icon=8
      nscf31=iabs(nsconf(3,1))
      ns32=nsconf(3,2)
      if (nsconf(3,2).eq.0.and.idip.eq.8) nsconf(3,2)=-8
      nscf32=iabs(nsconf(3,2))
      idip0=idip
      nosubc=0
      nc3=0
      rewind 2
      if (nc0.eq.0) go to 102
      do 105 nc=1,nc0
  105 read (2)
c
  102 do 90 i=1,kp
      stn(i)=0.0
      wt(i)=0.0
      gamma(i)=0.0
      q(i)=0.0
      q2(i)=0.0
      pdipsc(i)=0.0
      eav(i)=0.0
      do 90 j=1,12
   90 rrsc(i,j)=0.0
      ncont1=1000
      ncont2=1000
      idele=1000
      emax=0.0
c
c          determine number of configs of each parity
c
      rewind 31
      rewind 32
      ic=31
      icn(1)=31
      icn(2)=31
      nc=0
      nmax=0
      lmax=0
      norbx=0
      ipct=0
      vpar1=-99999999.0
      nc2=0
  110 nc=nc+1
      if (nc+nc0.gt.ncmax) go to 130
      read (2,end=112) nt2,lt2,wt2,ncspvs,vpar,conf,nconf,iz,z,
     1  ion,irel,hxid,mesh,c,idb,exf,corrf,kut,npar,
     2  nlbcd,nnlz,nkkk,e,ee8,npnl,r,ru, ((pnl(i,m),i=1,km),m=1,npnl),
     3  iw6
      go to 115
  112 ncmax=nc0+nc-1
      go to 130
  115 cf1(nc)=conf(1)
      cf2(nc)=conf(2)
      cf3(nc)=conf(3)
      etot(nc)=109.73731*vpar(1)
      ee(nc)=e(ncspvs)
      ee8nc(nc)=ee8
      norb(nc)=ncspvs
      if (ic.ne.32.or.ns32.ne.-7.or.ipct.ne.0) go to 118
      if (nc.gt.nc2+7.and.vpar(1).lt.vpar1) ipct=nc-nc2-1
  118 vpar1=vpar(1)
      if (idip.lt.9.or.nt2(ncspvs).lt.99) go to 120
      if (ncont1.eq.1000) ncont1=nc
      if (ee(nc).eq.ee(ncont1)) ncont2=nc
      ieras=ncont2-ncont1
      if (ieras.gt.0) idele=1000/ieras
      ieras=nc-ncont2-1
      if (ieras.gt.0) idele=min0(idele,3000/ieras)
  120 if (nc.eq.1) iont=ion
      if (nc.eq.1) izt=iz
      if (iont.eq.ion.and.izt.eq.iz) go to 132
  130 nc3=nc-1
      if (nc3.eq.0) go to 900
      backspace 2
      go to 160
  132 if (ncspvs.gt.norbx) norbx=ncspvs
      prty=0.0
      do 135 i=1,ncspvs
      n(i,nc)=nt2(i)
      l(i,nc)=lt2(i)
      w(i,nc)=wt2(i)
      if (i.eq.ncspvs.and.w(i,nc).le.1.0) go to 134
      nmax=max0(nmax,n(i,nc))
      lmax=max0(lmax,l(i,nc))
  134 eras=l(i,nc)
  135 prty=prty+w(i,nc)*eras
      two=2.0
      prty=mod(prty,two)
      if (nc.eq.1) prty1=prty
      if (prty.eq.prty1) go to 150
      if (ic.eq.32) go to 130
      prty1=prty
      nc2=nc-1
      ic=32
      icn(2)=32
  150 write (ic) nt2,lt2,wt2,ncspvs,vpar,conf,nconf,iz,z,
     1  ion,irel,hxid,mesh,c,idb,exf,corrf,kut,npar,
     2  nlbcd,nnlz,nkkk,e,ee8,npnl,r,ru, ((pnl(i,m),i=1,km),m=1,npnl)
      go to 110
c
  160 if (nc3.eq.1.and.cf1(1).eq.'dummy ') go to 700
      write (9,13)
   13 format (34h1rcn2---input for rcg mod 10 or 11///)
      if (nc2.eq.0) nc2=nc3
      nsconf(2,1)=nc2
      nsconf(2,2)=nc3-nc2
      if (nscf31.eq.0) nsconf(3,1)=nc2
      if (nscf32.eq.0) nsconf(3,2)=nsconf(2,2)
      do 162 i=1,8
      iww(i)=0
      do 162 nc=1,kco
      lbo(i,nc)=lb(i,nc)
      lb(i,nc)=lsymb(1)
      ll(i,nc)=0
      nn(i,nc)=0
      wwo(i,nc)=ww(i,nc)
  162 ww(i,nc)=0.0
c
c          set up partially-filled or interacting shells
c
c     first, find orbitals not always full, but with more
c        than one electron in some configuration,
c          or find singly-occupied orbital which is not the outermost orbital
      j1=0
      if (nmax.eq.0) go to 170
      nmin=1
      do 169 nnn=nmin,nmax
      lmaxp1=min0(nnn,lmax+1)
      do 169 lp1=1,lmaxp1
      lll=lp1-1
      wmax=1.0
      a=4*lll+2
      wmin=a
      do 166 nc=1,nc3
      ncspvs=norb(nc)
      do 165 i=1,ncspvs
      if (n(i,nc).ne.nnn.or.l(i,nc).ne.lll) go to 165
      wmin=min(wmin,w(i,nc))
      wmax=max(wmax,w(i,nc))
      if (w(i,nc).eq.1.0.and.i.ne.ncspvs) wmax=2.0
      go to 166
  165 continue
      wmin=0.0
  166 continue
      if (wmin.eq.a.or.wmax.eq.1.0) go to 169
      j1=j1+1
      do 168 nc=1,nc3
      nn(j1,nc)=nnn
  168 ll(j1,nc)=lll
  169 continue
c
c     second, find remaining (singly-occupied) orbitals
c        (for one parity at a time)
  170 nsubco=nosubc
      nosubc=0
      k=1
      ncn=1
      ncx=nc2
      if (icon.ne.1) icon=max0(icon,j1+1)
  171 j3=j1
      do 180 nc=ncn,ncx
      nc1=max0(nc-1,ncn)
      do 172 j=1,8
  172 nlb(j,nc)='   '
      ncspvs=norb(nc)
      do 179 i=1,ncspvs
      if (j3.eq.0.and.i.eq.ncspvs.and.nc.eq.ncx) go to 177
      if(j3.eq.0) go to 174
      do 173 j=1,j3
      llll=ll(j,nc1)
      lll2=l(i,nc)
      nnnn=nn(j,nc1)
      nnn2=n(i,nc)
      if (n(i,nc).eq.nn(j,nc1).and.l(i,nc).eq.ll(j,nc1)) go to 178
  173 continue
  174 if (j3.eq.j1.or.nc.eq.ncn) go to 176
      j=j3
      if (l(i,nc).eq.ll(j,nc1).and.i.eq.ncspvs) go to 178
  176 a=4*l(i,nc)+2
      if (w(i,nc).eq.a) go to 179
  177 j3=j3+1
      if (icon.gt.1) j3=min0(j3,icon)
      do 1177 nc1=nc,ncx
 1177 ll(j3,nc1)=l(i,nc)
      j=j3
  178 ww(j,nc)=w(i,nc)
      nn(j,nc)=n(i,nc)
      if (nn(j,ncn).eq.0) nn(j,ncn)=n(i,nc)
      jj=ll(j,nc)
      lb(j,nc)=lsymb(jj+1)
c     encode (3,16,nlb(j,nc)) nn(j,nc),lb(j,nc)
      write (nlb(j,nc),16) nn(j,nc),lb(j,nc)
   16 format (i2,a1)
  179 continue
  180 continue
      nosubc=max0(nosubc,j3)
      if (nosubc.le.8) go to 181
      write (9,17)
   17 format (/'*****more than 8 subshells!')
      go to 700
  181 if (nc2.eq.nc3.or.k.eq.2) go to 182
      k=2
      ncn=nc2+1
      ncx=nc3
      go to 171
c
c          if configurations same as for previous case, set ictc=1
c
  182 ictc=1
      if (nosubc.ne.nsubco) ictc=0
      if (ictc.eq.0) go to 185
      do 184 i=1,nosubc
      do 183 nc=1,nc3
      if (ww(i,nc).ne.wwo(i,nc)) ictc=0
      if (ww(i,nc).eq.0.0) go to 183
      if (lb(i,nc).ne.lbo(i,nc)) ictc=0
  183 continue
  184 continue
      if (ictc.eq.0) go to 185
      backspace 11
      go to 200
c          punch control card
  185 nsconf(1,1)=nosubc
      nsconf(1,2)=nosubc
      if (nc2.eq.nc3) nsconf(1,2)=0
      if (iw6.ge.0) iw6=6
      if (iw6.lt.0) iw6=-6
      if (idip.eq.6) iw6=8*iw6/abs(iw6)
      write (9,18) nck,nocset,nsconf,iabg,option,iquad,dmin,iprint,
     1  iengyd,ispecc,iw6,icon,isli,idip,ipct,ictc,irel
   18 format (4x,1h2,a2,i3,i1,2i2,i1,2i2,i1,a28,i1,1x,9h1000.0000,
     1  2a5,2a1,6i2,i8)
      if (icon.ne.1) write (11,18) nck,nocset,nsconf,iabg,option,iquad,
     1  dmin,iprint,iengyd,ispecc,iw6,ipct,ictc
      if (nocset.lt.0) nocset=nocset-1
c          punch configuration cards
  191 k=1
      ncn=1
      ncx=nc2
  192 if (ncn.eq.ncx) go to 196
      do 195 i=1,nosubc
      do 194 nc=ncn,ncx
      if (ww(i,nc).eq.0.0) go to 194
      do 193 m=ncn,ncx
      if (ww(i,m).ne.0.0) go to 193
      ll(i,m)=ll(i,nc)
      lb(i,m)=lb(i,nc)
  193 continue
      go to 195
  194 continue
  195 continue
  196 do 198 nc=ncn,ncx
      do 197 i=1,nosubc
  197 iww(i)=ww(i,nc)
      write  (9,19) (lb(i,nc),iww(i), i=1,8),cf1(nc),cf2(nc),cf3(nc),
     1  etot(nc),ee8nc(nc)
   19 format (1x,8(a1,i2,4x),5x,3a6,5x,4heav=,f14.3,3h kk,
     1  5x,5hekin=,f9.4,3h ry)
      if (icon.ne.1) write (11,20) (lb(i,nc),iww(i), i=1,8),
     1  cf1(nc),cf2(nc),cf3(nc),etot(nc),ee8nc(nc)
   20 format (8(a1,i2,2x),3a6,f13.3,f9.4)
  198 continue
      if (nc2.eq.nc3.or.k.eq.2) go to 200
      k=2
      ncn=nc2+1
      ncx=nc3
      go to 192
c
c
c          rearrange, scale, and punch single-conf parameters
c
  200 rewind 31
      rewind 32
      iflag=0
      kk=1
      nfirst=1
      nlast=nc2
      ic=31
      do 495 nc=1,nc3
      icn(1)=ic
      icn(2)=ic
      read (ic) nt2,lt2,wt2,ncspvs,vpar,conf,nconf,iz,z,
     1  ion,irel,hxid,mesh,c,idb,exf,corrf,kut,npar,
     2  nlbcd,nnlz,nkkk,e,ee8
      i1=ncspvs+1
      do 201 i=i1,25
  201 l(i,nc)=77
      ncfg2=nconf
      nconf=99
      nconfn(kk)=99
      if (nc.eq.1) e1=vpar(1)
      kpar(1)=0
      vpar(1)=eav11+109.73731*(vpar(1)-e1)
      eav(nc)=vpar(1)
c          determine energy widths for pseudo-discrete configurations
      del(nc)=1.0
      if (nc.ge.ncont1) del(nc)=0.0
      if (idip.eq.8.and.nt2(ncspvs).ge.99) del(nc)=0.0
      if (nc.eq.nfirst.and.nt2(ncspvs).lt.99) go to 202
      if (idip.ne.7.or.w(ncspvs,nc).ne.1.0) go to 206
      if (l(ncspvs,nc).ne.l(ncspvs,nc-1)) emax=eav(nc)-109.737*e(ncspvs)
  202 zc=ion+1
      if (zc.le.0.0) zc=1.0
      fn=99.0
      if (e(ncspvs).lt.0.0) fn=zc/sqrt(-e(ncspvs))
      del0=109.73731
      if (fn.eq.99.0) go to 203
      del0=2.0*del0*(zc**2)/(fn**3)
      if (nc.eq.nfirst) go to 1202
      if (l(ncspvs,nc).ne.l(ncspvs,nc-1)) go to 206
      if (n(ncspvs,nc).gt.n(ncspvs,nc-1)+1) go to 203
 1202 emax=eav(nc)+0.5*del0
      if (nc.eq.nfirst.or.nc.eq.nc2.or.nc.eq.nc3) go to 206
      ncs1=ncspvs
      vpar1=vpar(1)
      read (ic) nt2,lt2,wt2,ncspvs,vpar(1)
      backspace ic
      eavp1=eav11+109.73731*(vpar(1)-e1)
      ncspvs=ncs1
      vpar(1)=vpar1
      if (eavp1.le.eav(nc)) go to 206
      x=(eavp1-eav(nc))/(eavp1-eav(nc-1))
      emax=min(emax,x*eav(nc)+(1.0-x)*eavp1)
      go to 206
  203 emin=emax
      emax=2.0*eav(nc)-emin
      if (nc.eq.nc2.or.nc.eq.nc3) go to 205
      ncs1=ncspvs
      vpar1=vpar(1)
      read (ic) nt2,lt2,wt2,ncspvs,vpar(1)
      backspace ic
      ib=lt2(ncspvs)
      eavp1=eav11+109.73731*(vpar(1)-e1)
      ncs2=ncspvs
      ncspvs=ncs1
      vpar(1)=vpar1
      if (nc.eq.nfirst.or.eav(nc).lt.eav(nc-1)) go to 1203
      if (ncspvs.ne.ncs2) go to 205
      if (ee(nc).lt.ee(nc-1)) go to 1203
      if (nc.gt.nfirst.and.ib.ne.l(ncspvs,nc)) go to 205
      if (nc.gt.nfirst.and.ib.eq.l(ncspvs,nc).and.ib.eq.l(ncspvs,nc-1))
     1  go to 204
 1203 emax=0.5*(eav(nc)+eavp1)
      emin=emax+eav(nc)-eavp1
      go to 205
  204 if (eavp1.le.eav(nc)) go to 205
      x=(eavp1-eav(nc))/(eavp1-min(eav(nc-1),emin))
      half=0.5
      x=max(x,half)
      emax=min(emax,x*eav(nc)+(1.0-x)*eavp1)
  205 if (emax.le.emin) go to 206
      del(nc)=sqrt((emax-emin)/del0)
c
  206 do 210 i=1,8
      ix(i)=0
      nlht(i)='   '
      ze(i)=-1.0
      do 210 k=1,5
      fk(i,k)=-1.0
      do 210 j=1,8
  210 fgk(i,j,k)=-1.0
c
      npar=1
      jx=0
      do 220 i=1,ncspvs
      a=4*l(i,nc)+1
      if (w(i,nc).lt.1.0.or.w(i,nc).gt.a) go to 220
      jx=jx+1
      nlht(jx)=nlbcd(i)(1:3)
      l(jx,nc)=l(i,nc)
      w(jx,nc)=w(i,nc)
      if (w(i,nc).eq.1.0.or.w(i,nc).eq.a) go to 220
      nk=l(i,nc)
      do 216 k=1,nk
      npar=npar+1
  216 fk(jx,k)=vpar(npar)
  220 continue
c
      if (jx.eq.0) go to 291
      do 230 i=1,jx
      if (l(i,nc).eq.0) go to 230
      npar=npar+1
      ze(i)=vpar(npar)
  230 continue
c
      if (jx.eq.1) go to 251
      jm1=jx-1
      do 240 i=1,jm1
      j1=i+1
      do 240 j=j1,jx
      nk=min0(l(i,nc),l(j,nc))
      if (nk.eq.0) go to 240
      do 235 k=1,nk
      npar=npar+1
  235 fgk(i,j,k)=vpar(npar)
  240 continue
c
      do 250 i=1,jm1
      j1=i+1
      do 250 j=j1,jx
      nk=min0(l(i,nc),l(j,nc))+1
      do 245 k=1,nk
      npar=npar+1
  245 fgk(j,i,k)=vpar(npar)
  250 continue
c
c
  251 npar=1
      do 260 i=1,nosubc
      do 256 j=1,jx
      if (nlht(j).ne.nlb(i,nc)) go to 256
      ix(i)=j
      do 252 k=1,5
      if (fk(j,k).lt.0.0) go to 253
      npar=npar+1
      kpar(npar)=1
  252 vpar(npar)=fk(j,k)*fact(1)
  253 if (fk(j,1).lt.0.0) go to 260
      if (iabg.eq.0) go to 260
      nk=ll(i,nc)
      if (nk.ne.2) go to 254
      nk=nk+1
      if (ww(i,nc).gt.2.and.ww(i,nc).lt.8) nk=nk+2
  254 do 255 k=1,nk
      npar=npar+1
      kpar(npar)=1
      vpar(npar)=0.0
  255 if (k.eq.1) vpar(npar)=alf
      go to 260
  256 continue
  260 continue
c
      jj=0
      do 270 i=1,nosubc
      ii=ix(i)
      if (ii.eq.0) go to 270
      if (ii.le.jj) iflag=1
      jj=ii
      if (ze(ii).lt.0.0) go to 270
      npar=npar+1
      kpar(npar)=2
      vpar(npar)=ze(ii)*fact(2)
  270 continue
c
      if (jx.eq.1) go to 291
      jm1=nosubc-1
      do 280 i=1,jm1
      if (ix(i).eq.0) go to 280
      j1=i+1
      do 279 j=j1,nosubc
      ii=ix(i)
      jj=ix(j)
      if (jj.eq.0) go to 279
      if (ii.lt.jj) go to 272
      jjj=ii
      ii=jj
      jj=jjj
  272 do 275 k=1,5
      if (fgk(ii,jj,k).lt.0.0) go to 279
      npar=npar+1
      kpar(npar)=3
  275 vpar(npar)=fgk(ii,jj,k)*fact(3)
  279 continue
  280 continue
c
      do 290 i=1,jm1
      if (ix(i).eq.0) go to 290
      j1=i+1
      do 289 j=j1,nosubc
      ii=ix(i)
      jj=ix(j)
      if (jj.eq.0) go to 289
      if (ii.lt.jj) go to 282
      jjj=ii
      ii=jj
      jj=jjj
  282 do 285 k=1,5
      if (fgk(jj,ii,k).lt.0.0) go to 289
      npar=npar+1
      kpar(npar)=4
  285 vpar(npar)=fgk(jj,ii,k)*fact(4)
  289 continue
  290 continue
c
  291 if (npar.ge.5) go to 294
      n1=npar+1
      do 292 i=n1,5
      kpar(i)=0
      ivpar(i)=0.0
  292 vpar(i)=0.0
  294 write (9,28) conf, (vpar(i), i=1,5), hxid,fact
   28 format (//1h0,3a6,6x,5f12.5,5x,a2,5x,5hfact=,5f6.2)
      if (nc.ge.ncont1) vpar(1)=-9500+idele*(nc-ncont1)
      if (nc.gt.ncont2) vpar(1)=-7500+idele*(nc-ncont2-1)
      do 295 i=1,npar
  295 ivpar(i)=10000.0*vpar(i)
      if (vpar(1).gt.99999.99) go to 296
      if (vpar(1).lt.-9999.99) go to 296
      write (11,29) conf,npar, (ivpar(i),kpar(i), i=1,5), hxid,
     1  (ifact(i), i=1,4)
   29 format (3a6,i2,5(i9,i1),a2,4i2)
      go to 298
  296 write (11,27) conf,npar, (vpar(i),kpar(i), i=1,5), hxid,
     1  (ifact(i), i=1,4)
   27 format (3a6,i2,f9.1,i1,4(f9.2,i1),a2,4i2)
  298 if (npar.le.5) go to 300
      write ( 9,30) (vpar(i), i=6,npar)
   30 format (7f12.5)
      write (11,31) (ivpar(i),kpar(i), i=6,npar)
   31 format (7(i9,i1))
c
c          calc configuration interaction parameters
c
  300 if (nc.lt.nlast) go to 495
      if (nfirst.eq.nlast) go to 350
      if (isli.gt.4) go to 350
      subr0=0.0
      p(1,1)=-99.0
      subr=slin
      nlm1=nlast-1
      neras=nsconf(3,kk)
      if (neras.ge.0.or.neras.le.-8) go to 301
      nlm1=min0(nlm1,nfirst-1+max0(-neras,ipct))
      ncd1=0
      ha1='   '
      hb1='   '
  301 do 329 ncd=nfirst,nlm1
      ncfg(1)=ncd+nc0
      ncpdf=ncd+1
      ncpdl=nlast
      if (ncd.ne.nfirst.and.neras.eq.-9) ncpdl=ncpdf
      irho1=-7
      isig1=-7
      do 329 ncpd=ncpdf,ncpdl
      ncfg(2)=ncpd+nc0
      nrk=0
      do 328 irho=1,nosubc
      do 328 isig=irho,nosubc
      do 328 irhop=1,nosubc
      do 327 isigp=irhop,nosubc
      mmin=0
      if (irho.ne.irhop.or.isig.ne.isigp) go to 303
      www=0
      do 302 i=isig,nosubc
  302 www=www+ww(i,ncd)+ww(i,ncpd)
      if (www.gt.2.0) go to 327
  303 do 304 i=1,nosubc
      ww1=ww(i,ncd)
      ww2=ww(i,ncpd)
      if (i.eq.irho) ww1=ww1-1.0
      if (i.eq.isig) ww1=ww1-1.0
      if (i.eq.irhop) ww2=ww2-1.0
      if (i.eq.isigp) ww2=ww2-1.0
      if (ww1.ne.ww2) go to 327
      if (ww1.lt.0.0) go to 327
      if (i.le.isig.or.i.le.isigp.or.ww1.le.0.0) go to 304
      if (ll(i,ncd).ne.ll(i,ncpd)) go to 327
      if (nn(i,ncd).ne.nn(i,ncpd)) mmin=-1
      if (nn(i,ncd)+nn(i,ncpd).eq.198.and.ee(ncd).ne.ee(ncpd)) mmin=-1
  304 continue
      a=4*ll(irho,ncd)+2
      if (ww(irho,ncd).eq.a.and.ww(irho,ncpd).eq.a) go to 327
      a=4*ll(isig,ncd)+2
      if (ww(isig,ncd).eq.a.and.ww(isig,ncpd).eq.a) go to 327
      kdmin=max0(iabs(ll(irho,ncd)-ll(irhop,ncpd)),iabs(ll(isig,
     1  ncd)-ll(isigp,ncpd)))
      kdmax=min0(ll(irho,ncd)+ll(irhop,ncpd),ll(isig,ncd)
     1  +ll(isigp,ncpd))
      if(kdmin.gt.kdmax) go to 327
      ovfact=1.0
      if (mmin.lt.0) go to 320
      if (iovfact.le.0.or.iovfact.eq.2) go to 320
c          calculate overlap factor for spectator electrons
      ha1t=ha1
      do 310 i=1,nosubc
      ww1=ww(i,ncd)
      if (i.eq.irho) ww1=ww1-1.0
      if (i.eq.isig) ww1=ww1-1.0
      if (ww1.le.0.0) go to 310
      ha=nlb(i,ncd)
      hb=ha
      call over
      ovfact=ovfact*(overlp**ww1)
      if (iovfact.gt.3) write (9,1031) ncfg,i,ha,ww1,overlp,ovfact
 1031 format (3i3,2x,a3,f5.1,2f10.6)
  310 continue
      ha1=ha1t
      ncd1=-7
  320 continue
      ha=nlb(irho,ncd)
      hb=nlb(isig,ncd)
      hc=nlb(irhop,ncpd)
      hd=nlb(isigp,ncpd)
      n12=2
      if (ncd.ne.ncd1) n12=1
      if (ha.ne.ha1.or.hb.ne.hb1) n12=1
      if (irho.ne.irho1.or.isig.ne.isig1) n12=1
      call sli2
      ncd1=ncd
      ha1=ha
      hb1=hb
      irho1=irho
      isig1=isig
      ncfg2=ncfg(2)
  327 continue
  328 continue
      if (nrk.eq.0) go to 329
      if (idip.eq.7.or.idip.eq.8) go to 324
      if (ncd.lt.ncont1) go to 326
  324 do 325 i=1,nrk
  325 rkaysc(i)=del(ncd)*del(ncpd)*rkaysc(i)
  326 write (9,32) del(ncd),del(ncpd),(rkaysc(i),i=1,nrk)
   32 format (9h sqrtdel=,2f10.4,5x,5(f11.4,2x)/7(f11.4,2x))
      n2=5
      write (11,33) conf1(2),conf1(3),conf2(2),conf2(3),nrk,
     1  (rkaysc(i),n2,i=1,5),hxid,(ifact(i), i=1,3),ifact(5)
   33 format (a6,a3,1h-,a6,a3,i1,5(f9.4,i1),a2,4i2)
      if (nrk.le.5) go to 329
      write (11,34) (rkaysc(i),n2, i=6,nrk)
   34 format (7(f9.4,i1))
  329 continue
c
  350 if (iquad.lt.3.and.iquad.ne.kk) go to 390
      n1=nfirst
      n2=nlast
      n3=n1
      n4=n2
      irmn1=irnq+1
      irmx1=irxq+1
      icn(1)=ic
      icn(2)=ic
      go to 402
  390 if (kk.eq.2) go to 400
      if (iw6.lt.0) write (6,38) nfirst,nlast,kk
   38 format (' finish g5inp for configurations',i4,'  to',i4,
     1  ',   parity=',i3)
      if (nc2.eq.nc3) go to 496
      kk=2
      nfirst=nc2+1
      nlast=nc3
      ic=32
      write (9,39)
   39 format (1h1)
      go to 495
c
c          calc quadrupole or dipole reduced matrix elements
c
  400 n1=1
      n2=nc2
      n3=nc2+1
      n4=nc3
      irmn1=irnd+1
      irmx1=irxd+1
      icn(1)=31
      icn(2)=32
  402 subr0=0.0
      subr=dipn
      ipwr=irmn1-1
      if (idip.eq.1) go to 460
      j1=icn(1)-30
      j2=icn(2)-30
      if (igen.lt.5) go to 3402
      elo=eav(1)
      ehi=elo
      do 1402 i=1,nc3
      ea=eav(i)
      if (ea.lt.elo) elo=ea
      if (ea.gt.ehi) ehi=ea
 1402 continue
      if (ehi.le.elo) ehi=elo+vpar(2)
      enmax=(ehi-elo)/109.73731
      enmax=enmax*1.1*xmax
      if (enmax.lt.0.001) stop 140
      ekmax=2.0*sqrt(enmax)
      ekmin=1.0e-3
      ekmaxl=log(ekmax)
      ekminl=log(ekmin)
      delekl=(ekmaxl-ekminl)/float(nbigks-1)
      write (11,42) nbigks,ekminl,ekmaxl,delekl,nenrgs,xmin,xmax
   42 format (i5,3f15.10,i10,2f10.2)
      do 2402 i=1,nbigks
      ekl=ekminl+delekl*(i-1)
 2402 bigks(i)=exp(ekl)
      icase=0
      write (9,43) enmax,nbigks
   43 format (/7h enmax=,f14.7,8h nbigks=,i4,//9h k-values/)
      write (9,44) (bigks(i),i=1,nbigks)
   44 format (8f14.7)
 3402 continue
      do 450 ipwr1=irmn1,irmx1,2
      ipwr=ipwr1-1
      do 450 ncd=n1,n2
      ncfg(1)=ncd+nc0
      do 450 ncpd=n3,n4
      ncfg(2)=ncpd+nc0
      do 439 irho=1,nosubc
      do 438 irhop=1,nosubc
      if (iabs(ll(irho,ncd)-ll(irhop,ncpd)).gt.ipwr) go to 438
      lsum=ll(irho,ncd)+ll(irhop,ncpd)
      if (lsum.lt.ipwr) go to 438
      if (mod(lsum+ipwr,2).ne.0) go to 438
      if (irho.ne.irhop) go to 410
      if (ncd.ne.ncpd) go to 404
      do 403 i=irho,nosubc
      eras=4*ll(i,ncd)+2
      www=ww(i,ncd)
      if ((www.eq.0.0.or.www.eq.eras).and.i.eq.irho) go to 438
      if (i.eq.irho) go to 403
      if (www.eq.0.0.or.www.eq.eras) go to 403
      if (ll(i,ncd).eq.0) go to 403
      go to 438
  403 continue
      go to 410
  404 www=0
      do 405 i=irho,nosubc
  405 www=www+ww(i,ncd)+ww(i,ncpd)
      if (www.ne.2.0) go to 438
  410 do 420 i=1,nosubc
      ww1=ww(i,ncd)
      ww2=ww(i,ncpd)
      if (i.ne.irho.and.i.ne.irhop) go to 412
      if (i.eq.irho) ww1=ww1-1.0
      if (i.eq.irhop) ww2=ww2-1.0
      if (ww1.lt.0.0) go to 438
      go to 414
  412 if (ww1+ww2.eq.0.0) go to 420
      if (nlb(i,ncd).ne.nlb(i,ncpd)) go to 438
  414 if (ww1.ne.ww2) go to 438
  420 continue
      ovfact=1.0
      if (iovfact.lt.2) go to 430
c          calculate overlap factor for spectator electrons
      ha1t=ha1
      do 425 i=1,nosubc
      ww1=ww(i,ncd)
      if (i.eq.irho) ww1=ww1-1.0
      if (ww1.le.0.0) go to 425
      ha=nlb(i,ncd)
      hb=ha
      call over
      ovfact=ovfact*(overlp**ww1)
      if (iovfact.gt.3) write (9,1031) ncfg,i,ha,ww1,overlp,ovfact
  425 continue
      ha1=ha1t
  430 continue
      ha=nlb(irho,ncd)
      hb=nlb(irhop,ncpd)
      mmin=0
      call dip
      go to 450
  438 continue
  439 continue
      ovfact=1.0
      mmin=-7
      call dip
  450 continue
      if (igen.lt.5) go to 460
      do 455 ibk=1,nbigks
      do 454 ic=1,icase
      do 452 icc=1,3
      conf1(icc)=cst(ic,icc)
  452 conf2(icc)=cst(ic,icc+3)
      ipwr=st(ic,1)
      frac=st(ic,2)
      hxid=st(ic,3)
      iover=st(ic,4)
      if1=st(ic,5)
      ha=kst(ic,1)
      hb=kst(ic,2)
      reddip=rdips(ibk,ic)
      write (11,46) conf1,conf2,reddip,ha,rj,ipwr,hb,frac,hxid,iover,if1
   46 format(3a6,2x,3a6,f12.5,1h(,a3,2h//,a1,i1,2h//,a3,1h),f6.3,a2,2i4)
  454 continue
  455 continue
      if (iw6.lt.0) write (6,47)
   47 format (' finish calculation of Bessel-function matrix elements')
  460 if (mod(ipwr,2).eq.0) go to 390
c
  495 continue
      if (iw6.lt.0.and.kk.eq.2) write (6,38) nfirst,nlast,kk
c
  496 if (iflag.eq.0) go to 500
      do 497 i=1,5
  497 write (9,40)
   40 format (11h **********)
      write (9,41)
   41 format (34h0*warning --- orbitals rearranged*)
c
c
c
  500 call seconds(t)
      t=t-t0
      write (9,50) t
   50 format (//20x,10h-99999999.,10x,2ht=,f7.3,4h sec)
      if (nocset.lt.0) write (11,51)
   51 format (20x,10h-55555555.)
      write (11,52)
   52 format (20x,10h-99999999.)
c
c
  700 nc0=nc0+nc3
      if (nc0.eq.ncmax) go to 900
      go to 102
c
  900 return
      end
      function s3j0sq(fj1,fj2,fj3)
c
c          calculate square of 3-j symbol with zero magnetic quantum nos.
c
c
      implicit real*8 (a-h,o-z)
      fj=fj1+fj2+fj3
      a=fj-fj1-fj1
      b=fj-fj2-fj2
      c=fj-fj3-fj3
      s3j0sq=fctrl(a)*fctrl(b)*fctrl(c)/fctrl(fj+1.0)
      a=fctrl(a/2.0)*fctrl(b/2.0)*fctrl(c/2.0)/fctrl(fj/2.0)
      s3j0sq=s3j0sq/a/a
      return
      end
      function s3j (fj1, fj2, fj3, fm1, fm2)
c
c          calculate 3-j symbol
c
      implicit real*8 (a-h,o-z)
      s3j=0.0
      fm3=fm1+fm2
          a=fj2+fj3+fm1
      b=fj1-fm1
      c=-fj1+fj2+fj3
      d=fj3+fm3
      e=fj1-fj2-fm3
      f=fj1-fj2+fj3
      g=fj1+fj2-fj3
      h=fj1+fj2+fj3+1.0
      e2=fctrl(b)*fctrl(fj1+fm1)*fctrl(fj2-fm2)*fctrl(fj2+fm2)
      e1=(fctrl(c)*fctrl(f)/fctrl(h))*fctrl(g)*fctrl(d)*fctrl(fj3-fm3)
      if (e1.le.0.0) go to 153
      e1=sqrt(e2)/sqrt(e1)
      if (e1) 153,153,150
  150 zero=0.0
      i1=max(zero,-e)
      i2=min(a,c,d)
      if (i2-i1) 153,151,151
  151 do 152 i=i1,i2
      fi=i
      e2=fctrl(fi)*fctrl(c-fi)*fctrl(d-fi)/fctrl(a-fi)
  152 s3j=s3j+(((-1.0)** mod (i,2))/e2)*fctrl(b+fi)/fctrl(e+fi)
      ieras=fj1+fm2+fm3
      s3j=s3j*((-1.0)**mod(ieras,2))/e1
  153 return
      end
      function fctrl(a)
c
c          calculate factorial of a
c
      implicit real*8 (a-h,o-z)
      fctrl=1.0
      if (abs(a)-0.1) 10, 10, 11
   10 a=0.0
   11 if (a) 12, 15, 13
   12 fctrl=0.0
      go to 15
   13 imax=a+0.1
      do 14 i=1,imax
   14 fctrl=fctrl*float(i)
   15 return
      end
      subroutine sbess(rb,itest,ls,eksq,sz,szp)
c
c     routine for the evaluation of spherical bessel functions
c           using recurrence relations
c
      implicit real*8 (a-h,o-z)
      common /blk2/ ibug1,ibug2,ibug3,ibug4,ibug5,ibug6,lswt,ldel,lmin
      common/inform/ iread,iwrite,ipunch
      dimension sb(200), s(200)
c
      if (itest.eq.3) eksq=-eksq
      ak=sqrt(eksq)
      r=ak*rb
      if (ls-r) 10,20,20
   10 go to (30,60,90), itest
   20 go to (180,60,90), itest
   30 sb(1)=sin(r)
      sb(2)=sin(r)/r-cos(r)
      if (ls-1) 40,50,140
   40 sz=sb(1)
      szp=ak*cos(r)
      go to 210
   50 sz=sb(2)
      szp=ak*(cos(r)/r-sin(r)/r**2+sin(r))
      go to 210
   60 sb(1)=-cos(r)
      sb(2)=-cos(r)/r-sin(r)
      if (ls-1) 70,80,140
   70 sz=sb(1)
      szp=ak*sin(r)
      go to 210
   80 sz=sb(2)
      szp=ak*(sin(r)/r+cos(r)/r**2-cos(r))
      go to 210
   90 sb(1)=1.0
      sb(2)=-(1.0+1.0/r)
      if (ls-1) 100,110,120
  100 sz=exp(-r)
      szp=-ak*exp(-r)
      go to 210
  110 sz=-(1.0+1.0/r)*exp(-r)
      szp=(1.0+1.0/r+1.0/r**2)*exp(-r)
      go to 210
  120 ls1=ls+1
      eras=-1.0
      do 130 l=2,ls1
      eras=-eras
  130 sb(l+1)=(2*l-1)*eras*sb(l)/r-sb(l-1)
      l=ls1
      sz=sb(l+1)*exp(-r)
      szp=ak*((l+1)*(-1)**l*sb(l+1)/r+sb(l))*exp(-r)
      go to 210
  140 ls1=ls+1
      do 150 l=2,ls1
      sb(l+1)=(2*l-1)*sb(l)/r-sb(l-1)
  150 continue
      if (itest-2) 200,160,200
  160 if (ls-ls/2*2) 170,200,170
  170 sz=-sz
      szp=-szp
      go to 200
  180 m=ls+12
      if (r.lt.0.05) m=ls+6
      s(m+1)=0.0
      s(m)=1.0e-20
      mm1=m-1
      do 190 i=1,mm1
      j=m+1-i
      s(j-1)=(2*j-1)/r*s(j)-s(j+1)
  190 continue
      sb(m)=sin(r)/s(1)
      sb(ls)=s(ls)*sb(m)
      sb(ls+1)=s(ls+1)*sb(m)
      sb(ls+2)=s(ls+2)*sb(m)
  200 sz=sb(ls+1)
      szp=ak*(sb(ls+1)/r+(ls*sb(ls)-(ls+1)*sb(ls+2))/(2*ls+1))
  210 if (ibug5-1) 240,220,240
  220 write(iwrite,230)sz,szp
  230 format (//11h sz,szp  = ,(2e16.8)//)
  240 continue
      return
      end
      subroutine seconds(t)
c
c          Timing routine (results for information only)
c               For other machines, set t=0.0 or add
c               appropriate code.
c
      real*8 t
      real etime,t1,t2
      dimension t2(2)
c      call dostim(i,j,k,l)
      t=(i*60+j)*60+k+l/100.
c
c------------------------------------
c          Use this code for a CRAY
c     t=second(t)
c------------------------------------
c          Use this code for a VAX or Macintosh
c     t1=secnds(0.0)
c     t=dble(t1)
c------------------------------------
c          Use this code for a SUN
c      t=etime(t2)
c-------------------------------------
c          Use this code for IBM RISC
c     it=mclock()
c     t=it
c     t=t/100.0
c-------------------------------------
      return
      end
