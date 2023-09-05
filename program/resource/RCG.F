c     overlay(g9,0,0)
      program rcg11
c     program rcg11(ing11,tape10=ing11,outg11,tape9=outg11,
c    1  tape3,tape20,tape31,tape32,tape41,
c    2  tape72,tape73,tape74,tape2e,tape2=tape2e,tape19,
c    3  outgine,tape11=outgine,tape13,tape5)
c
c     Pprogram copyright 1980, Los Alamos National Laboratory and
c          U.S. Government.  This program may be freely distributed
c          gratis any place in the world, but may not be sold.
c
c
c
c          RCG-Vers. 11.1.1 (August 1996), main program
c
c
c          RCG is a program to compute coefficient matrices for 
c               atomic energy-level parameters (fk, gk, zeta, alpha,
c               beta, gamma, t, rk), read parameter values,
c               and compute and diagonalize the energy matrices
c               to obtain energy levels and eigenvectors.
c          Also, if desired, to compute angular coefficient matrices
c               for magnetic dipole and
c               for electric dipole and quadrupole transitions,
c               read radial multipole integrals, and calculate
c               oscillator strengths and transition probabilities.
c
c          First version (RCG Mod 0) coded by B. Fagan and R. D. Cowan,
c               Los Alamos Scientific Laboratory, summer and fall 1964.
c
c          RCG Mod 5 (including configuration interaction)
c               coded fall, 1968 by R. D. Cowan for the IBM 7030 (Stretch).
c               --- modified for the CDC 6500
c               at Purdue University, March 1971.  Converted July-November
c               1971 to LASL CDC 7600, using large core memory.
c               Dimensions increased to 8 subshells, February 1975.
c               Autoionization trans.-prob. calcs. added spring 1975.
c               plane-wave-born collision-strength options added
c               Jan-Feb 1980 by W. D. Robb and R. D. Cowan.
c          modified to allow different l for final subshell, July 1981,
c               and to accept rescaling cards, October 1981.
c          Mod 10:
c               Faster 3nj routines incorporated July 21, 1983.
c               Modified for CRAY 1 computers, December 1983.
c               Modified for Zeeman-Lab. (Amsterdam) CYBER 170/750, Feb. 1984.
c               Option to truncate to given set of LS values added June 1984.
c               Write on tape11 of RCE input added at NBS (now NIST) May 1986.
c               Changes in action of print-control variables ipct
c                    and ictc made at Zeeman Lab., December 1987.
c
c               A version for the VAX 8200 made at Lund University (Sweden),
c                    March-April 1988, incorporating numerous minor
c                    additions and improvements.
c               Reconverted to the CRAY
c                    at LANL fall 1988, leaving comment cards for easy
c                    reconversion to the VAX.  Encode and decode
c                    statements removed by changing many variables to
c                    character strings, January 1989.
c               This version (Mod 11, 1992) has commons modified so that a
c                    common of given name has the same length in all
c                    routines.  New timing subroutine seconds coded
c                    with alternative sections available for CRAY, VAX 
c                    or Macintosh, SUN, and IBM System/6000 RISC.
c               August 1995, code changed to write on unit 41 only non-
c                    zero coefficient matrix elements instead of entire
c                    upper triangle of coefficient matrix--ditto on tape2e.
c                    (With algorithm used for illp, kmx is limited to 9999.)
c                    Also, in calcv and rceinp, fixed bugs when a 1 x 1 
c                    matrix is present.
c               -------------------------------------------------------
c               NOTE: BACKSPACE commands in this program may cause
c                    difficulties on the IBM RISC (backspaces of long
c                    unformatted records not effective) if FORTRAN
c                    compiler versions earlier than 2.02 are used.
c                         Also, DECfortran version 3.0 is inadequate,
c                    and version 3.2 is required.
c                         Very time-consuming backspaces in subroutine 
c                    RCEINP replaced May 1993 by rewind and
c                    reads forward.
c               -------------------------------------------------------
c               Vers. 11.1 May 1996, previously-used fixed numerical dimensions
c                    for U2, ... U6, V2, ...V6, have been replaced by variables
c                    defined in parameter statements, and subroutine ckdim
c                    added to dynamically check in each run the adequacy of
c                    dimensions of these variables and those of CFP1, CFP2,
c                    CFGP1, and CFGP2.
c               Vers. 11.1.1 August 1996, coding quirks in main (following 102),
c                    calcfct (dimension of fct), class1 (near start), and
c                    energy (do loop to 99), modified to allow compilation
c                    with bounds checking.
c               The values of the dimension variables used in this version 
c                    of RCG are too small to handle cfp decks for f5, f6, 
c                    f7, f8, f9, and f10.  To make possible use of these
c                    subshells (in subshell 1), make the following changes 
c                    in parameter statements throughout the program:
c                         kls1=4719
c                         kjp=1000
c                         kmx=5000        (or greater)
c                         ktran=100000     (or greater)
c                    For two-open subshell configurations, even larger 
c                    dimensions may be required, for example:
c                         kjp=1000
c                         klsp=8000
c                         kmx=5000
c                         ktran=100000   
c                                [In general, ktrans.ge.(kmx**2)/kbgks]
c                    If the f subshell is the second rather than first 
c                    subshell--e.g., for d9 f7--then it is kls2 instead
c                    of kls1 that must be changed to 119, etc.
c               -------------------------------------------------------
c                1997., a modified version to details calculate dielectronic
c              recombinationc  cross section was finished by Dong Chenzhong. 
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      parameter (kbgks=41,ktran=100000)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kiser),pci(kiser)
      dimension nparj(kc,kc),iser(kiser)
      equivalence (dumlc4,nparj),(dumlc4(kc**2+1),iser)
      common/c3lc5/goss(ktran,kbgks)
      common/c3lcd/dumlc5
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      common  dumblk(1850)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      common/c6/emin,emax,sumwt,flbdn,flbdx,fnunp,fnuxp,nlev,iewr
      common/ctkev/nptkev,ntkev,tkev(6),tunrgy(6),brnchl(6),brncht(6),
     1  eionry
      dimension cfp1(klsp1,klsp1),ddjj(kmx,1)
      equivalence (cfp1,cfgp1)
      dimension sjnk(2),sjxk(2),notkp(2)
      character*16 fil
      character*10 parnam(kpr,2),aa
      character*8 fidls(kmx,2),fidjj(kmx,2),ldes(kmx),ldesp(kmx)
      common/char/parnam,fidls,fidjj,ldes,ldesp
      common/djj/ddjj
c


c      open files
c
c          if iii=0, choose external names of input and
c               output files interactively (for vax).
c          if iii=1, use standard file names (for vax).
c          for cray and cdc computers, set iii>1 and
c               uncomment program card at start of program.
c
      iii=1
      if (iii.eq.1) go to 50
      if (iii.gt.1) go to 60
c
      write(6,*) ' input file name '
      read(5,3) fil
    3 format(a)
      open(10,file=fil,status='old')
      write(6,*) ' output file name '
      read(5,3) fil
      open(9,file=fil,status='unknown')
      write(6,*) ' file name for least-sqs. coeff. (blank, no file)'
      read(5,3) fil
      open(2,file=fil,status='unknown',form='unformatted')
      write (6,*) ' file name for least-sqs. input (blank, no file) '
      read(5,3) fil
      open(11,file=fil,status='unknown')
      go to 55
c
   50 open(10,file='ing11',status='old')
      open(888,file='autoionization.out',status='unknown')
      open(889,file='autoionization-initial.out',status='unknown')
      open(890,file='autoionization-ar.out',status='unknown')
      open(8,file='di.out',status='unknown')
      open(16,file='ds.out',status='unknown')
      open(9,file='outg11',status='unknown')
      open(2,file='tape2e',status='unknown',form='unformatted')
      open(11,file='outgine',status='unknown')
   55 open(20,status='scratch',form='unformatted')
      open(31,status='scratch',form='unformatted')
      open(32,status='scratch',form='unformatted')

      open(41,status='scratch',form='unformatted')
      open(72,file='tape72',status='unknown',form='unformatted')
      open(73,file='tape73',status='unknown',form='unformatted')
      open(74,file='tape74',status='unknown',form='unformatted')
      open(3,status='scratch')
      open(19,file='tape19',status='unknown')
      open(13,status='scratch')
      open(5,status='scratch')
cccccccccc��10.21��



      
      open(122,file='22222',status='unknown')

!added by sumg in 2007/1/3
      open(101,file='Eav.dat',status='unknown')
      open(102,file='Spec.dat',status='unknown')
      open(112,file='Spec-simpled.dat',status='unknown')
      open(103,file='wave-osci.dat',status='unknown')      
      open(104,file='config-transition.dat',status='unknown')
      open(105,file='eigenvector-matrix.dat',status='unknown')
      open(106,file='J-value.dat',status='unknown')!L6393-6419
      open(107,file='J-value-ls.dat',status='unknown')
	open(108,file='J-value-jj.dat',status='unknown')
      open(109,file='eigenJ.dat',status='unknown')
      open(110,file='eigen.dat',status='unknown')
      open(116,file='cross-in.dat',status='unknown')
      open(117,file='J-level.dat',status='unknown')
      open(118,file='emission-spec.dat',status='unknown')
      open(119,file='absor-spec.dat',status='unknown')

      open(200,file='Jenergy-totaa.dat',status='unknown')
      open(201,file='Jenergy-fwhm.dat',status='unknown')
      open(222,file='spectra.dat',status='unknown')
      open(223,file='spectra-full.dat',status='unknown')
!      open(107,file='temp.dat',status='unknown')
      open(150,file='eigenvector-matrix-cof.dat',status='unknown')
      open(151,file='J-value-Simp.dat',status='unknown')

      open(160,file='test001.dat',status='unknown')
      open(161,file='test002.dat',status='unknown')
      open(162,file='test003.dat',status='unknown')




c
c          set input and output disk unit numbers
c
   60 ir=10
      iw=9
      id2def=72
      ila=31
      ilb=32
      ic=41
c
c          calculate table of scaled factorials
c
      call calcfct
c
      ntkev=0
      nptkev=0
      delekev=0.0
      iabg=1
      iv=0
      emina=0.0
      flbdn=0.0
      flbdx=0.0
      nolskp=0
      notkp(1)=0
      notkp(2)=0
      zero=0.0
      half=0.5
      one=1.0
      thrhal=1.5
      two=2.0
      call clock(time0)
      write (iw,4)
    4 format (1h1/)
      ires=0
c
   80 read (ir,5) kcpl
      write (122,5) kcpl
    5 format (i5)
     
      backspace ir
      if (kcpl.le.2) go to 94
      if (kcpl.gt.10) go to 90
      if (kcpl.eq.3) go to 85
      write (iw,6) kcpl
      
    6 format (//30h *****control card value kcpl=,i3,11h is illegal//)
      read (ir,5)
       write (122,5)
      go to 80
c
c          Read optional first control card (kcpl.eq.3)
c               (id2.gt.0--e.g. id2=42 or 72-- if cuvfd to be called)
c
   85 read (ir,7) kcpl,ilncuv,id2t,flbdn,flbdx,delekev,eionry,nptkev,
     1  (tkev(i),i=2,6),emina
      write (122,7) kcpl,ilncuv,id2t,flbdn,flbdx,delekev,eionry,nptkev,
     1  (tkev(i),i=2,6),emina
 
    7 format (i5,i2,i3,2e5.1,2f10.5,i5,5f5.3,f10.5)
      do 87 i=1,5
   87 if (tkev(i+1).gt.0.0) ntkev=i
      tkev(1)=9999.9
      write (iw,11) eionry,iabg,iv,nptkev,(tkev(i),i=2,6),time0
      
   11 format (11h0rcg mod 11,5x,7heionry=,f10.5,
     1  7x,5hiabg=,i1,3x,3hiv=,i1,4x,6hntkev=,i1,3x,5htkev=,
     2  5f6.2,6x,5htime=,f8.2)
      if (id2t.eq.0) go to 80
      id2=id2t
c
c     call overlay(2hg9,1,0)
      call cuvfd
      ires=7
      go to 80
c
c          Read optional second control card (kcpl.gt.3)
c               (for configurations with serial no..ge.nclskp(k);
c          retain only those basis states having
c               one of the notkp(k) values of total l and s)
c
   90 read (ir,8) j,k,nolskp,(muls1(i),lhs1(i),i=1,nolskp)
      write (122,8) j,k,nolskp,(muls1(i),lhs1(i),i=1,nolskp)
	  
    8 format (i4,i1,i5,14(i4,a1))
      nclskp(k)=j
      notkp(k)=nolskp
      if (ires.eq.7) write (iw,4)
      ires=0
      if (nolskp.le.0) go to 80
      write (iw,9) k,j,(muls1(i),lhs1(i),i=1,nolskp)
    9 format (11h for parity,i2,19h and configs. with ,
     1  14hserial no..ge.,i3,18h, keep only terms ,14(i3,a1))
      do 92 i=1,nolskp
      eras=muls1(i)
      scrskp(i,k)=0.5*(eras-1.0)
      do 91 j=1,24
      if (lhs1(i).ne.lsymb(j)) go to 91
      scrlkp(i,k)=j-1
      go to 92
   91 continue
   92 continue
      go to 80
c
   94 if (id4.gt.0) go to 95
      id2=id2def
      id3=id2+1
      id4=id3+1
   95 if (flbdn.le.0.0) flbdn=0.001
      if (flbdx.le.flbdn) flbdx=500000.0
      if (delekev.le.0.0) delekev=0.00025
c
c          Read final control card (or rescale card if kcpl=0).
c
c          Read kind of coupling kcpld(i)(1=ls, or 2=jj),
c               number of sub-shells in each configuration, and
c               number of configurations (for each parity).
c          If iabg.ge.1, parameters alpha, beta, gamma are included
c               for equivalent electrons (also t for d2-d8, and
c               t1 and t2 for d3-d7).  If iabg=2 or 4, then illegal-k
c               parameters are included for non-equivalent electrons.
c               If iabg.ge.3, then SL coupling is used instead of LS.
c          If eav=-55555555., input for least-squares energy-level-fitting
c               program RCE is written on tape 2.
c          If ictbcd.gt.0, input for Argonne least-squares program
c               is written on tape 19.  (Tapes 2 and 19 cannot
c               both be written in the same run.)
c          If ictbcd.lt.0, input for Zeeman Laboratory least-squares
c               program (KONFIT) is written on tape 5 (=tape 19).
c          If igen=kcpld(3).ge.5, plane-wave-Born collision
c               strengths will be calculated (igen=9 gives minimum print).
c               Values of kcpl(4)-(5) and (6)-(7) must be set appropriately
c               for minimum and maximum values of the multipole index,
c               for parity conserving and changing excitations, respectively.
c
      coupl1=coupl(1)
c     ks=8
c     kc=50
      irw19=0
      rewind 2
      iscale=0
      deleav=0.0
      uenrgy=0.0
      fact0(1)=0.0
      fact0(2)=0.0
      fact0(3)=0.0
      fact0(4)=0.0
      fact0(5)=0.0
      texcit=0.0
      if (kcpl.eq.0) go to 101
c
  100 read (ir,10) kcpl,nck,nocset,nsconf,iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld,ielpun,sjnk(1),sjxk(1),sjnk(2),sjxk(2),imag,iquad,ueninp,
     2  dmin,ilncuv,iplev,icpc,icfc,idip, iengyd,ispecc,
     3  iw6,ipct,ictc,ictbcd
      write(122,10) kcpl,nck,nocset,nsconf,iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld,ielpun,sjnk(1),sjxk(1),sjnk(2),sjxk(2),imag,iquad,ueninp,
     2  dmin,ilncuv,iplev,icpc,icfc,idip, iengyd,ispecc,
     3  iw6,ipct,ictc,ictbcd

   10 format (i5,i1,2i2,i1,2i2,i1,2i2,2i1,i3,i2,i3,
     1  9i1,i1,4f2.1,2i1,f10.5,   e5.1,5i1, 2i1,   4i2)
      if (kcpl.lt.0) stop '(normal exit)'
      if (ueninp.le.0.0) ueninp=1000.0
      if (kcpl.gt.0) go to 104
c          If (kcpl.eq.0) interpret as a rescale card.
      backspace ir
  101 read (ir,12) deleav,kcpld,ielpun,ueninp,texcit
!      write(122,12) deleav,kcpld,ielpun,ueninp,texcit
   12 format (20x,f10.5,10i1,10x,f10.5,f5.2)
      iscale=0
      if (ueninp.le.0.0) go to 102
      iscale=7
      uenrgy=ueninp
  102 i=0
      do 103 j=1,5
      i=i+2
      if (j.lt.5) eras=10*kcpld(i-1)+kcpld(i)
      if (j.eq.5) eras=10*kcpld(9)+ielpun
      if (eras.ge.98.5) eras=100.0
      if (eras.gt.0.0.and.eras.lt.1.5) eras=0.1
  103 fact0(j)=eras/100.0
      go to 100
c
  104 if (nsconf(2,1).le.kc.and.nsconf(2,2).le.kc) go to 105
      write (iw,13) nsconf(2,1),nsconf(2,2),kc
   13 format (' no. of configurations=',2i4,' greater than dim. kc=',i2)
      stop '(too many configurations)'
  105 if (iscale.eq.0) uenrgy=ueninp
      scale=ueninp/uenrgy
      if (nlt11.eq.0) nlt11=119
      if (nevmax.eq.0) nevmax=500
      if (nocset.ne.0.and.nlsmax.ne.0) nlsmax=500
      if (ielpun.eq.2) ictbcd=0
      if (sjxk(1).le.0.0) sjxk(1)=99.0
      if (sjxk(2).le.0.0) sjxk(2)=99.0
      if (nolskp.eq.0.and.sjxk(1)+sjxk(2).ne.198.0) nolskp=-7
      if (nolskp.eq.0) go to 106
c     kcpl=1
c     kcpld(2)=1
c     nlsmax=0
  106 if (iengyd.eq.0) iengyd=500
      if (iengyd.eq.2) iengyd=(nevmax+10)/11
      igdlev=0
      if (ispecc.eq.0) igdlev=7
      if (igdlev.ne.0) ispecc=8
      iplotc=0
      if (ispecc.eq.0) iplotc=1
      igen=kcpld(3)
      if (igen.ge.5) go to 110
      irnq=2
      irxq=2
      irnd=1
      irxd=1
      go to 120
  110 irnq=kcpld(4)
      irxq=max0(irnq,kcpld(5))
      irnd=max0(1,kcpld(6))
      irxd=max0(irnd,kcpld(7))
      if (nsconf(2,2).le.0) iquad=1
      dmin=0.0
      ispecc=1
      ntkev=0
      nptkev=0
      if (nck(1).le.0) nck(1)=1
  120 if (nck(1).eq.0) nck(1)=kc
      if (nck(2).eq.0) nck(2)=kc
      call clock(time0)
      coupl(1)=coupl1
      if (iabg.ge.3) coupl(1)=coupl(12)
c        NOTE---The SL-coupling option concerns only (scrs4,scrl4)scrj8.
c               The JJ, JK, etc. representations still use (Li,Si)Ji.
      if (ires.eq.7) write (iw,4)
      ires=7
      write (iw,15) coupl(kcpl),nsconf,iabg,iv,nlt11,kcpld,sjxk,
     1  ilncuv,iplev,icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd

   15 format (11h0rcg mod 11,a6,9h coupling,4x,7hnsconf=,3i2,3x,
     1  2i2,i3,4x,5hiabg=,i1,3x,3hiv=,i1,2x,i4,1x,9i1,2f5.1,2x,
     2  6hprint=,5i1, i4,4i2)
      if (iw6.lt.0)
     1  write (6,15) coupl(kcpl),nsconf,iabg,iv,nlt11,kcpld,sjxk,
     2  ilncuv,iplev,icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd
      if (ictbcd.lt.0) rewind 5
      if (ictbcd.le.0.and.ielpun.lt.2) go to 180
      if (irw19.ne.0) go to 180
      rewind 19
      irw19=7
  180 if (nocset.eq.0) go to 200
      ictbcd=0
      if (nocset.lt.0) go to 200
  182 read (2) nocdes,nscrj8,npar,j1x
      npar=npar-j1x+1
      do 183 n=1,nscrj8
      read (2) l
      do 183 m=1,npar
  183 read (2) a
      if (nocdes.ne.nocset) go to 182
      go to 100
c
c          Calc. level designations and coefficient matrices
c
c 200 call overlay(2hg9,2,0)
  200 call lncuv
      call clock(time)
      delt=time-time0
      write (iw,25) delt
   25 format (/19h0finished lncuv at ,f6.3,4h min)
      if (iw6.lt.0) write (6,1025) delt
 1025 format (/19h finished lncuv at ,f6.3,4h min)
c
      il=ila
      rewind ic
      noicwr=0
      k=1
c
  400 kk=k
      noic(k)=noicwr
      noicmup(k)=0
      nolskp=notkp(k)
      do 410 i=1,ks
      ll(i)=llijk(i,1,k)
  410 fll(i)=fllijk(i,1,k)
      nosubc=nsconf(1,k)
      sjn=sjnk(k)
      sjx=sjxk(k)
      if (ictc.ne.0) go to 450
c     call overlay(2hg9,3,0)
      call plev
      call clock(time)
      delt=time-time0
      write (iw,26) delt
   26 format (/19h0finished plev at  ,f6.3,4h min/1h1)
      if (iw6.lt.0) write (6,1026) delt   
 1026 format (19h finished plev at  ,f6.3,4h min)
c     call overlay(2hg9,4,0)
      call pfgd
      call clock(time)
      delt=time-time0
      if (iw6.lt.0) write (6,1027) delt
 1027 format (19h finished pfgd at  ,f6.3,4h min)
      if (nsconf(1,2).eq.0.and.icpc.eq.9) go to 100
      if (nsconf(2,k).le.1) go to 430
c     call overlay(2hg9,5,0)
      call prk
      call clock(time)
      delt=time-time0
      if (iw6.lt.0) write (6,1028) delt
 1028 format (18h finished prk at  ,f7.3,4h min)	  
  430 nopc=25
      npar1=-7
      j1=1
      write (20) npar1,kpar,k,i,j,aa,cave,j1,nopc, (pc(n1), n1=1,nopc)
      rewind 20
      j1x=nsconf(2,k)
      notsx=0
      do 440 i=1,nosubc
  440 notsx=max0(notsj1(i,j1x+1),notsx)
      rewind il
      ilc=il
      do 442 nn=1,2
      write (ilc) notsj1,nscrj8,sj8mn,sj8mx,npar,nparj,parnam,
     1  notsx, ((fl(l,i),s(l,i), l=1,notsx), i=1,nosubc),nalsjp,pj
  442 ilc=ic
      noicwr=noicwr+1
c     call overlay(2hg9,6,0)
c          write (6,2468) noicwr,noicmup
c2468 format (' noicwr,noicmup=',i5,2x,2i5)
      call calcfc
      call clock(time)
      delt=time-time0
      if (iw6.lt.0) write (6,1029) delt
 1029 format (19h finished calcfc at,f6.3,4h min)	  
c          Write (6,2468) noicwr,noicmup
      iarg1=0
      iarg2=il
      iarg3=il
      irmn=1
      irmx=1
c     if (imag.eq.k.or.imag.gt.2) call overlay(2hg9,7,0)
      if (imag.eq.k.or.imag.gt.2) call mupole
c          Write (6,2468) noicwr,noicmup
      iarg1=2
      irmn=irnq
      irmx=irxq
c     if (iquad.eq.k.or.iquad.gt.2) call overlay(2hg9,7,0)
      if (iquad.eq.k.or.iquad.gt.2) call mupole
c          Write (6,2468) noicwr,noicmup
  450 rewind il
      if (il.eq.ilb) go to 500
      if (nsconf(1,2).le.0) go to 600
      il=ilb
      k=2
      go to 400
c
  500 iarg1=iiprty
      iarg2=ila
      iarg3=ilb
      irmn=irnd
      irmx=irxd
      if (ictc.ne.0) go to 600
c     call overlay(2hg9,7,0)
      call mupole
c          Write (6,2468) noicwr,noicmup
c
c          Calculate energy levels and spectra
c
c 600 call overlay(2hg9,8,0)
  600 call energy
      rewind ila
      rewind ilb
      go to 100
c
      end
      block data
 
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      parameter (kbgks=41,kenrgs=21,kcase=50,ktran=100000,klam=10000)
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      dimension ddjj(kmx,1)
      character*10 parnam(kpr,2)
      character*8 fidls(kmx,2),fidjj(kmx,2),ldes(kmx),ldesp(kmx)
      common/char/parnam,fidls,fidjj,ldes,ldesp
      common/djj/ddjj
      common/pwborn/nbigks,nenrgs,ekminl,ekmaxl,delekl,bigks(kbgks),
     1  xmin,xmax,tev(25),corr(kenrgs),ibk,ipwr,i11
c
      data parnam(1,1),parnam(1,2)/'eav       ','eav       '/
      data (coupl(i),i=1,12)/6h    ls,6h    jj,6h  jjjk,6h  lslk,
     1  6h  lsjk,6hlsjlks,6hlsjlsj,6hj1-lsj,1h ,1h ,1h ,6h    sl/
      data (lsymb(i),i=1,24)/1hs,1hp,1hd,1hf,1hg,1hh,1hi,
     1  1hk,1hl,1hm,1hn,1ho,1hq,1hr,1ht,1hu,1hv,1hw,
     2  1hx,1hy,1hz,1ha,1hb,1hc/
      data tev/1.0,1.5,2.0,3.0,5.0,7.0,10.0,15.0,20.0,30.0,
     1  50.0,70.0,100.0,150.0,200.0,300.0,500.0,700.0,1000.0,
     2  1500.0,2000.0,3000.0,5000.0,7000.0,10000.0/
      end
      function cijkf(a,b,c)
c
      implicit real*8 (a-h,o-z)
c
      d=s3j0sq(a,b,c)
      d=sqrt((2.0*a+1.0)*(2.0*b+1.0)*d)
      two=2.0
      if (mod(0.5*(b+c-a),two).ne.0.0) d=-d
      cijkf=d
      return
      end
      subroutine locdsk(idsk,flldes,nides)
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
c
      rewind idsk
  100 read (idsk,end=250) lld,nid,flld,not,nlt,norcd
      if (flld.eq.flldes.and.nid.eq.nides) go to 300
      do 200 nn=1,norcd
  200 read (idsk)
      go to 100
  250 l=flldes
      write (iw,25) lsymb(l+1),nides,idsk
      if (iw6.lt.0) write (6,25) lsymb(l+1),nides,idsk
   25 format (' *****data for  ',a1,i2,'  not present on disk unit ',i2)
      stop 'Required cfp deck not present in calculation of disks 72-74'
  300 return
      end
      subroutine sprin
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2a/sj8k(2),notsjp(ks,100),ncfgp(kmx),nalsp(kmx,ks)
      common/c3a/isubj(kc),muls(ks),lhs(ks),
     1  nals(kmx,ks),ncfg(kmx),nalsj(kmx,ks),scrl(kmx,ks),scrs(kmx,ks),
     2  fj(kmx,ks),scrj(kmx,ks), mul(ks),lh(ks),lf(klsp),nsjk(110),
     3  fk(kmx),fkj(kmx),scrl6(kmx),scrs6(kmx),fk6(kmx),lhqq(kmx),
     4  multqq(kmx),nalsjp(kjp,ks),pj(kjp,ks),noicrd
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      common       c(kmx,kmx)
      common/c3lc2/tmx(kmx,kmx)
      common/c3lc3/ct4(kmx,kmx)
      common/c3lc4/vect(kmx,kmx)
      common/c3lcd/dumlc5
      common    elem(3,kc,2),vpar(kpr,2),avp(9,2),aveig(2),avcg(2),
     1  npark(2),npav(kc),    eig(kmx),elem1(3),fnt(9,2),i1,i2,
     2  ifact(4),fact(4),lcser(kmx),x(kmx)
      dimension tmxp(kmx,kmx),ddjj(kmx,1)
      equivalence (vect,tmxp)
      character*10 parnam(kpr,2)
      character*8 fidls(kmx,2),fidjj(kmx,2),ldes(kmx),ldesp(kmx)
      character*8 idelem(11)
      common/char/parnam,fidls,fidjj,ldes,ldesp
      common/djj/ddjj
      data blank/6h      /
c
c
c          Print coef, mupole, energy, or eigenvector matrix.
c               If necessary, transform and print again.
c               For mupole elements, also print squares.
c          kpar=-1,0,+1,+2 for fk,gk,zeta,mupole,respectively.
c          kpar=-2 for rk
c          kpar=+3,+4 for energy or eigenvector matrix, respectively.
c
c
c     ks=8
      k=kk
      j1x=nsconf(2,k)
      jab=max0(j1b-j1a,1)
      itest=0
  100 if (kpar-2) 101,108,108
  101 if (icfc.eq.3.and.kpar.ne.-2) itest=1
      if (icfc.eq.4.and.kpar.eq.-2) itest=1
      if (icfc.gt.4) itest=1
      if (itest.gt.0) write (iw,10)
   10 format (1h2)
  108 ip=1
      kcpl1=1
      if (kpar-1) 121,115,170
  115 kcpl1=kcpl
      go to 121
c
  120 if (kpar-1) 121,121,170
  121 nlsp=nls
      if (itest.eq.0) go to 200
      write (iw,14) parnam(npar,k),cave,coupl(kcpl1),scrj8,
     1  (jn, (llijk(l,jn,k),nijk(l,jn,k), l=1,ks), jn=j1a,j1b,jab)

   14 format (1h0,a10,6x,5hcave=,f9.5,10x,a6,9h coupling,8x,2hj=,f4.1,
     1  10x,6hconfig,i3,8(2x,a1,i2)/84x,i3,8(2x,a1,i2))
      write (iw,15)
   15 format (1h0)
      go to 200
  170 if (kpar-3) 171,180,190
  171 ip=2
      i12=1
      jx=max0(nsconf(2,i1),nsconf(2,i2))
      jxm1=min0(jx-1,8)
      if (idip.eq.0) go to 200
      if (idip.gt.1) write (iw,10)
  172 do 174 j=1,jx
      if (j.gt.jxm1.and.j.lt.jx) go to 174
      write (iw,16) i12,ix, j,(llijk(l,j,i1),nijk(l,j,i1),l=1,ks),scrj8,
     1  j,(llijk(l,j,i2),nijk(l,j,i2), l=1,ks),scrj8p,coupl(kcpl1)

  174 continue
   16 format (7h mup mx,i3,4h ii=,i1,i3,8(2x,a1,i2),3x,2hj=,
     1  f4.1,4h ---,i3,8(2x,a1,i2),3x,3hjp=,f4.1,2x,a6,4h cpl)
      write (iw,15)
      go to 200
c
  180 kcpl1=kcpl
      nlst=nls
      if (iengyd.gt.2) nls=min0(nls,11*iengyd)
      nlsp=nls
      jxj=j1x
      i=5
      if (iengyd.lt.200) i=1
      if (scrj8.ne.sj8mn) jxj=min0(jxj,i)
      write (iw,18)  coupl(kcpl1),scrj8,   ((elem(i,jn,k), i=1,3),
     1  jn, (llijk(l,jn,k),nijk(l,jn,k), l=1,ks), jn=1,jxj)
c-------���
!      write (105,18)  coupl(kcpl1),scrj8,   ((elem(i,jn,k), i=1,3),
!     1  jn, (llijk(l,jn,k),nijk(l,jn,k), l=1,ks), jn=1,jxj)
   18 format (15h1 energy matrix,4h   (,a6,9h coupling,1h),7x,
     1  2hj=,f4.1,7x,3a6,5x,6hconfig,i3,8(2x,a1,i2)/
     2  (55x,3a6,11x,i3,8(2x,a1,i2)))
      if (jxj.lt.j1x) write (iw,13)
     1  (elem(i,j1x,k),i=1,3), j1x,(llijk(l,j1x,k),nijk(l,j1x,k),l=1,ks)
   13 format (55x,3a6,11x,i3,8(2x,a1,i2))
      write (iw,15)
      if (iengyd-2) 500,200,200
c
  190 kcpl1=kcpl
      nlsp=nls
  191 if (kcpl1-1) 196,192,196
c                Calculate g-factors
  192 m=nosubc
      if (scrj8.le.0.0) go to 196
      do 193 l=1,nls
  193 ct4(l,1)=0.50116*(scrs(l,m)**2+scrs(l,m)-scrl(l,m)**2-scrl(l,m))/
     1     (scrj8**2+scrj8)+1.50116
      do 194 n=1,nls
      ct4(n,2)=0.0
      do 194 l=1,nls
  194 ct4(n,2)=ct4(n,2)+ct4(l,1)*(c(l,n)**2)
      write  (iw,20) (ct4(n,2), n=1,nls)
   20 format (//11h   g-values/(28x,11f9.3))
  196 if (kcpld(kcpl1).gt.0) go to 281
      write (iw,19) coupl(kcpl1)
   19 format (//15h   eigenvectors,4h   (,a6,9h coupling,1h)/)
c
  200 if (kpar-2) 201,202,205
  201 if (itest) 282,282,205
  202 if (idip-1) 282,282,205
  205 lx=0
  210 ln=lx+1
c      lx=lx+11
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      lx=lx+1000
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      if (lx-nlsp) 212,212,211
  211 lx=nlsp
  212 if (kpar-4) 213,245,245
  213 if (kpar.eq.2) go to 215
      write (iw,24) (ncfg(l), l=ln,lx)
      go to 216
  215 write (iw,24) (ncfgp(l), l=ln,lx)
  216 if (kcpl1-1) 230,220,230
  220 write (iw,22) (fidls(l,ip), l=ln,lx)
   22 format (28x, 11(2x,a7,:))
      go to 240
  230 write (iw,23) (fidjj(l,ip), l=ln,lx)
   23 format (28x, 11(1x,a8,:))
  240 write (iw,24) (l, l=ln,lx)
   24 format (26x,11i9)
      if (kpar-3) 250,290,245
  245 write (iw,24)
      if (kcpl1.ne.kcpl) go to 248
      do 246 l=ln,lx
      n=lcser(l)
c 246 encode (8,28,idelem(l-ln+1)) elem(2,n,k),elem(3,n,k)
  246 write (idelem(l-ln+1),28) elem(2,n,k),elem(3,n,k)
   28 format (a6,a2)
      n=(ln+11)/11
      write (iw,25) n, (idelem(l-ln+1),l=ln,lx)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      write (105,25) n, (idelem(l-ln+1),l=ln,lx)
   25 format (i21,9x,400(a8,1x))
!      write (150,25) n, (idelem(l-ln+1),l=ln,lx) !SuMG 20120822
      write (iw,29) (ldes(l),l=ln,lx)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      write (105,29) (ldes(l),l=ln,lx)
!	write (150,2900) (ldes(l),l=ln,lx) !SuMG 20120822
! 2900 format (13x,400(a8,1x,:))          !SuMG 20120822
   29 format (30x,400(a8,1x,:))
  248 if (ln.gt.nevmax) go to 281
c
c          Print coef, dipole, or eigenvector matrix
c
  250 do 280 l=1,nls
      n=ncfg(l)
      d=elem(2,n,k)
      e=elem(3,n,k)
      if (kpar.gt.2) go to 255
      d=blank      
      e=d
  255 if (kcpl1-1) 260,260,270
  260 write (iw,26) n,d,e, fidls(l,1), l, (c(l,lp), lp=ln,lx)
      write (105,26) n,d,e, fidls(l,1), l, (c(l,lp), lp=ln,lx)
	write (150,2600) (c(l,lp), lp=ln,lx)      !SuMG 20120822
 2600 format (1000f9.5)                              !SuMG 20120822
   26 format (i3,1h:,2a6, 1x,a7, i3,1x,1000f9.5)
      go to 280
  270 write (iw,27) n,d,e, fidjj(l,1), l, (c(l,lp), lp=ln,lx)
!!!!!!!!!!!!!!!!!!!!!! Print coef, dipole, or eigenvector matrix------L877
      write (105,27) n,d,e, fidjj(l,1), l, (c(l,lp), lp=ln,lx)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   27 format (i3,1h:,2a6, 1x,a8, i3,1000f9.5)
  280 continue
      if (lx-nlsp) 210,281,281
  281 write (iw,27)
      if (kpar-4) 282,283,283
  282 if (kcpl1-kcpl) 300,400,300
  283 if (nls-1) 288,288,1283
 1283 pur=0.0
      do 286 n=1,nls
      ct4(n,1)=0.0
      do 285 l=1,nls
      eras=c(l,n)**2
      if (eras-ct4(n,1)) 285,285,284
  284 ct4(n,1)=eras
  285 continue
  286 pur=pur+ct4(n,1)
      fnls=nls
      avp(kcpl1,k)=avp(kcpl1,k)+pur
      fnt(kcpl1,k)=fnt(kcpl1,k)+fnls
      pur=pur/fnls
      nnn=min0(nls,nevmax)
	write (iw,30) pur, (ct4(n,1), n=1,nnn)
!     print purity Ln902
c      write (105,30) pur, (ct4(n,1), n=1,nnn)
   30 format (13x,8h purity=,f5.3,2x,11f9.5/(28x,11f9.5))
  288 if (nolskp.ne.0) go to 398
      if (kcpl1-kcpl) 400,289,400
  289 if (nls-1) 400,400,300
c
c          Print energy matrix
c
  290 eras=c(1,1)
      do 298 l=1,nls
      n=ncfg(l)
      d=elem(2,n,k)
      e=elem(3,n,k)
      if (kcpl1-1) 291,291,295
  291 if (eras.gt.9999.0) go to 292
      write (iw,31) n,d,e, fidls(l,1), l, (c(l,lp), lp=ln,lx)
c	   write (105,31) n,d,e, fidls(l,1), l, (c(l,lp), lp=ln,lx)
   31 format (i3,1h:,2a6, 1x,a7, i3,1x,11f9.3)
      go to 298
  292 write (iw,32) n,d,e, fidls(l,1), l, (c(l,lp), lp=ln,lx)
   32 format (i3,1h:,2a6, 1x,a7, i3,1x,11f9.2)
      go to 298
  295 if (eras.gt.9999.0) go to 296
      write (iw,33) n,d,e, fidjj(l,1), l, (c(l,lp), lp=ln,lx)
   33 format (i3,1h:,2a6,  1x,a8, i3,11f9.3)
      go to 298
  296 write (iw,34) n,d,e, fidjj(l,1), l, (c(l,lp), lp=ln,lx)
   34 format (i3,1h:,2a6,  1x,a8, i3,11f9.2)
  298 continue
      if (lx.ge.11*iengyd) go to 299
      if (lx-nlsp) 210,299,299
  299 write (iw,34)
      nls=nlst
      go to 500
c
c          Transform matrix
c
  300 if (kcpl1-1) 305,305,355
  305 do 320 l=1,nls
      do 320 lp=1,nlsp
      ct4(l,lp)=0.0
      do 310 l0=1,nls
  310 ct4(l,lp)=ct4(l,lp)+tmx(l0,l)*c(l0,lp)
  320 continue
      if (kpar-2) 331,321,396
  321 do 330 l=1,nls
      do 330 lp=1,nlsp
      c(l,lp)=0.0
      do 325 l0=1,nlsp
  325 c(l,lp)=c(l,lp)+ct4(l,l0)*tmxp(l0,lp)
  330 continue
      go to 395
  331 do 340 l=1,nls
      do 340 lp=1,l
      c(l,lp)=0.0
      do 335 l0=1,nls
  335 c(l,lp)=c(l,lp)+ct4(l,l0)*tmx(l0,lp)
  340 c(lp,l)=c(l,lp)
      go to 395
c
  355 do 370 l=1,nls
      do 370 lp=1,nlsp
      temp=0.0
      if (iabs(kpar).gt.1) go to 356
      if (ncfg(l).ne.ncfg(lp)) go to 365
  356 do 360 l0=1,nls
      eras=tmx(l,l0)
      if (eras.eq.0.0) go to 360
      temp=temp+eras*c(l0,lp)
  360 continue
  365 ct4(l,lp)=temp
  370 continue
      if (kpar-2) 381,371,397
  371 do 380 l=1,nls
      do 380 lp=1,nlsp
      c(l,lp)=0.0
      do 375 l0=1,nlsp
  375 c(l,lp)=c(l,lp)+ct4(l,l0)*tmxp(lp,l0)
  380 continue
      go to 395
  381 do 390 l=1,nls
      do 389 lp=1,l
      temp=0.0
      if (iabs(kpar).gt.1) go to 383
      if (ncfg(l).ne.ncfg(lp)) go to 386
  383 do 385 l0=1,nls
      eras=tmx(lp,l0)
      if (eras.eq.0.0) go to 385
      temp=temp+ct4(l,l0)*eras
  385 continue
  386 c(l,lp)=temp
  389 c(lp,l)=temp
  390 continue
c
  395 if (kpar.lt.2.and.itest.gt.0) write (iw,35)
      if (kpar.eq.2.and.idip.gt.1) write (iw,35)
   35 format (1h0)
      kcpl1=kcpl
      go to 120
  396 kcpl1=2
      go to 398
  397 kcpl1=1
c               Store eigenvectors in coupling kcpl
  398 do 399 l=1,nls
      do 399 lp=1,nls
      vect(l,lp)=c(l,lp)
  399 c(l,lp)=ct4(l,lp)
      if (nolskp.eq.0) go to 191
c
  400 if (kpar-2) 500,405,500
  405 if (i12-2) 410,500,500
  410 write (ic) scrj8,scrj8p,nls,nlsp, ((c(l,lp),l=1,nls), lp=1,nlsp),
     1  ncfg,ncfgp
      noicwr=noicwr+1
      noicmup(kk)=noicmup(kk)+1
      if (idip.eq.0) go to 500
      do 430 l=1,nls
      do 430 lp=1,nlsp
  430 c(l,lp)=c(l,lp)**2
      write (iw,35)
      i12=2
      go to 172
c
  500 if (kpar.lt.2.and.itest.eq.0) go to 600
      call clock(time)
      delt=time-time0
c      write (iw,50) delt
   50 format (11x,'time=',f6.3,4h min)
      if (kpar.eq.2.and.iw6.lt.0) write (6,51) scrj8,scrj8p,delt,
     1  nls,nlsp
   51 format (' finished mupole matrix for  j=',f3.1,'  and jp=',
     1   f3.1,'  at time=',f6.3,4h min,',     matrix size=',i4,
     2   ' by ',i4)
      if (kpar.eq.4.and.iw6.lt.0) write (6,52) scrj8,delt,nls
   52 format (' finished energy for  j=',f3.1,
     1   '  at time=',f6.3,4h min,',     matrix size=',i4)
      if (kpar-4) 600,501,501
  501 continue
      call sprn37
  600 return
      end
      subroutine sprn37
c
c          Print eigenvectors in representations 3-7
c
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3a/isubj(kc),muls(ks),lhs(ks),
     1  nals(kmx,ks),ncfg(kmx),nalsj(kmx,ks),scrl(kmx,ks),scrs(kmx,ks),
     2  fj(kmx,ks),scrj(kmx,ks), mul(ks),lh(ks),lf(klsp),nsjk(110),
     3  fk(kmx),fkj(kmx),scrl6(kmx),scrs6(kmx),fk6(kmx),lhqq(kmx),
     4  multqq(kmx),nalsjp(kjp,ks),pj(kjp,ks),noicrd
      common       c(kmx,kmx)
      common/c3lc2/tmx(kmx,kmx)
      common/c3lc3/ct4(kmx,kmx)
      common/c3lc4/vect(kmx,kmx)
      common/c3lcd/dumlc5
      common    elem(3,kc,2),vpar(kpr,2),avp(9,2),aveig(2),avcg(2),
     1  npark(2),npav(kc),    eig(kmx),elem1(3),fnt(9,2),i1,i2
     2  ,ifact(4),fact(4)
c
      k=kk
  100 if (nosubc-1) 940,940,101
  101 if (nls-1) 940,940,102
  102 if (nls-nlsmax) 103,103,940
  103 kcpl1=3
      iq=nosubc
      iqm1=iq-1
      iqm2=iq-2
c
  110 if (kcpld(kcpl1)) 150,150,900
  150 read (ic) ((tmx(l,lp), lp=1,nls),  fk(l),fkj(l),scrj(l,iqm1),
     1  scrj(l,iqm2),scrl6(l),fk6(l),scrs6(l),lhqq(l),multqq(l),l=1,nls)
      noicrd=noicrd+1
c
c          Transform eigenvectors
c
  200 do 210 l=1,nls
      do 210 lp=1,nls
      c(l,lp)=0.0
      do 205 i=1,nls
  205 c(l,lp)=c(l,lp)+tmx(i,l)*vect(i,lp)
  210 continue
c
c          Print eigenvectors in new coupling
c
c      write (8,22) coupl(kcpl1)
      write (iw,22) coupl(kcpl1)
   22 format (//15h   eigenvectors,4h   (,a6,9h coupling,1h)/)
c
      lx=0
  240 ln=lx+1
      lx=lx+11
      if (lx-nls) 242,242,241
  241 lx=nls
  242 do 250 l=1,nls
      n=ncfg(l)
      d=elem(2,n,k)
      e=elem(3,n,k)
      go to (243,243,243,244,245,246,247) kcpl1
  243 write (iw,23) n,d,e,scrj(l,iqm1),fkj(l),l,(c(l,lp),lp=ln,lx)
   23 format (i3,1h=,a6,a5,f4.1,1hk,f4.1,i3,1x,11f9.5)
      write (8,23) n,d,e,scrj(l,iqm1),fkj(l),l,(c(l,lp),lp=ln,lx)
      go to 250
  244 lp1=scrl(l,nosubc)+1.0
      lhs4=lsymb(lp1)
      write (iw,24) n,d,e,lhs4,fk(l),l,(c(l,lp),lp=ln,lx)
   24 format (i3,1h=,2a6,2x,a1,f4.1,i4,1x,11f9.5)
      write (8,24) n,d,e,lhs4,fk(l),l,(c(l,lp),lp=ln,lx)
      go to 250
  245 write (iw,23) n,d,e,scrj(l,iqm1),fk(l),l,(c(l,lp),lp=ln,lx)
      write (8,23) n,d,e,scrj(l,iqm1),fk(l),l,(c(l,lp),lp=ln,lx)
      go to 250
  246 write (iw,26) n,d,e,scrj(l,iqm2),lhqq(l),fk6(l),multqq(l),l,
     1  (c(l,lp), lp=ln,lx)
   26 format (i3,1h=,a6,a5,f4.1,a1,f3.1,i2,i3,11f9.5)
      write (8,26) n,d,e,scrj(l,iqm2),lhqq(l),fk6(l),multqq(l),l,
     1  (c(l,lp), lp=ln,lx)
      go to 250
  247 write (iw,27) n,d,e,scrj(l,iqm2),multqq(l),lhqq(l),scrj(l,iqm1),
     1  l, (c(l,lp), lp=ln,lx)
   27 format (i3,1h=,a6,a5,f4.1,i2,a1,f3.1,i3,11f9.5)
      write (8,27) n,d,e,scrj(l,iqm2),multqq(l),lhqq(l),scrj(l,iqm1),
     1  l, (c(l,lp), lp=ln,lx)
  250 continue
      write (iw,23)
      write (8,23)
      if (lx.ge.nevmax) go to 300
      if (lx-nls) 240,300,300
c
c          Calculate purities
c
  300 if (nls.le.1) go to 900
      pur=0.0
      do 330 n=1,nls
      ct4(n,1)=0.0
      do 320 l=1,nls
      eras=c(l,n)**2
      if (eras-ct4(n,1)) 320,320,310
  310 ct4(n,1)=eras
  320 continue
  330 pur=pur+ct4(n,1)
      fnls=nls
      avp(kcpl1,k)=avp(kcpl1,k)+pur
      fnt(kcpl1,k)=fnt(kcpl1,k)+fnls
      pur=pur/fnls
      nnn=min0(nls,nevmax)
      write  (9,30) pur, (ct4(n,1), n=1,nnn)
   30 format (13x,8h purity=,f5.3,2x,11f9.5/(15x,11f9.5))
c
c
  900 kcpl1=kcpl1+1
      if (kcpl1-4) 110,110,910
  910 if (kcpl1-6) 920,110,921
  920 if (iq-3) 930,110,110
  921 if (kcpl1-7) 110,110,930
  930 call clock(time)
      delt=time-time0
      write (iw,93) delt
   93 format (11x,5htime=,f6.3,4h min)
  940 return
      end
      function uncpla(fj1,fj2,fj, fk,fj1p,fjp)
c
      implicit real*8 (a-h,o-z)
c
      a=sqrt((2.0*fj+1.0)*(2.0*fjp+1.0))
      two=2.0
      if (mod(fj1+fj2+fjp+fk,two).gt.0.0) a=-a
      uncpla=a*s6j(fj1,fj,fj2, fjp,fj1p,fk)
      return
      end
      function uncplb(fj1,fj2,fj, fk,fj2p,fjp)
c
      implicit real*8 (a-h,o-z)
c
      a=sqrt((2.0*fj+1.0)*(2.0*fjp+1.0))
      two=2.0
      if (mod(fj1+fj+fj2p+fk,two).gt.0.0) a=-a
      uncplb=a*s6j(fj2,fj,fj1, fjp,fj2p,fk)
      return
      end
      function recpsh(fj1,fj2,fjp,fj3,fj,fjpp)
c
      implicit real*8 (a-h,o-z)
c
      a=sqrt((2.0*fjp+1.0)*(2.0*fjpp+1.0))
      two=2.0
      if (mod(fj1+fj2+fj3+fj,two).gt.0.0) a=-a
      recpsh=a*s6j(fj1,fj2,fjp, fj3,fj,fjpp)
      return
      end
      function recpjp(fj1,fj2,fjp,fj3,fj,fjpp)
c
      implicit real*8 (a-h,o-z)
c
      a=sqrt((2.0*fjp+1.0)*(2.0*fjpp+1.0))
      two=2.0
      if (mod(fj1+fj+fjpp,two).gt.0.0) a=-a
      recpjp=a*s6j(fj1,fj2,fjp, fj3,fj,fjpp)
      return
      end
      function recpex(fj1,fj2,fjp,fj3,fj,fjpp)
c
      implicit real*8 (a-h,o-z)
c
      a=sqrt((2.0*fjp+1.0)*(2.0*fjpp+1.0))
      two=2.0
      if (mod(fj2+fj3+fjp+fjpp,two).gt.0.0) a=-a
      recpex=a*s6j(fj2,fj1,fjp, fj3,fj,fjpp)
      return
      end
      subroutine clock(time)
c
      implicit real*8 (a-h,o-z)
      call seconds(t)
      time=t/60.0
      return
      end
      subroutine seconds(t)
c
c          Timing routine (results for information only).
c               For other machines, set t=0.0 or add
c               appropriate code.
c
      real*8 t
      real etime,t1,t2
      dimension t2(2)
C      call dostim(i,j,k,l)
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
      subroutine calcfct
c
c          Note: If your compiler will not accept a dimension of the
c                form (0:200), this can be changed to (200) and the
c                statement  fct(0)=1.0  removed, provided the program
c                is compiled without bounds checking (and the compiler
c                places fctz immediately in front of fct).
c
      implicit real*8 (a-h,o-z)
      common/cfactrl/scale,scalem1,fctn(200),fctz,fct(0:200)
c
      scale=8.0
      scalem1=1.0/scale
      fctz=1.0
      fctn(1)=0.0
      fct(0)=1.0
      fct(1)=1.0/scale
      do 100 i=2,70
      fctn(i)=0.0
  100 fct(i)=fct(i-1)*i/scale
      return
      end
      function s9j(a1,a2,a3,a4,a5,a6,a7,a8,a9)
c
      implicit real*8 (a-h,o-z)
c
      a9j=0.0
      a=max(abs(a1-a9), abs(a2-a6), abs(a4-a8))
      c=min(a1+a9, a2+a6, a4+a8)
      fj=2.0*a+1.0
      j1=fj
      j2=2.0*c+1.0
      if (j2.lt.j1) go to 302
      do 301 j=j1,j2,2
      a9j=a9j-((-1.0)**j)*fj*s6j(a1,a2,a3,a6,a9,a)
     1  *s6j(a4,a5,a6,a2,a,a8)*s6j(a7,a8,a9,a,a1,a4)
      a=a+1.0
  301 fj=fj+2.0
  302 s9j=a9j
      return
      end
      function s6j(fj1,fj2,fj3,fl1,fl2,fl3)
c
      implicit real*8 (a-h,o-z)
      common/cfactrl/scale,scalem1,fctn(200),fctz,fct(0:200)
c
      delsq(ia,ib,ic,id)=fct(id-ia)*fct(id-ib)*fct(id-ic)/fct(id+1)
      s6j=0.0
      s1=fj1+fj2+fj3
      s2=fj1+fl2+fl3
      s3=fl1+fj2+fl3
      is1=s1
      is2=s2
      is3=s3
      if ((s1-is1).gt.0.01) go to 200
      if ((s2-is2).gt.0.01) go to 200
      if ((s3-is3).gt.0.01) go to 200
      is4=fl1+fl2+fj3
      is5=fj1+fj2+fl1+fl2
      is6=fj2+fj3+fl2+fl3
      is7=fj3+fj1+fl3+fl1
      kn=max0(is1,is2,is3,is4)
      kx=min0(is5,is6,is7)
      if (kx.lt.kn) go to 200
      it1=2.000001*fj1
      it2=2.000001*fj2
      it3=2.000001*fj3
      it4=2.000001*fl1
      it5=2.000001*fl2
      it6=2.000001*fl3
      coef=sqrt(delsq(it1,it2,it3,is1)*delsq(it1,it5,it6,is2)
     1         *delsq(it4,it2,it6,is3)*delsq(it4,it5,it3,is4))*scalem1
      sgn=-1+2*mod(kn,2)
      sum=0.0
      do 100 k=kn,kx
      sgn=-sgn
  100 sum=sum+sgn*fct(k+1)/(fct(k-is1)*fct(k-is2)*fct(k-is3)*fct(k-is4)
     1  *fct(is5-k)*fct(is6-k)*fct(is7-k))
      s6j=coef*sum
  200 return
      end
      function s3j0sq(fj1,fj2,fj3)
c
c          Calculate square of 3-j symbol with zero magnetic quantum nos.
c
      implicit real*8 (a-h,o-z)
      common/cfactrl/scale,scalem1,fctn(200),fctz,fct(0:200)
c
      s3j0sq=0.0
      fj=fj1+fj2+fj3
      ifj=fj
      if (mod(ifj,2).ne.0) go to 100
      ia=fj-2.0*fj1
      ib=fj-2.0*fj2
      ic=fj-2.0*fj3
      if (ia.lt.0.or.ib.lt.0.or.ic.lt.0) go to 100
      b=fct(ia)*fct(ib)*fct(ic)/fct(ifj+1)
      a=fct(ifj/2)/(fct(ia/2)*fct(ib/2)*fct(ic/2))
      s3j0sq=scalem1*b*(a**2)
  100 return
      end
      function fctrl(a)                                
c                                                                    
c          calculate factorial of a                                   
c                                                                      
      implicit real*8 (a-h,o-z)
c
      fctrl=1.0                                                       
      if (abs(a)-0.1) 10, 10, 11                                      
   10 a=0.0                                                           
   11 if (a) 12, 15, 13                                                 
   12 fctrl=0.0                                                   
      go to 15                                                          
   13 imax=a+0.1                                                     
      do 14 i=1,imax                                                   
   14 fctrl=fctrl*i                                                    
   15 return                                                           
      end                                                              
      subroutine sort2(n,l,x,t,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12)
c
c         n numbers in table x are sorted numerically increasing in    
c         value. Then l tables of y are reordered to correspond to their
c         associated x. Temporary table t must be 2n words long.        
c
      parameter (klam=10000)
      implicit real*8 (a-h,o-z)
      dimension x(klam),t(2*klam),y1(klam),y2(klam),y3(klam),y4(klam),
     1  y5(klam),y6(klam),y7(klam),y8(klam),y9(klam),y10(klam),
     2  y11(klam),y12(klam)                     
      integer t,y1,y3,y4                                              
c
      if ( n.le.1 ) return                                             
      do 5 i = 1,n                                                    
    5 t(i) = i                                                          
      j = 1                                                            
    6 if (x(j).le.x(j+1)) go to 8                                      
      m = j                                                             
      eras   = x(m+1)                                                   
    7 x(m+1) = x(m)                                                    
      t(m+1) = t(m)                                                    
      m = m - 1                                                      
      if ( m.eq.0 ) go to 9                                            
      if ( x(m).gt.eras   ) go to 7                                    
    9 x(m+1) = eras                                                     
      t(m+1) = j + 1                                                 
    8 j = j + 1                                                         
      if ( j.lt.n ) go to 6                                           
c          Commence ordering of associated tables of y.                  
      if (l.eq.0) go to 100
      go to (101,102,103,104,105,106,107,108,109,110,111,112), l
  112 call order2(n,t,y12)                                            
  111 call order2(n,t,y11)                                            
  110 call order2(n,t,y10)                                           
  109 call order2(n,t,y9)                                               
  108 call order2(n,t,y8)                                             
  107 call order2(n,t,y7)                                              
  106 call order2(n,t,y6)                                              
  105 call order2(n,t,y5)                                               
  104 call orderi(n,t,y4)                                              
  103 call orderi(n,t,y3)                                           
  102 call order2(n,t,y2)                                              
  101 call orderi(n,t,y1)                                              
  100 return                                                           
      end                                                               
      subroutine orderi(n,t,y)
c
c         A table of n numbers starting at y is ordered according to a 
c         sequence table in the first n words of t. t must be integer  
c         and 2n in length.
c                                             
c          The variable y is type integer.
c
      parameter (klam=10000)
      implicit real*8 (a-h,o-z)
      dimension t(2*klam),y(klam)                                          
      integer t1,t2,t,y                                               
c
      do 1 i = 1,n                                                     
      t1 = t(i)                                                       
      t2 = n + i                                                       
    1 t(t2) = y(t1)                                                    
      do 2 i = 1,n                                                      
      t2 = n + i                                                      
    2 y(i) = t(t2)                                                     
      return                                                            
      end                                                             
      subroutine order2(n,t,y)
c
c         A table of n numbers starting at y is ordered according to a 
c         sequence table in the first n words of t. t must be integer 
c         and 2n in length.                                             
c
c          The variable y is real.
c
      implicit real*8 (a-h,o-z)
      parameter (klam=10000)
      dimension t(2*klam),y(klam),yt(klam)                                  
      integer t1,t2,t                                                  
c
      do 1 i = 1,n                                                     
      t1 = t(i)                                                        
c     t2 = n + i                                                        
      t2=i
    1 yt(t2) = y(t1)                                                    
      do 2 i = 1,n                                                      
c     t2 = n + i                                                        
      t2=i
    2 y(i) = yt(t2)                                                    
      return                                                            
      end                                                               
      subroutine orderch(n,t,y)
c
c          A table of n 8-character strings starting at y is ordered
c          according to a sequence table in the first n words of t.
c          t must be integer and 2n in length.                                         
c
c          The variable y is character*8.
c
      implicit real*8 (a-h,o-z)
      parameter (klam=10000)
      dimension t(2*klam),y(klam),yt(klam)
      character*8 y,yt
      integer t1,t2,t                                                  
c
      do 1 i = 1,n                                                    
      t1 = t(i)                                                        
c     t2 = n + i                                                     
      t2=i
    1 yt(t2) = y(t1)                                               
      do 2 i = 1,n                                                   
c     t2 = n + i                                                      
      t2=i
    2 y(i) = yt(t2)                                                  
      return                                                            
      end                    
c     overlay(g9,1,0)
      subroutine cuvfd
c
c          Read cfp from cards or tape,
c               and set up tables for u, v, fk(i,i), d(i).
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3c/cfp(klsp1,klsp1),
     1  multbr(kls1,2),lbrbcd(kls1,2),ialfbr(kls1,2),flbr(kls1,2),
     2  sbr(kls1,2),itrm(kls1),ipnt(kls1),abg(kls1,3),cavei(3),
     3  nalsji(kjp),pji(kjp),njki(25)
      common       cfpm1(klsp1,klsp1),cfp2(klsp1,klsp1)
      common pc(6100)
      common/sortdum/dum(2),idum(2)
c
      dimension cfgp(klsp1,klsp1),ua(klsp1,klsp1),va(klsp1,klsp1),
     1  uv(klsp1,klsp1),cfgpt(klsp1,klsp1)
      dimension cavedn(7),tdn(21,7),t1dn(21,3),t2dn(21,3)
      equivalence (cfp2,cfgp,ua,va),(cfpm1,cfgpt,uv)
      character*10 zetanm,abgnam(3),abgnm1,abgnm2,aa
c
      data zetanm/'zeta'/
      data (abgnam(i),i=1,3)/'alpha','beta','gamma'/
      data abgnm1,abgnm2/'alpha','1000 alpha'/
      data ialf1/1h1/
      data sortys,sortno/1h ,7hno sort/
      data cavedn/-108.88888887,-122.5,-116.66666667,-97.22222222,
     1 -70.0,-40.83333333,-15.55555555/
      data (tdn(i,1),i=1,5)/60.0,210.0,100.0,170.0,0.0/
      data (tdn(i,2),i=1,9)/60.0,210.0,30.0,130.0,210.0,52.5,
     1  34.36931771,322.5,135.0/
      data (tdn(i,3),i=1,21)/70.0,10.0,135.0,40.0,30.0,175.0,
     1  310.0,140.0,37.41657387,150.0,10.0,66.66666667,
     2  -55.27707984,248.33333333,235.0,160.0,127.2792206,
     3  190.0,0.0,0.0,640.0/
      data (tdn(i,4),i=1,21)/0.0,50.0,30.0,155.0,105.0,5.0,15.0,
     1  90.0,0.0,170.0,150.0,134.1640786,230.0,35.0,39.68626967,
     2  195.0,0.0,148.492424,275.0,225.0,320.0/
      data (tdn(i,5),i=1,21)/0.0,20.0,45.0,20.0,-30.0,125.0,
     1  80.0,70.0,-37.41657387,300.0,0.0,33.33333333,
     2  55.27707984,91.66666667,225.0,150.0,-127.2792206,
     3  360.0,0.0,0.0,0.0/
      data (tdn(i,6),i=1,9)/0.0,0.0,0.0,50.0,90.0,17.5,
     1  -34.36931771,67.5,315.0/
      data (tdn(i,7),i=1,5)/0.0,0.0,0.0,140.0,0.0/
      data (t1dn(i,1),i=1,9)/-9.0,21.0,-15.0,35.0,-21.0,0.0,
     1  -13.74772708,84.0,-141.0/
      data (t1dn(i,2),i=1,21)/0.0,-24.0,26.0,-12.0,12.0,-6.0,96.0,28.0,
     1  14.96662955,-136.0,0.0,20.0,-92.86549413,66.0,-30.0,-36.0,
     2  118.7939392,-144.0,0.0,-54.99090834,336.0/
      data (t1dn(i,3),i=1,21)/0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
     1  0.0,160.9968944,0.0,0.0,47.6235236,0.0,0.0,178.1909089,0.0,0.0,
     2  0.0/
      data (t2dn(i,1),i=1,9)/-9.0,21.0,6.136363636,-3.75,2.25,0.0,
     1  -13.74772708,-9.0,-1.5/
      data (t2dn(i,2),i=1,21)/0.0,-2.863636364,-12.75,-12.0,12.0,17.25,
     1  3.0,28.0,14.96662955,3.5,12.681818182,20.0,0.603022689,
     2  -6.568181818,-6.75,-36.0,-12.72792206,-4.5,0.0,-54.99090834,
     3  -36.0/
      data (t2dn(i,3),i=1,21)/0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
     1  27.15015068,0.0,0.0,5.031152949,0.0,0.0,47.6235236,0.0,0.0,
     2  -19.09188309,0.0,0.0,0.0/
c
c
c          Set unit numbers onto which cfp, uv, and coeffs are
c               to be written
c
      id3=id2+1
      id4=id3+1
      write (iw,8) id2,id3,id4,ilncuv
    8 format (//' cuvfd---write units',3i5,10x,'ilncuv=',i2)
      rewind id2
      rewind id3
      rewind id4
      llm1=0
      fllm1=0.0
      nim1=-7
      nim2=-7
      ntm1=1
      icpc=0
      if (ilncuv.gt.2) icpc=ilncuv
      abgnam(1)=abgnm1
      if (ictbcd.ne.0) abgnam(1)=abgnm2
      go to 120
c
c          Sset back cfp tables
c
  110 llm2=llm1
      nim2=nim1
      ntm2=ntm1
      nltm2=nltm1
      do 112 m=1,ntm1
      mult(m,3)=mult(m,2)
      lbcd(m,3)=lbcd(m,2)
      s(m,3)=s(m,2)
      fl(m,3)=fl(m,2)
  112 ialf(m,3)=ialf(m,2)
      llm1=ll(1)
      fllm1=fll(1)
      nim1=ni(1)
      ntm1=not
      nltm1=nlt
      do 115 m=1,not
      mult(m,2)=mult(m,1)
      lbcd(m,2)=lbcd(m,1)
      s(m,2)=s(m,1)
      fl(m,2)=fl(m,1)
      ialf(m,2)=ialf(m,1)
      do 115 n=1,nop
  115 cfpm1(m,n)=cfp(m,n)
c
c          Read sub-shell data, and terms to be included
c
  120 read (ir,9) ll(1),ni(1),not,nop,icuv,klast,nlt,
     1  (mult(m,1),lbcd(m,1),ialf(m,1), m=1,12), nosort
      write(122,9) ll(1),ni(1),not,nop,icuv,klast,nlt,
     1  (mult(m,1),lbcd(m,1),ialf(m,1), m=1,12), nosort
    9 format (3x,a1,3i4,2x,a1,i1,i4,4x,12(i1,a1,a2), i4)
      if (klast.eq.0) klast=0
      if (not.le.0) go to 900
      eras=sortys
      if (nosort.ne.0) eras=sortno
      if (ilncuv.eq.0) go to 122
      write (iw,10)
   10 format (1h1)
  122 if (nlt.le.12) go to 124
      read (ir,11) (mult(m,1),lbcd(m,1),ialf(m,1), m=13,nlt)
      write(122,11) (mult(m,1),lbcd(m,1),ialf(m,1), m=13,nlt)
   11 format (20(i1,a1,a2))
  124 if (nlt.gt.0) go to 126
      write (iw,12) ll(1),ni(1),not,nop,icuv,klast,nlt,eras
   12 format (/1h ,a1,i2,2i5,a1,i1,i5,5x,9hall terms,10x,a7)
      if (ilncuv.gt.0) write (iw,9)
      go to 127
  126 write (iw,13) ll(1),ni(1),not,nop,icuv,klast,nlt,
     1  (mult(m,1),lbcd(m,1),ialf(m,1), m=1,nlt)
   13 format (/1h ,a1,i2,2i5,a1,i1,i5,5x,20(i1,a1,a2,1x)/
     1  29x,20(i1,a1,a2,1x))
  127 do 128 j=1,24
      if (lsymb(j).eq.ll(1)) go to 129
  128 continue
  129 fll(1)=j-1
c
c          Read cfp table from cards
c
  140 read (ir,16) (multbr(n,2),lbrbcd(n,2),ialfbr(n,2), n=1,nop)
      write(122,16) (multbr(n,2),lbrbcd(n,2),ialfbr(n,2), n=1,nop)
   16 format (20(i1,a1,a2))
      do 141 n=1,nop
      do 141 m=1,not
  141 cfp2(m,n)=0.0
      m=0
  142 m=m+1
      it=0
  143 ito=it
      read (ir,17) mult(m,4),lbcd(m,4),ialf(m,4),it,
     1  (ipnt(j),pc(j), j=1,4)
      write(122,17) mult(m,4),lbcd(m,4),ialf(m,4),it,
     1  (ipnt(j),pc(j), j=1,4)
   17 format (i1,a1,a2,i4, 4(i3,f13.10))
      if (ito.gt.0) go to 144
      m1=mult(m,4)
      l1=lbcd(m,4)
      ia1=ialf(m,4)
  144 do 145 j=1,4
      n=ipnt(j)
      if (n.eq.0) go to 145
      cfp2(m,n)=pc(j)
  145 continue
c check card ordering
      if (m1.ne.mult(m,4)) go to 146
      if (l1.ne.lbcd(m,4)) go to 146
      if (ia1.ne.ialf(m,4)) go to 146
      if (iabs(it).eq.(ito+1)) go to 147
  146 write (iw,18) ll(1),ni(1),m1,l1,ia1,ito,mult(m,4),lbcd(m,4),
     1  ialf(m,4),it
   18 format (//35h0cuvfd 18--cfd cards out of order  ,a1,i2,i4,a1,a2,i6
     1  /34x,i4,a1,a2,i6///)
  147 if (it.gt.0) go to 143
      if (m.lt.not) go to 142
c
c          Reorder parents to correspond to terms of preceeding l(n),
c               and reorder terms with specified nlt terms first
c
  150 if (ll(1).eq.llm1.and.ni(1).eq.nim1+1) go to 155
      do 151 i=1,nop
  151 ipnt(i)=i
      go to 170
  155 do 160 n=1,nop
      do 159 m=1,ntm1
      if (multbr(n,2).ne.mult(m,2)) go to 159
      if (lbrbcd(n,2).ne.lbcd(m,2)) go to 159
      if (ialfbr(n,2).eq.ialf(m,2)) go to 160
  159 continue
      write (iw,19) multbr(n,2),lbrbcd(n,2),ialfbr(n,2),ll(1),ni(1),
     1  llm1,nim1
   19 format (//18h0cuvfd 19--parent ,i1,a1,a2,4h of ,a1,i2,
     1  27h  not found among terms of ,a1,i2)
  160 ipnt(m)=n
c
  170 if (nlt.gt.0) go to 175
      do 171 i=1,not
  171 itrm(i)=i
      nlt=not
      go to 185
  175 m=nlt
      do 180 i=1,not
      do 178 j=1,nlt
      if (mult(i,4).ne.mult(j,1)) go to 178
      if (lbcd(i,4).ne.lbcd(j,1)) go to 178
      if (ialf(i,4).eq.ialf(j,1)) go to 179
  178 continue
      m=m+1
      itrm(m)=i
      go to 180
  179 itrm(j)=i
  180 continue
      if (m.eq.not) go to 185
      write (iw,20) m,not
   20 format (//17h0cuvfd 20--m,not=,2i5)
c          Calc values of s and l
  185 do 190 m=1,not
      do 188 j=1,24
      if (lsymb(j).eq.lbcd(m,4)) go to 189
  188 continue
  189 fl(m,4)=j-1
      a=mult(m,4)-1
  190 s(m,4)=0.5*a
      do 195 n=1,nop
      do 192 j=1,24
      if (lsymb(j).eq.lbrbcd(n,2)) go to 193
  192 continue
  193 flbr(n,2)=j-1
      a=multbr(n,2)-1
  195 sbr(n,2)=0.5*a
      if (fll(1)-fllm1) 198,196,200
  196 if (ni(1).gt.nim1) go to 200
  198 write (iw,21)
   21 format (//37h0cuvfd 21--cfp decks out of order****//)
c
  200 do 202 m=1,not
      i=itrm(m)
c     decode (1,22,ialf(i,4)) n
      write (11,1021) ialf(i,4)
 1021 format (a2)
      backspace 11
      read (11,22) n
      backspace 11
   22 format (i1)
      a=n
      if (a.eq.0.0) a=9.5
  202 pc(m)=-100.0*(s(i,4)+1.0)-fl(i,4)+0.05*a
c
c          If all terms included and nosort=0, sort by s and l
c
      if (nlt.lt.not.or.nosort.ne.0) go to 203
      call sort2(nlt,1,pc(1),pc(200),itrm,dum,idum,idum,dum,dum,
     1  dum,dum,dum,dum,dum,dum)
c
  203 do 205 n=1,nop
      j=ipnt(n)
      multbr(n,1)=multbr(j,2)
      lbrbcd(n,1)=lbrbcd(j,2)
      ialfbr(n,1)=ialfbr(j,2)
      sbr(n,1)=sbr(j,2)
      flbr(n,1)=flbr(j,2)
      do 205 m=1,not
      i=itrm(m)
  205 cfp(m,n)=cfp2(i,j)
      do 210 m=1,not
      i=itrm(m)
      mult(m,1)=mult(i,4)
      lbcd(m,1)=lbcd(i,4)
      ialf(m,1)=ialf(i,4)
      s(m,1)=s(i,4)
  210 fl(m,1)=fl(i,4)
      if (ilncuv.ne.1.and.ilncuv.ne.4) go to 220
      write (iw,23) (multbr(n,1),lbrbcd(n,1),ialfbr(n,1), n=1,nop)
   23 format (//10h0cfp table//5x,10(i9,a1,a2)/(5x,10(i9,a1,a2)))
      do 218 m=1,not
  218 write (iw,24) mult(m,1),lbcd(m,1),ialf(m,1), (cfp(m,n), n=1,nop)
   24 format (1h ,i1,a1,a4,10f12.8/(2x,10f12.8))
c          Check orthonormality of cfp rows
  220 do 230 m=1,not
      do 229 m1=m,not
      sum=-1.0
      if (m.eq.m1) go to 222
      sum=0.0
      if (mult(m,1).ne.mult(m1,1)) go to 229
      if (lbcd(m,1).ne.lbcd(m1,1)) go to 229
  222 do 224 n=1,nop
  224 sum=sum+cfp(m,n)*cfp(m1,n)
      if (abs(sum).lt.1.0e-6) go to 229
      write (iw,25) mult(m,1),lbcd(m,1),ialf(m,1),
     1             mult(m1,1),lbcd(m1,1),ialf(m1,1)
   25 format (//36h0cuvfd 25--cfp not orthonormal for  ,2(i4,a1,a2)//)
  229 continue
  230 continue
c          Check orthonormality of cfp columns
      if (ni(1).eq.0) go to 250
      a=ni(1)
      b=(4.0*fll(1)+3.0-a)/a
      do 239 n=1,nop
      sum=-b*(2.0*flbr(n,1)+1.0)*(2.0*sbr(n,1)+1.0)
      do 238 n1=n,nop
      if (n.eq.n1) go to 232
      sum=0.0
      if (multbr(n,1).ne.multbr(n1,1)) go to 238
      if (lbrbcd(n,1).ne.lbrbcd(n1,1)) go to 238
  232 do 234 m=1,not
      a=(2.0*fl(m,1)+1.0)*(2.0*s(m,1)+1.0)
  234 sum=sum+a*cfp(m,n)*cfp(m,n1)
      if (abs(sum).lt.1.0e-6) go to 238
      write (iw,25) multbr(n,1),lbrbcd(n,1),ialfbr(n,1),
     1             multbr(n1,1),lbrbcd(n1,1),ialfbr(n1,1)
  238 continue
  239 continue
c
c          Read or calc cfgp (if needed) and write disk id2
c
  250 nlp=1
      nocfp=0
      if (ll(1).ne.llm1.or.ni(1).ne.(nim1+1)) go to 252
      nlp=nltm1
      nocfp=1
  252 nlgp=0
      nocfgp=0
      if (ll(1).ne.llm2.or.ni(1).ne.(nim2+2)) go to 254
      nlgp=nltm2
      nocfgp=2.0*fll(1)+1.0
  254 norcd=1+nocfp+nocfgp
      if (nocfp.gt.0) norcd=norcd+1
      if (nocfgp.gt.0) norcd=norcd+1
      write (id2) ll(1),ni(1),fll(1),not,nlt,norcd
      write (id2) (mult(m,1),lbcd(m,1),ialf(m,1),fl(m,1),s(m,1),
     1  m=1,nlt), nlp,nlgp,nocfp,nocfgp
      if (nocfp.eq.0) go to 257
      write (id2) ((cfp(m,n),m=1,nlt), n=1,nlp)
      write (id2) (mult(m,2),lbcd(m,2),ialf(m,2),fl(m,2),s(m,2),m=1,nlp)
  257 if (nocfgp.eq.0) go to 300
c
  260 write (id2) (mult(m,3),lbcd(m,3),ialf(m,3),fl(m,3),s(m,3),
     1  m=1,ntm2)
      flp=-1.0
      do 285 k=1,nocfgp
      flp=flp+1.0
      sp=0.5*(1.0+(-1.0)**k)
      mulp=2.0*sp+1.0
      iflp=flp
      lll=lsymb(iflp+1)
      a=sqrt((2.0*flp+1.0)*(2.0*sp+1.0))
      do 273 m=1,nlt
      x0=fl(m,1)+s(m,1)+1.0
      do 273 n=1,nlgp
      sum=0.0
      do 272 n1=1,nop
      b=s6j(fll(1),fll(1),flp, fl(m,1),fl(n,3),fl(n1,2))
      if (b.eq.0.0) go to 272
      b=b*s6j(half,half,sp, s(m,1),s(n,3),s(n1,2))
      if (b.eq.0.0) go to 272
      b=b*sqrt((2.0*fl(n1,2)+1.0)*(2.0*s(n1,2)+1.0))
      b=b*cfp(m,n1)*cfpm1(n1,n)
      sum=sum+b
  272 continue
      sum=sum*a
      x=x0+fl(n,3)+s(n,3)
      if (mod(x,two).gt.zero) sum=-sum
  273 cfgp(m,n)=sum
      if (ilncuv.ne.1.and.ilncuv.ne.4) go to 276
      write (iw,29) ll(1),mulp,lll, (mult(n,3),lbcd(n,3),ialf(n,3),
     1   n=1,nlgp)
   29 format (///11h0cfgp for  ,a1,2h2(,i1,a1,1h)//5x,10(i9,a1,a2)/
     1  (5x,10(i9,a1,a2)))
      do 275 m=1,nlt
  275 write (iw,24) mult(m,1),lbcd(m,1),ialf(m,1), (cfgp(m,n), n=1,nlgp)
  276 write (id2) ((cfgp(m,n),m=1,nlt), n=1,nlgp)
c          check orthonormality of cfgp rows
      if (nlgp.ne.nltm2) go to 295
      l=200
      do 280 m=1,nlt
      do 279 m1=m,nlt
      if (mult(m,1).ne.mult(m1,1)) go to 279
      if (lbcd(m,1).ne.lbcd(m1,1)) go to 279
      l=l+1
      if (k.eq.1) pc(l)=0.0
  277 do 278 n=1,nlgp
  278 pc(l)=pc(l)+cfgp(m,n)*cfgp(m1,n)
  279 continue
  280 continue
c
  285 continue
c
      l=200
      do 290 m=1,nlt
      do 289 m1=m,nlt
      if (mult(m,1).ne.mult(m1,1)) go to 289
      if (lbcd(m,1).ne.lbcd(m1,1)) go to 289
      l=l+1
      if (m.eq.m1) pc(l)=pc(l)-1.0
      if (abs(pc(l)).lt.1.0e-6) go to 289
      write (iw,30) mult(m,1),lbcd(m,1),ialf(m,1),
     1             mult(m1,1),lbcd(m1,1),ialf(m1,1)
   30 format (/37h cuvfd 30--cfgp not orthonormal for  ,2(i4,a1,a2)/)
  289 continue
  290 continue
  295 continue
c
c          Calculate number of terms of each kind
c
  300 k=0
      n2=-100
      do 310 m=1,nlt
      n1=n2
      n2=-100.0*s(m,1)-fl(m,1)
      if (n2.ne.n1) go to 309
      ntrmk(k)=ntrmk(k)+1
      go to 310
  309 k=k+1
      ntrmk(k)=1
  310 continue
      ndifft=k
c
c          Calculate number of levels of each j
c
      m=0
      do 315 j=1,nlt
      eji=abs(fl(j,1)-s(j,1))-1.0
      nji=fl(j,1)+s(j,1)-eji
      do 315 ij=1,nji
      m=m+1
      eji=eji+1.0
      nalsji(m)=j
      a=j
      pc(m)=-200.0*eji-25.0*s(j,1)-fl(j,1)+0.001*a
  315 pji(m)=eji
      ntotji=m
      call sort2(m,2,pc(1),pc(500),nalsji,pji,idum,idum,dum,dum,dum,
     1  dum,dum,dum,dum,dum)
c
      k=1
      njki(k)=1
      if (m.le.1) go to 320
      do 319 j=2,m
      if (pji(j).ne.pji(j-1)) go to 317
      njki(k)=njki(k)+1
      go to 319
  317 k=k+1
      njki(k)=1
  319 continue
  320 ndifji=k
c
c        Write u,v on disk id3, and coeffs for l(n) on disk id4
c
  400 fn=ni(1)
      nmxm1=4.0*fll(1)+1.0
      npar=0
      if (ni(1).eq.0.or.ni(1).eq.(nmxm1+1).or.fll(1).eq.0.0) go to 410
      npar=1
      if (ni(1).eq.1.or.ni(1).eq.nmxm1) go to 410
      npar=1.0+fll(1)
      if (iabg.eq.0) go to 410
      npar=1.0+fll(1)+fll(1)
      if (fll(1).ne.two) go to 410
      npar=npar+1
      if (ni(1).gt.2.and.ni(1).lt.8) npar=npar+2
  410 norcd=1+npar
      write (id4) ll(1),ni(1),fll(1),not,nlt,norcd
      write (id4) ndifft, (ntrmk(k), k=1,ndifft), ntotji,
     1  (nalsji(m),pji(m), m=1,ntotji), ndifji, (njki(m), m=1,ndifji)
      if (npar.eq.0) go to 800
      if (ni(1).eq.1) go to 500
      norcd=4.0*fll(1)+2.0
      write (id3) ll(1),ni(1),fll(1),not,nlt,norcd
c
c          Calc. u matrices
c
      nor=norcd/2
      do 485 irp1=1,nor
      k=irp1-1
      r=k
      do 435 m=1,not
      mpx=min0(m,nlt)
      do 435 mp=1,mpx
      a=0.0
      b=0.0
      if (s(m,1).ne.s(mp,1)) go to 434
      if (r.gt.(fl(m,1)+fl(mp,1))) go to 434
      if (r.lt.abs(fl(m,1)-fl(mp,1))) go to 434
      do 432 n=1,nop
      b=cfp(m,n)*cfp(mp,n)
      if (b.eq.0.0) go to 432
      b=b*s6j(fll(1),fll(1),r, fl(m,1),fl(mp,1),flbr(n,1))
      x=mod(flbr(n,1),two)
      if (x.gt.0.0) b=-b
      a=a+b
  432 continue
      a=a*sqrt((2.0*fl(m,1)+1.0)*(2.0*fl(mp,1)+1.0))*fn
      x=mod(fll(1)+fl(m,1)+r,two)
      if (x.gt.0.0) a=-a
      b=a
      x=mod(fl(m,1)-fl(mp,1),two)
      if (x.ne.0.0) b=-b
  434 ua(m,mp)=a
  435 ua(mp,m)=b
      write (id3) k, ((ua(m,mp),m=1,nlt), mp=1,nlt)
c
      if (r.eq.0.0.or.npar.le.1) go to 485
      x=mod(r,two)
      if (x.gt.0.0) go to 460
c          calc fk
  440 a=2.0*fll(1)+1.0
      cij=0.5*a*s3j0sq(fll(1),r,fll(1))
      cave=cij*fn*(fn-1.0)/(a+fll(1)+fll(1))
      cavep=cave-fn*cij
      cij=cij*a
      if (ilncuv.gt.1) write (iw,41) k,cave,ll(1),ni(1)
   41 format (//2h0f,i1,8x,5hcave=,f12.7,10x,a1,i2//)
c
      nopc=0
      mmax=0
      do 450 l=1,ndifft
      mmin=mmax+1
      mmax=mmax+ntrmk(l)
      do 450 m=mmin,mmax
      cij1=cij/(2.0*fl(m,1)+1.0)
      do 448 mp=mmin,m
      nopc=nopc+1
      a=0.0
      do 445 mpp=1,not
  445 a=a+ua(mpp,m)*ua(mpp,mp)
      pc(nopc)=cij1*a
      if (m.ne.mp) go to 448
      pc(nopc)=pc(nopc)+cavep
  448 continue
      if (icpc.eq.0) go to 450
      n2=nopc-m+mmin
      write (iw,42) nopc,mult(m,1),lbcd(m,1), (pc(n1), n1=n2,nopc)
   42 format (2i5,a1,10f11.6/(13x,10f11.6))
  450 continue
      kpar=-1
      write (aa,43) k,ll(1),ni(1)
   43 format (1hf,i1,1h(,a1,i2,4h)   )
      write (id4) kpar,k,aa,cave,nopc, (pc(n1), n1=1,nopc)
      call clock(time)
      delt=time-time0
      if (ilncuv.gt.1) write (iw,45) aa,nopc,cave,delt
   45 format (1h ,a7,7h    pc(,i4,1h),7x,5hcave=,f12.7,8x,5htime=,f6.3,
     1  4h min)
      go to 485
c          Calc. beta or gamma
  460 if (k.gt.5) go to 485
      i=(k+1)/2
      do 480 m=1,nlt
      a=0.0
      do 465 mp=1,not
  465 a=a+ua(mp,m)**2
      a=a/(2.0*fl(m,1)+1.0)
      go to (471,473,475) i
  471 abg(m,2)=3.0*a
      abg(m,3)=0.0
      go to 480
  473 abg(m,3)=abg(m,2)+7.0*a
      go to 480
  475 abg(m,2)=abg(m,2)+11.0*a
      abg(m,3)=abg(m,3)+11.0*a
  480 continue
c
  485 continue
c          Finish calculation of alpha, beta, gamma, t, t1, and t2
      if (npar.le.1.or.iabg.eq.0) go to 500
      a=4.0*fll(1)+1.0
      b=fn*(fn-a-1.0)
      cavei(2)=b/26.0
      b=b*fll(1)/a
      afact=1.0
      if (ictbcd.ne.0) afact=0.001
      cavei(1)=b*(fll(1)+1.0)*afact
      a=1.0/(2.0*fll(1)-1.0)
      cavei(3)=a*b
      do 487 m=1,nlt
      abg(m,1)=fl(m,1)*(fl(m,1)+1.0)*afact+cavei(1)
      abg(m,2)=0.25*abg(m,2)+cavei(2)
  487 abg(m,3)=a*abg(m,3)+cavei(3)
      do 488 i=1,nopc
  488 pc(i)=0.0
      k=0
      imax=fll(1)
      do 492 i=1,imax
      j=i
      aa=abgnam(j)
      if (ll(1).eq.lsymb(3).and.i.eq.2) j=3
      if (ilncuv.gt.1) write (iw,48) aa,cavei(j),ll(1),ni(1)
   48 format (//1h0,a10,5hcave=,f12.7,10x,a1,i2//)
      m=0
      nopc=0
      do 490 l=1,ndifft
      nk=ntrmk(l)
      do 490 n=1,nk
      m=m+1
      n2=nopc+1
      nopc=nopc+n
      pc(nopc)=abg(m,j)
      if (icpc.eq.0) go to 490
      write (iw,42) nopc, mult(m,1),lbcd(m,1), (pc(n1), n1=n2,nopc)
  490 continue
      write (id4) kpar,k,aa,cavei(j),nopc, (pc(n1), n1=1,nopc)
      call clock(time)
      delt=time-time0
      if (ilncuv.gt.1) write (iw,45) aa,nopc,cavei(j),delt
  492 continue
      if (fll(1).ne.2.0) go to 500
      if (ni(1).le.1.or.ni(1).ge.9) go to 500
      j=ni(1)-1
      k=0
      m=0
      nopc=0
      do 495 l=1,ndifft
      nk=ntrmk(l)
      do 495 n=1,nk
      n2=nopc+1
      do 494 n1=1,n
      m=m+1
      nopc=nopc+1
      pc(nopc)=tdn(m,j)
      if (n1.eq.n) pc(nopc)=pc(nopc)+cavedn(j)
  494 continue
      if (icpc.eq.0) go to 495
      write (iw,42) nopc,mult(m,1),lbcd(m,1), (pc(n1), n1=n2,nopc)
  495 continue
      write (aa,49) ll(1),ni(1)
   49 format(2ht(,a1,i2,5h)    )
      write (id4) kpar,k,aa,cavedn(j),nopc, (pc(n1), n1=1,nopc)
      if (ni(1).le.2.or.ni(1).ge.8) go to 500
      j=min0(ni(1)-2,8-ni(1))
      eras=0.0
      do 499 i=1,2
      m=0
      nopc=0
      do 498 l=1,ndifft
      nk=ntrmk(l)
      do 498 n=1,nk
      n2=nopc+1
      do 497 n1=1,n
      m=m+1
      nopc=nopc+1
      pc(nopc)=t1dn(m,j)
      if (i.eq.2) pc(nopc)=t2dn(m,j)
      if (ni(1).gt.5) pc(nopc)=-pc(nopc)
  497 continue
      if (icpc.eq.0) go to 498
      write (iw,42) nopc,mult(m,1),lbcd(m,1), (pc(n1), n1=n2,nopc)
  498 continue
      write (aa,50) i,ll(1),ni(1)
   50 format(1ht,i1,1h(,a1,i2,4h)   )
  499 write (id4) kpar,k,aa,eras,nopc, (pc(n1), n1=1,nopc)
c
c          Calc. v matrices
c
  500 nov=nor
      if (ni(1).eq.1) nov=1
      do 585 irp1=1,nov
      k=irp1-1
      if (nov.eq.1) k=1
      r=k
      do 535 m=1,nlt
      do 535 mp=1,nlt
      a=0.0
      b=0.0
      if (s(m,1)+s(mp,1).lt.1.0) go to 534
      if (abs(s(m,1)-s(mp,1)).gt.1.0) go to 534
      if (fl(m,1)+fl(mp,1).lt.r) go to 534
      if (abs(fl(m,1)-fl(mp,1)).gt.r) go to 534
      do 532 n=1,nop
      b=cfp(m,n)*cfp(mp,n)
      if (b.eq.0.0) go to 532
      b=b*s6j(half,half,one, s(m,1),s(mp,1),sbr(n,1))
     1   *s6j(fll(1),fll(1),r, fl(m,1),fl(mp,1),flbr(n,1))
      x=mod(s(m,1)+sbr(n,1)+1.5+flbr(n,1),two)
      if (x.gt.0.0) b=-b
      a=a+b
  532 continue
      a=a*fn*sqrt(1.5*(2.0*s(m,1)+1.0)*(2.0*s(mp,1)+1.0)
     1  *(2.0*fl(m,1)+1.0)*(2.0*fl(mp,1)+1.0))
      x=mod(fll(1)+fl(m,1)+r,two)
      if (x.gt.0.0) a=-a
      b=a
      x=mod(fl(m,1)-fl(mp,1)+s(m,1)-s(mp,1),two)
      if (x.ne.0.0) b=-b
  534 va(m,mp)=a
  535 va(mp,m)=b
      if (nov.eq.1) go to 539
      write (id3) k, ((va(m,mp),m=1,nlt), mp=1,nlt)
  539 if (k.ne.1) go to 585
c          Calc. coeffs of zeta
  540 if (ilncuv.gt.1) write (iw,52) ll(1),ni(1)
   52 format (//5h0zeta,33x,a1,i2//)
c
      b=sqrt(fll(1)*(fll(1)+1.0)*(2.0*fll(1)+1.0))
      nopc=0
      mmax=0
      do 560 l=1,ndifji
      mmin=mmax+1
      mmax=mmax+njki(l)
      do 560 m=mmin,mmax
      j=nalsji(m)
      do 550 mp=mmin,m
      jp=nalsji(mp)
      nopc=nopc+1
      pc(nopc)=0.0
      a=va(j,jp)
      if (a.eq.0.0) go to 550
      x=mod(fl(jp,1)+s(j,1)+pji(m),two)
      if (x.gt.0.0) a=-a
      pc(nopc)=a*b*s6j(s(j,1),fl(j,1),pji(m), fl(jp,1),s(jp,1),one)
  550 continue
      if (icpc.eq.0) go to 560
      n2=nopc-m+mmin
      write (iw,54) nopc,mult(j,1),lbcd(j,1),pji(m),
     1  (pc(n1), n1=n2,nopc)
   54 format (2i5,a1,f4.1,10f11.6/(17x,10f11.6))
  560 continue
      kpar=1
      cave=0.0
      aa=zetanm
      write (id4) kpar,k,aa,cave,nopc, (pc(n1), n1=1,nopc)
      call clock(time)
      delt=time-time0
      if (ilncuv.gt.1) write (iw,45) aa,nopc,cave,delt
c
  585 continue
c
  800 call clock(time)
      delt=time-time0
c      write (iw,60) ll(1),ni(1),delt
   60 format (26h finished cuvfd calc for  ,a1,i2,11h   at time=,f7.3,
     1  4h min)
      go to 110
c
c          Write dummy records required by system bug on ibm7030
c
  900 write (id2) (pc(j), j=1,20)
      write (id3) (pc(j), j=1,20)
      write (id4) (pc(j), j=1,20)
      rewind id2
      rewind id3
      rewind id4
      return
      end
c     overlay(g9,2,0)
      subroutine lncuv
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kiser),pci(kiser)
      dimension nparj(kc,kc),iser(kiser)
      equivalence (dumlc4,nparj),(dumlc4(kc**2+1),iser)
      common/c3lcd/dumlcd
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      common/energies/etot(kc,2),ee8(kc,2),e0kin(kc),ekin(kmx)
      dimension cfp1(klsp1,klsp1)
      equivalence (cfp1,cfgp1)
      data iblank/1h /
c
c
c
c          Read and check input configurations
c
c     ks=8
  200 ierror=0
      write (iw,10) uenrgy
   10 format (/8h0  k   j,11x,13hconfiguration,35x,
     1  35hn   par   i   terms of li(ni) -----,7x,
     2  9h(e unit =,f8.1,6h cm-1))
      ii=0
      do 259 k=1,2
      if (nsconf(1,k).le.0) go to 259
      write (iw,11)
   11 format (1h )
      nosubc=nsconf(1,k)
      jmax=nsconf(2,k)
      do 202 i=1,ks
      ll(i)=lsymb(1)
      fll(i)=0.0
      nlastt(i)=1
      mult(1,i)=1
      lbcd(1,i)=lsymb(1)
      jjj=max0(nsconf(2,1),nsconf(2,2))
      do 202 j=1,jjj
      llijk(i,j,k)=lsymb(1)
      fllijk(i,j,k)=0.0
  202 nijk(i,j,k)=0
      do 249 j=1,jmax
      n=0
      iprity=1
      read (ir,20) (ll(i),ni(i), i=1,8),(pci(i),i=1,3),a1,a2
      write(122,20) (ll(i),ni(i), i=1,8),(pci(i),i=1,3),a1,a2
   20 format (8(a1,i2,2x),3a6,f13.3,f9.4)
      do 229 i=1,nosubc
      nijk(i,j,k)=ni(i)
      do 212 l=1,24
      if (lsymb(l).ne.ll(i)) go to 212
      ill=l-1
      fll(i)=l-1
      fllijk(i,j,k)=fll(i)
      go to 213
  212 continue
  213 llijk(i,j,k)=ll(i)
      if (ll(i).eq.llijk(i,1,k)) go to 220
      if (i.eq.nosubc.and.ni(i).eq.1) go to 220
      do 217 m=1,j
      if (nijk(i,m,k).ne.0) go to 218
  217 continue
      go to 220
  218 if (ll(i).eq.llijk(i,m,k)) go to 220
      ierror=7
  220 n=n+ni(i)
      if (mod(ni(i)*ill,2).ne.0) iprity=-iprity
  229 continue
c
      npt=0
      do 232 i=1,nosubc
      nn=nijk(i,j,k)
      nfull=4.0*fll(i)+2.0
      if (nn.gt.1.and.nn.lt.nfull-1) go to 230
      not=1
      nlt=1
      mult(1,i)=1
      lbcd(1,i)=lsymb(1)
      ialf(1,i)=iblank
      fl(1,i)=0.0
      s(1,i)=0.0
      if (nn.eq.0.or.nn.eq.nfull) go to 1230
      mult(1,i)=2
      lbcd(1,i)=ll(i)
      fl(1,i)=fll(i)
      s(1,i)=0.5
      go to 1230
  230 call locdsk(id2,fll(i),nijk(i,j,k))
      read (id2) (mult(m,i),lbcd(m,i),ialf(m,i),fl(m,i),s(m,i), m=1,nlt)
 1230 if (i.eq.1.and.j.lt.jmax) nlt=min0(nlt,nlt11)
      if (i.eq.1.and.jmax.eq.1) nlt=min0(nlt,nlt11)
      if (nlt.eq.not) go to 232
      npt=npt+1
      if (npt.gt.1) go to 231
      write (iw,21) k,j, (ll(ip),nijk(ip,j,k),ip=1,ks), n,iprity,i,
     1  (mult(l,i),lbcd(l,i),ialf(l,i), l=1,nlt)
   21 format (i4,i4,7x,8(a1,i2,3x),i5,i5,i5,3x,13(i1,a1,a2)/
     1  81x,13(i1,a1,i2))
      go to 232
  231 write (iw,22) i, (mult(l,i),lbcd(l,i),ialf(l,i), l=1,nlt)
   22 format (73x,i5,3x,13(i1,a1,a2)/81x,13(i1,a1,a2))
  232 continue
      if (npt.gt.0) go to 240
      a1=a1*1000.0/uenrgy
!     output configuration energy
      write (iw,23) k,j, (ll(i),nijk(i,j,k),i=1,ks), n,iprity,
     1  (pci(i),i=1,3),a1,a2
   23 format (i4,i4,7x,8(a1,i2,3x),i5,i5,8x,3hall,8x,3a6,f13.3,f9.4)
!--------------------------------------------------------------------------
      write (101,"(i4,'$',i4,'$',f13.3)") k,j,a1



!�����������
!--------------------------------------------------------------------------
      etot(j,k)=a1
      ee8(j,k)=a2
  240 if (j.gt.1) go to 245
      if (k-1) 241,241,242
  241 no=n
  242 iprtyo=iprity
      go to 249
  245 if (n.ne.no) go to 247
      if (iprity.eq.iprtyo) go to 249
  247 ierror=7
  249 continue
  259 ii=ii+iprity
      iiprty=1
      if (ii.ne.0) iiprty=2
c
      if (ierror.eq.0) go to 281
      write (iw,25)
   25 format (//' lncuv 25--deck setup error: '
     1  'occ. nos. or parities inconsistent'/)
      if (iw6.lt.0) write (6,25)
      stop '(lncuv 25)'
c
c          Calc (li//ck//lj) table
c
  281 write (iw,28)
   28 format (///)
      if (ilncuv.le.0) go to 900
      n=nosubc
      do 299 i1=1,nosubc
      do 299 i2=i1,nosubc
      if (i2-i1) 283,283,284
  283 i=i1
      go to 285
  284 n=n+1
      i=n
  285 do 286 nk=1,6
  286 cijk(i,nk)=0.0
      fk0=abs(fll(i1)-fll(i2))-2.0
      kmin=fk0+2.0
      nok=(fll(i1)+fll(i2)-fk0)/2.0
      do 295 nk=1,nok
      fk0=fk0+2.0
  295 cijk(i,nk)=cijkf(fll(i1),fll(i2),fk0)
  297 write (iw,29) kmin,i1, ll(i1),i2, ll(i2), (cijk(i,nk), nk=1,nok)
   29 format (6h kmin=,i2,5x,1h(,i1,a1,6h//ck//,i1,a1,2h)=,
     1  3x,6f15.8)
  299 continue
c          Check dimensions of Ui, Vi, cfp, and cfgp
  900 call ckdim
      return
      end
      subroutine ckdim
c
c        subroutine (called from lncuv) to check adequacy of dimensions
c          kls1, kls2,...kls6 for the variables u1,v1,u2,v2,...u6,v6,
c                                           and cfp1,cfp2,cfgp1,cfgp2
c        other dimensional checks are made at the end of subroutine plev
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      dimension kdim(8),nltn(14,2),nlpn(14,2),nlgpn(14,2),icfgp(2)
c
      kdim(1)=kls1
      kdim(2)=kls2
      kdim(3)=kls3
      kdim(4)=kls4
      kdim(5)=kls5
      kdim(6)=kls6
      kdim(7)=1
      kdim(8)=1
      ierror=0
      icfp=1
      icfgp(1)=1
      icfgp(2)=1
c
      nosubc=nsconf(1,1)
      do 699 i=1,nosubc
      do 680 k=1,2
      jmax=nsconf(2,k)
      if (jmax.le.0) go to 680
      nmax=0
      nltmax=0
      do 110 n=1,14
      nltn(n,k)=0
      nlpn(n,k)=0
  110 nlgpn(n,k)=0
c
      do 180 j=1,jmax
      n=nijk(i,j,k)
      if (n.le.0) go to 180
      if (nltn(n,k).ne.0) go to 180
      fll(i)=fllijk(i,j,k)
      call locdsk(id2,fll(i),n)
      read (id2) (ia,ia,ia,a,a,m=1,nlt),nlp,nlgp,nocfp,nocfgp
      nmax=max(n,nmax)
      nltmax=max(nlt,nltmax)
      if (nltmax.eq.nlt) nt=n
      nltn(n,k)=nlt
      nlpn(n,k)=nlp
      nlgpn(n,k)=nlgp
  180 continue
      l=fll(i)
      lsy=lsymb(l+1)
c
      if (nmax.le.1) go to 680
      if (i.le.6) go to 205
c           check occupation number for i.gt.6
      write (iw,19) k,i
      if (iw6.lt.0) write (6,19) k,i
   19 format (' ***** parity=',i1,
     1  '  occupation.gt.1 for subshell number ',i1)
      ierror=7
      go to 299
c          check dimensions for uk and vk
  205 if (nltmax.le.kdim(i)) go to 210
      write (iw,20) k,i,i,lsy,nt,nltmax,i,kdim(i)
      if (iw6.lt.0) write (6,20) k,i,i,lsy,nt,nltmax,i,kdim(i)
   20 format (' ***** parity=',i1,'  u',i1,' and v',i1,' for ',a1,i2,
     1  ' require dim. of ',i5, 
     2  ':',5x,'dimension kls',i1,' is only ',i3)
      ierror=7
c
  210 nlpmax=0
      nlgpmax=0
      nt1=0
      nt2=0
      np=0
      ngp=0
      do 215 n=2,14
      if (nltn(n-1,k).eq.0.or.nltn(n,k).eq.0) go to 212
      if (nlpmax.ge.nlpn(n,k)) go to 212
      nlpmax=nlpn(n,k)
      nt1=nltn(n,k)
      np=n
  212 if (n.eq.2) go to 215
      if (nltn(n-2,k).eq.0.or.nltn(n,k).eq.0) go to 215
      if (nlgpmax.ge.nlgpn(n,k)) go to 215
      nlgpmax=nlgpn(n,k)
      nt2=nltn(n,k)
      ngp=n
  215 continue
c          Check dimensions for cfp within one parity
  220 if (np.eq.0) go to 230
      m=1
      if (i.gt.1) m=2
      if (nt1.le.kdim(m).and.nlpmax.le.kdim(m)) go to 230
      write (iw,22) k,m,lsy,np,nt1,nlpmax,m,kdim(m)
      if (iw6.lt.0) write (6,22) k,m,lsy,np,nt1,nlpmax,m,kdim(m)
   22 format (' ***** parity=',i1,'  cfp',i1,' for ',a1,i2,
     1  ' requires dims. of ',2i4,
     2  ':',5x,'dimension kls',i1,' is only ',i3)
      ierror=7
c          Check dimensions for cfgp
  230 if (ngp.eq.0) go to 240
      m=1
      if (icfgp(k).ge.2) m=2
      icfgp(k)=icfgp(k)+1
      if (nt2.le.kdim(m).and.nlgpmax.le.kdim(m)) go to 240
      write (iw,23) k,m,lsy,ngp,nt2,nlgpmax,m,kdim(m)
      if (iw6.lt.0) write (6,23) k,m,lsy,ngp,nt2,nlgpmax,m,kdim(m)
   23 format (' ***** parity=',i1,'  cfgp',i1,' for ',a1,i2,
     1  ' requires dims. of',2i4,
     2  ':',5x,'dimension kls',i1,' is only ',i3)
      ierror=7
c          Check dimensions for g,h,i... electrons
  240 if (l.le.3) go to 299
      write (iw,24) i,lsy,nmax,i,2*l+1,i,2*l-1
      if (iw6.lt.0) write (6,24) i,lsy,nmax,i,2*l+1,i,2*l-1
   24 format (' ***** WARNING:  For subshell ',i1,' (',a1,i2,'),'/20x,
     1  ' third dimension of u',i1,' and cfp or cfgp must be at least',
     2  i3/20x,' and that of v',i1,' must be at least',i3)
  299 continue
c
c          Check dimensions of inter-parity cfp
c
  610 if (k.eq.1) go to 680
      nlpmax=0
      nt1=0
      np=0
      do 615 n=2,14
      if (nltn(n-1,1).eq.0.or.nltn(n,2).eq.0) go to 612
      if (nlpmax.ge.nlpn(n,2)) go to 612
      nlpmax=nlpn(n,2)
      nt1=nltn(n,2)
      np=n
      go to 615
  612 if (nltn(n-1,2).eq.0.or.nltn(n,1).eq.0) go to 615
      if (nlpmax.ge.nlpn(n,1)) go to 615
      nlpmax=nlpn(n,1)
      nt1=nltn(n,1)
      np=n
  615 continue
c          
  620 if (np.eq.0) go to 680
      m=1
      if (icfp.gt.1) m=2
      icfp=icfp+1
      if (nt1.le.kdim(m).and.nlpmax.le.kdim(m)) go to 680
      write (iw,62) m,lsy,np,nt1,nlpmax,m,kdim(m)
      if (iw6.lt.0) write (6,62) m,lsy,np,nt1,nlpmax,m,kdim(m)
   62 format (' ***** pars.1,2  cfp',i1,' for ',a1,i2,
     1  ' requires dims. of ',2i4,
     2  ':',5x,'dimension kls',i1,' is only ',i3)
      ierror=7
  680 continue
  699 continue
c
      if (ierror.eq.0) go to 799
      write (iw,59)
      if (iw6.lt.0) write (6,59)
   59 format (' ***** dimensions exceeded')
      stop ' (ckdim 59)'
  799 return
      end
c     overlay(g9,3,0)
      subroutine plev
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kiser),pci(kiser)
      dimension nparj(kc,kc),iser(kiser)
      equivalence (dumlc4,nparj),(dumlc4(kc**2+1),iser)
      common/c3lcd/dumlcd
      common/c3lc7/m,i,j,k,l,i1,j2,k1,l8,j1
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      common/sortdum/dum(2),idum(2)
      dimension cfp1(klsp1,klsp1)
      equivalence (cfp1,cfgp1)
      data iblank/1h /
c
c
c     ks=8
c     kjp=1000
c     klsp=210
c     kjk=400
      ntottj(1)=0
      ndifft=0
      sumx=0.0
      sj8mn=1000.0
      sj8mx=0.0
      sj8mx1=0.0
      do 50 i=1,ks
      nalsjp(1,i)=0
      notsj1(i,1)=0
      ntotjj(i,1)=0
   50 ndiffj(i)=0
c
      notsx=0
      jx=nsconf(2,kk)
      do 229 j1=1,jx
      ll(nosubc)=llijk(nosubc,j1,kk)
      fll(nosubc)=fllijk(nosubc,j1,kk)
      do 79 i=1,ks
      nots=notsj1(i,j1)
c             Read terms from disk 72
      ni(i)=nijk(i,j1,kk)
      nn=ni(i)
      nfull=4.0*fll(i)+2.0
      if (nn.gt.1.and.nn.lt.nfull-1) go to 70
      not=1
      nlt=1
      nlastt(i)=nlt
      not1=nots+1
      nots=nots+nlt
      mult(not1,i)=1
      lbcd(not1,i)=lsymb(1)
      ialf(not1,i)=iblank
      fl(not1,i)=0.0
      s(not1,i)=0.0
      if (nn.eq.0.or.nn.eq.nfull) go to 78
      mult(not1,i)=2
      lbcd(not1,i)=ll(i)
      ialf(not1,i)=iblank
      fl(not1,i)=fll(i)
      s(not1,i)=0.5
      go to 78
   70 call locdsk(id2,fll(i),ni(i))
      if (i.eq.1.and.j1.lt.jx) nlt=min0(nlt,nlt11)
      if (i.eq.1.and.jx.eq.1) nlt=min0(nlt,nlt11)
      nlastt(i)=nlt
      not1=nots+1
      nots=nots+nlt
      read (id2) (mult(m,i),lbcd(m,i),ialf(m,i),fl(m,i),s(m,i),
     1  m=not1,nots)
   78 notsj1(i,j1+1)=nots
      notsx=max0(nots,notsx)
   79 continue
c
c          Calc. preliminary ls terms
c
      m=ntottj(j1)
      n1=notsj1(1,j1)+1
      n2=notsj1(2,j1)+1
      n3=notsj1(3,j1)+1
      n4=notsj1(4,j1)+1
      n5=notsj1(5,j1)+1
      n6=notsj1(6,j1)+1
      n7=notsj1(7,j1)+1
      n8=notsj1(8,j1)+1
      n11=notsj1(1,j1+1)
      n22=notsj1(2,j1+1)
      n33=notsj1(3,j1+1)
      n44=notsj1(4,j1+1)
      n55=notsj1(5,j1+1)
      n66=notsj1(6,j1+1)
      n77=notsj1(7,j1+1)
      n88=notsj1(8,j1+1)
      do 120 i=n1,n11
      do 120 j=n2,n22
      do 120 k=n3,n33
      do 120 l=n4,n44
      do 120 i1=n5,n55
      do 120 j2=n6,n66
      do 120 k1=n7,n77
      do 120 l8=n8,n88
c
c          15-fold do loop (101 lines) moved to subroutine plevdolp
c               because of VAX-compiler limitations
c
      call plevdolp
c
  120 continue
      notott=m
      l=ntottj(j1)+1
      ntottj(j1+1)=m
      if (iplev) 125,125,121
  121 write (iw,12)
   12 format (9h1ls terms)
      do 122 m=l,notott
  122 write (iw,13) (ncfgp(m),
     1              nalsp(m,i),pscrs(m,i),pscrl(m,i), i=1,nosubc)
   13 format (1h , 8(i5,i3,f5.1,f3.0))
c
c        Sort on decreasing   25*scrs4+scrl4
c
  125 m1=ntottj(j1+1)-ntottj(j1)
      if (m1.le.1) go to 129
      call sort2(m1,11,pc(l),pci,nalsp(l,1),pscrs(l,1),nalsp(l,2),
     1   nalsp(l,3),pscrl(l,1),pscrs(l,2),pscrl(l,2),pscrs(l,3),
     2   pscrl(l,3),pscrs(l,4),pscrl(l,4),dum)
      call orderi(m1,pci,nalsp(l,4))
      if (nosubc.le.4) go to 129
      if (nosubc.lt.7) go to 127
      call order2(m1,pci,pscrl(l,8))
      call order2(m1,pci,pscrs(l,8))
      call orderi(m1,pci,nalsp(l,8))
      call order2(m1,pci,pscrl(l,7))
      call order2(m1,pci,pscrs(l,7))
      call orderi(m1,pci,nalsp(l,7))
  127 call order2(m1,pci,pscrl(l,6))
      call order2(m1,pci,pscrs(l,6))
      call orderi(m1,pci,nalsp(l,6))
      call order2(m1,pci,pscrl(l,5))
      call order2(m1,pci,pscrs(l,5))
      call orderi(m1,pci,nalsp(l,5))
c
  129 if (iplev) 135,135,130
  130 write (iw,14)
   14 format (///18h0ls terms (sorted)/)
      do 131 m=l,notott
  131 write (iw,13) (ncfgp(m),
     1              nalsp(m,i),pscrs(m,i),pscrl(m,i), i=1,nosubc)
      write (iw,15)
   15 format (1h1)
c
c        Calc. number of terms of each kind
c
  135 k=ndifft
      n2=-100
  140 do 143 m=l,notott
      n1=n2
      n2=25.0*pscrs(m,nosubc)+pscrl(m,nosubc)
      if (n2-n1) 142,141,1942
  141 ntrmk(k)=ntrmk(k)+1
      go to 143
 1942 if (m.eq.l) go to 142
      stop '(terms not correctly sorted at PLEV 141)'
  142 k=k+1
      ntrmk(k)=1
      sj8mn=min(sj8mn,abs(pscrs(m,nosubc)-pscrl(m,nosubc)))
      sj8mx=max(sj8mx,pscrs(m,nosubc)+pscrl(m,nosubc))
      sj8mx1=max(sj8mx1,pscrs(m,nosubc)+pscrl(m,nosubc))
  143 continue
      ndifft=k
  150 if (sj8mn.eq.sj8mx) go to 170
      if (sj8mn.ge.sjn) go to 160
      sj8mn=sj8mn+1.0
      go to 150
  160 if (sj8mx.le.sjx) go to 170
      sj8mx=sj8mx-1.0
      go to 160
  170 nscrj8=sj8mx-sj8mn+1.0
c
c          Calc. preliminary levels for each subshell
c
  200 if (nolskp.ne.0) go to 229
      sum=0.0
      do 225 i=1,nosubc
      m=ntotjj(i,j1)
      n1=notsj1(i,j1)+1
      n11=notsj1(i,j1+1)
      do 205 j=n1,n11
      eji=abs(fl(j,i)-s(j,i))-1.0
      nji=fl(j,i)+s(j,i)-eji
      do 205 ij=1,nji
      m=m+1
      eji=eji+1.0
      nalsjp(m,i)=j
      a=j
      ncfgjp(m,i)=j1
      pc(m)=-200.0*eji-25.0*s(j,i)-fl(j,i)+0.001*a
  205 pj(m,i)=eji
      nototj(i)=m
      ntotjj(i,j1+1)=m
      l=ntotjj(i,j1)+1
      if (iplev) 215,215,206
  206 write (iw,20) i
   20 format (/20h0levels of subshell ,i1)
      do 211 n=l,m
      j=nalsjp(n,i)
  211 write (iw,21)  ncfgjp(n,i),nalsjp(n,i),mult(j,i),lbcd(j,i),pj(n,i)
   21 format (i13,i4,i5,a1,f5.1)
c
c        Sort on decreasing pj
c
  215 m1=ntotjj(i,j1+1)-ntotjj(i,j1)
      call sort2(m1,2,pc(l),pci,nalsjp(l,i),pj(l,i),idum,idum,dum,dum,
     1  dum,dum,dum,dum,dum,dum)
c
      if (iplev) 218,218,216
  216 write (iw,22) i
   22 format (/20h0levels of subshell ,i1,9h (sorted))
      do 217 n=l,m
      j=nalsjp(n,i)
  217 write (iw,21)  ncfgjp(n,i),nalsjp(n,i),mult(j,i),lbcd(j,i),pj(n,i)
c
c        Calc. number of levels of each pj
c
  218 k=ndiffj(i)+1
      njk(k,i)=1
      l=l+1
      if (m-l) 224,220,220
  220 do 223 j=l,m
      if (pj(j,i)-pj(j-1,i)) 222,221,222
  221 njk(k,i)=njk(k,i)+1
      go to 223
  222 k=k+1
      njk(k,i)=1
  223 continue
  224 ndiffj(i)=k
  225 sum=sum+pj(l-1,i)
      if (sum.gt.sumx) sumx=sum
  229 continue
c
      if (sumx.eq.sj8mx1) go to 256
      write (iw,23) sj8mx1,sumx
   23 format (///15h0maximum scrj8=,f5.1,10h  from ls ,
     1  10hcalc, and=,f5.1, 14h  from jj calc
     2  /52h   (ls.lt.jj is ok if j values have been restricted)
     3  /52h    (jj.eq.0 is ok if ls terms have been restricted))
  256 do 270 i=1,ks
      if (i.le.nosubc.and.nolskp.eq.0) go to 270
      do 260 j=1,jx
      if (i.le.nosubc) go to 258
      notsj1(i,j+1)=j
  258 ntotjj(i,j)=j
      nototj(i)=j
      ndiffj(i)=j
      njk(j,i)=1
      nalsjp(j,i)=j
  260 pj(j,i)=0.0
  270 continue
c
  300 ierror=0
      maxm=0
      maxk=0
      do 310 i=1,ks
      maxm=max0(maxm,nototj(i))
  310 maxk=max0(maxk,ndiffj(i))
      if (notott.gt.klsp.or.ndifft.gt.klsp) ierror=7
      if (maxm.gt.kjp.or.maxk.gt.kjk) ierror=7
      if (notsx.gt.klsc) ierror=7
      write (iw,30) kk,klsp,notott,klsp,ndifft,kjp,(nototj(i),i=1,ks),
     1  kjk,(ndiffj(i),i=1,ks),klsc,notsx
!     output maximum subscript values
   30 format (///25h maximum subscript values,', parity number',i2//
     1  32h nalsp(m,i), pscrl(m,i),   klsp=,i4,15h   m=notott=   ,i5/
     2  17h ntrmk(k), lf(k),, 10x,5hklsp=,i4,15h   k=ndifft=   ,i5/
     3  32h nalsjp(m,i), pj(m,i),     kjp= ,i4,15h   m=nototj(i)=,8i5/
     4  10h njk(k,i),,17x,5hkjk= ,i4,3x,12hk=ndiffj(i)=,8i5/
     5  16h fl(m,i),s(m,i),,11x,5hklsc=,i4,14h   mmax=notsx=,i6)
      jx=jx+1
      write (iw,31) (ntottj(j), j=1,jx)
   31 format (/8h0ntottj=,20i6/(8x,20i6))
      write (iw,32) (ntrmk(k), k=1,ndifft)
   32 format (/8h0 ntrmk=,20i6/(8x,20i6))
      if (ierror.eq.0) go to 400
      write (iw,33)
   33 format (//25h***** dimensions exceeded)
      if (iw6.ge.0) go to 399
      write (6,30) kk,klsp,notott,klsp,ndifft,kjp,(nototj(i),i=1,ks),
     1  kjk,(ndiffj(i),i=1,ks),klsc,notsx
      write (6,33)
  399 stop '(plev 33)'
  400 return
      end
      subroutine plevdolp
c
c          15-fold do loop (101 lines) moved from subroutine plev          
c               because of VAX-compiler limitations

      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kiser),pci(kiser)
      dimension nparj(kc,kc),iser(kiser)
      equivalence (dumlc4,nparj),(dumlc4(kc**2+1),iser)
      common/c3lcd/dumlcd
      common/c3lc7/m,i,j,k,l,i1,j2,k1,l8,j1
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      dimension cfp1(klsp1,klsp1)
      equivalence (cfp1,cfgp1)
      data iblank/1h /
c
c
c     ks=8
c     kjp=1000
c     klsp=210
c     kjk=400
      es2=abs(s(i,1)-s(j,2))-1.0
      ns2=s(i,1)+s(j,2)-es2
      do 110 is2=1,ns2
      es2=es2+1.0
      el2=abs(fl(i,1)-fl(j,2))-1.0
      nl2=fl(i,1)+fl(j,2)-el2
      do 110 il2=1,nl2
      el2=el2+1.0
      es3=abs(es2-s(k,3))-1.0
      ns3=es2+s(k,3)-es3
      do 110 is3=1,ns3
      es3=es3+1.0
      el3=abs(el2-fl(k,3))-1.0
      nl3=el2+fl(k,3)-el3
      do 110 il3=1,nl3
      el3=el3+1.0
      es4=abs(es3-s(l,4))-1.0
      ns4=es3+s(l,4)-es4
      do 110 is4=1,ns4
      es4=es4+1.0
      el4=abs(el3-fl(l,4))-1.0
      nl4=el3+fl(l,4)-el4
      do 110 il4=1,nl4
      el4=el4+1.0
      es5=abs(es4-s(i1,5))-1.0
      ns5=es4+s(i1,5)-es5
      do 110 is5=1,ns5
      es5=es5+1.0
      el5=abs(el4-fl(i1,5))-1.0
      nl5=el4+fl(i1,5)-el5
      do 110 il5=1,nl5
      el5=el5+1.0
      es6=abs(es5-s(j2,6))-1.0
      ns6=es5+s(j2,6)-es6
      do 110 is6=1,ns6
      es6=es6+1.0
      el6=abs(el5-fl(j2,6))-1.0
      nl6=el5+fl(j2,6)-el6
      do 110 il6=1,nl6
      el6=el6+1.0
      es7=abs(es6-s(k1,7))-1.0
      ns7=es6+s(k1,7)-es7
      do 110 is7=1,ns7
      es7=es7+1.0
      el7=abs(el6-fl(k1,7))-1.0
      nl7=el6+fl(k1,7)-el7
      do 110 il7=1,nl7
      el7=el7+1.0
      es8=abs(es7-s(l8,8))-1.0
      ns8=es7+s(l8,8)-es8
      do 110 is8=1,ns8
      es8=es8+1.0
      el8=abs(el7-fl(l8,8))-1.0
      nl8=el7+fl(l8,8)-el8
      do 110 il8=1,nl8
      el8=el8+1.0
      if (abs(el8-es8).gt.sjx) go to 110
      if (el8+es8.lt.sjn) go to 110
      if (nolskp.le.0) go to 100
      if (j1.lt.nclskp(kk)) go to 100
      do 95 ii=1,nolskp
      if (el8.eq.scrlkp(ii,kk).and.es8.eq.scrskp(ii,kk)) go to 100
   95 continue
      go to 110
  100 m=m+1
      go to (108,107,106,105,104,103,102,101) nosubc
  101 nalsp(m,8)=l8
      pscrs(m,8)=es8
      pscrl(m,8)=el8
  102 nalsp(m,7)=k1
      pscrs(m,7)=es7
      pscrl(m,7)=el7
  103 nalsp(m,6)=j2
      pscrs(m,6)=es6
      pscrl(m,6)=el6
  104 nalsp(m,5)=i1
      pscrs(m,5)=es5
      pscrl(m,5)=el5
  105 nalsp(m,4)=l
      pscrs(m,4)=es4
      pscrl(m,4)=el4
  106 nalsp(m,3)=k
      pscrs(m,3)=es3
      pscrl(m,3)=el3
  107 nalsp(m,2)=j
      pscrs(m,2)=es2
      pscrl(m,2)=el2
  108 nalsp(m,1)=i
      pscrs(m,1)=s(i,1)
      pscrl(m,1)=fl(i,1)
      ncfgp(m)=j1
      a=0.0
      prod=1.0
      eras=0.02
      do 109 ii=1,nosubc
      b=nalsp(m,ii)
      a=a+prod*b
      if (ii.gt.4) eras=0.1
  109 prod=prod*eras
      pc(m)=-(25.0*pscrs(m,nosubc)+pscrl(m,nosubc))+0.002*a
  110 continue
      return
      end
c     overlay(g9,4,0)
      subroutine pfgd
c
c          Calc. preliminary single-configuration matrix elements
c
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kiser),pci(kiser)
      dimension nparj(kc,kc),iser(kiser)
      equivalence (dumlc4,nparj),(dumlc4(kc**2+1),iser)
      common/c3lcd/dumlcd
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      dimension cfp1(klsp1,klsp1),ddjj(kmx,1)
      equivalence (cfp1,cfgp1)
      dimension vfg(200,15)
      character*10 parnam(kpr,2)
      character idfg(15)*11
      character*8 fidls(kmx,2),fidjj(kmx,2),ldes(kmx),ldesp(kmx)
      common/char/parnam,fidls,fidjj,ldes,ldesp
      common/djj/ddjj
c
      character*10 abg(3),ze(8),aa
      data (abg(i),i=1,3) /'1000 alpha','beta      ','gamma     '/
      data (ze(i),i=1,8) /'zeta 1','zeta 2','zeta 3','zeta 4',
     1  'zeta 5','zeta 6','zeta 7','zeta 8'/
c
c
c     ks=8
c
      j1x=nsconf(2,kk)
      lx=ntottj(j1x+1)
      do  97 l=1,lx
      muls1(l)=2.0*pscrs(l,1)+1.0
      muls4(l)=2.0*pscrs(l,nosubc)+1.0
      i=pscrl(l,1)+1.0
      lhs1(l)=lsymb(i)
      i=pscrl(l,nosubc)+1.0
   97 lhs4(l)=lsymb(i)
c
      npar=0
      nfg=0
      nparjo=0
      rewind 20
c
      do 499 j1=1,j1x
      ll(nosubc)=llijk(nosubc,j1,kk)
      fll(nosubc)=fllijk(nosubc,j1,kk)
      npar=npar+1
      parnam(npar,kk)=parnam(1,1)
      do 99 i=1,ks
   99 ni(i)=nijk(i,j1,kk)
c
c          Obtain equivalent-electron Coulomb coefficients fk(i,i) 
c               from disk 74, and terms of li(ni) from disk 72
c
  100 do 199 i=1,nosubc
      if (ni(i).le.1) go to 199
      n=4.0*fll(i)
      if (ni(i).gt.n) go to 199
      call locdsk(id2,fll(i),ni(i))
      read (id2) (mulsi(m),lbcdi(m),ia,a,a, m=1,nlt)
      call locdsk(id4,fll(i),ni(i))
      if (nsconf(1,kk).gt.1) go to 115
      if (sjn.gt.0.0.or.sjx.lt.99.0) go to 115
      read (id4)
      go to 170
c
  115 read (id4) ndiffi,(nti(k),k=1,ndiffi)
c
c          Find correlation between terms of conf. j1 and terms of li(ni)
c
      nopc=0
      mx=0
      do 169 k=1,ndifft
      mn=mx+1
      mx=mx+ntrmk(k)
      if (mx.le.ntottj(j1)) go to 169
      if (mx.gt.ntottj(j1+1)) go to 170
      do 159 m=mn,mx
      j=nalsp(m,i)
      npi0=0
      mxi=0
      do 125 k1=1,ndiffi
      mni=mxi+1
      mxi=mxi+nti(k1)
      if (mult(j,i).ne.mulsi(mni)) go to 125
      if (lbcd(j,i).eq.lbcdi(mni)) go to 130
  125 npi0=npi0+(nti(k1)*(nti(k1)+1))/2
  130 do 149 mp=mn,m
      jp=nalsp(mp,i)
      nopc=nopc+1
      pc(nopc)=0.0
      iser(nopc)=-7
      if (mult(j,i).ne.mult(jp,i)) go to 149
      if (lbcd(j,i).ne.lbcd(jp,i)) go to 149
      do 133 l=1,nosubc
      if (pscrl(m,l).ne.pscrl(mp,l)) go to 149
      if (pscrs(m,l).ne.pscrs(mp,l)) go to 149
      if (l.eq.i) go to 133
      if (nalsp(m,l).ne.nalsp(mp,l)) go to 149
  133 continue
      npi=npi0
      do 139 mi=mni,mxi
      do 135 mpi=mni,mi
      npi=npi+1
      if (j-notsj1(i,j1).ne.mi) go to 135
      if (jp-notsj1(i,j1).ne.mpi) go to 135
      iser(nopc)=npi
      go to 149
  135 continue
  139 continue
  149 continue
  159 continue
  169 continue
c
c          Write preliminary coefficients pc on disk 20
c
  170 npari=norcd-2
      if (iabg.eq.0) npari=fll(i)
      do 198 n=1,npari
      if (nsconf(1,kk).gt.1) go to 175
      if (sjn.gt.0.0.or.sjx.lt.99.0) go to 175
      read (id4) kpar,k,aa,cave,nopc, (pc(j),j=1,nopc)
      if (kpar.eq.1) go to 198
      go to 185
  175 read (id4) kpar,k,aa,cave,npi, (pci(j),j=1,npi)
      if (kpar.eq.1) go to 198
      do 180 j=1,nopc
      if (iser(j).le.0) go to 180
      l=iser(j)
      pc(j)=pci(l)
  180 continue
c
  185 npar=npar+1
      nfg=nfg+1
      if (k.ne.0) go to 186
      if (iabg) 198,198,188
  186 write (aa,14) k,i,i
   14 format (1hf,i1,1h(,2i1,5h)    )
  188 parnam(npar,kk)=aa
      write (20) npar,kpar,k,i,i,aa,cave,j1,nopc, (pc(n1), n1=1,nopc)
      if (icpc.le.1.or.icpc.eq.3) go to 197
      write (iw,16) aa,cave
   16 format (1h2,a10,5x,5hcave=,f12.7//)
      nopc=0
      lfg=0
      mx=0
      do 191 l=1,ndifft
      mn=mx+1
      mx=mx+ntrmk(l)
      if (mx.le.ntottj(j1)) go to 191
      if (mx.gt.ntottj(j1+1)) go to 197
      do 190 m=mn,mx
      j=nalsp(m,i)
      n2=nopc+1
      nopc=n2+m-mn
      write (iw,17) ncfgp(j),nopc,mult(j,i),lbcd(j,i),muls4(m),
     1  lhs4(m), (pc(n1), n1=n2,nopc)
   17 format (2i5,5h    (,i1,a1,1h),i4,a1, 10f10.5/(25x, 10f10.5))
      if (icpc.lt.5) go to 190
      lfg=lfg+1
      vfg(lfg,nfg)=pc(nopc)
      write (idfg(nfg),19) k,i,llijk(i,1,1),i,llijk(i,1,1)
   19 format (1hf,i1,1h(,i2,a1,1h,,i2,a1,1h))
  190 continue
  191 continue
  197 if (icpc.eq.0) go to 198
      call clock(time)
      delt=time-time0
      write (iw,18) aa,nopc,cave,delt, (ll(l),ni(l), l=1,nosubc)
   18 format (/1h ,a10,5x,3hpc(,i5,1h),5x,5hcave=,f12.7,17x,5hdelt=,
     1  f6.3,4h min,7x, 8(a1,i2,3x))
  198 continue
  199 continue
c
c          Obtain spin-orbit coefficients zeta(i) from disk 74
c
  200 do 299 i=1,nosubc
      if (ni(i).le.0) go to 299
      if (fll(i).le.0.0) go to 299
      nn=4.0*fll(i)+2.0
      if (ni(i).ge.nn) go to 299
      if (ni(i).gt.1.and.ni(i).lt.nn-1) go to 205
      norcd=2
      m=1
      nti(1)=1
      n1=2
      nalsji(1)=1
      nalsji(2)=1
      pji(1)=fll(i)+0.5
      pji(2)=fll(i)-0.5
      ndifji=2
      nti(1)=1
      nti(2)=1
      go to 220
  205 call locdsk(id4,fll(i),ni(i))
      if (nsconf(1,kk).gt.1) go to 215
      read (id4)
      go to 270
c
  215 read (id4) m,(nti(k),k=1,m), n1,(nalsji(k),pji(k),k=1,n1),
     2  ndifji,(nti(k),k=1,ndifji)
c
c          Find correl. between levels in conf j1 and levels of li(ni)
c
  220 nopc=0
      mx=0
      kx=ndiffj(i)
      do 269 k=1,kx
      mn=mx+1
      mx=mx+njk(k,i)
      if (mx.le.ntotjj(i,j1)) go to 269
      if (mx.gt.ntotjj(i,j1+1)) go to 270
      do 259 m=mn,mx
      j=nalsjp(m,i)-notsj1(i,j1)
      npi0=0
      mxi=0
      do 225 ki=1,ndifji
      mni=mxi+1
      mxi=mxi+nti(ki)
      if (pj(m,i).eq.pji(mni)) go to 230
  225 npi0=npi0+(nti(ki)*(nti(ki)+1))/2
  230 do 249 mp=mn,m
      jp=nalsjp(mp,i)-notsj1(i,j1)
      nopc=nopc+1
      pc(nopc)=0.0
      iser(nopc)=-7
      if (pj(m,i).ne.pj(mp,i)) go to 249
      npi=npi0
      do 239 mi=mni,mxi
      do 235 mpi=mni,mi
      npi=npi+1
      if (j.ne.nalsji(mi)) go to 235
      if (jp.ne.nalsji(mpi)) go to 235
      iser(nopc)=npi
      go to 249
  235 continue
  239 continue
  249 continue
  259 continue
  269 continue
c
c          Write pc on disk 20
c
  270 npari=norcd-1
      do 289 n=1,npari
      if (ni(i).gt.1.and.ni(i).lt.nn-1) go to 271
      a=-0.5
      if (ni(i).eq.1) a=0.5
      eras1=a*fll(i)
      eras2=-a*(fll(i)+1.0)
      kpar=1
      k=0
      cave=0.0
      if (nsconf(1,kk).gt.1) go to 1270
      pc(1)=eras1
      pc(2)=eras2
      go to 285
 1270 pci(1)=eras1
      pci(2)=eras2
      go to 277
  271 if (n.eq.npari) go to 272
      read (id4)
      go to 289
  272 if (nsconf(1,kk).gt.1) go to 275
      read (id4) kpar,k,aa,cave,nopc, (pc(j),j=1,nopc)
      go to 285
  275 read (id4) kpar,k,aa,cave,npi, (pci(j),j=1,npi)
  277 do 280 j=1,nopc
      if (iser(j).le.0) go to 280
      l=iser(j)
      pc(j)=pci(l)
  280 continue
  285 npar=npar+1
      aa=ze(i)
      parnam(npar,kk)=aa
      write (20) npar,kpar,k,i,i,aa,cave,j1,nopc, (pc(n1), n1=1,nopc)
      if (icpc.le.1.or.icpc.eq.3) go to 288
      write (iw,16) aa,cave
      nopc=0
      mx=0
      kx=ndiffj(i)
      do 287 k=1,kx
      mn=mx+1
      mx=mx+njk(k,i)
      if (mx.le.ntotjj(i,j1)) go to 287
      if (mx.gt.ntotjj(i,j1+1)) go to 288
      do 286 m=mn,mx
      j=nalsjp(m,i)
      n2=nopc+1
      nopc=n2+m-mn
  286 write (iw,28) ncfgjp(m,i),nopc,mult(j,i),lbcd(j,i),pj(m,i),
     1  (pc(n1),n1=n2,nopc)
   28 format (3i5,a1,f4.1,10f11.6/(22x,10f11.6))
  287 continue
  288 if (icpc.eq.0) go to 289
      call clock(time)
      delt=time-time0
      write (iw,18) aa,nopc,cave,delt, (ll(l),ni(l), l=1,nosubc)
  289 continue
  299 continue
c
c          Calculate Coulomb direct coefficients fk(i,j)
c
      noscm1=nosubc-1
      if (noscm1.le.0) go to 498
      irho=0
c          Read reduced matrix elements U,V from disk 73
      do 7304 i=1,nosubc
      if (ni(i).le.1) go to 7304
      n=4.0*fll(i)+2.0
      if (ni(i).eq.n) go to 7304
      call locdsk(id3,fll(i),ni(i))
      nor=norcd/2
      do 303 k=1,nor
      go to (1303,2303,3303,4303,5303,6303), i
 1303 read (id3) n, ((u1(ii,jj,k),ii=1,nlt),jj=1,nlt)
      go to 303
 2303 read (id3) n, ((u2(ii,jj,k),ii=1,nlt),jj=1,nlt)
      go to 303
 3303 read (id3) n, ((u3(ii,jj,k),ii=1,nlt),jj=1,nlt)
      go to 303
 4303 read (id3) n, ((u4(ii,jj,k),ii=1,nlt),jj=1,nlt)
      go to 303
 5303 read (id3) n, ((u5(ii,jj,k),ii=1,nlt),jj=1,nlt)
      go to 303
 6303 read (id3) n, ((u6(ii,jj,k),ii=1,nlt),jj=1,nlt)
  303 continue
      do 304 k=1,nor
      go to (1304,2304,3304,4304,5304,6304), i
 1304 read (id3) n, ((v1(ii,jj,k),ii=1,nlt),jj=1,nlt)
      go to 304
 2304 read (id3) n, ((v2(ii,jj,k),ii=1,nlt),jj=1,nlt)
      go to 304
 3304 read (id3) n, ((v3(ii,jj,k),ii=1,nlt),jj=1,nlt)
      go to 304
 4304 read (id3) n, ((v4(ii,jj,k),ii=1,nlt),jj=1,nlt)
      go to 304
 5304 read (id3) n, ((v5(ii,jj,k),ii=1,nlt),jj=1,nlt)
      go to 304
 6304 read (id3) n, ((v6(ii,jj,k),ii=1,nlt),jj=1,nlt)
  304 continue
 7304 continue
c
      do 399 i=1,noscm1
      nii=ni(i)
      if (ni(i)) 399,399,306
  306 if (fll(i)) 399,399,307
  307 n=4.0*fll(i)+2.0
      if (ni(i)-n) 308,399,399
  308 i1=i+1
      do 389 j=i1,nosubc
      nij=ni(j)
      if (ni(j)) 389,389,310
  310 if (fll(j)) 389,389,311
  311 n=4.0*fll(j)+2.0
      if (ni(j)-n) 312,389,389
  312 if (fll(i)-fll(j)) 313,314,314
  313 kmax=2.0*fll(i)
      go to 315
  314 kmax=2.0*fll(j)
  315 do 385 k=1,kmax
      if (iabg.ne.2.and.iabg.ne.4.and.mod(k,2).ne.0) go to 385
      if (icpc.le.1.or.icpc.eq.3) go to 320
      write (iw,31)
   31 format (1h2)
      write (iw,32) k,i,j
   32 format (2h f,i1,1h(,i1,1h,,i1,1h)//)
  320 fk=k
      cij=cijkf(fll(i),fll(i),fk)*cijkf(fll(j),fll(j),fk)
      if (mod(k,2).ne.0) cij=1.0
c
  330 nopc=0
      nfg=nfg+1
      lfg=0
      mmax=0
      do 383 l=1,ndifft
      mmin=mmax+1
      mmax=mmax+ntrmk(l)
      if (ncfgp(mmax).ne.j1) go to 383
      notsi=notsj1(i,j1)
      notsj=notsj1(j,j1)
      do 382 m=mmin,mmax
      ji=nalsp(m,i)
      jj=nalsp(m,j)
      ki=ji-notsi
      kj=jj-notsj
      do 381 mp=mmin,m
      jpi=nalsp(mp,i)
      jpj=nalsp(mp,j)
      kpi=jpi-notsi
      kpj=jpj-notsj
      nopc=nopc+1
      pc(nopc)=0.0
      do 341 ip=1,nosubc
      if (pscrs(m,ip)-pscrs(mp,ip)) 381,331,381
  331 if (ip-i) 339,332,335
  332 if (s(ji,i)-s(jpi,i)) 381,341,381
  335 if (ip-j) 340,336,339
  336 if (pscrl(m,ip)-pscrl(mp,ip)) 381,337,381
  337 if (s(jj,j)-s(jpj,j)) 381,341,381
  339 if (pscrl(m,ip)-pscrl(mp,ip)) 381,340,381
  340 if (nalsp(m,ip)-nalsp(mp,ip)) 381,341,381
  341 continue
      do 350 iii=1,2
      mm=m
      if (iii.eq.2) mm=mp
      do 350 ip=1,nosubc
      ii=nalsp(mm,ip)
      tl(iii,ip)=fl(ii,ip)
      ts(iii,ip)=s(ii,ip)
      tscl(iii,ip)=pscrl(mm,ip)
  350 tscs(iii,ip)=pscrs(mm,ip)
      tk=fk
      call rdij(i,j)
c
      pc(nopc)=a*cij
  381 continue
      if (icpc.le.1.or.icpc.eq.3) go to 382
      n2=nopc-m+mmin
      write (iw,17) ncfgp(m),nopc,muls1(m),lhs1(m),muls4(m),
     1  lhs4(m), (pc(n1), n1=n2,nopc)
      if (icpc.lt.5) go to 382
      lfg=lfg+1
      vfg(lfg,nfg)=pc(nopc)
      write (idfg(nfg),19) k,i,llijk(i,1,1),j,llijk(j,1,1)
  382 continue
  383 continue
      npar=npar+1
      kpar=-1
      cave=0.0
      write (aa,14) k,i,j
      parnam(npar,kk)=aa
      write (20) npar,kpar,k,i,j,aa,cave,j1,nopc, (pc(n1), n1=1,nopc)
      if (icpc.eq.0) go to 385
      call clock(time)
      delt=time-time0
      write (iw,18) aa,nopc,cave,delt, (ll(l),ni(l), l=1,nosubc)
  385 continue
  389 continue
  399 continue
c
c          Calculate Coulomb exchange coefficients gk(i,j)
c
  400 do 497 i=1,noscm1
      nii=ni(i)
      if (ni(i)) 497,497,401
  401 n=4.0*fll(i)+2.0
      if (ni(i)-n) 403,497,497
  403 i1=i+1
      do 489 j=i1,nosubc
      nij=ni(j)
      if (ni(j)) 489,489,405
  405 n=4.0*fll(j)+2.0
      if (ni(j)-n) 406,489,489
  406 kmax=fll(i)+fll(j)
      kmin=abs(fll(i)-fll(j))
      kdmin=0
      irp1mx=kmax-kmin+1
      mn=i+1
      mx=j-1
      do 485 k=kmin,kmax
      if (iabg.ne.2.and.iabg.ne.4.and.mod(k-kmin,2).ne.0) go to 485
      fk=k
      cij=(cijkf(fll(i),fll(j),fk))**2
      a=ni(i)*ni(j)
      cave=a*s3j0sq(fll(i),fk,fll(j))/2.0
      lpl=fll(i)+fll(j)+fk
      if (mod(lpl,2).eq.0) go to 407
      cij=0.5*((-1.0)**k)
      cave=-cij*a/((2.0*fll(i)+1.0)*(2.0*fll(j)+1.0))
      cij=2.0*cij
  407 if (icpc.le.1.or.icpc.eq.3) go to 410
      write (iw,31)
      write (iw,40) k,i,j,cave
   40 format (2h g,i1,1h(,i1,1h,,i1,1h),6x,5hcave=,f12.7//)
c
  410 nopc=0
      nfg=nfg+1
      lfg=0
      mmax=0
      do 483 l=1,ndifft
      mmin=mmax+1
      mmax=mmax+ntrmk(l)
      if (ncfgp(mmax).ne.j1) go to 483
      notsi=notsj1(i,j1)
      notsj=notsj1(j,j1)
      do 482 m=mmin,mmax
      ji=nalsp(m,i)
      jj=nalsp(m,j)
      ki=ji-notsi
      kj=jj-notsj
      do 481 mp=mmin,m
      jpi=nalsp(mp,i)
      jpj=nalsp(mp,j)
      kpi=jpi-notsi
      kpj=jpj-notsj
      nopc=nopc+1
      pc(nopc)=0.0
      do 417 ip=1,nosubc
      if (ip-i) 414,417,413
  412 if (nalsp(m,ip)-nalsp(mp,ip)) 481,417,481
  413 if (ip-j) 412,415,414
  414 if (nalsp(m,ip)-nalsp(mp,ip)) 481,415,481
  415 if (pscrl(m,ip)-pscrl(mp,ip)) 481,416,481
  416 if (pscrs(m,ip)-pscrs(mp,ip)) 481,417,481
  417 continue
c
      do 450 iii=1,2
      mm=m
      if (iii.eq.2) mm=mp
      do 450 ip=1,nosubc
      ii=nalsp(mm,ip)
      tl(iii,ip)=fl(ii,ip)
      ts(iii,ip)=s(ii,ip)
      tscl(iii,ip)=pscrl(mm,ip)
  450 tscs(iii,ip)=pscrs(mm,ip)
      fllrho=fll(i)
      fllrhop=fll(i)
      fllsig=fll(j)
      fllsigp=fll(j)
      tk=fk
      call reij(i,j)
c
      pc(nopc)=cij*rsum
      if (m.ne.mp) go to 481
      pc(nopc)=pc(nopc)+cave
  481 continue
c
      if (icpc.le.1.or.icpc.eq.3) go to 482
      n2=nopc-m+mmin
      write (iw,17) ncfgp(m),nopc,muls1(m),lhs1(m),muls4(m),
     1  lhs4(m), (pc(n1), n1=n2,nopc)
      if (icpc.lt.5) go to 482
      lfg=lfg+1
      vfg(lfg,nfg)=pc(nopc)
      write (idfg(nfg),47) k,i,llijk(i,1,1),j,llijk(j,1,1)
   47 format (1hg,i1,1h(,i2,a1,1h,,i2,a1,1h))
  482 continue
  483 continue
      npar=npar+1
      kpar=0
      write (aa,48) k,i,j
   48 format (1hg,i1,1h(,2i1,5h)    )
      parnam(npar,kk)=aa
      write (20) npar,kpar,k,i,j,aa,cave,j1,nopc, (pc(n1), n1=1,nopc)
      if (icpc.eq.0) go to 485
      call clock(time)
      delt=time-time0
      write (iw,18) aa,nopc,cave,delt, (ll(l),ni(l), l=1,nosubc)
  485 continue
  489 continue
  497 continue
c
  498 nparj(j1,j1)=npar-nparjo
      nparjo=npar
  499 continue
      if (icpc.lt.5) go to 900
c
c          Write RCN input coefficients for LS-dependent H-F calcns.
c
      do 510 k=1,lfg
      m1=2.0*pscrs(k,1)+1.0
      l1=pscrl(k,1)
      l1=lsymb(l1+1)
      m=2.0*pscrs(k,nosubc)+1.0
      l=pscrl(k,nosubc)
      l=lsymb(l+1)
  510 write (11,51) llijk(1,1,1),nijk(1,1,1),m1,l1,llijk(2,1,1),
     1  m,l,nfg,(vfg(k,j),idfg(j),j=1,nfg)
!      write (150,51) llijk(1,1,1),nijk(1,1,1),m1,l1,llijk(2,1,1),
!     1  m,l,nfg,(vfg(k,j),idfg(j),j=1,nfg)
      write(150,*) llijk(1,1,1),(vfg(k,j),idfg(j),j=1,nfg)
   51 format (a1,i1,1h(,i1,a1,1h),a1,i2,a1,i5,5x,3(f9.5,a11)/
     1  (4(f9.5,a11)))
      write (11,28)
c
  900 return
      end
      subroutine rdij(i,j)
c
c          Calculate Coulomb direct coeffs. rd(i,j)
c
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kiser),pci(kiser)
      dimension nparj(kc,kc),iser(kiser)
      equivalence (dumlc4,nparj),(dumlc4(kc**2+1),iser)
      common/c3lcd/dumlcd
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      dimension cfp1(klsp1,klsp1)
      equivalence (cfp1,cfgp1)
c
      n=tk+1.0
      a=zero
      do 200 ii=i,j
      if (ts(1,ii).ne.ts(2,ii)) go to 399
      if (tscs(1,ii).ne.tscs(2,ii)) go to 399
  200 continue
  300 ixx=tl(1,j)+tscl(2,j-1)+tscl(1,j)
      a=(-one)**ixx
      a=a*s6j(tscl(1,j-1),tscl(2,j-1),tk, tl(2,j),tl(1,j),tscl(1,j))
      mn=i+1
      mx=j-1
      if (mn-mx) 350,350,352
  350 do 351 m1=mn,mx
  351 a=a*uncpla(tscl(1,m1-1),tl(1,m1),tscl(1,m1),
     1    tk,tscl(2,m1-1),tscl(2,m1))
  352 if (i-1) 366,366,355
  355 a=a*uncplb(tscl(1,i-1),tl(1,i),tscl(1,i), tk,tl(2,i),tscl(2,i))
  366 if (nii.eq.1) go to 380
      if (irho.ne.0) go to 371
      go  to (371,372,373,374,375,376) i
  371 a=a*u1(ki,kpi,n)
      go to 380
  372 a=a*u2(ki,kpi,n)
      go to 380
  373 a=a*u3(ki,kpi,n)
      go to 380
  374 a=a*u4(ki,kpi,n)
      go to 380
  375 a=a*u5(ki,kpi,n)
      go to 380
  376 a=a*u6(ki,kpi,n)
  380 if (nij.eq.1) go to 399
      if (irho.ne.0) go to 381
      go to (381,382,383,384,385,386) j
  381 a=a*u1(kj,kpj,n)
      go to 399
  382 a=a*u2(kj,kpj,n)
      go to 399
  383 a=a*u3(kj,kpj,n)
      go to 399
  384 a=a*u4(kj,kpj,n)
      go to 399
  385 a=a*u5(kj,kpj,n)
      go to 399
  386 a=a*u6(kj,kpj,n)
  399 continue
c
      return
      end
      subroutine reij(i,j)
c
c          Calculate Coulomb exchange coeffs. re(i,j)
c
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kiser),pci(kiser)
      dimension nparj(kc,kc),iser(kiser)
      equivalence (dumlc4,nparj),(dumlc4(kc**2+1),iser)
      common/c3lcd/dumlcd
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      dimension cfp1(klsp1,klsp1)
      equivalence (cfp1,cfgp1)
c
      data sqrt3h/1.224744871/
c
  400 ixx=tl(1,j)+tscl(2,j-1)+tscl(1,j)
      ar=(-one)**ixx
      ixx=ts(1,j)+tscs(2,j-1)+tscs(1,j)
      a1r=(-one)**ixx
      a1r=a1r*s6j(tscs(1,j-1),ts(1,j),tscs(1,j),ts(2,j),tscs(2,j-1),
     1  one)
      mn=i+1
      mx=j-1
      if (mn-mx) 420,420,422
  420 do 421 m1=mn,mx
      ixx=tscl(1,m1-1)+tl(1,m1)+tscl(2,m1)
      if (mod(ixx,2).gt.0) ar=-ar
      ar=ar*sqrt((2.0*tscl(1,m1)+1.0)*(2.0*tscl(2,m1)+1.0))
  421 a1r=a1r*uncpla(tscs(1,m1-1),ts(1,m1),tscs(1,m1),
     1      one,tscs(2,m1-1),tscs(2,m1))
  422 if (i-1) 430,430,425
  425 ixx=tscl(1,i-1)+tscl(1,i)+tl(2,i)
      if (mod(ixx,2).gt.0) ar=-ar
      ar=ar*sqrt((2.0*tscl(1,i)+1.0)*(2.0*tscl(2,i)+1.0))
      a1r=a1r*uncplb(tscs(1,i-1),ts(1,i),tscs(1,i),
     1      one,ts(2,i),tscs(2,i))
  430 a1r=a1r*ar
      do 431 m1=i,mx
      if (tscs(1,m1)-tscs(2,m1)) 433,431,433
  431 continue
      if (ts(1,i)-ts(2,i)) 433,432,433
  432 if (ts(1,j)-ts(2,j)) 433,440,433
  433 ar=zero
c
  440 rsum=zero
      r=kdmin-1
      do 469 irp1=1,irp1mx
      r=r+1.0
      n=r+1.0
      pr=s6j(tscl(1,j-1),tscl(2,j-1),r, tl(2,j),tl(1,j),tscl(1,j))
      p1r=4.0
      if (mn-mx) 443,443,445
  443 do 444 m1=mn,mx
      if (mod(r,two).gt.zero) pr=-pr
  444 pr=pr*s6j(tscl(1,m1-1),tscl(2,m1-1),r,
     1    tscl(2,m1),tscl(1,m1),tl(1,m1))
  445 if (i.le.1) go to 447
      if (mod(r,two).gt.zero) pr=-pr
      pr=pr*s6j(tl(1,i),tl(2,i),r,
     1          tscl(2,i),tscl(1,i),tscl(1,i-1))
  447 p1r=p1r*pr*a1r
      pr=pr*ar
      if (nii.gt.1) go to 450
      p1r=p1r*sqrt3h
      go to 459
  450 if (irho.ne.0) go to 451
      go to(451,452,453,454,455,456) i
  451 pr=pr*u1(ki,kpi,n)
      p1r=p1r*v1(ki,kpi,n)
      go to 459
  452 pr=pr*u2(ki,kpi,n)
      p1r=p1r*v2(ki,kpi,n)
      go to 459
  453 pr=pr*u3(ki,kpi,n)
      p1r=p1r*v3(ki,kpi,n)
      go to 459
  454 pr=pr*u4(ki,kpi,n)
      p1r=p1r*v4(ki,kpi,n)
      go to 459
  455 pr=pr*u5(ki,kpi,n)
      p1r=p1r*v5(ki,kpi,n)
      go to 459
  456 pr=pr*u6(ki,kpi,n)
      p1r=p1r*v6(ki,kpi,n)
  459 if (nij.gt.1) go to 460
      p1r=p1r*sqrt3h
      go to 468
  460 if (irho.ne.0) go to 461
      go to (461,462,463,464,465,466) j
  461 pr=pr*u1(kj,kpj,n)
      p1r=p1r*v1(kj,kpj,n)
      go to 468
  462 pr=pr*u2(kj,kpj,n)
      p1r=p1r*v2(kj,kpj,n)
      go to 468
  463 pr=pr*u3(kj,kpj,n)
      p1r=p1r*v3(kj,kpj,n)
      go to 468
  464 pr=pr*u4(kj,kpj,n)
      p1r=p1r*v4(kj,kpj,n)
      go to 468
  465 pr=pr*u5(kj,kpj,n)
      p1r=p1r*v5(kj,kpj,n)
      go to 468
  466 pr=pr*u6(kj,kpj,n)
      p1r=p1r*v6(kj,kpj,n)
  468 b=(2.0*r+1.0)*s6j(fllrho,fllrhop,r, fllsig,fllsigp,tk)
      if (mod(r,two).gt.zero) b=-b
      rsum=rsum+b*(pr+p1r)
  469 continue
      rsum=-0.5*rsum
c
      return
      end
c     overlay(g9,5,0)
      subroutine prk
c
c          Calc. preliminary configuration-interaction matrix elements
c
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      parameter (kcc=kiser/4,klc4=2*kiser+1)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kcc*8),cc(kcc,8)
      dimension nparj(kc,kc)
      equivalence (dumlc4,nparj)
      common/c3lcd/dumlcd
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      common/sortdum/dum(2),idum(2)
      character*10 parnam(kpr,2),aa
      character*8 fidls(kmx,2),fidjj(kmx,2),ldes(kmx),ldesp(kmx)
      common/char/parnam,fidls,fidjj,ldes,ldesp
      dimension cfp1(klsp1,klsp1),nopccc(klc1)
      equivalence (cfp1,cfgp1),(dumlc3,nopccc)
      dimension intest(80),ddjj(kmx,1)
      common/djj/ddjj
c
c
c     ks=8
c     kcc=2500
c     klc1=78**2-(17**2)*9
c     kpc=90000
c     nktotx=locf(ccc(1))-locf(cijr(1))
c          nktotx=dimension of cijr and ccc
c
      nktotx=8
      npcx=kpc
      nccx=klc1
c
      nparjo=npar
      j1x=nsconf(2,kk)
      if (j1x.le.1) go to 900
      do 400 i=1,80
  400 intest(i)=0
      if (nsconf(3,kk).ne.0) go to 500
      read (ir,50) (intest(i),i=1,80)
      write(122,50) (intest(i),i=1,80)
   50 format (80i1)
c
c
c          Calculate rk(i,j)
c
  500 j1xm1=j1x-1
      noccx=0
      jtest=0
      do 799 j1a=1,j1xm1
      j1ap1=j1a+1
      do 799 j1b=j1ap1,j1x
      jtest=jtest+1
      nparj(j1a,j1b)=0
      if (nsconf(3,kk).eq.0.and.intest(jtest).eq.0) go to 799
      if (nsconf(3,kk).gt.0.and.j1b.gt.j1a+nsconf(3,kk)) go to 799
      if (nsconf(3,kk).eq.-9.and.(j1a.eq.1.or.j1b.eq.j1a+1)) go to 501
      if (nsconf(3,kk).eq.-9) go to 799
      if (nsconf(3,kk).eq.-8) go to 501
      if (nsconf(3,kk).lt.0.and.j1a.gt.max0(-nsconf(3,kk),ipct))
     1  go to 799
  501 do 798 irho=1,nosubc
      irs(1)=irho
      do 798 isig=irho,nosubc
      irs(2)=isig
      do 798 irhop=1,nosubc
      irs(3)=irhop
      do 797 isigp=irhop,nosubc
      irs(4)=isigp
      fllsig=fllijk(isig,j1a,kk)
      fllsigp=fllijk(isigp,j1b,kk)
c              Check whether irho...isigp is a possible set 
c                      of interacting electrons
      if (isig.eq.nosubc.or.isigp.eq.nosubc) go to 1501
      if (nijk(nosubc,j1a,kk).eq.1.and.nijk(nosubc,j1b,kk).eq.1.and.
     1  fllijk(nosubc,j1a,kk).ne.fllijk(nosubc,j1b,kk)) go to 797
 1501 if (irho.ne.irhop.or.isig.ne.isigp) go to 503
      nn=0
      do 502 i=isig,nosubc
  502 nn=nn+nijk(i,j1a,kk)+nijk(i,j1b,kk)
      if (nn.gt.2) go to 797
  503 do 504 i=1,nosubc
      nijkp(i,1)=nijk(i,j1a,kk)
  504 nijkp(i,2)=nijk(i,j1b,kk)
      nijkp(irho,1)=nijkp(irho,1)-1
      nijkp(isig,1)=nijkp(isig,1)-1
      nijkp(irhop,2)=nijkp(irhop,2)-1
      nijkp(isigp,2)=nijkp(isigp,2)-1
      do 505 i=1,nosubc
      if (nijkp(i,1).ne.nijkp(i,2)) go to 797
  505 if (nijkp(i,1).lt.0) go to 797
c
      kdmin=max(abs(fll(irho)-fll(irhop)),abs(fllsig-fllsigp))
      kdmax=min(abs(fll(irho)+fll(irhop)),abs(fllsig+fllsigp))
      nkd=(kdmax-kdmin)/2+1
      kemin=max(abs(fll(irho)-fllsigp),abs(fllsig-fll(irhop)))
      nke=nkd
      if (irho.eq.isig.or.irhop.eq.isigp) nke=0
      if (nkd.le.0) go to 797
      irp1mx=kdmax-kdmin+1
      nktot=nkd+nke
      if (nktot.le.nktotx) go to 506
      write (iw,51) nktot,nktotx
   51 format (///12h0*****nktot=,i7,29h is greater than dim of cijr=,i7,
     1  6h *****///)
      stop '(prk 51)'
  506 fk=kdmin-2
      do 507 nn=1,nkd
      fk=fk+2.0
  507 cijr(nn)=cijkf(fll(irho),fll(irhop),fk)
     1  *cijkf(fllsig,fllsigp,fk)
      if (nke.le.0) go to 509
      fk=kemin-2
      n1=nkd+1
      do 508 nn=n1,nktot
      fk=fk+2.0
  508 cijr(nn)=cijkf(fll(irho),fllsigp,fk)
     1  *cijkf(fll(irhop),fllsig,fk)
  509 continue
c
      do 511 i=1,4
  511 pc(i)=irs(i)
      call sort2(4,0,pc,pc(5),idum,dum,idum,idum,dum,dum,dum,dum,dum,
     1  dum,dum,dum)
      in=pc(1)
      ix=pc(2)
      jn=pc(3)
      jx=pc(4)
c
c          Determine class of configuration interaction
c
      i=1
      j=3
      if (irho.le.irhop) go to 521
      i=3
      j=1
  521 neqp1=1
      do 522 k=1,3
      kp1=k+1
      do 522 l=kp1,4
  522 if (irs(k).eq.irs(l)) neqp1=neqp1+1
      iclass=0
      go to (526,525,524,523), neqp1
  523 iclass=1
      go to 527
  524 iclass=2
      if (irho.eq.irhop) iclass=11
      if (iclass.eq.11.and.fllsig.ne.fllsigp) iclass=6
      go to 527
  525 if (irs(i).eq.irs(i+1).and.irs(i).lt.irs(j)) iclass=3
      if (irs(j).eq.irs(j+1).and.irs(j).lt.irs(i+1)) iclass=4
      if (irs(j).eq.irs(j+1).and.irs(j).gt.irs(i+1)) iclass=5
      if (irs(i).eq.irs(j)) iclass=6
      if (irs(i+1).eq.irs(j)) iclass=7
      if (irs(i+1).eq.irs(j+1)) iclass=8
      if (iclass.eq.8.and.fllsig.ne.fllsigp) iclass=10
      go to 527
  526 if (irs(i+1).lt.irs(j)) iclass=9
      if (irs(j).lt.irs(i+1)) iclass=10
c
c          Determine whether configs are to be transposed (itrnsp=2)
c
  527 itrnsp=1
      if (iclass.eq.2.and.irho.lt.irhop) go to 530
      if (irhop.eq.isigp) go to 528
      if (irho.eq.isig) go to 530
      if (irho.lt.irhop) go to 530
      if (irho.eq.irhop.and.isig.le.isigp) go to 530
  528 itrnsp=2
c
c          Read reduced matrix elements U,V from disk 73
c
  530 j=0
      if (isig.eq.irhop.or.isig.eq.isigp) j=isig
      if (irho.eq.irhop.or.irho.eq.isigp) j=irho
      if (j.eq.0) go to 540
      nj=min0(nijk(j,j1a,kk),nijk(j,j1b,kk))
      nii=nj
      nij=nj
      if (nj.le.1) go to 540
      nfull=4.0*fll(j)+2.0
      if (nj.eq.nfull) go to 797
      call locdsk(id3,fll(j),nj)
      nor=norcd/2
      do 533 k=1,nor
  533 read (id3) n, ((u1(ii,jj,k),ii=1,nlt), jj=1,nlt)
      do 534 k=1,nor
  534 read (id3) n, ((v1(ii,jj,k),ii=1,nlt), jj=1,nlt)
c
c          Read cfp or cfgp from disk 72
c
  540 do 565 i=1,nosubc
      ndel(i)=iabs(nijk(i,j1a,kk)-nijk(i,j1b,kk))
      if (ndel(i).eq.0.or.ndel(i).gt.2) go to 565
      ifl(i)=max0(nijk(i,j1a,kk),nijk(i,j1b,kk))
      if (ndel(i).eq.1.and.ifl(i).le.2) go to 565
      call locdsk(id2,fll(i),ifl(i))
      read (id2) (ia,ia,ia,a,a, m=1,nlt), nlp,nlgp,nocfp,nocfgp
      if (nocfp.eq.0) go to 555
      if (ifl(i).gt.2.and.ndel(i).eq.1) go to 545
      read (id2)
      go to 554
  545 if (i.gt.1) go to 550
      read (id2) ((cfp1(m,n), m=1,nlt), n=1,nlp)
      go to 554
  550 read (id2) ((cfp2(m,n,i-1), m=1,nlt), n=1,nlp)
  554 read (id2)
  555 if (ndel(i).ne.2) go to 565
      read (id2)
      n=1.0+min(fll(irho)+fllsig, fll(irhop)+fllsigp)
      if (i.gt.in) go to 561
      do 560 k=1,n
  560 read (id2) ((cfgp1(m,l,k), m=1,nlt), l=1,nlgp)
      go to 565
  561 do 562 k=1,n
  562 read (id2) ((cfgp2(m,l,k), m=1,nlt), l=1,nlgp)
  565 continue
c
      tc0=1.0
      ixx=0
      do 570 i=irho,isig
  570 if (i.gt.irho) ixx=ixx+nijk(i,j1a,kk)
      do 571 i=irhop,isigp
  571 if (i.gt.irhop) ixx=ixx+nijk(i,j1b,kk)
      if (irho.eq.isig) ixx=ixx+1
      if (irhop.eq.isigp) ixx=ixx+1
      ixx=mod(ixx,2)
      if (ixx.gt.0) tc0=-tc0
      n=nijk(irho,j1a,kk)
      n1=n*nijk(isig,j1a,kk)
      if (irho.eq.isig) n1=(n1*(n-1))/n
      n=nijk(irhop,j1b,kk)
      n1=n1*n*nijk(isigp,j1b,kk)
      if (irhop.eq.isigp) n1=(n1*(n-1))/n
      if (j.gt.0) n1=n1/(nj*nj)
      eras=n1
      tc0=tc0*sqrt(eras)
      if (irho.eq.isig.and.irhop.eq.isigp) tc0=0.5*tc0
c
c          Calculate matrix elements
c
  600 ln=ntottj(j1a)+1
      lx=ntottj(j1a+1)
      lpn=ntottj(j1b)+1
      lpx=ntottj(j1b+1)
      nopc=0
      do 700 lp=lpn,lpx
      do 700 l=ln,lx
      if (pscrl(l,nosubc).ne.pscrl(lp,nosubc)) go to 700
      if (pscrs(l,nosubc).ne.pscrs(lp,nosubc)) go to 700
      nopc=nopc+1
      tc=0.0
      do 610 i=1,nosubc
      if (i.lt.in) go to 605
      if (i.lt.jx) go to 606
  605 if (pscrl(l,i).ne.pscrl(lp,i)) go to 690
      if (pscrs(l,i).ne.pscrs(lp,i)) go to 690
  606 do 607 j=1,4
  607 if (i.eq.irs(j)) go to 610
      if (nalsp(l,i)-notsj1(i,j1a).ne.nalsp(lp,i)-notsj1(i,j1b))goto 690
  610 continue
c          Multiply by cfp
      tc=tc0
      do 630 i=1,nosubc
      if (ndel(i).ne.1) go to 630
      if (ifl(i).le.2) go to 630
      if (iclass.eq.1.and.i.eq.ix) go to 630
      l1=l
      l2=lp
      j11=j1a
      j12=j1b
      if (nijk(i,j1a,kk).gt.nijk(i,j1b,kk)) go to 622
      l1=lp
      l2=l
      j11=j1b
      j12=j1a
  622 n1=nalsp(l1,i)-notsj1(i,j11)
      n2=nalsp(l2,i)-notsj1(i,j12)
      if (i.gt.1) go to 627
      tc=tc*cfp1(n1,n2)
      go to 630
  627 tc=tc*cfp2(n1,n2,i-1)
  630 continue
c
      if (tc.eq.0.0) go to 690
c
      l1=l
      l2=lp
      j11=j1a
      j12=j1b
      if (irho.lt.irhop) go to 635
      l1=lp
      l2=l
      j11=j1b
      j12=j1a
  635 if (in.eq.1.or.in.eq.ix) go to 640
      if (nijk(in,j11,kk).le.1) go to 640
      m=in
      n1=nalsp(l1,m)
      n2=nalsp(l2,m)
      tc=tc*recpsh(pscrl(l1,m-1),fl(n2,m),pscrl(l2,m),fll(m),
     1    pscrl(l1,m),fl(n1,m)) *recpsh(pscrs(l1,m-1),s(n2,m),
     2  pscrs(l2,m),half,pscrs(l1,m),s(n1,m))
      if (tc.eq.0.0) go to 690
c
  640 mn=in+1
      mx=ix-1
      if (mn.gt.mx) go to 650
      do 645 m=mn,mx
      n1=nalsp(l1,m)
      n2=nalsp(l2,m)
      tc=tc*recpex(pscrl(l2,m-1),fll(in),pscrl(l1,m-1),fl(n1,m),
     1  pscrl(l1,m),pscrl(l2,m)) *recpex(pscrs(l2,m-1),half,
     2  pscrs(l1,m-1),s(n1,m),pscrs(l1,m),pscrs(l2,m))
  645 continue
      if (tc.eq.0.0) go to 690
c
  650 l1=l
      l2=lp
      j11=j1a
      j12=j1b
      flljx=fllsig
      if (isig.gt.isigp) go to 655
      l1=lp
      l2=l
      j11=j1b
      j12=j1a
      flljx=fllsigp
  655 if (jn.ge.jx) go to 660
      if (nijk(jx,j11,kk).le.1) go to 660
      m=jx
      n1=nalsp(l1,m)
      n2=nalsp(l2,m)
      tc=tc*recpjp(pscrl(l1,m-1),flljx,pscrl(l2,m-1),fl(n2,m),
     1  pscrl(l1,m),fl(n1,m)) *recpjp(pscrs(l1,m-1),half,
     2  pscrs(l2,m-1),s(n2,m),pscrs(l1,m),s(n1,m))
      if (tc.eq.0.0) go to 690
c
  660 mn=jn+1
      mx=jx-1
      if (mn.gt.mx) go to 670
      flljx=fllijk(jx,j11,kk)
      do 665 m=mn,mx
      n1=nalsp(l1,m)
      n2=nalsp(l2,m)
      tc=tc*recpex(pscrl(l1,m-1),fl(n1,m),pscrl(l1,m),flljx,
     1  pscrl(l2,m),pscrl(l2,m-1)) *recpex(pscrs(l1,m-1),s(n1,m),
     2  pscrs(l1,m),half,pscrs(l2,m),pscrs(l2,m-1))
  665 continue
  670 continue
c
  690 pc(nopc)=tc
  700 continue
      if (nopc.le.npcx) go to 701
      write (iw,70) nopc,npcx
   70 format (///11h0*****nopc=,i7,27h is greater than dim of pc=,i7,
     1  6h *****///)
      stop '(prk 70)'
c
  701 fllrho=fll(irho)
      fllrhop=fll(irhop)
      if (itrnsp.ne.2) go to 702
      eras=fllrho
      fllrho=fllrhop
      fllrhop=eras
      eras=fllsig
      fllsig=fllsigp
      fllsigp=eras
  702 if (iclass.ne.7) go to 705
      kkk=kdmin
      kdmin=kemin
      kemin=kkk
      eras=fllrho
      fllrho=fllsig
      fllsig=eras
      if (mod(fll(irhop)-fll(irho),two).eq.zero) go to 705
      do 703 nn=1,nkd
  703 cijr(nn)=-cijr(nn)
  705 nopc=0
      nocc=0
      do 780 lp=lpn,lpx
      do 780 l=ln,lx
      if (pscrl(l,nosubc).ne.pscrl(lp,nosubc)) go to 780
      if (pscrs(l,nosubc).ne.pscrs(lp,nosubc)) go to 780
      nopc=nopc+1
      if (pc(nopc).eq.0.0) go to 780
      do 710 nn=1,nktot
  710 ccc(nn)=0.0
      lci=l
      lcip=lp
      if (itrnsp.eq.2) go to 722
      l1=l
      l2=lp
      j11=j1a
      j12=j1b
      go to 730
  722 l1=lp
      l2=l
      j11=j1b
      j12=j1a
  730 go to (731,732,733,734,735,736,737,738,739,740,741), iclass
  731 call class1
      go to 750
  732 call class2
      go to 750
  733 call class3
      go to 750
  734 call class4
      go to 750
  735 call class5
      go to 750
  736 call class6
      go to 750
  737 call class7
      go to 750
  738 call class8
      go to 750
  739 call class9
      go to 750
  740 call clas10
      go to 750
  741 call clas11
  750 continue
c
      nocc=nocc+1
      if (nocc.le.nccx) go to 755
      write (iw,75) nocc,nccx,j1a,j1b,irho,isig,irhop,isigp,ln,l,lx,
     1  lpn,lp,lpx
   75 format (///11h0*****nocc=,i7,31h is greater than dim of nopccc=,
     1  i7,6h *****,10x,2i1,i2,3i1,5x,3i5,5x,3i5///)
      stop '(prk 75)'
  755 nopccc(nocc)=nopc
      do 760 nn=1,nktot
  760 cc(nocc,nn)=pc(nopc)*cijr(nn)*ccc(nn)
  780 continue
      noccx=max(noccx,nocc)
c
      if (iclass.ne.7) go to 781
      kkk=kdmin
      kdmin=kemin
      kemin=kkk
  781 do 790 nn=1,nktot
      cave=0.0
      if (iclass.ne.11) go to 782
      if (nn.le.nkd) go to 782
      a=nijk(irho,j1a,kk)
      cave=0.5*a*cijr(nn)/((2.0*fll(irho)+1.0)*(2.0*fllsig+1.0))
  782 nopc=0
      m=1
      do 784 lp=lpn,lpx
      do 783 l=ln,lx
      if (pscrl(l,nosubc).ne.pscrl(lp,nosubc)) go to 783
      if (pscrs(l,nosubc).ne.pscrs(lp,nosubc)) go to 783
      nopc=nopc+1
      pc(nopc)=0.0
      if (m.gt.nocc) go to 783
      if (nopccc(m).ne.nopc) go to 783
      pc(nopc)=cc(m,nn)
      if ((l-ln).eq.(lp-lpn)) pc(nopc)=pc(nopc)+cave
      m=m+1
  783 continue
  784 continue
      npar=npar+1
      if (nn-nkd) 785,785,786
  785 k=kdmin+2*(nn-1)
      write (aa,77) j1a,j1b,k,irho,isig,irhop,isigp
   77 format (2i2,i1,1hd,4i1)
      go to 787
  786 k=kemin+2*(nn-nkd-1)
      write (aa,78) j1a,j1b,k,irho,isig,irhop,isigp
   78 format (2i2,i1,1he,4i1)
  787 parnam(npar,kk)=aa
      if (icpc.le.2) go to 789
      write (iw,80) aa,cave,iclass
   80 format (1h0,a10,5x,5hcave=,f12.7,15x,16hconf inter class,i3/)
      write (iw,81) (muls1(lp),lhs1(lp),muls4(lp),lhs4(lp),
     1  lp=lpn,lpx)
   81 format (10x,12(3x,1h(,i1,a1,1h),i2,a1)/
     1        12x,12(3x,1h(,i1,a1,1h),i2,a1)/
     2        12x,12(3x,1h(,i1,a1,1h),i2,a1)/
     3        12x,12(3x,1h(,i1,a1,1h),i2,a1))
      nt=0
      k1=1
      do 1788 k=1,ndifft
      nt=nt+ntrmk(k)
      if (nt.eq.ln-1) k1=k+1
      if (nt.eq.lx) k2=k
      if (nt.eq.lpn-1) k1p=k+1
      if (nt.eq.lpx) k2p=k
 1788 continue
      npc2=0
      l2=ln-1
      do 4788 k=k1,k2
      lxn=ntrmk(k)
      l1=l2+1
      l2=l2+lxn
      l2p=lpn-1
      do 2788 kp=k1p,k2p
      l2p=l2p+ntrmk(kp)
      if (pscrl(l2,nosubc).ne.pscrl(l2p,nosubc)) go to 2788
      if (pscrs(l2,nosubc).ne.pscrs(l2p,nosubc)) go to 2788
      go to 3788
 2788 continue
      go to 4788
 3788 npc1=npc2
      npc2=npc2+ntrmk(k)*ntrmk(kp)
      do 788 l=l1,l2
      npc1=npc1+1
  788 write (iw,82) muls1(l),lhs1(l),muls4(l),lhs4(l),
     1  (pc(i), i=npc1,npc2,lxn)
   82 format (2h (,i1,a1,1h),i2,a1,2x,12f10.5/(12x,12f10.5))
 4788 continue
      if (npc2.ne.nopc) write (iw,83) npc2,nopc
   83 format (///16h0*****npc2,nopc=,2i8,6h *****///)
  789 if (icpc.eq.0) go to 1789
      call clock(time)
      delt=time-time0
      write(iw,84) aa,nopc,cave,iclass,delt,(llijk(l,j1a,kk),
     1  nijk(l,j1a,kk),l=1,ks), (llijk(l,j1b,kk),nijk(l,j1b,kk),l=1,ks)
   84 format (/1h ,a10,4x,3hpc(,i5,1h),4x,5hcave=,f12.7,5x,7hiclass=,i2,
     1  6x,5hdelt=,f6.3,4h min,7x, 8(a1,i2,3x)/87x,8(a1,i2,3x))
 1789 kpar=-2
      write (20) npar,kpar,k,j1a,j1b,aa,cave,j,nopc, (pc(i), i=1,nopc)
  790 continue
c
  797 continue
  798 continue
      nparj(j1a,j1b)=npar-nparjo
      nparjo=npar
  799 continue
c
      write (iw,86) noccx
   86 format (//7h0noccx=,i5)
      write (iw,87) npar
   87 format (///1h0,8x,5hnpar=,i4//9x,16hnparj-----------/)
      do 890 i=1,j1x
  890 write (iw,89) i, (nparj(i,j), j=i,j1x)
   89 format (4h j1=,i2,2x,40i3/(8x,40i3))
c
  900 continue
      return
      end
      subroutine class1
c
c          Calculate for irho=isig=irhop.lt.isigp
c                 or for irhop.lt.irho=isig=isigp
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kiser),pci(kiser)
      dimension nparj(kc,kc),iser(kiser)
      equivalence (dumlc4,nparj),(dumlc4(kc**2+1),iser)
      common/c3lcd/dumlcd
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      dimension cfp1(klsp1,klsp1)
      equivalence (cfp1,cfgp1)
c
c
      n1=nalsp(l1,ix)
      n2=nalsp(l2,ix)
      if (ix.eq.1) go to 120
      a1=pscrl(l1,ix-1)
      a2=pscrl(l2,ix-1)
      a3=pscrs(l1,ix-1)
      a4=pscrs(l2,ix-1)
  120 a5=pscrl(l1,ix)
      a6=pscrl(l2,ix)
      a7=pscrs(l1,ix)
      a8=pscrs(l2,ix)
      b1=fl(n1,ix)
      b2=fl(n2,ix)
      b3=s(n1,ix)
      b4=s(n2,ix)
c
      e1=1.0
      if (in.lt.ix) go to 130
      flli=fllsigp
      if (irho.eq.1) go to 141
      e1=recpsh(a1,b2,a6,flli,a5,b1)*recpsh(a3,b4,a8,half,a7,b3)
      go to 140
  130 flli=fll(in)
      e1=-recpjp(a1,flli,a2,b2,a5,b1)*recpjp(a3,half,a4,b4,a7,b3)
  140 if (e1.eq.0.0) go to 900
c
  141 i=1
      j=2
      nii=min0(nijk(ix,j11,kk),nijk(ix,j12,kk))
      nij=1
      tl(2,1)=b2
      ts(2,1)=b4
      tscl(2,1)=b2
      tscs(2,1)=b4
      tl(1,2)=fll(ix)
      ts(1,2)=0.5
      tl(2,2)=flli
      ts(2,2)=0.5
      tscl(1,2)=b1
      tscl(2,2)=b1
      tscs(1,2)=b3
      tscs(2,2)=b3
c
      if (nii-1) 900,144,143
  143 nlp=notsj1(ix,j12+1)-notsj1(ix,j12)
      kpi=n2-notsj1(ix,j12)
      go to 145
  144 nlp=1
      tl(1,1)=fll(ix)
      ts(1,1)=0.5
      tscl(1,1)=fll(ix)
      tscs(1,1)=0.5
      e2=e1
  145 do 200 m=1,nlp
      if (nii.le.1) go to 152
      ki=m
      n=n1-notsj1(ix,j11)
      if (ix.gt.1) go to 150
      e2=e1*cfp1(n,m)
      go to 151
  150 e2=e1*cfp2(n,m,ix-1)
  151 if (e2.eq.0.0) go to 200
      n=m+notsj1(ix,j12)
      tl(1,1)=fl(n,ix)
      ts(1,1)=s(n,ix)
      tscl(1,1)=fl(n,ix)
      tscs(1,1)=s(n,ix)
  152 tk=kdmin-2
      do 160 nn=1,nkd
      tk=tk+2.0
      call rdij(i,j)
      ccc(nn)=ccc(nn)+e2*a
  160 continue
  200 continue
c
  900 return
      end
      subroutine class2
c
c          Calculate for irho=isig.lt.irhop=isigp
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kiser),pci(kiser)
      dimension nparj(kc,kc),iser(kiser)
      equivalence (dumlc4,nparj),(dumlc4(kc**2+1),iser)
      common/c3lcd/dumlcd
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      dimension cfp1(klsp1,klsp1)
      equivalence (cfp1,cfgp1)
c
c
      n1=nalsp(l1,jx)
      n2=nalsp(l2,jx)
      n3=nalsp(l1,in)
      n4=nalsp(l2,in)
      a1=pscrl(l1,jx)
      a2=pscrs(l1,jx)
      a3=pscrl(l1,jx-1)
      a4=pscrl(l2,jx-1)
      a5=pscrs(l1,jx-1)
      a6=pscrs(l2,jx-1)
      b1=fl(n1,jx)
      b2=fl(n2,jx)
      b3=s(n1,jx)
      b4=s(n2,jx)
      b5=fl(n3,in)
      b6=fl(n4,in)
      b7=s(n3,in)
      b8=s(n4,in)
c
      tfl=abs(a3-a4)-1.0
      nmin=tfl+2.0
      nmax=min(2.0*fll(in),2.0*fllsigp,a3+a4)+1.0
      if (nmin.gt.nmax) go to 900
      tfsn=abs(a5-a6)
      tfsx=a5+a6
c
      e1=sqrt((2.0*b2+1.0)*(2.0*b4+1.0)*(2.0*a3+1.0)*(2.0*a5+1.0))
      xx=a4+a6+b2+b4+a1+a2+fll(in)+fllsigp
      if (mod(xx,two).gt.zero) e1=-e1
      mn=in+1
      mx=jx-1
      if (mn.gt.mx) go to 170
      do 150 m=mn,mx
      e1=e1*sqrt((2.0*pscrl(l2,m)+1.0)*(2.0*pscrs(l2,m)+1.0)
     1  *(2.0*pscrl(l1,m-1)+1.0)*(2.0*pscrs(l1,m-1)+1.0))
      i=nalsp(l2,m)
      xx=fl(i,m)+s(i,m)+pscrl(l2,m)+pscrs(l2,m)+pscrl(l1,m-1)
     1  +pscrs(l1,m-1)
      if (mod(xx,two).gt.zero) e1=-e1
  150 continue
  170 if (in.eq.1) go to 200
      a7=pscrl(l1,in)
      a8=pscrl(l2,in)
      a9=pscrs(l1,in)
      a10=pscrs(l2,in)
      a11=pscrl(l1,in-1)
      a12=pscrs(l1,in-1)
      e1=e1*sqrt((2.0*a8+1.0)*(2.0*a10+1.0)*(2.0*b5+1.0)*(2.0*b7+1.0))
      xx=a11+a12+b6+b8+a7+a9
      if (mod(xx,two).gt.zero) e1=-e1
c
  200 i1=n1-notsj1(jx,j11)
      i2=n2-notsj1(jx,j12)
      i3=n3-notsj1(in,j11)
      i4=n4-notsj1(in,j12)
      do 300 n=nmin,nmax
      tfl=tfl+1.0
      tfs=(1+(-1)**n)/2
      if (tfs.lt.tfsn.or.tfs.gt.tfsx) go to 300
      e2=cfgp1(i3,i4,n)*cfgp2(i2,i1,n)
      if (e2.eq.0.0) go to 300
      if (tfs.eq.1.0) e2=-e2
      e2=e1*e2*s6j(b1,tfl,b2, a4,a1,a3)*s6j(b3,tfs,b4, a6,a2,a5)
      if (mn.gt.mx) go to 270
      do 250 m=mn,mx
      i=nalsp(l2,m)
      e2=e2*s6j(fl(i,m),pscrl(l2,m-1),pscrl(l2,m),
     1          tfl,pscrl(l1,m),pscrl(l1,m-1))
  250 e2=e2*s6j(s(i,m),pscrs(l2,m-1),pscrs(l2,m),
     1          tfs,pscrs(l1,m),pscrs(l1,m-1))
  270 if (in.eq.1) go to 280
      e2=e2*s6j(a11,b6,a8, tfl,a7,b5)
      e2=e2*s6j(a12,b8,a10, tfs,a9,b7)
  280 fk=kdmin-2
      do 290 nn=1,nkd
      fk=fk+2.0
  290 ccc(nn)=ccc(nn)
     1  +e2*s6j(fll(in),fll(in),tfl, fllsigp,fllsigp,fk)
  300 continue
c
  900 return
      end
      subroutine class3
c
c          Calculate for irho=isig.lt.irhop.lt.isigp
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kiser),pci(kiser)
      dimension nparj(kc,kc),iser(kiser)
      equivalence (dumlc4,nparj),(dumlc4(kc**2+1),iser)
      common/c3lcd/dumlcd
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      dimension cfp1(klsp1,klsp1)
      equivalence (cfp1,cfgp1)
c
c
      i=in
      j=jn
      n1=nalsp(l1,i)
      n2=nalsp(l2,i)
      tfln=max(abs(fll(j)-fllsigp),abs(fl(n1,i)-fl(n2,i)))
      tfsn=abs(s(n1,i)-s(n2,i))
      tflx=min(fll(j)+fllsigp,2.0*fll(i),fl(n1,i)+fl(n2,i))
      tfsx=min(s(n1,i)+s(n2,i),one)
      jm1=j-1
      do 120 m=i,jm1
      tfln=max(abs(pscrl(l1,m)-pscrl(l2,m)),tfln)
      tfsn=max(abs(pscrs(l1,m)-pscrs(l2,m)),tfsn)
      tflx=min(pscrl(l1,m)+pscrl(l2,m),tflx)
  120 tfsx=min(pscrs(l1,m)+pscrs(l2,m),tfsx)
      if (tfln.gt.tflx) go to 900
      if (tfsn.gt.tfsx) go to 900
c
      n3=nalsp(l1,j)
      n4=nalsp(l2,j)
      a1=pscrl(l1,j-1)
      a2=pscrl(l2,j-1)
      a3=pscrs(l1,j-1)
      a4=pscrs(l2,j-1)
      a5=pscrl(l1,j)
      a6=pscrl(l2,j)
      a7=pscrs(l1,j)
      a8=pscrs(l2,j)
      b1=fl(n3,j)
      b2=fl(n4,j)
      b3=s(n3,j)
      b4=s(n4,j)
c
      e1=sqrt((2.0*b2+1.0)*(2.0*b4+1.0)*(2.0*a1+1.0)*(2.0*a3+1.0)
     1  *(2.0*a6+1.0)*(2.0*a8+1.0))
      xx=fll(i)+fll(j)+fllsigp+0.5+a1+a3-a2-a4+a5+a7-a6-a8
      if (mod(xx,two).ne.zero) e1=-e1
      tfl=tfln-1.0
      nmin=tfln+1.0
      nmax=tflx+1.0
      i1=n1-notsj1(i,j11)
      i2=n2-notsj1(i,j12)
      do 200 n=nmin,nmax
      tfl=tfl+1.0
      tfs=(1+(-1)**n)/2
      if (tfs.lt.tfsn.or.tfs.gt.tfsx) go to 200
      e2=e1
      if (nijk(i,j12,kk).eq.0) go to 130
      e2=e1*cfgp1(i1,i2,n)
      if (e2.eq.0.0) go to 200
  130 if (i.eq.1) go to 140
      a9=pscrl(l1,i-1)
      a10=pscrs(l1,i-1)
      a11=pscrl(l1,i)
      a12=pscrl(l2,i)
      a13=pscrs(l1,i)
      a14=pscrs(l2,i)
      b5=fl(n1,i)
      b6=fl(n2,i)
      b7=s(n1,i)
      b8=s(n2,i)
      xx=a9+a10+b6+b8+a11+a13
      if (mod(xx,two).gt.zero) e2=-e2
      e2=e2*sqrt((2.0*a12+1.0)*(2.0*a14+1.0)*(2.0*b5+1.0)*(2.0*b7+1.0))
      e2=e2*s6j(a9,b6,a12, tfl,a11,b5)*s6j(a10,b8,a14, tfs,a13,b7)
  140 mn=i+1
      mx=j-1
      if (mn.gt.mx) go to 160
      do 150 m=mn,mx
      n5=nalsp(l1,m)
      a9=pscrl(l1,m-1)
      a10=pscrs(l1,m-1)
      a11=pscrl(l2,m)
      a12=pscrs(l2,m)
      b5=fl(n5,m)
      b6=s(n5,m)
      xx=b5+b6+a9+a10+a11+a12
      if (mod(xx,two).gt.zero) e2=-e2
      e2=e2*sqrt((2.0*a9+1.0)*(2.0*a10+1.0)*(2.0*a11+1.0)*(2.0*a12+1.0))
  150 e2=e2*s6j(tfl,pscrl(l2,m-1),a9, b5,pscrl(l1,m),a11)
     1     *s6j(tfs,pscrs(l2,m-1),a10, b6,pscrs(l1,m),a12)
  160 e3=e2*sqrt((2.0*tfl+1.0)*(2.0*tfs+1.0))
      if (tfs.eq.1.0) e3=-e3
      e3=e3*s9j(tfl,fll(j),fllsigp, a2,b2,a6, a1,b1,a5)
     1     *s9j(tfs,half,half, a4,b4,a8, a3,b3,a7)
      fk=kdmin-2
      do 170 nn=1,nkd
      fk=fk+2.0
  170 ccc(nn)=ccc(nn)+e3*s6j(fll(i),fll(i),tfl, fllsigp,fll(j),fk)
  200 continue
c
  900 return
      end
      subroutine class4
c
c          Calculate for irhop.lt.irho=isig.lt.isigp
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kiser),pci(kiser)
      dimension nparj(kc,kc),iser(kiser)
      equivalence (dumlc4,nparj),(dumlc4(kc**2+1),iser)
      common/c3lcd/dumlcd
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      dimension cfp1(klsp1,klsp1)
      equivalence (cfp1,cfgp1)
c
c
  110 m=jn
      n1=nalsp(l1,m)
      n2=nalsp(l2,m)
      a1=pscrl(l1,m-1)
      a2=pscrl(l2,m-1)
      a3=pscrs(l1,m-1)
      a4=pscrs(l2,m-1)
      a5=pscrl(l1,m)
      a6=pscrl(l2,m)
      a7=pscrs(l1,m)
      a8=pscrs(l2,m)
      b1=fl(n1,m)
      b2=fl(n2,m)
      b3=s(n1,m)
      b4=s(n2,m)
      if (abs(a1-a2).gt.fll(in)) go to 900
      if (abs(a5-a6).gt.fllsigp) go to 900
      if (a1+a2.lt.fll(in)) go to 900
      if (a5+a6.lt.fllsigp) go to 900
      if (abs(a3-a4).gt.0.5) go to 900
      if (abs(a7-a8).gt.0.5) go to 900
c
      e1=sqrt((2.0*b1+1.0)*(2.0*b3+1.0)*(2.0*a2+1.0)*(2.0*a4+1.0)
     1  *(2.0*a6+1.0)*(2.0*a8+1.0))
      e2=fll(in)+fllsigp
      fxx=mod(e2+fll(m)+thrhal+a2+a4+a1-a3,two)
      if (fxx.ne.0.0) e1=-e1
c
      tfl=max(abs(fll(in)-fllsigp),abs(b1-b2))-1.0
      nmin=tfl+2.0
      nmax=min(2.0*fll(m),e2,b1+b2)+1.0
      if (nmin.gt.nmax) go to 900
      tfsx=b3+b4
      i1=n1-notsj1(m,j11)
      i2=n2-notsj1(m,j12)
      do 200 n=nmin,nmax
      tfl=tfl+1.0
      e2=cfgp2(i1,i2,n)
      if (e2.eq.0.0) go to 200
      tfs=(1+(-1)**n)/2
      if (tfs.gt.tfsx) go to 200
      if (tfs.eq.1.0) e2=-e2
      e2=e1*e2*sqrt((2.0*tfl+1.0)*(2.0*tfs+1.0))
      e2=e2*s9j(a1,fll(in),a2, a5,fllsigp,a6, b1,tfl,b2)
      e2=e2*s9j(a3,half,a4, a7,half,a8, b3,tfs,b4)
      fk=kdmin-2
      do 150 nn=1,nkd
      fk=fk+2.0
  150 ccc(nn)=ccc(nn)
     1  +e2*s6j(fll(m),fll(m),tfl, fll(in),fllsigp,fk)
  200 continue
c
  900 return
      end
      subroutine class5
c
c          Calculate for irhop.lt.isigp.lt.irho=isig
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kiser),pci(kiser)
      dimension nparj(kc,kc),iser(kiser)
      equivalence (dumlc4,nparj),(dumlc4(kc**2+1),iser)
      common/c3lcd/dumlcd
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      dimension cfp1(klsp1,klsp1)
      equivalence (cfp1,cfgp1)
c
c
      i=ix
      j=jx
      n1=nalsp(l1,j)
      n2=nalsp(l2,j)
      b1=fl(n1,j)
      b2=fl(n2,j)
      b3=s(n1,j)
      b4=s(n2,j)
      tfln=max(abs(fll(i)-fll(in)),abs(b1-b2))
      tfsn=abs(b3-b4)
      tflx=min(fll(i)+fll(in),2.0*fllsig,b1+b2)
      tfsx=min(b3+b4,one)
      do 120 m=i,j
      a1=pscrl(l1,m)
      a2=pscrl(l2,m)
      a3=pscrs(l1,m)
      a4=pscrs(l2,m)
      if (m.eq.j) go to 120
      tfln=max(abs(a1-a2),tfln)
      tfsn=max(abs(a3-a4),tfsn)
      tflx=min(a1+a2,tflx)
      tfsx=min(a3+a4,tfsx)
  120 continue
      if (tfln.gt.tflx) go to 900
      if (tfsn.gt.tfsx) go to 900
c
      n3=nalsp(l1,i)
      n4=nalsp(l2,i)
      a5=pscrl(l1,j-1)
      a6=pscrl(l2,j-1)
      a7=pscrs(l1,j-1)
      a8=pscrs(l2,j-1)
      a9=pscrl(l1,i-1)
      a10=pscrl(l2,i-1)
      a11=pscrs(l1,i-1)
      a12=pscrs(l2,i-1)
      a13=pscrl(l1,i)
      a14=pscrl(l2,i)
      a15=pscrs(l1,i)
      a16=pscrs(l2,i)
      b5=fl(n3,i)
      b6=fl(n4,i)
      b7=s(n3,i)
      b8=s(n4,i)
c
      e1=sqrt((2.0*b6+1.0)*(2.0*b8+1.0)*(2.0*a10+1.0)*(2.0*a12+1.0)
     1  *(2.0*a13+1.0)*(2.0*a15+1.0)*(2.0*b1+1.0)*(2.0*b3+1.0)
     2  *(2.0*a6+1.0)*(2.0*a8+1.0))
      xx=fll(in)+fllsig+a5+a7+b1+b3+a1+a3
      if (mod(xx,two).gt.zero) e1=-e1
      tfl=tfln-1.0
      nmin=tfln+1.0
      nmax=tflx+1.0
      i1=n1-notsj1(j,j11)
      i2=n2-notsj1(j,j12)
      do 200 n=nmin,nmax
      tfl=tfl+1.0
      tfs=(1+(-1)**n)/2
      if (tfs.lt.tfsn.or.tfs.gt.tfsx) go to 200
      e2=e1
      if (nijk(j,j12,kk).eq.0) go to 130
      e2=e1*cfgp2(i1,i2,n)
      if (e2.eq.0.0) go to 200
  130 e3=e2*s6j(b2,tfl,b1, a5,a1,a6)*s6j(b4,tfs,b3, a7,a3,a8)
      mn=i+1
      mx=j-1
      if (mn.gt.mx) go to 160
      do 150 m=mn,mx
      n5=nalsp(l1,m)
      a17=pscrl(l2,m-1)
      a18=pscrs(l2,m-1)
      a19=pscrl(l1,m)
      a20=pscrl(l2,m)
      a21=pscrs(l1,m)
      a22=pscrs(l2,m)
      b9=fl(n5,m)
      b10=s(n5,m)
      xx=b9+b10+a19+a21+a17+a18
      if (mod(xx,two).gt.zero) e3=-e3
      e3=e3*sqrt((2.0*a19+1.0)*(2.0*a21+1.0)*(2.0*a17+1.0)
     1  *(2.0*a18+1.0))
  150 e3=e3*s6j(b9,pscrl(l1,m-1),a19, tfl,a20,a17)
     1    *s6j(b10,pscrs(l1,m-1),a21, tfs,a22,a18)
  160 e4=e3*sqrt((2.0*tfl+1.0)*(2.0*tfs+1.0))
      if (tfs.eq.1.0) e4=-e4
      e4=e4*s9j(a9,fll(in),a10, b5,fll(i),b6, a13,tfl,a14)
     1     *s9j(a11,half,a12, b7,half,b8, a15,tfs,a16)
      fk=kdmin-2
      do 170 nn=1,nkd
      fk=fk+2.0
  170 ccc(nn)=ccc(nn)+e4*s6j(fllsig,fllsig,tfl, fll(i),fll(in),fk)
  200 continue
c
  900 return
      end
      subroutine class6
c
c          Calculate for irho=irhop.lt.isig.lt.isigp
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kiser),pci(kiser)
      dimension nparj(kc,kc),iser(kiser)
      equivalence (dumlc4,nparj),(dumlc4(kc**2+1),iser)
      common/c3lcd/dumlcd
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      dimension cfp1(klsp1,klsp1)
      equivalence (cfp1,cfgp1)
c
  110 m=jn
      n1=nalsp(l1,m)
      n2=nalsp(l2,m)
      a1=pscrl(l1,m-1)
      a2=pscrl(l2,m-1)
      a3=pscrs(l1,m-1)
      a4=pscrs(l2,m-1)
      a5=pscrl(l1,m)
      a6=pscrl(l2,m)
      a7=pscrs(l1,m)
      a8=pscrs(l2,m)
      b1=fl(n1,m)
      b2=fl(n2,m)
      b3=s(n1,m)
      b4=s(n2,m)
      if (jn.lt.nosubc.or.jx.lt.nosubc) go to 115
      a6=a2
      a8=a4
      b1=fllsig
      b2=0.0
      b3=0.5
      b4=0.0
  115 tfl=max(abs(a1-fllsig), abs(a2-fllsigp), abs(b2-a5))-1.0
      nfl=min(a1+fllsig, a2+fllsigp, b2+a5)-tfl
      if (nfl.le.0) go to 300
      tfs=max(abs(a3-0.5), abs(a4-0.5), abs(b4-a7))-1.0
      nfs=min(a3+0.5, a4+0.5, b4+a7)-tfs
      tfsn=tfs
      if (nfs.le.0) go to 300
      xx=a1+b1+a5+b2+fllsigp+a6+a3+b3+a7+b4+0.5+a8
      e1=sqrt((2.0*b1+1.0)*(2.0*a6+1.0)*(2.0*b3+1.0)*(2.0*a8+1.0))
c
      do 200 nl=1,nfl
      tfl=tfl+1.0
      e2=e1*(2.0*tfl+1.0)*s6j(b2,fllsig,b1, a1,a5,tfl)
     1  *s6j(b2,a2,a6, fllsigp,a5,tfl)
      tfs=tfsn
      do 200 ns=1,nfs
      tfs=tfs+1.0
      e3=e2*(2.0*tfs+1.0)*s6j(b4,half,b3, a3,a7,tfs)
     1  *s6j(b4,a4,a8, half,a7,tfs)
      if (mod(xx+tfl+tfs,two).gt.zero) e3=-e3
      do 130 iii=1,2
      l3=l1
      if (iii.eq.2) l3=l2
      mm1=m-1
      do 130 ip=1,mm1
      ii=nalsp(l3,ip)
      tl(iii,ip)=fl(ii,ip)
      ts(iii,ip)=s(ii,ip)
      tscl(iii,ip)=pscrl(l3,ip)
  130 tscs(iii,ip)=pscrs(l3,ip)
      tl(1,m)=fllsig
      ts(1,m)=0.5
      tl(2,m)=fllsigp
      ts(2,m)=0.5
      tscl(1,m)=tfl
      tscs(1,m)=tfs
      tscl(2,m)=tfl
      tscs(2,m)=tfs
      i=irho
      j=m
      nij=1
      ki=nalsp(l1,i)-notsj1(i,j11)
      kpi=nalsp(l2,i)-notsj1(i,j12)
      tk=kdmin-2
      do 150 nn=1,nkd
      tk=tk+2.0
      call rdij(i,j)
      ccc(nn)=ccc(nn)+e3*a
  150 continue
      n1=nkd+1
      tk=kemin-2
      do 160 nn=n1,nktot
      tk=tk+2.0
      call reij(i,j)
      ccc(nn)=ccc(nn)+e3*rsum
  160 continue
  200 continue
c
  300 continue
      return
      end
      subroutine class7
c
c          Calculate for irho.lt.isig=irhop.lt.isigp
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kiser),pci(kiser)
      dimension nparj(kc,kc),iser(kiser)
      equivalence (dumlc4,nparj),(dumlc4(kc**2+1),iser)
      common/c3lcd/dumlcd
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      dimension cfp1(klsp1,klsp1)
      equivalence (cfp1,cfgp1)
c
c
      i=ix
      n1=nalsp(l1,i)
      a1=pscrl(l1,i-1)
      a2=pscrl(l2,i-1)
      a3=pscrs(l1,i-1)
      a4=pscrs(l2,i-1)
      a5=pscrl(l1,i)
      a6=pscrl(l2,i)
      a7=pscrs(l1,i)
      a8=pscrs(l2,i)
      b1=fl(n1,i)
      b2=s(n1,i)
      tfln=max(abs(fll(in)-a5),abs(b1-a2))
      tfsn=max(abs(0.5-a7),abs(b2-a4))
      tflx=min(fll(in)+a5,b1+a2)
      tfsx=min(0.5+a7,b2+a4)
      if (tfln.gt.tflx) go to 900
      if (tfsn.gt.tfsx) go to 900
c
      j=i+1
      nij=1
      n2=nalsp(l2,i)
      ki=n1-notsj1(i,j11)
      kpi=n2-notsj1(i,j12)
      tl(1,i)=b1
      tl(2,i)=fl(n2,i)
      ts(1,i)=b2
      ts(2,i)=s(n2,i)
      tl(1,j)=fll(in)
      tl(2,j)=fllsigp
      ts(1,j)=0.5
      ts(2,j)=0.5
      tscl(1,i-1)=a2
      tscl(2,i-1)=a2
      tscs(1,i-1)=a4
      tscs(2,i-1)=a4
      tscl(2,i)=a6
      tscs(2,i)=a8
      tscl(1,j)=a5
      tscl(2,j)=a5
      tscs(1,j)=a7
      tscs(2,j)=a7
c
      e1=sqrt((2.0*a1+1.0)*(2.0*a3+1.0))
      xx1=fll(in)+0.5+b1+b2+a1+a3
      tfl=tfln-1.0
      nlx=tflx-tfl
      nsx=tfsx-tfsn+1.0
      do 200 nl=1,nlx
      tfl=tfl+1.0
      tscl(1,i)=tfl
      e2=e1*s6j(fll(in),a2,a1, b1,a5,tfl)
      tfs=tfsn-1.0
      do 200 ns=1,nsx
      tfs=tfs+1.0
      tscs(1,i)=tfs
      e3=e2*sqrt((2.0*tfl+1.0)*(2.0*tfs+1.0))
     1  *s6j(half,a4,a3, b2,a7,tfs)
      if (mod(xx1+tfl+tfs,two).gt.zero) e3=-e3
      tk=kemin-2
      do 150 nn=1,nkd
      tk=tk+2.0
      call reij(i,j)
      ccc(nn)=ccc(nn)-e3*rsum
  150 continue
      n1=nkd+1
      tk=kdmin-2
      do 160 nn=n1,nktot
      tk=tk+2.0
      call rdij(i,j)
      ccc(nn)=ccc(nn)-e3*a
  160 continue
  200 continue
c
  900 return
      end
      subroutine class8
c
c          Calculate for irho.lt.irhop.lt.isig=isigp
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kiser),pci(kiser)
      dimension nparj(kc,kc),iser(kiser)
      equivalence (dumlc4,nparj),(dumlc4(kc**2+1),iser)
      common/c3lcd/dumlcd
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      dimension cfp1(klsp1,klsp1)
      equivalence (cfp1,cfgp1)
c
c
      i=ix
      j=jx
      n1=nalsp(l1,i)
      n2=nalsp(l2,i)
      a1=pscrl(l1,i-1)
      a2=pscrl(l2,i-1)
      a3=pscrs(l1,i-1)
      a4=pscrs(l2,i-1)
      a5=pscrl(l1,i)
      a6=pscrl(l2,i)
      a7=pscrs(l1,i)
      a8=pscrs(l2,i)
      b1=fl(n1,i)
      b2=fl(n2,i)
      b3=s(n1,i)
      b4=s(n2,i)
      tfln=max(abs(fll(in)-a5),abs(a2-b1),abs(fll(i)-a6))
      tfsn=max(abs(0.5-a7),abs(a4-b3),abs(0.5-a8))
      tflx=min(fll(in)+a5,a2+b1,fll(i)+a6)
      tfsx=min(0.5+a7,a4+b3,0.5+a8)
      if (tfln.gt.tflx) go to 900
      if (tfsn.gt.tfsx) go to 900
c
      nii=1
      kj=nalsp(l1,j)-notsj1(j,j11)
      kpj=nalsp(l2,j)-notsj1(j,j12)
      do 120 iii=1,2
      l3=l1
      if (iii.eq.2) l3=l2
      do 120 ip=i,j
      ii=nalsp(l3,ip)
      tl(iii,ip)=fl(ii,ip)
      ts(iii,ip)=s(ii,ip)
      tscl(iii,ip)=pscrl(l3,ip)
  120 tscs(iii,ip)=pscrs(l3,ip)
      tl(1,i)=fll(in)
      tl(2,i)=fll(i)
      ts(1,i)=0.5
      ts(2,i)=0.5
c
      e1=sqrt((2.0*a1+1.0)*(2.0*a3+1.0)*(2.0*b2+1.0)*(2.0*b4+1.0))
      xx1=fll(i)-fll(in)+a2+a4-a1-a3+a6+a8
      tfl=tfln-1.0
      nlx=tflx-tfl
      nsx=tfsx-tfsn+1.0
      do 200 nl=1,nlx
      tfl=tfl+1.0
      tscl(1,i-1)=tfl
      tscl(2,i-1)=tfl
      e2=e1*(2.0*tfl+1.0)*s6j(fll(in),a2,a1, b1,a5,tfl)
     1  *s6j(a2,b1,tfl, fll(i),a6,b2)
      tfs=tfsn-1.0
      do 200 ns=1,nsx
      tfs=tfs+1.0
      tscs(1,i-1)=tfs
      tscs(2,i-1)=tfs
      e3=e2*(2.0*tfs+1.0)*s6j(half,a4,a3, b3,a7,tfs)
     1  *s6j(a4,b3,tfs, half,a8,b4)
      if (mod(xx1-tfl-tfs,two).ne.zero) e3=-e3
      tk=kdmin-2
      do 150 nn=1,nkd
      tk=tk+2.0
      call rdij(i,j)
      ccc(nn)=ccc(nn)+e3*a
  150 continue
      n1=nkd+1
      tk=kemin-2
      do 160 nn=n1,nktot
      tk=tk+2.0
      call reij(i,j)
      ccc(nn)=ccc(nn)+e3*rsum
  160 continue
  200 continue
c
  900 return
      end
      subroutine class9
c
c          Calculate for irho.lt.isig.lt.irhop.lt.isigp
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kiser),pci(kiser)
      dimension nparj(kc,kc),iser(kiser)
      equivalence (dumlc4,nparj),(dumlc4(kc**2+1),iser)
      common/c3lcd/dumlcd
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      dimension cfp1(klsp1,klsp1)
      equivalence (cfp1,cfgp1)
c
c
      a1=pscrl(l1,ix-1)
      a2=pscrl(l2,ix-1)
      a3=pscrs(l1,ix-1)
      a4=pscrs(l2,ix-1)
      a5=pscrl(l1,ix)
      a6=pscrl(l2,ix)
      a7=pscrs(l1,ix)
      a8=pscrs(l2,ix)
      a9=pscrl(l1,jn-1)
      a10=pscrl(l2,jn-1)
      a11=pscrs(l1,jn-1)
      a12=pscrs(l2,jn-1)
      a13=pscrl(l1,jn)
      a14=pscrl(l2,jn)
      a15=pscrs(l1,jn)
      a16=pscrs(l2,jn)
      tfln=max(abs(fll(in)-fll(ix)),abs(fll(jn)-fllsigp),abs(a5-a6),
     1  abs(a9-a10))
      tflx=min(fll(in)+fll(ix),fll(jn)+fllsigp,a5+a6,a9+a10)
      if (tfln.gt.tflx) go to 900
      tfsn=max(abs(a7-a8),abs(a11-a12))
      tfsx=min(one,a7+a8,a11+a12)
      if (tfsn.gt.tfsx) go to 900
      n1=nalsp(l1,ix)
      n2=nalsp(l2,ix)
      n3=nalsp(l1,jn)
      n4=nalsp(l2,jn)
      b1=fl(n1,ix)
      b2=fl(n2,ix)
      b3=s(n1,ix)
      b4=s(n2,ix)
      b5=fl(n3,jn)
      b6=fl(n4,jn)
      b7=s(n3,jn)
      b8=s(n4,jn)
      e6=(2.0*a1+1.0)*(2.0*b1+1.0)*(2.0*a6+1.0)*(2.0*a9+1.0)
     1  *(2.0*b6+1.0)*(2.0*a14+1.0)*(2.0*a3+1.0)*(2.0*b3+1.0)
     2  *(2.0*a8+1.0)*(2.0*a11+1.0)*(2.0*b8+1.0)*(2.0*a16+1.0)
      e6=sqrt(e6)
      xx=fllsigp+a9+a13-a10-a14+0.5+a11+a15-a12-a16
      if (mod(xx,two).ne.zero) e6=-e6
      mn=ix+1
      mx=jn-1
c
      tfl=tfln-1.0
      nlx=tflx-tfl
      nsx=tfsx-tfsn+1.0
      do 300 nl=1,nlx
      tfl=tfl+1.0
      e1=e6*s9j(a2,b2,a6,fll(in),fll(ix),tfl,a1,b1,a5)
     1     *s9j(tfl,a10,a9,fll(jn),b6,b5,fllsigp,a14,a13)*(2.0*tfl+1.0)
      if (e1.eq.0.0) go to 300
      if (tfl.eq.0.0) go to 140
      if (mod(tfl,two).ne.zero) e1=-e1
      if (mn.gt.mx) go to 140
      do 130 m=mn,mx
      n5=nalsp(l1,m)
      if (fl(n5,m).eq.0.0) go to 130
      e1=e1*recpex(pscrl(l2,m-1),tfl,pscrl(l1,m-1),fl(n5,m),
     1  pscrl(l1,m),pscrl(l2,m))
  130 continue
      if (e1.eq.0.0) go to 300
  140 tfs=tfsn-1.0
      do 200 ns=1,nsx
      tfs=tfs+1.0
      e2=e1*s9j(a4,b4,a8,half,half,tfs,a3,b3,a7)
     1     *s9j(tfs,a12,a11,half,b8,b7,half,a16,a15)*(2.0*tfs+1.0)
      if (e2.eq.0.0) go to 200
      if (tfs.eq.0.0) go to 155
      if (mod(tfs,two).ne.zero) e2=-e2
      if (mn.gt.mx) go to 155
      do 150 m=mn,mx
      n5=nalsp(l1,m)
      if (s(n5,m).eq.0.0) go to 150
      e2=e2*recpex(pscrs(l2,m-1),tfs,pscrs(l1,m-1),s(n5,m),
     1  pscrs(l1,m),pscrs(l2,m))
  150 continue
      if (e2.eq.0.0) go to 200
  155 tk=kdmin-2
      do 160 nn=1,nkd
      tk=tk+2.0
      e3=e2*s6j(fll(in),fll(ix),tfl,fllsigp,fll(jn),tk)
      if (mod(fll(ix)+fll(jn)+tfl,two).ne.zero) e3=-e3
  160 ccc(nn)=ccc(nn)+e3
      n1=nkd+1
      tk=kemin-2
      do 170 nn=n1,nktot
      tk=tk+2.0
      e3=e2*s6j(fll(in),fll(ix),tfl,fll(jn),fllsigp,tk)
      if (mod(tfs,two).ne.zero) e3=-e3
  170 ccc(nn)=ccc(nn)+e3
  200 continue
  300 continue
c
  900 return
      end
      subroutine clas10
c
c          Calculate for irho.lt.irhop.lt.isig.lt.isigp
c                 or for irho.lt.irhop.lt.isigp.lt.isig
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kiser),pci(kiser)
      dimension nparj(kc,kc),iser(kiser)
      equivalence (dumlc4,nparj),(dumlc4(kc**2+1),iser)
      common/c3lcd/dumlcd
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      dimension cfp1(klsp1,klsp1)
      equivalence (cfp1,cfgp1)
c
c
      flljn=fllsig
      flljx=fllsigp
      if (irho.lt.irhop.and.isig.le.isigp) go to 110
      if (irho.ge.irhop.and.isig.ge.isigp) go to 110
      flljn=fllsigp
      flljx=fllsig
  110 la=l1
      lb=l2
      ja=j11
      jb=j12
      tl(1,jn)=flljn
      tl(2,jn)=flljx
      ts(1,jn)=0.5
      ts(2,jn)=0.5
      if (l1.eq.lci.and.isig.le.isigp) go to 120
      if (l1.eq.lcip.and.isigp.le.isig) go to 120
      la=l2
      lb=l1
      ja=j12
      jb=j11
      tl(1,jn)=flljx
      tl(2,jn)=flljn
c
  120 i=ix
      j=jn
      nii=1
      nij=1
      n1=nalsp(l1,i)
      n2=nalsp(l2,i)
      n3=nalsp(la,j)
      n4=nalsp(lb,j)
      a1=pscrl(l1,i-1)
      a2=pscrl(l2,i-1)
      a3=pscrs(l1,i-1)
      a4=pscrs(l2,i-1)
      a5=pscrl(l1,i)
      a6=pscrl(l2,i)
      a7=pscrs(l1,i)
      a8=pscrs(l2,i)
      a9=pscrl(la,j-1)
      a10=pscrl(lb,j-1)
      a11=pscrs(la,j-1)
      a12=pscrs(lb,j-1)
      a13=pscrl(la,j)
      a14=pscrl(lb,j)
      a15=pscrs(la,j)
      a16=pscrs(lb,j)
      b1=fl(n1,i)
      b2=fl(n2,i)
      b3=s(n1,i)
      b4=s(n2,i)
      b5=fl(n3,j)
      b6=fl(n4,j)
      b7=s(n3,j)
      b8=s(n4,j)
      if (jn.lt.nosubc.or.jx.lt.nosubc) go to 130
      a14=a10
      a16=a12
      b5=flljn
      b6=0.0
      b7=0.5
      b8=0.0
c
  130 tli=max(abs(fll(in)-a5),abs(a2-b1),abs(fll(i)-a6))-1.0
      ntli=min(fll(in)+a5,a2+b1,fll(i)+a6)-tli
      if (ntli.le.0) go to 900
      tljn=max(abs(flljn-a9),abs(a13-b6),abs(flljx-a10))-1.0
      ntlj=min(flljn+a9,a13+b6,flljx+a10)-tljn
      if (ntlj.le.0) go to 900
      tsin=max(abs(0.5-a7),abs(a4-b3),abs(0.5-a8))-1.0
      ntsi=min(0.5+a7,a4+b3,0.5+a8)-tsin
      if (ntsi.le.0) go to 900
      tsjn=max(abs(0.5-a11),abs(a15-b8),abs(0.5-a12))-1.0
      ntsj=min(0.5+a11,a15+b8,0.5+a12)-tsjn
      if (ntsj.le.0) go to 900
c
      jm1=j-1
      do 150 iii=1,2
      m=l1
      if (iii.eq.2) m=l2
      do 150 ip=i,jm1
      ii=nalsp(m,ip)
      tl(iii,ip)=fl(ii,ip)
      ts(iii,ip)=s(ii,ip)
      tscl(iii,ip)=pscrl(m,ip)
  150 tscs(iii,ip)=pscrs(m,ip)
      tl(1,i)=fll(in)
      tl(2,i)=fll(ix)
      ts(1,i)=0.5
      ts(2,i)=0.5
c
      e1=sqrt((2.0*a1+1.0)*(2.0*a3+1.0)*(2.0*b2+1.0)*(2.0*b4+1.0)
     1  *(2.0*b5+1.0)*(2.0*b7+1.0)*(2.0*a14+1.0)*(2.0*a16+1.0))
      xx1=fll(in)+fll(i)+flljx+b1+b1+a1+a2+a6+b5+b6+a9+a13+a14
     1  +1.5+b3+b3+a3+a4+a8+b7+b8+a11+a15+a16
      do 200 nli=1,ntli
      tli=tli+1.0
      e2=e1*(2.0*tli+1.0)*s6j(fll(in),a2,a1, b1,a5,tli)
      e2=e2*s6j(a2,b1,tli, fll(i),a6,b2)
      tscl(1,i-1)=tli
      tscl(2,i-1)=tli
      tlj=tljn
      do 200 nlj=1,ntlj
      tlj=tlj+1.0
      e3=e2*(2.0*tlj+1.0)*s6j(b6,flljn,b5, a9,a13,tlj)
      e3=e3*s6j(b6,a10,a14, flljx,a13,tlj)
      tscl(1,j)=tlj
      tscl(2,j)=tlj
      tsi=tsin
      do 200 nsi=1,ntsi
      tsi=tsi+1.0
      e4=e3*(2.0*tsi+1.0)*s6j(half,a4,a3, b3,a7,tsi)
      e4=e4*s6j(a4,b3,tsi, half,a8,b4)
      tscs(1,i-1)=tsi
      tscs(2,i-1)=tsi
      tsj=tsjn
      do 200 nsj=1,ntsj
      tsj=tsj+1.0
      e5=e4*(2.0*tsj+1.0)*s6j(b8,half,b7, a11,a15,tsj)
      e5=e5*s6j(b8,a12,a16, half,a15,tsj)
      xx=xx1+tli+tlj+tsi+tsj
      if (mod(xx,two).gt.zero) e5=-e5
      tscs(1,j)=tsj
      tscs(2,j)=tsj
      tk=kdmin-2
      do 160 nn=1,nkd
      tk=tk+2.0
      call rdij(i,j)
      ccc(nn)=ccc(nn)+e5*a
  160 continue
      n1=nkd+1
      tk=kemin-2
      do 170 nn=n1,nktot
      tk=tk+2.0
      call reij(i,j)
      ccc(nn)=ccc(nn)+e5*rsum
  170 continue
  200 continue
c
  900 return
      end
      subroutine clas11
c
c          Calculate for irho=irhop, isig=isigp=nosubc, ni(isig)=1
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3/    cfp2(kls2,kls2,7),cijk(10,6),
     1         u2(kls2,kls2,7),u3(kls3,kls3,9),u4(kls4,kls4,9),
     2         v2(kls2,kls2,7),v3(kls3,kls3,7),v4(kls4,kls4,7),
     2  u5(kls5,kls5,7),u6(kls6,kls6,7),v5(kls5,kls5,5),v6(kls6,kls6,5),
     3  nti(41),irp1mx,nalsji(kjp),tfln,tflx,tfsn,tfsx,
     4  pji(kjp),mulsi(kls1),lbcdi(kls1),irho,irhop,isig,isigp,fllrho,
     5  fllsig,in,jn,jx,nii,nij,ki,kj,kpi,kpj,kdmin,kemin,nkd,nke,nktot,
     6  tr,tk,tc,rsum,  j11,j12,l1,l2,tl(2,ks),ts(2,ks),
     7  tscl(2,ks),tscs(2,ks),nijkp(ks,2),irs(ks),ifl(ks),ndel(ks),
     8  cijr(8),ccc(8),n1,n2,n3,n4,e1,e2,e3,
     9  e4,e5,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,b1,b2,b3,b4,b5,b6,
     a  cfgp2(kls2,kls2,7),nalsjp(kjp,ks),pj(kjp,ks)
      common       u1(kls1,kls1,9),dumlc1(klc1)
      common/c3lc2/cfgp1(kls1,kls1,7),pc(kpc),dumlc2(klc2)
      common/c3lc3/v1(kls1,kls1,9),dumlc3(klc1)
      common/c3lc4/dumlc4(kmx**2-kiser),pci(kiser)
      dimension nparj(kc,kc),iser(kiser)
      equivalence (dumlc4,nparj),(dumlc4(kc**2+1),iser)
      common/c3lcd/dumlcd
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks),muls1(klsp),muls4(klsp),
     2  lhs1(klsp),lhs4(klsp)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      dimension cfp1(klsp1,klsp1)
      equivalence (cfp1,cfgp1)
c
  100 i=irho
      j=isig
      nij=1
      ki=nalsp(lci,i)-notsj1(i,j1a)
      kpi=nalsp(lcip,i)-notsj1(i,j1b)
      do 110 iii=1,2
      mm=lci
      if (iii.eq.2) mm=lcip
      do 110 ip=1,nosubc
      ii=nalsp(mm,ip)
      tl(iii,ip)=fl(ii,ip)
      ts(iii,ip)=s(ii,ip)
      tscl(iii,ip)=pscrl(mm,ip)
  110 tscs(iii,ip)=pscrs(mm,ip)
      tk=kdmin-2
      do 150 nn=1,nkd
      tk=tk+2.0
      call rdij(i,j)
      ccc(nn)=a
  150 continue
      n1=nkd+1
      tk=kemin-2
      do 160 nn=n1,nktot
      tk=tk+2.0
      call reij(i,j)
      ccc(nn)=rsum
  160 continue
c
      return
      end
c     overlay(g9,6,0)
      subroutine calcfc
c
c          Set up final coef. matrices, and calc. LS-JJ transf. matrix
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      parameter (kcc=kiser/4)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3a/isubj(kc),muls(ks),lhs(ks),
     1  nals(kmx,ks),ncfg(kmx),nalsj(kmx,ks),scrl(kmx,ks),scrs(kmx,ks),
     2  fj(kmx,ks),scrj(kmx,ks),mul(ks),lh(ks),lf(klsp),nsjk(110),
     3  fk(kmx),fkj(kmx),scrl6(kmx),scrs6(kmx),fk6(kmx),lhqq(kmx),
     4  multqq(kmx),nalsjp(kjp,ks),pj(kjp,ks),noicrd
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      common       c(kmx,kmx)
      common/c3lc2/tmx(kmx,kmx)
      common/c3lc3/ct4(kmx,kmx)
      common/c3lc4/dumlc4(kmx**2-kcc*8),cc(kcc,8)
      dimension nparj(kc,kc)
      equivalence (dumlc4,nparj)
      common/c3lcm/mn1,mx1,mn2,mx2,mn3,mx3,mn4,mx4,mn5,mx5,
     1  mn6,mx6,mn7,mx7,mn8,mx8,sj2,sj3,sj4,sj5,sj6,sj7,sj8
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks)
      character*10 parnam(kpr,2),aa,eav
      character*8 fidls(kmx,2),fidjj(kmx,2),ldes(kmx),ldesp(kmx)
      character*8 fieras
      common/char/parnam,fidls,fidjj,ldes,ldesp
      dimension pc(kiser),v1(kls1,kls1,9),p5(kiser),ip5(kiser)
      equivalence (ct4,pc,v1),(cc,p5,ip5)
      dimension illp(kmx**2),coeff(kmx**2),ddjj(kmx,1)
      common/djj/ddjj
      equivalence (dumlc4,illp),(ct4,coeff)
      data tmxh/3htmx/
      data eav/'eav       '/
c
c
c          Calculate final levels and coefficient matrices
c
c     ks=8
c     kc=50
      j1x=nsconf(2,kk)
      rewind il
      read (il) notsj1,nscrj8,sj8mn,sj8mx,npar,nparj,parnam,
     1  notsx, ((fl(l,i),s(l,i), l=1,notsx), i=1,nosubc),nalsjp,pj
c          write on tape5 input for least-squares program konfit
      if (ictbcd.gt.0) write (19,14)
   14 format (5x,1h )
      if (ictbcd.ge.0) go to 200
c     encode (80,15,p5)
      write (11,15)
   15 format (45h matrix coefficients written by program rcg11,35x)
      backspace 11
      read (11,11) (p5(i),i=1,10)
   11 format (10a8)
      ip5(9)=nscrj8
      ip5(10)=npar
      ip5(11)=j1x
      ip5(12)=2-kcpl
      do 110 i=1,npar
c 110 p5(i+12)=parnam(i,kk)
  110 read (parnam(i,kk),12) p5(i+12)
   12 format (a8,2x)
      j=npar+12
      j1=j
      do 120 i=1,j1x
      j=j+1
c 120 encode (10,16,p5(j)) (llijk(jj,i,kk),nijk(jj,i,kk), jj=1,3)
      write (11,16) (llijk(jj,i,kk),nijk(jj,i,kk), jj=1,3)
   16 format (3(a1,i1,1x))
      backspace 11
      read (11,13) p5(j)
   13 format (a8)
  120 backspace 11
      write (iw,17) (ip5(i),i=1,j1)
   17 format (1x,8a10/1x,4i10/(1x,5a10))
      j1=j1+1
      write (iw,18) (p5(i),i=j1,j)
   18 format (1x,5a10)
c     buffer out (5,1) (p5(1),p5(j))
c     itest5=unit(5)
c
c
  200 scrj8=sj8mn-1.0
      do 900 n=1,nscrj8
      scrj8=scrj8+1.0
      rewind 20
c
c          Set up LS levels
c
      l=0
      mx=0
      do 229 k=1,ndifft
      lf(k)=0
      mn=mx+1
      mx=mx+ntrmk(k)
      sjmn=abs(pscrl(mn,nosubc)-pscrs(mn,nosubc))
      sjmx=pscrl(mn,nosubc)+pscrs(mn,nosubc)
      if (scrj8.lt.sjmn) go to 229
      if (scrj8.gt.sjmx) go to 229
      do 219 m=mn,mx
      l=l+1
      if (l.gt.kmx) go to 219
      ncfg(l)=ncfgp(m)
      do 215 i=1,nosubc
      nals(l,i)=nalsp(m,i)
      scrl(l,i)=pscrl(m,i)
  215 scrs(l,i)=pscrs(m,i)
  219 continue
      lf(k)=1
  229 continue
      nls=l
      if (nls.le.kmx) go to 300
      write (iw,22) scrj8,nls,kmx
   22 format (' For J=',f4.1,',  matrix size',i5,'  is greater than '
     1  'dimension kmx=',i5)
      if (iw6.lt.0) write (6,22) scrj8,nls,kmx
      stop '(calcfc 229)'
c
c          Set up JJ levels
c
  300 if (nolskp.ne.0) go to 350
      l=0
      k=0
      j1=1
      mx1=0
      k1mx=ndiffj(1)
      do 349 k1=1,k1mx
      mn1=mx1+1
      mx1=mx1+njk(k1,1)
      if (nalsjp(mx1,1).gt.notsj1(1,j1+1)) j1=j1+1
      mx2=0
      k2mx=ndiffj(2)
      do 348 k2=1,k2mx
      mn2=mx2+1
      mx2=mx2+njk(k2,2)
      j=nalsjp(mx2,2)
      if (j.le.notsj1(2,j1).or.j.gt.notsj1(2,j1+1)) go to 348
      mx3=0
      k3mx=ndiffj(3)
      do 347 k3=1,k3mx
      mn3=mx3+1
      mx3=mx3+njk(k3,3)
      j=nalsjp(mx3,3)
      if (j.le.notsj1(3,j1).or.j.gt.notsj1(3,j1+1)) go to 347
      mx4=0
      k4mx=ndiffj(4)
      do 346 k4=1,k4mx
      mn4=mx4+1
      mx4=mx4+njk(k4,4)
      j=nalsjp(mx4,4)
      if (j.le.notsj1(4,j1).or.j.gt.notsj1(4,j1+1)) go to 346
      mx5=0
      k5mx=ndiffj(5)
      do 345 k5=1,k5mx
      mn5=mx5+1
      mx5=mx5+njk(k5,5)
      j=nalsjp(mx5,5)
      if (j.le.notsj1(5,j1).or.j.gt.notsj1(5,j1+1)) go to 345
      mx6=0
      k6mx=ndiffj(6)
      do 344 k6=1,k6mx
      mn6=mx6+1
      mx6=mx6+njk(k6,6)
      j=nalsjp(mx6,6)
      if (j.le.notsj1(6,j1).or.j.gt.notsj1(6,j1+1)) go to 344
      mx7=0
      k7mx=ndiffj(7)
      do 343 k7=1,k7mx
      mn7=mx7+1
      mx7=mx7+njk(k7,7)
      j=nalsjp(mx7,7)
      if (j.le.notsj1(7,j1).or.j.gt.notsj1(7,j1+1)) go to 343
      mx8=0
      k8mx=ndiffj(8)
      do 342 k8=1,k8mx
      mn8=mx8+1
      mx8=mx8+njk(k8,8)
      j=nalsjp(mx8,8)
      if (j.le.notsj1(8,j1).or.j.gt.notsj1(8,j1+1)) go to 342
      sj2=abs(pj(mn1,1)-pj(mn2,2))-1.0
      nj2=pj(mn1,1)+pj(mn2,2)-sj2
      do 339 ij2=1,nj2
      sj2=sj2+1.0
      sj3=abs(sj2-pj(mn3,3))-1.0
      nj3=sj2+pj(mn3,3)-sj3
      do 339 ij3=1,nj3
      sj3=sj3+1.0
      sj4=abs(sj3-pj(mn4,4))-1.0
      nj4=sj3+pj(mn4,4)-sj4
      do 339 ij4=1,nj4
      sj4=sj4+1.0
      sj5=abs(sj4-pj(mn5,5))-1.0
      nj5=sj4+pj(mn5,5)-sj5
      do 339 ij5=1,nj5
      sj5=sj5+1.0
      sj6=abs(sj5-pj(mn6,6))-1.0
      nj6=sj5+pj(mn6,6)-sj6
      do 339 ij6=1,nj6
      sj6=sj6+1.0
      sj7=abs(sj6-pj(mn7,7))-1.0
      nj7=sj6+pj(mn7,7)-sj7
      do 339 ij7=1,nj7
      sj7=sj7+1.0
      sj8=abs(sj7-pj(mn8,8))-1.0
      nj8=sj7+pj(mn8,8)-sj8
      do 339 ij8=1,nj8
      sj8=sj8+1.0
      if (sj8.ne.scrj8) go to 339
c
      k=k+1
      nsjk(k)=0
c
c          8-fold do loop (37 lines) moved to subroutine cafcdolp
c               because of VAX-compiler limitations
c
      call cafcdolp(l,k)
c
  339 continue
  342 continue
  343 continue
  344 continue
  345 continue
  346 continue
  347 continue
  348 continue
  349 continue
      ndifsj=k
      njj=l
      if (njj.ne.nls) write (iw,35) nls,njj,scrj8
   35 format (///5h0nls=,i3,5x,5h njj=,i3,5x,11h for scrj8=,f4.1)
      if (nls.le.kmx) go to 350
      write (iw,36) nls,kmx,scrj8
   36 format (///18h0*****matrix size=,i4,
     1  25h  greater than dimension=,i4,'     for scrj8=',f4.1)
      nls=kmx
c
c          Calculate subshell to be used in basis-state labels
c
  350 do 390 j=1,j1x
      isubj(j)=0
      isub=0
      do 380 i=1,nosubc
      i1=nosubc-i+1
      w=nijk(i1,j,kk)
      wfm1=4.0*fllijk(i1,j,kk)+1.0
      if (w.eq.0.0.or.w.gt.wfm1) go to 380
      if (w.eq.1.0.or.w.eq.wfm1) go to 370
      isubj(j)=-i1
      go to 380
  370 if (isubj(j).eq.0.and.i1.lt.isub) isubj(j)=i1
      isub=i1
  380 continue
      if (isubj(j).eq.0) isubj(j)=1
  390 continue
c
c          Write complete quantum numbers,
c               and form basis-state labels
c
      ipt=0
      if (icfc.eq.0) go to 405
      ipt=1
      if (kcpld(1)+kcpld(2).gt.1) ipt=0
      if (kcpld(9).ge.9.or.ispecc.ge.9) ipt=0
      jjj=min0(j1x,9)
      if (ipt.eq.0) go to 400
      if (jjj+nls*((ks+3)/4).gt.55.or.icfc.gt.2) write (iw,37)
   37 format (1h1)
!     output
  400 write(iw,38) scrj8,(j,(llijk(i,j,kk),nijk(i,j,kk),i=1,ks),j=1,jjj)
!       write(101,38)scrj8,(j,(llijk(i,j,kk),nijk(i,j,kk),i=1,ks),j=1,jjj)
   38 format (3h0j=,f4.1,10x,13hconfiguration,i10,4x,8(a1,i2,3x)/
     1  (30x,i10,4x,8(a1,i2,3x)))
      if (j1x.gt.9) write (iw,39)  j1x, (llijk(i,j1x,kk),nijk(i,j1x,kk),
     1  i=1,ks)
   39 format (30x,i10,4x,8(a1,i2,3x))
      write (iw,40)
   40 format (7h ------/)
  405 do 470 l=1,nls
      do 410 i=1,nosubc
      m=nals(l,i)
      mul(i)=mult(m,i)
      lh(i)=lbcd(m,i)
      muls(i)=2.0*scrs(l,i)+1.0
      lp1=scrl(l,i)+1.0
  410 lhs(i)=lsymb(lp1)
      j=ncfg(l)
      i1=iabs(isubj(j))
      mi=mul(i1)
      li=lh(i1)
      if (isubj(j).lt.0) go to 420
      mi=muls(i1)
      li=lhs(i1)
c 420 encode (8,41,fidls(l,1)) mi,li,muls(nosubc),lhs(nosubc)
  420 write (fidls(l,1),41) mi,li,muls(nosubc),lhs(nosubc)
   41 format (1h(,i1,a1,1h),i2,a1,1x)
      if (ipt.eq.0) go to 440
      if (nosubc.le.3) go to 430
      write (iw,42) l, ncfg(l), (nals(l,i),mul(i),lh(i),
     1    muls(i),lhs(i), i=1,nosubc)
	write (106,42) l, ncfg(l), (nals(l,i),mul(i),lh(i),
     1    muls(i),lhs(i), i=1,nosubc)

      write (151,"(1h(,i3,i2,a1,1h),i2,a1,
     1  7(3h  (,i1,i3,a1,1h),i2,a1))")            !SuMG 20120822
     ! (nals(l,i),mul(i),lh(i),muls(i),lhs(i), i=1,nosubc)    !SuMG 20120822

      write (107,42) l, ncfg(l), (nals(l,i),mul(i),lh(i),
     1    muls(i),lhs(i), i=1,nosubc)
C      write (108,42) l, ncfg(l), (nals(l,i),mul(i),lh(i),
C     1    muls(i),lhs(i), i=1,nosubc)
   42 format(1h ,i3,i3,2x,1h(,i3,i2,a1,1h),i2,a1,
     1  7(3h  (,i1,i3,a1,1h),i2,a1))
      go to 440
!     output
  430 write (iw,43) ncfg(l), (nals(l,i),mul(i),lh(i),
     1    muls(i),lhs(i), i=1,nosubc)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
c-----���Ls���-----------6398--------------------------------------------------

	write (106,43) ncfg(l), (nals(l,i),mul(i),lh(i),
     1    muls(i),lhs(i), i=1,nosubc)
      write (151,"(3(1h(,i3,i3,a1,1h),i3,a1,4x))")            !SuMG 20120822
     ! (nals(l,i),mul(i),lh(i),muls(i),lhs(i), i=1,nosubc)    !SuMG 20120822



      write (107,4333) ncfg(l), (nals(l,i),mul(i),lh(i),
     1    muls(i),lhs(i), i=1,nosubc)

C      write (108,4333) ncfg(l), (nals(l,i),mul(i),lh(i),
C     1    muls(i),lhs(i), i=1,nosubc)
 4333 format (i2,3(1h(,i3,i3,a1,1h),i3,a1))
   43 format (1h ,i2,4x,3(1h(,i3,i3,a1,1h),i3,a1,4x))
  440 if (nolskp.ne.0) go to 470
      do 445 i=1,nosubc
      m=nalsj(l,i)
      mul(i)=mult(m,i)
      lh(i)=lbcd(m,i)
  445 continue
      fji=fj(l,i1)
      if (isubj(j).gt.0) fji=scrj(l,i1)
c     encode (8,44,fidjj(l,1)) mul(i1),lh(i1),fji
      write (fidjj(l,1),44) mul(i1),lh(i1),fji
   44 format (1h(,i1,a1,f4.1,1h))
c
      ddjj(l,i1)=fji
c
      if (ipt.eq.0) go to 470
      if (nosubc.gt.4) go to 470
      if (nosubc.le.2) go to 460
      write (iw,45) l,
     1 (nalsj(l,i),mul(i),lh(i),fj(l,i),scrj(l,i), i=1,nosubc)
	 write (106,45) l,
     1 (nalsj(l,i),mul(i),lh(i),fj(l,i),scrj(l,i), i=1,nosubc)
   45 format (1h+,i60,4x,1h(,i3,i2,a1,f4.1,1h),f4.1,
     1  3(3h  (,i2,i2,a1,f4.1,1h),f4.1))

      write (151,"(64x,1h(,i3,i2,a1,f4.1,1h),f4.1,
     1  3(3h  (,i2,i2,a1,f4.1,1h),f4.1))")       !SuMG 20120822
     ! (nalsj(l,i),mul(i),lh(i),fj(l,i),scrj(l,i), i=1,nosubc)   !SuMG 20120822

      go to 470

  460 write (iw,46) l,
     1 (nalsj(l,i),mul(i),lh(i),fj(l,i),scrj(l,i), i=1,nosubc)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!     ���JJ���--------------------------------------------
      write (106,46) l,
     1 (nalsj(l,i),mul(i),lh(i),fj(l,i),scrj(l,i), i=1,nosubc)
      write (151,"(64x,3(4x,1h(,i3,i3,a1,f5.1,1h),f5.1))")       !SuMG 20120822
     ! (nalsj(l,i),mul(i),lh(i),fj(l,i),scrj(l,i), i=1,nosubc)   !SuMG 20120822


	write (108,4666) 
     1 (nalsj(l,i),mul(i),lh(i),fj(l,i),scrj(l,i), i=1,nosubc)
 4666 format (3(1h(,i3,i3,a1,f5.1,1h),f5.1))
   46 format (1h+,i60,3x,3(4x,1h(,i3,i3,a1,f5.1,1h),f5.1))
  470 continue
      if (nolskp.ne.0) go to 595
      if (ipt.eq.0) go to 505
      write (iw,43)
      if (nosubc.le.4) go to 505
      do 472 l=1,nls
      do 471 i=1,nosubc
      m=nalsj(l,i)
      mul(i)=mult(m,i)
  471 lh(i)=lbcd(m,i)
      write (iw,47) l,
     1 (nalsj(l,i),mul(i),lh(i),fj(l,i),scrj(l,i), i=1,nosubc)
c      write (106,47) l,
c     1 (nalsj(l,i),mul(i),lh(i),fj(l,i),scrj(l,i), i=1,nosubc)
   47 format (i5,1x,8(2h (,i2,i2,a1,f4.1,1h),f4.1))
  472 continue
      write (iw,43)
c
c          Calculate transformation matrix
c
  505 do 530 ls=1,nls
      ilssl=scrl(ls,nosubc)+scrs(ls,nosubc)-scrj8
      ilssl=mod(ilssl,2)
      do 530 jj=1,njj
      tmx(ls,jj)=0.0
      do 510 i=1,nosubc
      if (nals(ls,i).ne.nalsj(jj,i)) go to 530
  510 continue
      tmx(ls,jj)=1.0
      if (iabg.ge.3.and.ilssl.ne.0) tmx(ls,jj)=-1.0
      if (nosubc.le.1) go to 530
      do 521 i=2,nosubc
      ml=nals(ls,i)
      if (fl(ml,i).eq.0.0.and.s(ml,i).eq.0.0) go to 521
      if (scrl(ls,i-1).eq.0.0.and.scrs(ls,i-1).eq.0.0) go to 521
      a=sqrt((2.0*scrl(ls,i)+1.0)*(2.0*scrs(ls,i)+1.0)
     1  *(2.0*fj(jj,i)+1.0)*(2.0*scrj(jj,i-1)+1.0))
      b=s9j(scrl(ls,i-1),fl(ml,i),scrl(ls,i), scrs(ls,i-1),
     1  s(ml,i),scrs(ls,i), scrj(jj,i-1),fj(jj,i),scrj(jj,i))
      tmx(ls,jj)=a*b*tmx(ls,jj)
  521 continue
  530 continue
c          Check orthonormality
      if (icfc.le.1) go to 540
      write (iw,53) coupl(1)
   53 format (  27h0Transformation matrix from,a6,15h to jj coupling)
  540 do 550 l=1,nls
      do 550 lp=l,nls
      sum=0.0
      if (l.eq.lp) sum=-1.0
      do 543 m=1,njj
  543 sum=sum+tmx(l,m)*tmx(lp,m)
      if (abs(sum).ge.1.0e-7) write (iw,54) l,lp
   54 format (6h rows ,i3, 5h and ,i3, 16h not orthonormal)
  550 continue
c
      if (icfc.le.1) go to 600
      lpx=0
  560 lpn=lpx+1
      lpx=lpx+11
      if (lpx.gt.njj) lpx=njj
      write (iw,55) (fidjj(lp,1), lp=lpn,lpx)
   55 format (//28x, 11(1x,a8))
      write (iw,56) (lp, lp=lpn,lpx)
   56 format (26x,11i9)
      write (iw,57)
   57 format (1h )
      do 580 l=1,nls
  580 write (iw,58) ncfg(l),fidls(l,1),l, (tmx(l,lp), lp=lpn,lpx)
   58 format (i11,2x,1x,a8,i4,2x,11f9.5)
      if (lpx.lt.njj) go to 560
  595 call clock(time)
      delt=time-time0
      write (iw,59) scrj8,delt
   59 format (///' calcfc, j=',f4.1,5x,5htime=,f6.3,4h min)
      if (iw6.lt.0) write (6,59) scrj8,delt
c
c          Form final coefficient matrices
c
  600 ilc=il
      do 601 nn=1,2
      write (ilc) scrj8,nls, ((tmx(l,lp),l=1,nls), lp=1,nls),
     1  ((nals(l,i),scrl(l,i),scrs(l,i),
     2  i=1,nosubc), ncfg(l),fidls(l,1),fidjj(l,1), l=1,nls)
  601 ilc=ic
      noicwr=noicwr+1
      npar=0
      nc=0
      if (ictbcd.le.0) go to 604
      nx=min0(n,j1x)
      write (19,61) n,nls,scrj8, coupl(kcpl), (llijk(i,nx,kk),
     1  nijk(i,nx,kk), i=1,6)
   61 format (2i6,6h     1,6x,f4.1, 3x,a6,5h cplg,6x, 2(2x,a1,i2),
     1  1x, 4(1x,a1,i1))
c
  604 nparo=npar
      read (20) npar,kpar,k20,i,j,aa,cave,j1,nopc, (pc(n1), n1=1,nopc)
      if (npar.eq.-7) go to 890
      if (ictbcd.eq.0) go to 609
      nparx=npar
      if (npar.eq.nparo+1) go to 609
      nn=-n
      npar20=npar
      npar=nparo+1
  605 nc=nc+1
      parnam(npar,kk)=eav
      do 607 lp=1,nls
      do 606 l=lp,nls
  606 c(l,lp)=0.0
      c(lp,lp)=0.0
      if (ncfg(lp).eq.nc) c(lp,lp)=1.0
  607 continue
      go to 805
  609 parnam(npar,kk)=aa
      j1a=j1
      j1b=j1
  610 do 611 l=1,nls
      do 611 lp=1,l
  611 c(l,lp)=0.0
      if (kpar.gt.0) go to 630
      if (kpar.eq.-2) go to 680
c
c          fk,gk matrix (lower triangle)
c
  620 lx=0
      lmx=0
      m=0
      do 629 k=1,ndifft
      lmx=lmx+ntrmk(k)
      if (ncfgp(lmx).eq.j1) go to 621
      if (lf(k).gt.0) lx=lx+ntrmk(k)
      go to 629
  621 if (lf(k).gt.0) go to 622
      m=m+(ntrmk(k)*(ntrmk(k)+1))/2
      go to 629
  622 ln=lx+1
      lx=lx+ntrmk(k)
      do 625 l=ln,lx
      do 625 lp=ln,l
      m=m+1
  625 c(l,lp)=pc(m)
  629 continue
      go to 690
c
c          zeta matrix (lower triangle)
c
  630 if (kcpl.eq.2) go to 640
c          ls coupling
      j1v=0
      thrhaf=1.5
      sqrt3h=sqrt(thrhaf)
      do 639 l=1,nls
      j=ncfg(l)
      if (j.ne.j1) go to 639
      if (j1v.eq.j) go to 632
      j1v=j
      lij=notsj1(i,j)
      v1(1,1,2)=sqrt3h
      el=fllijk(i,j,kk)
      if (nijk(i,j,kk).eq.1) go to 632
      call locdsk(id3,el,nijk(i,j,kk))
      nor=(norcd/2)+2
      do 631 m=1,nor
  631 read (id3) k, ((v1(ii,jj,2),ii=1,nlt), jj=1,nlt)
  632 do 638 lp=1,l
      if (ncfg(lp).ne.j) go to 638
      k=nosubc
      do 634 m=1,k
      if (m.eq.i) go to 633
      if (nals(l,m).ne.nals(lp,m)) go to 638
      if (m.gt.i) go to 633
      if (scrl(l,m).ne.scrl(lp,m)) go to 638
      if (scrs(l,m).ne.scrs(lp,m)) go to 638
      go to 634
  633 if (abs(scrl(l,m)-scrl(lp,m)).gt.1.0) go to 638
      if (abs(scrs(l,m)-scrs(lp,m)).gt.1.0) go to 638
  634 continue
      eras=1.0
      ii=scrl(lp,k)+scrs(l,k)+scrj8
      if (iabg.ge.3) ii=scrl(l,k)+scrs(lp,k)+scrj8
      if (mod(ii,2).ne.0) eras=-1.0
      eras=eras*s6j(scrl(l,k),scrs(l,k),scrj8,scrs(lp,k),scrl(lp,k),
     1  one)
      if (i.eq.k) go to 636
      ip1=i+1
      do 635 m=ip1,k
      lt=nals(l,m)
  635 eras=eras*uncpla(scrl(l,m-1),fl(lt,m),scrl(l,m),1.d0,scrl(lp,m-1),
     1  scrl(lp,m))*uncpla(scrs(l,m-1),s(lt,m),scrs(l,m),one,
     2  scrs(lp,m-1),scrs(lp,m))
  636 lt=nals(l,i)
      lr=nals(lp,i)
      if (i.gt.1) eras=eras*uncplb(scrl(l,i-1),fl(lt,i),scrl(l,i),
     1  one,fl(lr,i),scrl(lp,i))*uncplb(scrs(l,i-1),s(lt,i),scrs(l,i),
     2  one,s(lr,i),scrs(lp,i))
      c(l,lp)=eras*sqrt(el*(el+1.0)*(2.0*el+1.0))*v1(lt-lij,lr-lij,2)
  638 continue
  639 continue
      go to 690
c          JJ coupling
  640 kix=ndiffj(i)
      lx=0
      do 679 k=1,ndifsj
      ln=lx+1
      lx=lx+nsjk(k)
      j=nalsj(lx,i)
      if (ncfg(ln).ne.j1) go to 679
      ml=1
      mc=1
      do 643 ki=1,kix
      if (ncfgjp(ml,i)-j1) 643,641,644
  641 if (pj(ml,i)-fj(ln,i)) 644,645,642
  642 mc=mc+(njk(ki,i)*(njk(ki,i)+1))/2
  643 ml=ml+njk(ki,i)
  644 write (iw,64) ln,i,fj(ln,i),ml,mc
   64 format (//19h0cannot find pj=fj(,i2,1h,,i1,2h)=,f4.1,
     1  5x,3hml=,i4,5x,3hmc=,i4//)
  645 m1=njk(ki,i)-1
      if (m1.gt.0) go to 655
c            (1 x 1  submatrix)
      do 653 lp=ln,lx
      c(lp,lp)=pc(mc)
  653 continue
      go to 679
c            (n x n  submatrix)
  655 do 656 l=ln,lx
      if (nalsj(l,i).eq.nalsjp(ml+1,i)) go to 657
  656 continue
  657 ldel=l-ln
  660 do 669 l0=ln,lx
      if (nalsj(l0,i).ne.nalsjp(ml,i)) go to 669
      m=mc
      l1=l0+ldel*m1
      do 665 l=l0,l1,ldel
      do 665 lp=l0,l,ldel
      c(l,lp)=pc(m)
      m=m+1
  665 continue
  669 continue
  679 continue
      go to 690
c
c          rk matrix (lower triangle)
c
  680 j1a=i
      j1b=j
      lamn=0
      lamx=0
      lbmx=0
      do 682 l=1,nls
      if (ncfg(l).lt.j1a) lamn=l
      if (ncfg(l).eq.j1a) lamx=l
      if (ncfg(l).lt.j1b) lbmn=l
  682 if (ncfg(l).eq.j1b) lbmx=l
      if (lamx.eq.0.or.lbmx.eq.0) go to 690
      lj=lamn
      lamn=lamn+1
      lbmn=lbmn+1
      lpj=lbmn
c
      ln=ntottj(j1a)+1
      lx=ntottj(j1a+1)
      lpn=ntottj(j1b)+1
      lpx=ntottj(j1b+1)
      nopc=0
      do 688 lp=lpn,lpx
      do 688 l=ln,lx
      itest=0
      if (pscrl(l,nosubc).ne.pscrl(lp,nosubc)) itest=1
      if (pscrs(l,nosubc).ne.pscrs(lp,nosubc)) itest=1
      if (itest.eq.0) nopc=nopc+1
      if (abs(pscrl(l,nosubc)-pscrs(l,nosubc)).gt.scrj8) go to 688
      if (abs(pscrl(lp,nosubc)-pscrs(lp,nosubc)).gt.scrj8) go to 688
      if (pscrl(l,nosubc)+pscrs(l,nosubc).lt.scrj8) go to 688
      if (pscrl(lp,nosubc)+pscrs(lp,nosubc).lt.scrj8) go to 688
      lj=lj+1
      if (lj.le.lamx) go to 686
      lj=lamn
      lpj=lpj+1
      if (lpj.le.lbmx) go to 686
      write (iw,68) j1a,j1b,l,lp,lj,lpj,lamn,lamx,lbmn,lbmx,nopc,
     1  pc(nopc),ln,lx,lpn,lpx
   68 format (//17h0***lpj.gt.lbmx  ,2i5,3x,4i5,3x,4i5,i10,f15.7,5x,4i5)
  686 if (itest.eq.0) c(lpj,lj)=pc(nopc)
  688 continue
c
c
c          Complete matrix (upper triangle)
c
  690 do 691 l=1,nls
      do 691 lp=1,l
  691 c(lp,l)=c(l,lp)
c
c          output
c
  700 k=kc
      nnn=n
      call sprin
c
c          Write matrix coefficients on unit ic
c               (non-zero coefficients only)
c
c 800 write (ic) ((c(l,lp),l=lp,nls), lp=1,nls)
  800 ncoeff=0
      do 801 lp=1,nls
      do 801 l=lp,nls
      if (c(l,lp).eq.0.0) go to 801
      ncoeff=ncoeff+1
      illp(ncoeff)=10000*l+lp
      coeff(ncoeff)=c(l,lp)
  801 continue
      if (ncoeff.gt.0) go to 802
      ncoeff=1
      illp(1)=10001
      coeff(1)=0.0
  802 write (ic) ncoeff,(illp(i),coeff(i),i=1,ncoeff)
      noicwr=noicwr+1
      if (ictbcd.eq.0) go to 604
      nn=n
  805 if (ictbcd.gt.0) go to 870
c          Set up matrix elements for Zeeman-Laboratory
c               least-squares program (KONFIT)
      if (npar.gt.1) go to 870
      i2to18=2**18
      do 810 l=1,nls
      fieras=fidls(l,1)
      if (kcpl.eq.2) fieras=fidjj(l,1)
c     encode (10,81,ip5(l)) ncfg(l),fieras
      write (11,81) ncfg(l),fieras
   81 format (i1,a8)
      backspace 11
      read (11,82) ip5(l)
   82 format (a8)
      backspace 11
  810 continue
      n5=nls
      if (kcpl.ge.2) go to 820
      m=nosubc
      do 815 l=1,nls
      n5=n5+1
      p5(n5)=0.0
      if  (scrj8.eq.0.0) go to 815
      p5(n5)=0.50116*(scrs(l,m)*(scrs(l,m)+1.)-scrl(l,m)*(scrl(l,m)+1.))
     1  /(scrj8*(scrj8+1.0))+1.50116
  815 continue
  820 n4=n5
      rewind 2
      write (2) n4,(p5(k),k=1,n4)
      ncoeff=0
c
  870 n5=0
      do 880 lp=1,nls
      do 879 l=lp,nls
      if (abs(c(l,lp)).le.1.0e-9) go to 879
      if (ictbcd.gt.0) go to 874
      n5=n5+1
      ip5(n5)=((lp*i2to18)+l)*i2to18+npar
      p5(n5+1000)=c(l,lp)
      go to 879
c          Write matrix elements for Argonne NL least-squares program
  874 if (kcpl.le.1) go to 875
      write (19,87) n,lp,l,npar,c(l,lp), nalsj(l,1),fidjj(l,1),
     1  parnam(npar,1)
   87 format (4i6,f12.7, 2h (,i3,1x,a8,2x,a8,3x,3(a1,i2,2x) )
      go to 879
  875 write(19,88) n,lp,l,npar,c(l,lp), nals(l,1),fidls(l,1),
     1  parnam(npar,1)
   88 format (4i6,f12.7, 2h (,i3,1x,a8,2x,a8,3x,3(a1,i2,2x) )
  879 continue
  880 continue
      if (ictbcd.gt.0) go to 888
      write (2) n5,(ip5(k),k=1,n5),(p5(k+1000),k=1,n5)
      ncoeff=ncoeff+n5
      nparx=npar
  888 if (nn.gt.0) go to 604
      nparo=npar
      npar=npar+1
      if (npar.eq.npar20) go to 609
      go to 605
c
  890 if (ictbcd.ge.0) go to 895
      write (iw,89) scrj8,nls,ncoeff
   89 format (1x,f10.1,2i5)
      p5(1)=scrj8
      ip5(2)=nls
      ip5(3)=ncoeff
c     buffer out (5,1) (p5(1),p5(3))
c     itest=unit(5)
      rewind 2
      read (2) n4,(p5(k),k=1,n4)
      n6=n4
      do 892 j=1,nparx
      read (2) n5,(p5(k+n6),k=1,n5),(p5(k+n6+ncoeff),k=1,n5)
  892 n6=n6+n5
      write (iw,90) (p5(k),k=1,nls)
   90 format (1x,5a10)
      if (n4.gt.nls) write (iw,9089) (p5(k+nls),k=1,nls)
 9089 format (1x,5f10.5)
      n4p1=n4+1
      write (iw,9090) (ip5(k),p5(k+ncoeff),k=n4p1,n6)
 9090 format (2(1x,o22,f12.8))
c     buffer out (5,1) (p5(1),p5(n6+ncoeff))
c     itest5=unit(5)
  895 if (ictbcd.gt.0)  write (19,14)
c
      call cpl37
c
c
  900 continue
c           Write dummy record, 
c                (required by system bug on Stretch, upon backspace)
      write (il) (pc(i), i=1,20)
c
      rewind 20
      rewind il
      if (ictbcd.le.0) go to 950
      m=nosubc
      if (kcpl.ne.1) go to 920
      read (il)
      do 915 n=1,nscrj8
      read (il) scrj8,nls,((a,l=1,nls),lp=1,nls),
     1  ((iii,scrl(l,i),scrs(l,i), i=1,m), iii,fieras,fieras, l=1,nls)
      do 910 l=1,nls
      pc(l)=0.0
      if  (scrj8.eq.0.0) go to 910
      pc(l)=0.50116*(scrs(l,m)*(scrs(l,m)+1.0)-scrl(l,m)*(scrl(l,m)+1.))
     1  /(scrj8*(scrj8+1.0))+1.50116
  910 continue
  915 write (19,91) (pc(l),l=1,nls)
   91 format (6f12.6)
      rewind il
  920 read (il)
      do 930 n=1,nscrj8
      read (il) scrj8,nls,((a,l=1,nls), lp=1,nls),
     1  ((iii,a,a, i=1,m), iii,fidls(l,1),fidjj(l,1), l=1,nls)
      if (kcpl.ne.1) go to 925
      write (19,92) (fidls(l,1), l=1,nls)
   92 format (6(1x,a8,1x,:,2x))
      go to 930
  925 write (19,92) (fidjj(l,1), l=1,nls)
  930 continue
      rewind il
      write (19,93) (parnam(i,1), i=1,nparx)
   93 format (6(2x,a10))
      end file 19
      write (iw,96) coupl(kcpl)
   96 format (/44h0coefficient matrices written on tape 19 in ,
     1  a6,9h coupling)
  950 return
      end
      subroutine cafcdolp(l,k)
c
c          8-fold do-loop,
c               moved from calcfc because of VAX-compiler limitations  
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      parameter (kcc=kiser/4)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3a/isubj(kc),muls(ks),lhs(ks),
     1  nals(kmx,ks),ncfg(kmx),nalsj(kmx,ks),scrl(kmx,ks),scrs(kmx,ks),
     2  fj(kmx,ks),scrj(kmx,ks),mul(ks),lh(ks),lf(klsp),nsjk(110),
     3  fk(kmx),fkj(kmx),scrl6(kmx),scrs6(kmx),fk6(kmx),lhqq(kmx),
     4  multqq(kmx),nalsjp(kjp,ks),pj(kjp,ks),noicrd
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      common       c(kmx,kmx)
      common/c3lc2/tmx(kmx,kmx)
      common/c3lc3/ct4(kmx,kmx)
      common/c3lc4/dumlc4(kmx**2-kcc*8),cc(kcc,8)
      dimension nparj(kc,kc)
      equivalence (dumlc4,nparj)
      common/c3lcm/mn1,mx1,mn2,mx2,mn3,mx3,mn4,mx4,mn5,mx5,
     1  mn6,mx6,mn7,mx7,mn8,mx8,sj2,sj3,sj4,sj5,sj6,sj7,sj8
      common  nalsp(klsp,ks),pscrl(klsp,ks),pscrs(klsp,ks),ncfgp(klsp),
     1  njk(kjk,ks),ncfgjp(kjp,ks)
      dimension pc(kiser),v1(kls1,kls1,9),p5(kiser),ip5(kiser)
      equivalence (ct4,pc,v1),(cc,p5,ip5)
      data tmxh/3htmx/
      data eav/3heav/
c
c
c     ks=8
c     kc=50
c
      do 325 m1=mn1,mx1
      do 325 m2=mn2,mx2
      do 325 m3=mn3,mx3
      do 325 m4=mn4,mx4
      do 325 m5=mn5,mx5
      do 325 m6=mn6,mx6
      do 325 m7=mn7,mx7
      do 325 m8=mn8,mx8
      l=l+1
      if (l.gt.kmx) go to 325
      nsjk(k)=nsjk(k)+1
      go to (324,323,322,321,318,317,316,315) nosubc
  315 scrj(l,8)=sj8
      fj(l,8)=pj(m8,8)
      nalsj(l,8)=nalsjp(m8,8)
  316 scrj(l,7)=sj7
      fj(l,7)=pj(m7,7)
      nalsj(l,7)=nalsjp(m7,7)
  317 scrj(l,6)=sj6
      fj(l,6)=pj(m6,6)
      nalsj(l,6)=nalsjp(m6,6)
  318 scrj(l,5)=sj5
      fj(l,5)=pj(m5,5)
      nalsj(l,5)=nalsjp(m5,5)
  321 scrj(l,4)=sj4
      fj(l,4)=pj(m4,4)
      nalsj(l,4)=nalsjp(m4,4)
  322 scrj(l,3)=sj3
      fj(l,3)=pj(m3,3)
      nalsj(l,3)=nalsjp(m3,3)
  323 scrj(l,2)=sj2
      fj(l,2)=pj(m2,2)
      nalsj(l,2)=nalsjp(m2,2)
  324 scrj(l,1)=pj(m1,1)
      fj(l,1)=pj(m1,1)
      nalsj(l,1)=nalsjp(m1,1)
  325 continue
      return
      end
      subroutine cpl37
c
c          Calc. transf. matrices from LS or JJ to representations 3-7
c
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      parameter (kcc=kiser/4)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3a/isubj(kc),muls(ks),lhs(ks),
     1  nals(kmx,ks),ncfg(kmx),nalsj(kmx,ks),scrl(kmx,ks),scrs(kmx,ks),
     2  fj(kmx,ks),scrj(kmx,ks), mul(ks),lh(ks),lf(klsp),nsjk(110),
     3  fk(kmx),fkj(kmx),scrl6(kmx),scrs6(kmx),fk6(kmx),lhqq(kmx),
     4  multqq(kmx),nalsjp(kjp,ks),pj(kjp,ks),noicrd
      common       c(kmx,kmx)
      common/c3lc2/tmx(kmx,kmx)
      common/c3lc3/ct4(kmx,kmx)
      common/c3lc4/dumlc4(kmx**2-kcc*8),cc(kcc,8)
      dimension nparj(kc,kc)
      equivalence (dumlc4,nparj)
      common/c3lcd/dumlc5
      dimension iql(kmx),iqm1l(kmx),iqm2l(kmx),scrjm1(kmx),scrjm2(kmx)
      character*10 parnam(kpr,2)
      character*8 fidls(kmx,2),fidjj(kmx,2),ldes(kmx),ldesp(kmx)
      common/char/parnam,fidls,fidjj,ldes,ldesp
      dimension ddjj(kmx,1)
      common/djj/ddjj
c
c
c        Calc. transformation matrices from LS (kcpl=1) or JJ (kcpl=2) to
c               five additional coupling representations (kcpl1=3,4,5,6,7)
c
  100 if (nosubc.le.1.or.nls.le.1) go to 980
      if (nls.gt.nlsmax) go to 980
      kcpl1=3
      if (kcpl.eq.1) go to 101
      rewind 2
      write (2) ((tmx(l,lp),l=1,nls), lp=1,nls)
  101 nmax=nsconf(2,kk)
      do 107 nc=1,nmax
      iq=0
      iqm1=0
      iqm2=0
      do 104 i=1,nosubc
      j=nosubc-i+1
      ieras=4.0*fllijk(j,nc,kk)+2.0
      if (nijk(j,nc,kk).eq.0.or.nijk(j,nc,kk).eq.ieras) go to 104
      if (iq.ne.0) go to 102
      iq=j
      go to 104
  102 if (iqm1.ne.0) go to 103
      iqm1=j
      go to 104
  103 if (iqm2.ne.0) go to 105
      iqm2=j
      go to 105
  104 continue
  105 iqm1=max0(1,iqm1)
      iqm2=max0(1,iqm2)
      do 106 l=1,nls
      if (ncfg(l).ne.nc) go to 106
      iql(l)=iq
      iqm1l(l)=iqm1
      iqm2l(l)=iqm2
  106 continue
  107 continue
      if (iabg.lt.3) go to 110
      do 109 l=1,nls
      m=nosubc
      i=scrl(l,m)+scrs(l,m)-scrj8
      if (mod(i,2).ne.0) go to 109
      do 108 lp=1,nls
  108 tmx(l,lp)=-tmx(l,lp)
  109 continue
c
  110 do 111 l=1,nls
  111 lf(l)=0
      if (kcpld(kcpl1).le.0) go to 200
      if (kcpl1.ne.4) go to 120
      if (kcpld(5)) 200,200,970
  120 if (kcpl1.ne.6) go to 970
  121 if (kcpld(7).gt.0) go to 970
  200 go to (100,100,300,400,500,600,700) kcpl1
c
c          jjJK coupling (kcpl1=3)
c
  300 do 349 l=1,nls
      iqm1=iqm1l(l)
      iq=max0(iql(l),iqm1+1)
      scrjm1(l)=scrj(l,iqm1)
      if (lf(l).ne.0) go to 349
      lf(l)=l
      nq=nalsj(l,iq)
      fkk=min(scrj(l,iqm1)+fl(nq,iq), scrj8+s(nq,iq))
      fkj(l)=fkk
      if (l.ge.nls) go to 349
      l1=l+1
      do 339 lp=l1,nls
      do 325 i=1,iq
      if (nalsj(l,i).ne.nalsj(lp,i)) go to 339
  325 continue
      do 330 i=1,iqm1
      if (fj(l,i).ne.fj(lp,i)) go to 339
      if (scrj(l,i).ne.scrj(lp,i)) go to 339
  330 continue
      lf(lp)=l
      fkk=fkk-1.0
      fkj(lp)=fkk
  339 continue
  349 continue
c
      do 369 l=1,nls
      iqm1=iqm1l(l)
      iq=max0(iql(l),iqm1+1)
      nq=nalsj(l,iq)
      do 368 lp=1,nls
      ct4(l,lp)=tmx(l,lp)
      c(l,lp)=0.0
      if(ncfg(l).ne.ncfg(lp)) go to 368
      if (lf(l).ne.lf(lp)) go to 368
      i=scrj(l,iqm1)+fl(nq,iq)+s(nq,iq)+scrj8+0.001
      a=sqrt((2.0*fkj(lp)+1.0)*(2.0*fj(l,iq)+1.0))
      if (mod(i,2).ne.0) a=-a
      b=s6j(fkj(lp),s(nq,iq),scrj8, fj(l,iq),scrj(l,iqm1),fl(nq,iq))
      c(l,lp)=a*b
  368 continue
  369 continue
      go to 900
c
c          LSLK coupling (kcpl1=4)
c
  400 do 449 l=1,nls
      iqm1=iqm1l(l)
      iq=max0(iql(l),iqm1+1)
      if (lf(l).ne.0) go to 449
      lf(l)=l
      nq=nals(l,iq)
      fkk=min(scrl(l,iq)+scrs(l,iqm1), scrj8+s(nq,iq))
      fk(l)=fkk
      if (l.ge.nls) go to 449
      l1=l+1
      do 439 lp=l1,nls
      do 425 i=1,iq
      if (nals(l,i).ne.nals(lp,i)) go to 439
  425 continue
      if (scrl(l,iq).ne.scrl(lp,iq)) go to 439
      do 430 i=1,iqm1
      if (scrl(l,i).ne.scrl(lp,i)) go to 439
      if (scrs(l,i).ne.scrs(lp,i)) go to 439
  430 continue
      lf(lp)=l
      fkk=fkk-1.0
      fk(lp)=fkk
  439 continue
  449 continue
c
      do 469 l=1,nls
      iqm1=iqm1l(l)
      iq=max0(iql(l),iqm1+1)
      do 468 lp=1,nls
      tmx(l,lp)=0.0
      if(ncfg(l).ne.ncfg(lp)) go to 468
      if (lf(l).ne.lf(lp)) go to 468
      nq=nals(l,iq)
      i=scrl(l,iq)+scrs(l,iqm1)+s(nq,iq)+scrj8+0.001
      a=sqrt((2.0*fk(lp)+1.0)*(2.0*scrs(l,iq)+1.0))
      if (mod(i,2).ne.0) a=-a
      b=s6j(fk(lp),s(nq,iq),scrj8, scrs(l,iq),scrl(l,iq),scrs(l,iqm1))
      tmx(l,lp)=a*b
  468 continue
  469 continue
      go to 930
c
c          LSJK coupling (kcpl1=5)
c
  500 do 549 l=1,nls
      iqm1=iqm1l(l)
      iq=max0(iql(l),iqm1+1)
      if (lf(l).ne.0) go to 549
      lf(l)=l
      nq=nals(l,iq)
      fjj=min(scrl(l,iqm1)+scrs(l,iqm1), fl(nq,iq)+fk(l))
      scrj(l,iqm1)=fjj
      scrjm1(l)=fjj
      if (l.ge.nls) go to 549
      l1=l+1
      do 539 lp=l1,nls
      do 525 i=1,iq
      if (nals(l,i).ne.nals(lp,i)) go to 539
  525 continue
      if (fk(l).ne.fk(lp)) go to 539
      do 530 i=1,iqm1
      if (scrl(l,i).ne.scrl(lp,i)) go to 539
      if (scrs(l,i).ne.scrs(lp,i)) go to 539
  530 continue
      lf(lp)=l
      fjj=fjj-1.0
      scrj(lp,iqm1)=fjj
      scrjm1(lp)=fjj
  539 continue
  549 continue
c
      do 569 l=1,nls
      iqm1=iqm1l(l)
      iq=max0(iql(l),iqm1+1)
      do 568 lp=1,nls
      ct4(l,lp)=tmx(l,lp)
      c(l,lp)=0.0
      if(ncfg(l).ne.ncfg(lp)) go to 568
      if (lf(l).ne.lf(lp)) go to 568
      nq=nals(lp,iq)
      i=scrl(l,iq)+scrj(lp,iqm1)+fl(nq,iq)+scrs(l,iqm1)+0.001
      a=sqrt((2.0*scrl(l,iq)+1.0)*(2.0*scrj(lp,iqm1)+1.0))
      if (mod(i,2).ne.0) a=-a
      b=s6j(scrl(l,iq),scrs(l,iqm1),fk(l), scrj(lp,iqm1),fl(nq,iq),
     1  scrl(l,iqm1))
      c(l,lp)=a*b
  568 continue
  569 continue
      go to 900
c
c          lsjLKS coupling (kcpl1=6)
c
c      calc qu. nos. for kcpl1=6 and 7 both
  600 do 646 l=1,nls
      iqm2=iqm2l(l)
      iqm1=max0(iqm1l(l),iqm2+1)
      iq=max0(iql(l),iqm1+1)
      if (lf(l).ne.0) go to 646
      l1=l
      nqm1=nals(l,iqm1)
      nq=nals(l,iq)
      njq=2.0*min(scrl(l,iqm2),scrs(l,iqm2))+1.0
      nlq=2.0*min(fl(nqm1,iqm1),fl(nq,iq))+1.0
      nsq=2.0*min(s(nqm1,iqm1),s(nq,iq))+1.0
      sjq=scrl(l,iqm2)+scrs(l,iqm2)
      do 645 ijq=1,njq
      slq=fl(nqm1,iqm1)+fl(nq,iq)
      do 644 ilq=1,nlq
      ssq=s(nqm1,iqm1)+s(nq,iq)
      do 643 isq=1,nsq
      fkk=sjq+slq+1.0
      fkmn=abs(sjq-slq)
      fjj=slq+ssq+1.0
      fjmn=abs(slq-ssq)
  602 fkk=fkk-1.0
      if (fkk.lt.fkmn) go to 643
      if (fkk+ssq-scrj8) 643,608,606
  606 if (abs(fkk-ssq).gt.scrj8) go to 602
  608 fjj=fjj-1.0
      if (fjj.lt.fjmn) go to 643
      if (fjj+sjq-scrj8) 643,615,612
  612 if (abs(fjj-sjq).gt.scrj8) go to 608
  615 lf(l1)=l
      scrj(l1,iqm2)=sjq
      scrjm2(l1)=sjq
      scrl6(l1)=slq
      fk6(l1)=fkk
      scrs6(l1)=ssq
      scrj(l1,iqm1)=fjj
      scrjm1(l1)=fjj
      i=slq+1.0
      lhqq(l1)=lsymb(i)
      multqq(l1)=2.0*ssq+1.0
      if (l1.ge.nls) go to 646
      l11=l1+1
      do 630 lp=l11,nls
      do 622 i=1,iq
      if (nals(lp,i).ne.nals(l,i)) go to 630
  622 continue
      do 625 i=1,iqm2
      if (scrl(lp,i).ne.scrl(l,i)) go to 630
      if (scrs(lp,i).ne.scrs(l,i)) go to 630
  625 continue
      l1=lp
      go to 602
  630 continue
      go to 646
  643 ssq=ssq-1.0
  644 slq=slq-1.0
  645 sjq=sjq-1.0
  646 continue
c
      do 669 l=1,nls
      iqm2=iqm2l(l)
      iqm1=max0(iqm1l(l),iqm2+1)
      iq=max0(iql(l),iqm1+1)
      nqm1=nals(l,iqm1)
      nq=nals(l,iq)
      a1=scrl(l,iqm2)
      a2=scrs(l,iqm2)
      a4=scrl(l,iqm1)
      a5=scrs(l,iqm1)
      a6=scrl(l,iq)
      a7=scrs(l,iq)
      a8=fl(nqm1,iqm1)
      a9= s(nqm1,iqm1)
      a10=fl(nq,iq)
      a11= s(nq,iq)
      do 668 lp=1,nls
      tmx(l,lp)=0.0
      if(ncfg(l).ne.ncfg(lp)) go to 668
      if (lf(l).ne.lf(lp)) go to 668
      a3=scrj(lp,iqm2)
      a12=fk6(lp)
      a13=scrl6(lp)
      a14=scrs6(lp)
      i=a1+a2+a3+a6+a7-scrj8+a8+a9+a10+a11+a13-a14
      a=sqrt((2.0*a4+1.0)*(2.0*a5+1.0)*(2.0*a6+1.0)*(2.0*a7+1.0)
     1      *(2.0*a13+1.0)*(2.0*a14+1.0)*(2.0*a12+1.0)*(2.0*a3+1.0))
      if (mod(i,2).ne.0) a=-a
      b=s6j(a1,a8,a4, a10,a6,a13) * s6j(a2,a9,a5, a11,a7,a14)
     1  *s6j(a12,a14,scrj8, a7,a6,a2) * s6j(a6,a2,a12, a3,a13,a1)
      tmx(l,lp)=a*b
  668 continue
  669 continue
      go to 930
c
c          lsj(LSJ) coupling (kcpl1=7)
c
  700 do 769 l=1,nls
      iqm2=iqm2l(l)
      iqm1=max0(iqm1l(l),iqm2+1)
      iq=max0(iql(l),iqm1+1)
      a1=scrj(l,iqm2)
      a2=scrl6(l)
      a3=fk6(l)
      a4=scrs6(l)
      do 768 lp=1,nls
      ct4(l,lp)=tmx(l,lp)
      c(l,lp)=0.0
      if(ncfg(l).ne.ncfg(lp)) go to 768
      if (lf(l).ne.lf(lp)) go to 768
      if (a1.ne.scrj(lp,iqm2)) go to 768
      if (a2.ne.scrl6(lp)) go to 768
      if (a4.ne.scrs6(lp)) go to 768
      a6=scrj(lp,iqm1)
      i=a1+a2+a4+scrj8
      a=sqrt((2.0*a3+1.0)*(2.0*a6+1.0))
      if (mod(i,2).ne.0) a=-a
      b=s6j(a1,a2,a3, a4,scrj8,a6)
      c(l,lp)=a*b
  768 continue
  769 continue
      go to 900
c
c          Output
c
  900 do 910 l=1,nls
      do 910 lp=1,nls
      tmx(l,lp)=0.0
      do 905 k=1,nls
  905 tmx(l,lp)=tmx(l,lp)+ct4(l,k)*c(k,lp)
  910 continue
c
  930 if (iabg.lt.3) go to 935
      do 934 l=1,nls
      m=nosubc
      i=scrl(l,m)+scrs(l,m)-scrj8
      if (mod(i,2).ne.0) go to 934
      do 933 lp=1,nls
  933 tmx(l,lp)=-tmx(l,lp)
  934 continue
  935 if (kcpl.eq.1) go to 939
      if (kcpl1.eq.5.or.kcpl1.eq.7) go to 939
c          transform from ls to jj representation
      rewind 2
      read (2) ((c(l,lp),l=1,nls), lp=1,nls)
      do 936 l=1,nls
      do 936 lp=1,nls
      ct4(l,lp)=tmx(l,lp)
  936 continue
      do 938 l=1,nls
      do 938 lp=1,nls
      tmx(l,lp)=0.0
      do 937 lpp=1,nls
  937 tmx(l,lp)=tmx(l,lp)+c(lpp,l)*ct4(lpp,lp)
  938 continue
  939 if (kcpld(kcpl1).ne.0) go to 970
      write (ic) ((tmx(l,lp), lp=1,nls),  fk(l),fkj(l),scrjm1(l),
     1  scrjm2(l),scrl6(l),fk6(l),scrs6(l),lhqq(l),multqq(l),l=1,nls)
      noicwr=noicwr+1
c
      if (icfc.le.0) go to 970
      write (iw,91) coupl(kcpl),coupl(kcpl1)
   91 format (9h0tmx from, a6, 5h  to ,a6,9h coupling//)
      lx=0
  940 ln=lx+1
      lx=lx+11
      if (lx.gt.nls) lx=nls
      go to (943,943,943,944,945,946,947) kcpl1
  943 write (iw,93) (scrjm1(l),fkj(l), l=ln,lx)
   93 format (28x,11(f4.1,1hk,f4.1))
      go to 950
  944 lp1=scrl(l,nosubc)+1.0
      lhs4=lsymb(lp1)
      write (iw,94) (lhs4,fk(l), l=ln,lx)
   94 format (28x,11(2x,a1,1h(,f4.1,1h)))
      go to 950
  945 write (iw,93) (scrjm1(l),fk(l), l=ln,lx)
      go to 950
  946 write (iw,96) (scrjm2(l),lhqq(l),fk6(l),multqq(l), l=ln,lx)
   96 format (28x,11(f4.1,a1,f3.1,i1))
      go to 950
  947 write (iw,97) (scrjm2(l),multqq(l),lhqq(l),scrjm1(l),
     1    l=ln,lx)
   97 format (28x,11(f4.1,i1,a1,f3.1))
  950 do 955 l=1,nls
      if (kcpl.eq.1) go to 953
      write (iw,98) ncfg(l),fidjj(l,1), l, (tmx(l,lp), lp=ln,lx)
   98 format (i11,2x,1x,a8,i4,2x,11f9.5)
      go to 955
  953 write (iw,98) ncfg(l),fidls(l,1), l, (tmx(l,lp), lp=ln,lx)
  955 continue
      if (lx.lt.nls) go to 940
c
  970 kcpl1=kcpl1+1
      if (kcpl1.le.4) go to 110
      if (kcpl1-6) 972,110,973
  972 if (nosubc-3) 980,110,110
  973 if (kcpl1-7) 110,121,980
  980 call clock(time)
      delt=time-time0
      write (iw,99) delt
   99 format (11x,5htime=,f6.3,4h min)
      return
      end
c     overlay(g9,7,0)
      subroutine mupole
c
c          Compute magnetic-dipole (ii=0), electric-dipole (ii=1),
c               or electric-quadrupole (ii=2) matrices
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      parameter (kcc=kiser/4,klc4=2*kiser+1,klc42=kmx**2)
      parameter (kmult=100)
      common/magee/nmult,ndum,nexp(kmx),sums(kmult),
     1  ials(kmult,ks,2),sl(kmult,ks,2),ss(kmult,ks,2),nexped(kmult,2),
     2  etrm(kmult,2)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2a/sj8k(2),notsjp(ks,100),ncfgp(kmx),nalsp(kmx,ks)
      common/c3a/isubj(kc),muls(ks),lhs(ks),
     1  nals(kmx,ks),ncfg(kmx),nalsj(kmx,ks),scrl(kmx,ks,2),
     2  scrs(kmx,ks,2), mul(ks),lh(ks),lf(klsp),nsjk(110),
     3  fk(kmx),fkj(kmx),scrl6(kmx),scrs6(kmx),fk6(kmx),lhqq(kmx),
     4  multqq(kmx),nalsjp(kjp,ks),pj(kjp,ks),noicrd
      common       c(kmx,kmx)
      common/c3lc2/tmx(kmx,kmx)
      common/c3lc3/ct4(kmx,kmx)
      common/c3lc4/dumlc4(klc42)
      common/c3lcd/dumlc5
      common    elem(3,kc,2),vpar(kpr,2),avp(9,2),aveig(2),avcg(2),
     1  npark(2),npav(kc),    eig(kmx),elem1(3),fnt(9,2),i1,i2
     2  ,ifact(4),fact(4)
      common    fl(kmx,ks,2),s(kmx,ks,2),cfp2(kls2,kls2),
     1  cfp1(klsp1,klsp1)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      dimension tmxp(kmx,kmx),vect(kmx,kmx),ddjj(kmx,1)
      equivalence (dumlc4,tmxp)
      dimension u1(klsp1,klsp1),nparj(kc,kc)
      equivalence (cfp1,u1),(dumlc4,vect),(dumlc4(klc4),nparj)
      character*10 parnam(kpr,2)
      character*8 fidls(kmx,2),fidjj(kmx,2),ldes(kmx),ldesp(kmx)
      character*8 fidmult(kmult,2)
      common/char/parnam,fidls,fidjj,ldes,ldesp
      common/char1/fidmult
      common/djj/ddjj
c
c
      irmn1=irmn+1
      irmx1=irmx+1
      rmx=irmx
      ii=iarg1
      il1=iarg2
      il2=iarg3
      ix=ii
      i1=il1-ila+1
      i2=il2-ila+1
      do 990 ir1=irmn1,irmx1,2
      r=ir1-1
      sums20=0.0
      sums21=0.0
      rewind il1
      read (il1) notsj1,nscrj8,sj8mn,sj8mx,npar,nparj,parnam,
     1  notsx, ((fl(l,i,1),s(l,i,1), l=1,notsx), i=1,nosubc)
      sj8k(i1)=sj8mn-1.0
      rewind il2
      read (il2) notsjp,nscrjp,sj8pmn,sj8pmx,npar,nparj,parnam,
     1  notsx, ((fl(l,i,2),s(l,i,2), l=1,notsx), i=1,nosubc)
      sj8k(i2)=sj8pmn-1.0
      j1a=nsconf(2,i1)
      j1b=nsconf(2,i2)
      do 105 i=1,j1a
      do 105 j=1,j1b
  105 sopi2(i,j)=0.0
      nmult=0
      do 106 i=1,kmult
  106 sums(i)=0.0
c
      nsc=nosubc
      sjd=sj8k(i1)
  110 sjd=sjd+1.0
      if (sjd.gt.sj8mx) go to 950
  120 n=sj8k(i1)-sjd
      if (n.lt.0) go to 126
  122 n=n+1
      do 124 i=1,n
  124 backspace il1
  126 read (il1) sj8k(i1),nls, ((tmx(l,lp),l=1,nls), lp=1,nls),
     1  ((nals(l,i),scrl(l,i,1),scrs(l,i,1),i=1,nsc),
     2  ncfg(l),fidls(l,1),fidjj(l,1), l=1,nls)
      if (sj8k(i1).ne.sjd) go to 120
      y=100.0
      do 127 i=irmn1,irmx1,2
      r1=i-1
      x=abs(sjd-r1)
      if (x.le.y) y=x
  127 continue
      if (ii.eq.0) y=abs(sjd-1.0)
  128 x=0.0
      if (i1.eq.i2) x=sjd
      sjpd=max(sj8pmn,y,x)
      go to 135
  130 sjpd=sjpd+1.0
      if (sjd.eq.0.0) sjpd=sjpd+1.0
  135 if (sjpd.gt.min(sjd+rmx,sj8pmx)) go to 110
  140 n=sj8k(i2)-sjpd
      if (n.lt.0) go to 146
  142 n=n+1
      do 144 i=1,n
  144 backspace il2
  146 read (il2) sj8k(i2),nlsp, ((tmxp(l,lp),l=1,nlsp), lp=1,nlsp),
     1  ((nalsp(l,i),scrl(l,i,2),scrs(l,i,2),i=1,nsc),
     2  ncfgp(l),fidls(l,2),fidjj(l,2), l=1,nlsp)
      if (sj8k(i2).ne.sjpd) go to 140
c
c
  150 nco=0
      ncpo=0
      do 879 l=1,nls
      nc=ncfg(l)
      do 878 lp=1,nlsp
      ncp=ncfgp(lp)
      c(l,lp)=0.0
      if (ii.gt.0) go to 300
c
c          Calculate magnetic dipole element
c
  200 if (nc.ne.ncp) go to 878
      do 210 i=1,nosubc
      if (nals(l,i).ne.nalsp(lp,i)) go to 878
      if (scrl(l,i,1).ne.scrl(lp,i,2)) go to 878
  210 if (scrs(l,i,1).ne.scrs(lp,i,2)) go to 878
      a1=scrl(l,nosubc,1)
      a2=scrs(l,nosubc,1)
      tc=1.00232*uncplb(a1,a2,sjd,one,a2,sjpd)
     1  *sqrt(a2*(a2+1.0)*(2.0*a2+1.0))
      if (sjd.eq.sjpd) tc=tc+sqrt(sjd*(sjd+1.0)*(2.0*sjd+1.0))
      go to 700
c
c          Calculate electric multipole element
c
  300 if (nc.eq.nco.and.ncp.eq.ncpo) go to 400
c
c          Determine whether a transition is possible (itrans.ne.0)
c
      itrant=itrans
      it=i
      jt=j
      itrans=0
      do 340 irho=1,nosubc
      do 340 irhop=1,nosubc
      do 302 i=1,nosubc
      if (i.eq.irho.or.i.eq.irhop) go to 302
      if (nijk(i,nc,i1)+nijk(i,ncp,i2).eq.0) go to 302
      if (fllijk(i,nc,i1).ne.fllijk(i,ncp,i2)) go to 340
      if (nijk(i,nc,i1).ne.nijk(i,ncp,i2)) go to 340
  302 continue
      if (irho.ne.irhop) go to 320
      if (il1.ne.il2.or.nc.ne.ncp) go to 305
      do 304 i=irho,nosubc
      ieras=4.0*fllijk(i,nc,i1)+2.0
      nn=nijk(i,nc,i1)
      if ((nn.eq.0.or.nn.eq.ieras).and.i.eq.irho) go to 340
      if (i.eq.irho) go to 304
      if (nn.eq.0.or.nn.eq.ieras) go to 304
      if (fllijk(i,nc,i1).eq.0.0) go to 304
      go to 340
  304 continue
      go to 320
  305 nn=0
      do 310 i=irho,nosubc
  310 nn=nn+nijk(i,nc,i1)+nijk(i,ncp,i2)
      if (nn.gt.2) go to 340
  320 a=fllijk(irho,nc,i1)+fllijk(irhop,ncp,i2)
      if (mod(a+r,two).ne.zero) go to 340
      if (a.lt.r) go to 340
      if (abs(fllijk(irho,nc,i1)-fllijk(irhop,ncp,i2)).gt.r) go to 340
      do 325 i=1,nosubc
      n=nijk(i,nc,i1)
      if (i.eq.irho) n=n-1
      m=nijk(i,ncp,i2)
      if (i.eq.irhop) m=m-1
      if (n.ne.m) go to 340
      if (n.lt.0) go to 340
  325 continue
      go to 350
  340 continue
      itrans=itrant
      i=it
      j=jt
      go to 878
c
c          Calculate theoretical S/P2
c
  350 nco=nc
      ncpo=ncp
      if (sopi2(nc,ncp).ne.0.0) go to 355
      eras=2.0
      do 354 i=1,nosubc
      b=nijk(i,nc,i1)
      b1=nijk(i,ncp,i2)
      if (b.ge.b1) go to 351
      a=4.0*fllijk(i,ncp,i2)+1.0
      go to 354
  351 a=4.0*fllijk(i,nc,i1)+2.0
      if (i.ne.irho) go to 354
      if (i1.ne.i2.or.nc.ne.ncp) go to 353
      eras=eras*b*(a-b)/(a*(a-1.0))
      go to 354
  353 a=a-1.0
      b=b-1.0
  354 eras=eras*fctrl(a)/(fctrl(b)*fctrl(a-b))
      sopi2(nc,ncp)=eras
      if (i1.eq.i2) sopi2(ncp,nc)=eras
c
c          Determine whether configs. are to be interchanged (itrans=-1)
c
  355 i=min0(irho,irhop)
      j=max0(irho,irhop)
      m=nijk(irho,nc,i1)
      n=nijk(irhop,ncp,i2)
      itrans=1
      tc0=1.0
      if (il1.eq.il2.and.nc.eq.ncp) go to 370
      a=m*n
      tc0=sqrt(a)
      if (irho.gt.irhop) n=m
      m=0
      do 360 k=i,j
      if (k.ne.i.and.k.ne.j) m=m+nijk(k,nc,i1)
  360 continue
      if (mod(m+n,2).eq.0) tc0=-tc0
      if (i.ne.irho) itrans=-1
      if (itrans.gt.0) go to 370
      if (mod(abs(sjpd-sjd+r),two).ne.zero) tc0=-tc0
c
c          Read cfp from disk 72, or u2 from disk 73 (for e2 transitions),
c               or read U0, U2, U4,... (for plane-wave-Born calculations)
c
  370 n=nijk(irho,nc,i1)
      all=fllijk(irho,nc,i1)
      if (i.eq.j) go to 390
      iii=1
  375 if (n.le.2) go to 385
      call locdsk(id2,all,n)
      read (id2) (ia,ia,ia,a,a, m=1,nlt), nlp
      if (iii.eq.1.and.itrans.eq.(-1)) go to 380
      if (iii.eq.2.and.itrans.eq.1) go to 380
      read (id2) ((cfp1(k,m), k=1,nlt), m=1,nlp)
      go to 385
  380 read (id2) ((cfp2(k,m), k=1,nlt), m=1,nlp)
  385 if (iii.eq.2) go to 400
      n=nijk(irhop,ncp,i2)
      all=fllijk(irhop,ncp,i2)
      iii=2
      go to 375
c
  390 if (n.lt.2) go to 400
      call locdsk(id3,all,n)
      if (ir1.le.1) go to 396
      do 394 k=2,ir1
  394 read (id3)
  396 read (id3) k73, ((u1(k,m), k=1,nlt), m=1,nlt)
c
c
c
  400 if (itrans) 410,878,405
  405 l1=l
      l2=lp
      nc1=nc
      nc2=ncp
      j1=i1
      j2=i2
      k1=1
      k2=2
      sj1=sjd
      sj2=sjpd
      go to 420
  410 l1=lp
      l2=l
      nc1=ncp
      nc2=nc
      j1=i2
      j2=i1
      k1=2
      k2=1
      sj1=sjpd
      sj2=sjd
c          Test selection rules
  420 do 430 m=1,nosubc
      a=abs(scrl(l,m,1)-scrl(lp,m,2))
      b=scrl(l,m,1)+scrl(lp,m,2)
      if (m.ge.j) go to 426
      if (m.lt.i) go to 424
      if (a.gt.fllijk(i,nc1,j1)) go to 878
      if (b.lt.fllijk(i,nc1,j1)) go to 878
      if (m.eq.i) go to 430
      go to 428
  424 if (a.ne.0.0) go to 878
      go to 427
  426 if (a.gt.r) go to 878
      if (b.lt.r) go to 878
  427 if (scrs(l,m,1).ne.scrs(lp,m,2)) go to 878
      if (m.eq.j) go to 430
  428 if (nals(l,m)-notsj1(m,nc).ne.nalsp(lp,m)-notsjp(m,ncp)) go to 878
  430 continue
c
  450 tc=tc0
      a1=scrl(l1,nosubc,k1)
      a2=scrl(l2,nosubc,k2)
      a3=scrs(l1,nosubc,k1)
      tc=tc*uncpla(a1,a3,sj1, r,a2,sj2)
c
      mn=j+1
      if (mn.gt.nosubc) go to 460
      do 455 m=mn,nosubc
      a1=scrl(l1,m-1,k1)
      a2=scrl(l1,m,k1)
      a3=scrl(l2,m,k2)
      n1=nals(l,m)
      a4=fl(n1,m,1)
  455 tc=tc*uncpla(a1,a4,a2, r,scrl(l2,m-1,k2),a3)
c
  460 if (il1.eq.il2.and.nc.eq.ncp) go to 600
c
c          Complete calculation for non configuration-diagonal case
c
  500 if (nijk(i,nc1,j1).le.2) go to 510
      n1=nals(l,i)-notsj1(i,nc)
      n2=nalsp(lp,i)-notsjp(i,ncp)
      a=cfp1(n1,n2)
      if (itrans.lt.0) a=cfp1(n2,n1)
      tc=tc*a
  510 if (nijk(j,nc2,j2).le.2) go to 520
      n1=nals(l,j)-notsj1(j,nc)
      n2=nalsp(lp,j)-notsjp(j,ncp)
      a=cfp2(n1,n2)
      if (itrans.gt.0) a=cfp2(n2,n1)
      tc=tc*a
c
  520 fli=fllijk(i,nc1,j1)
      if (i.eq.1) go to 530
      if (nijk(i,nc1,j1).eq.1) go to 530
      a1=scrl(l1,i-1,k1)
      a2=scrl(l1,i,k1)
      a3=scrl(l2,i,k2)
      n1=nals(l,i)
      n2=nalsp(lp,i)
      if (itrans.gt.0) go to 522
      n1=n2
      n2=nals(l,i)
  522 a4=fl(n1,i,j1)
      a5=fl(n2,i,j2)
      b1=scrs(l1,i-1,k1)
      b2=scrs(l1,i,k1)
      b3=scrs(l2,i,k2)
      b4=s(n1,i,j1)
      b5=s(n2,i,j2)
      tc=tc*recpsh(a1,a5,a3,fli,a2,a4)*recpsh(b1,b5,b3,half,b2,b4)
c
  530 mn=i+1
      mx=j-1
      if (mn.gt.mx) go to 540
      do 539 m=mn,mx
      a1=scrl(l1,m-1,k1)
      a2=scrl(l2,m-1,k2)
      a3=scrl(l1,m,k1)
      a4=scrl(l2,m,k2)
      n1=nals(l,m)
      a5=fl(n1,m,1)
      b1=scrs(l1,m-1,k1)
      b2=scrs(l2,m-1,k2)
      b3=scrs(l1,m,k1)
      b4=scrs(l2,m,k2)
      b5=s(n1,m,1)
  539 tc=tc*recpex(a2,fli,a1,a5,a3,a4)*recpex(b2,half,b1,b5,b3,b4)
c
  540 flj=fllijk(j,nc2,j2)
      n1=nals(l,j)
      n2=nalsp(lp,j)
      if (itrans.gt.0) go to 542
      n1=n2
      n2=nals(l,j)
  542 a1=scrl(l1,j-1,k1)
      a2=scrl(l2,j-1,k2)
      a3=scrl(l1,j,k1)
      a4=scrl(l2,j,k2)
      if (i.eq.j) go to 560
      a5=fl(n1,j,j1)
      a6=fl(n2,j,j2)
      b5=s(n1,j,j1)
      if (b5.eq.0.0) go to 550
      b1=scrs(l1,j-1,k1)
      b2=scrs(l2,j-1,k2)
      b3=scrs(l1,j,k1)
      b6=s(n2,j,j2)
      tc=tc*recpjp(b2,half,b1,b5,b3,b6)
  550 if (a5.eq.0.0) go to 560
      if (mod(flj+a5-a6,two).ne.zero) tc=-tc
      tc=tc*sqrt((2.0*a1+1.0)*(2.0*a6+1.0)*(2.0*a3+1.0)*(2.0*a4+1.0))
      tc=tc*s9j(a1,a2,fli, a5,a6,flj, a3,a4,r)
      go to 700
  560 if (j.eq.1) go to 700
      if (a2.eq.0.0) go to 700
      tc=tc*uncplb(a2,fli,a3, r,flj,a4)
      go to 700
c
c          Complete calculation for configuration-diagonal case
c
  600 if (i.eq.1) go to 620
      n1=nals(l,i)
      n2=nalsp(lp,i)
  610 a1=scrl(l1,i-1,k1)
      a3=scrl(l1,i,k1)
      a4=scrl(l2,i,k2)
      a5=fl(n1,i,1)
      a6=fl(n2,i,2)
      tc=tc*uncplb(a1,a5,a3, r,a6,a4)
  620 if (nijk(i,nc1,j1).eq.1) go to 700
      n1=nals(l,i)-notsj1(i,nc)
      n2=nalsp(lp,i)-notsjp(i,ncp)
      tc=tc*u1(n1,n2)
c
  700 a1=tc*tc
      sums21=sums21+a1
      if (i1.ne.i2) go to 720
      if (sjd.ne.sjpd) go to 710
      if (l.le.lp) go to 725
      go to 720
  710 sums21=sums21+a1
  720 sums20=sums20+a1
  725 if (iabg.lt.3) go to 730
      m=nosubc
      ipp=scrl(l,m,1)+scrs(l,m,1)-sjd+scrl(lp,m,2)+scrs(lp,m,2)-sjpd
      if (mod(ipp,2).ne.0) tc=-tc
  730 c(l,lp)=tc
c
c          Sum line strength for each multiplet (special for Norm Magee)
c
      if (ielpun.lt.2) go to 878
      if (a1.le.0.0) go to 878
      if (nmult.eq.0) go to 830
      do 820 nn=1,nmult
      do 810 jj=1,ks
      if (nals(l,jj).ne.ials(nn,jj,1).or.nalsp(lp,jj).ne.ials(nn,jj,2))
     1  go to 820
      if (scrl(l,jj,1).ne.sl(nn,jj,1).or.scrl(lp,jj,2).ne.sl(nn,jj,2))
     1  go to 820
      if (scrs(l,jj,1).ne.ss(nn,jj,1).or.scrs(lp,jj,2).ne.ss(nn,jj,2))
     1  go to 820
  810 continue
      sums(nn)=sums(nn)+a1
      go to 878
  820 continue
  830 nmult=nmult+1
      if (nmult.le.kmult) go to 832
      write (iw,83) nmult,kmult
   83 format ('0*****nmult=',i3,'  greater than dimension kmult=',i3)
      stop '(mupole 83)'
  832 nn=nmult
      do 840 jj=1,ks
      ials(nn,jj,1)=nals(l,jj)
      ials(nn,jj,2)=nalsp(lp,jj)
      sl(nn,jj,1)=scrl(l,jj,1)
      sl(nn,jj,2)=scrl(lp,jj,2)
      ss(nn,jj,1)=scrs(l,jj,1)
      ss(nn,jj,2)=scrs(lp,jj,2)
      sums(nn)=a1
      fidmult(nn,1)=fidls(l,1)
      fidmult(nn,2)=fidls(lp,2)
      nexped(nn,1)=0.0
      nexped(nn,2)=0.0
  840 continue
c
  878 continue
  879 continue
c
c          Output (transform to JJ coupling if necessary)
c
  900 kpar=2
      scrj8=sjd
      scrj8p=sjpd
      call sprin
c
  925 go to 130
c
c          Write dummy record
c
  950 scrj8=-7.0
      nls=1
      write (ic) scrj8,scrj8,nls,nls, c(1,1), ncfg,ncfgp
      noicwr=noicwr+1
      noicmup(kk)=noicmup(kk)+1
      rewind il1
      rewind il2
      j1x=nsconf(2,i1)
      j2x=nsconf(2,i2)
      ssopi2=0.0
      do 958 nc=1,j1x
      do 958 ncp=1,j2x
  958 ssopi2=ssopi2+sopi2(nc,ncp)
      write (iw,92) sums21,sums20,ssopi2
   92 format (///15h0sums21,sums20=,2f12.5/8x,7hssopi2=,f12.5//)
      do 960 i=1,j1x
  960 write (iw,93) (sopi2(i,j), j=1,j2x)
   93 format (45x,9f8.3)
      if (ii.eq.0) sopi2(1,1)=sums21
      write (ic) sopi2
      noicwr=noicwr+1
      noicmup(kk)=noicmup(kk)+1
  990 continue
      return
      end
c     overlay(g9,10,0)
      subroutine energy
c
c          Read parameter values, calc. energy matrices, and diagonalize;
c               with continuum electrons present, also calculate kinetic 
c               energies, and autoionization probabilities and rates
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      parameter (kcc=kiser/4,klc4=2*kiser+1,klc42=kmx**2,kexc=999)
      parameter (kbgks=41,kenrgs=21,kcase=50,ktran=100000,klam=10000)
      parameter (kmult=100)
      common/magee/nmult,ndum,nexp(kmx),sums(kmult),
     1  ials(kmult,ks,2),sl(kmult,ks,2),ss(kmult,ks,2),nexped(kmult,2),
     2  etrm(kmult,2)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3a/isubj(kc),muls(ks),lhs(ks),
     1  nals(kmx,ks),ncfg(kmx),nalsj(kmx,ks),scrl(kmx,ks),scrs(kmx,ks),
     2  fj(kmx,ks),scrj(kmx,ks), mul(ks),lh(ks),lf(klsp),nsjk(110),
     3  fk(kmx),fkj(kmx),scrl6(kmx),scrs6(kmx),fk6(kmx),lhqq(kmx),
     4  multqq(kmx),nalsjp(kjp,ks),pj(kjp,ks),noicrd
      common       c(kmx,kmx)
      common/c3lc2/tmx(kmx,kmx)
      common/c3lc3/ct4(kmx,kmx)
      common/c3lc4/dumlc4(klc42)
      common/c3lc5/ci(kmx,kmx),dum5(ktran*kbgks-kmx**2)
      common/c3lc6/gaaxc(kmx,kexc),brnchx(kexc,kexc)
      common/c3lcd/dumlc5
      common    elem(3,kc,2),vpar(kpr,2),avp(9,2),aveig(2),avcg(2),
     1  npark(2),npav(kc),    eig(kmx),elem1(3),fnt(9,2),i1,i2,
     2  ifact(4),fact(4),lcser(kmx),x(kmx)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      common/c6/emin,emax,sumwt,flbdn,flbdx,fnunp,fnuxp,nlev,iewr
      dimension vect(kmx,kmx),nparj(kc,kc),dele(kmx),enk(2),exk(2)
      equivalence (dumlc4(klc4),nparj),(dele,ct4)
      dimension cpurty(kmx,kc),nlcfgj(kc),nscfgj(kc)
      dimension aa(kmx,kmx),cii(kmx,kmx),jpar(kpr)
      equivalence (ct4,aa,cpurty),(dumlc4,vect,cii,jpar)
      equivalence (dumlc4,nlcfgj),(dumlc4(500),nscfgj)
      common/c7/g1,sumgaa,sumgar,sumgaat
      common/c8/exc(kexc),jexc(kexc),mexc(kexc)
      common/c9/l1,l2,cflag(kc,2),cgengy(kc,2),swt(kc,2),imax
      common/pwborn/nbigks,nenrgs,ekminl,ekmaxl,delekl,bigks(kbgks),
     1  xmin,xmax,tev(25),corr(kenrgs),ibk,ipwr,i11
      common/energies/etot(kc,2),ee8(kc,2),e0kin(kc),ekin(kmx)
      character*10 parnam(kpr,2)
      character*8 fidls(kmx,2),fidjj(kmx,2),ldes(kmx),ldesp(kmx)
      character*8 ldesn(kmx),fidmult(kmult,2)
      common/char/parnam,fidls,fidjj,ldes,ldesp
      common/char1/fidmult
      common/djj/ddjj
      equivalence (elem(1,1,1),ielem)
      dimension illp(kmx**2),coeff(kmx**2),ddjj(kmx,1)
      equivalence (dumlc4,illp),(ct4,coeff)
      data blnk,star/1h ,1h*/


c
c     ks=8
c     kmx=5000
c     kexc=999
      ikkk=kcpld(8)
      if (nlsmax.ne.0) ikkk=0
      iprint=kcpld(9)
      m2x=max(nsconf(2,1),nsconf(2,2))
      do 99 m3=1,2
      do 99 m2=1,m2x
      do 99 m1=1,3
   99 elem(m1,m2,m3)=blnk
      iewr=0
c
c          Read quantum numbers
c
  100 il=ila
      ie=ila
      nlsx=0
      k=1
      g1aa=0.0
      sumgaa=0.0
      sumgaat=0.0
      rewind ic
  101 rewind ie
      read (ic) notsj1,nscrj8,sj8mn,sj8mx,npar,nparj,parnam
      icrd=1
      kk=k
c
c          Read parameter values
c
      if (iprint.ge.7) go to 102
      write (iw,12)
   12 format (1h1)
  102 ixc=0
      ixc1=1
      nlst=0
      do 103 i=1,kexc
      jexc(i)=kexc+1
  103 exc(i)=0.0
c
      j1x=nsconf(2,k)
      npar0=1
      do 131 i=1,j1x
      npav(i)=npar0
      npar1=npar0+1
      npar4=npar0+4
      nparsn=nparj(i,i)+npar0-1
  105 read (ir,10) (elem1(n),n=1,3), x(npar0),
     1  (x(n),jpar(n),n=npar1,npar4),type,ifact
      write(122,10) (elem1(n),n=1,3), x(npar0),
     1  (x(n),jpar(n),n=npar1,npar4),type,ifact
	 
   10 format (2a6,a7,1x,f10.5,4(f9.4,i1),a2,4i2)
  106 if (npar0+k.ne.2) go to 109
      if (elem1(1).ne.6h    0 ) go to 109
c          Interpret as a rescale card
      deleav=x(1)
      ieras=10000.0*x(2)+0.2
      ieras=10*ieras+jpar(2)
      do 107 j=1,5
      ii=ieras/100
      jj=ieras-100*ii
      if (jj.eq.99) jj=100
      eras=jj
      if (eras.gt.0.0.and.eras.lt.1.5) eras=0.1
      fact0(6-j)=0.01*eras
  107 ieras=ii
      eras=x(4)
      if (eras.le.0.0) go to 108
      scale=scale*uenrgy/eras
      uenrgy=eras
      go to 105
  108 uenrgy=scale*uenrgy
      scale=1.0
      go to 105
c
  109 if (x(npar0).lt.-90000000.0) go to 900
      if (x(npar0).lt.-50000000.0) go to 800
      if (x(npar0).lt.-30000000.0) go to 100
      do 112 n=1,3
  112 elem(n,i,k)=elem1(n)
      do 114 j=1,5
  114 vpar(npar0+j-1,k)=x(npar0+j-1)
      if (nparj(i,i).le.5) go to 120
      npar5=npar4+1
      read (ir,11) (vpar(n,k),jpar(n),n=npar5,nparsn)
       write(122,11) (vpar(n,k),jpar(n),n=npar5,nparsn)
   11 format (7(f9.4,i1))
  120 do 121 j=1,4
      if (ifact(j).eq.99.or.ifact(j).eq.0) ifact(j)=100
      eras=ifact(j)
  121 fact(j)=0.01*eras
c          Shift Eav and/or rescale single-configuration parameters
      n1=npar1
      eras=vpar(npar0,k)
      if (eras.le.-4000.0) go to 123
      vpar(npar0,k)=eras+deleav
      n1=npar0
  123 do 125 n=n1,nparsn
  125 vpar(n,k)=scale*vpar(n,k)
      if (npar1.gt.nparsn) go to 127
      do 126 n=npar1,nparsn
      j=jpar(n)
      if (j.lt.1.or.j.gt.4) go to 126
      if (fact0(j).eq.0.0) go to 126
      vpar(n,k)=vpar(n,k)*fact0(j)/fact(j)
  126 continue
  127 do 128 j=1,4
      if (fact0(j).gt.0.0) fact(j)=fact0(j)
  128 continue
      e0kin(i)=0.0
      if (vpar(npar0,k).gt.-4000.0) go to 130
      eras=ee8(i,k)
      eras=eras*109737.0/uenrgy
      e0kin(i)=etot(1,1)-etot(i,k)+eras+vpar(npar0,k)
c

  130 write (iw,13) (elem(n,i,k),n=1,3),uenrgy,type,fact,
     1  i, (llijk(l,i,k),nijk(l,i,k), l=1,nosubc)
  
   13 format (//1x,3a6,4x,20hparameter values in ,f7.1,7h cm-1 (,
     1  a2,6h times,4f5.2,1h), 3x,i3,8(2x,a1,i2))
      write (iw,14) (parnam(n,k),n=npar0,nparsn)
   14 format (/39x,a10,4(5x,a10)/4x,7(5x,a10)/4x,7(5x,a10)/4x,7(5x,a10))
      write(iw,15) (vpar(n,k),n=npar0,nparsn)

   15 format (/ 30x,5f15.3/(7f15.3))

      npar0=nparsn+1
      cflag(i,k)=blnk
      cgengy(i,k)=0.0
      swt(i,k)=0.0
  131 continue
      
      not=npar0
      njj=nparj(j1x,j1x)
      if (j1x.le.1) go to 139
      j1xm1=j1x-1
      do 138 j1a=1,j1xm1
      j1ap1=j1a+1
      do 138 j1b=j1ap1,j1x
      jab=max0(j1b-j1a,1)
      if (nparj(j1a,j1b).eq.0) go to 138
      npar4=npar0+4
      read(ir,16) (elem1(n),n=1,3),(vpar(n,k),jpar(n),n=npar0,npar4),
     1  type,ifact
   16 format (2a6,a7,1x,5(f9.4,i1),a2,4i2)
      if (ifact(4).eq.99.or.ifact(4).eq.0) ifact(4)=100
      eras=ifact(4)
      fact5=0.01*eras
      nparsn=nparj(j1a,j1b)+npar0-1
      if (nparj(j1a,j1b).le.5) go to 132
      npar5=npar4+1
      read (ir,11) (vpar(n,k),jpar(n),n=npar5,nparsn)
       write(122,11) (vpar(n,k),jpar(n),n=npar5,nparsn)
c          Rescale configuration-interaction parameters
  132 scale1=scale
      j=jpar(npar0)
      if (j.lt.1.or.j.gt.5) go to 133
      if (fact0(j).eq.0.0) go to 133
      scale1=scale*fact0(j)/fact5
      fact5=fact0(j)
  133 do 134 n=npar0,nparsn
  134 vpar(n,k)=scale1*vpar(n,k)
c
  136 write (iw,17) (elem1(n),n=1,3),uenrgy,type,fact5,
     1  (jn, (llijk(l,jn,k),nijk(l,jn,k), l=1,ks), jn=j1a,j1b,jab)
   17 format (//1x,2a6,a7,3x,20hparameter values in ,f7.1,7h cm-1 (,
     1  a2,6h times, f5.2,1h),18x,i3,8(2x,a1,i2)/89x,i3,8(2x,a1,i2))
      write (iw,18) (parnam(n,k),n=npar0,nparsn)
      
   18 format (/37x,a10,4(5x,a10)/2x,7(5x,a10)/2x,7(5x,a10)/2x,7(5x,a10))
      write (iw,15) (vpar(n,k),n=npar0,nparsn)
      npar0=nparsn+1
  138 continue
  139 do 140 i=1,9
      avp(i,k)=0.0
  140 fnt(i,k)=0.0
      avcg(k)=0.0
      aveig(k)=0.0
      sumwt=0.0
      emin=1.0e20
      emax=-1.0e20
      nlev=0
      npar=nparsn
      npark(k)=npar
      do 150 l=1,kmx
  150 lcser(l)=0
c
c          Calculate energy matrices
c
  200 do 399 nn=1,nscrj8
      read (ic) scrj8,nls, ((tmx(l,lp),l=1,nls), lp=1,nls),
     1  ((nals(l,i),scrl(l,i),scrs(l,i),
     2  i=1,nosubc), ncfg(l),fidls(l,1),fidjj(l,1), l=1,nls)
      icrd=icrd+1
      nlsx=max0(nlsx,nls)
      noicrd=0
      wt=2.0*scrj8+1.0
      eras=0.0
      if (nls.le.0) nls=1
      do 212 l=1,nls
      do 211 lp=1,l
  211 c(l,lp)=0.0
      j=ncfg(l)
      i=npav(j)
      eras=eras+vpar(i,k)
  212 c(l,l)=vpar(i,k)
      avcg(k)=avcg(k)+eras*wt
      if (npar.le.1) go to 225
      do 222 ipar=2,npar
      do 218 j=1,j1x
      if (ipar.eq.npav(j)) go to 222
  218 continue
c
c          Read coefficient matrix elements and calculate energy matrix
c
c     read (ic) ((ct4(l,lp),l=lp,nls), lp=1,nls)
c     do 220 l=1,nls
c     do 220 lp=1,l
c 220 c(l,lp)=c(l,lp)+vpar(ipar,k)*ct4(l,lp)
      icrd=icrd+1
      noicrd=noicrd+1
      read (ic) ncoeff,(illp(i),coeff(i),i=1,ncoeff)
      do 220 i=1,ncoeff
      l=illp(i)/10000
      lp=illp(i)-10000*l
  220 c(l,lp)=c(l,lp)+vpar(ipar,k)*coeff(i)
c
  222 continue
  225 do 230 l=1,nls
      do 230 lp=1,l
  230 c(lp,l)=c(l,lp)
      if (iprint.ge.7) go to 240
      kpar=3
      call sprin
  240 lx=0
      do 250 l=1,nls
      j=ncfg(l)
      i=npav(j)
      if (vpar(i,k).gt.-4000.0) lx=l
  250 continue
      lxp1=lx+1
      jx=nls-lx+1
      jxp1=jx+1
      nlsp1=nls+1
      l=nosubc
      j=1
      kkk=1
      if (lx.eq.0.or.lx.eq.nls) go to 271
      i=0
      do 260 lp=1,nls
      if (lp.le.lx) go to 260
      i=i+1
      do 255 l=1,lx
      ci(l,i)=c(l,lp)
      c(l,lp)=0.0
  255 c(lp,l)=0.0
  260 continue
c          Calculate statistical weight of first configuration or
c               (if continuum configurations present) of ion core
      do 265 l=lxp1,nls
      j=ncfg(l)
      i=npav(j)
      if (vpar(i,k).lt.-9000.0) go to 266
  265 continue
  266 kkk=k
      m=0
      do 270 i=1,nosubc
      l=nosubc-i+1
      if (nijk(l,j,kkk).gt.0) m=m+1
      if (m.eq.2) go to 271
  270 continue
  271 g1=1.0
      do 280 i=1,l
      e1=4.0*fllijk(i,j,kkk)+2.0
      e2=nijk(i,j,kkk)
  280 g1=g1*fctrl(e1)/(fctrl(e2)*fctrl(e1-e2))
      if (lx.gt.0.and.lx.lt.nls) g1aa=g1
      if (g1aa.gt.0.0) g1=g1aa
c
c          Calculate eigenvalues and vectors
c
  300 i=0
      call clock(time1)
c          c contains matrix to be diagonalized.
c          mlew returns eigenvalues and vectors in eig and c, respectively
c     call overlay(2hg9,8,3)
      call mlew
      eras=0.0
      do 320 lp=1,nls
  320 eras=eras+eig(lp)
      call clock(time)
      tdiag=time-time1
      aveig(k)=aveig(k)+eras*wt
      eras=nls
      sumwt=sumwt+eras*wt
      emin=min(emin,eig(1))
      emax=max(emax,eig(nls))
      nlev=nlev+nls
c          Check orthonormality of eigenvectors
      do 329 l=1,nls
      do 329 lp=l,nls
      eras=0.0
      if (l.eq.lp) eras=-1.0
      eras1=eras
      do 328 j=1,nls
      eras=eras+c(j,l)*c(j,lp)
  328 eras1=eras1+c(l,j)*c(lp,j)
      if (abs(eras).gt.1.0e-10.or.abs(eras1).gt.1.0e-10)
     1  write (iw,29) l,lp,eras,eras1
   29 format (35h *****Poor orthonormality for l,lp=,2i4,3x,1p,2e10.2)
  329 continue
c
c      Calculate configuration serial number for level lp
c
      do 330 j=1,j1x
      nlcfgj(j)=0
      nscfgj(j)=0
      do 330 lp=1,nls
  330 cpurty(lp,j)=0.0
      do 331 l=1,nls
      lcser(l)=0
      j=ncfg(l)
      nscfgj(j)=nscfgj(j)+1
      do 331 lp=1,nls
  331 cpurty(lp,j)=cpurty(lp,j)+c(l,lp)**2
c
      do 333 lp=1,nls
      eras=0.0
      do 332 j=1,j1x
      if (cpurty(lp,j).lt.eras) go to 332
      eras=cpurty(lp,j)
      lcser(lp)=j
      m=j
  332 continue
  333 nlcfgj(m)=nlcfgj(m)+1
c
      do 334 j=1,j1x
  334 if (nlcfgj(j).ne.nscfgj(j)) cflag(j,k)=star
      icount=0
  335 ieras=0
      do 337 j=1,j1x
      if (nlcfgj(j).ge.nscfgj(j)) go to 337
      ieras=7
      eras=0.0
      do 336 lp=1,nls
      j1=lcser(lp)
      if (j1.eq.j.or.nlcfgj(j1).le.nscfgj(j1)) go to 336
      if (cpurty(lp,j).lt.eras) go to 336
      eras=cpurty(lp,j)
      m=lp
  336 continue
      j1=lcser(m)
      lcser(m)=j
      nlcfgj(j1)=nlcfgj(j1)-1
      nlcfgj(j)=nlcfgj(j)+1
  337 continue
      icount=icount+1
      if (ieras.ne.0.and.icount.le.nls) go to 335
      eras=2.0*scrj8+1.0
      do 338 lp=1,nls
      j=lcser(lp)
      cgengy(j,k)=cgengy(j,k)+eras*eig(lp)
  338 swt(j,k)=swt(j,k)+eras
      nntrm=0
c          Calculate level designations
      do 340 lp=1,nls
      c2x=0.0
      do 339 l=1,nls
      if (ncfg(l).ne.lcser(lp)) go to 339
      c2=c(l,lp)**2
!	write(160,"(10x,2i4,x,2f9.3)") lp,l,c2,c2x	
      if (c2.lt.c2x) go to 339
      ld=l
      c2x=c2
  339 continue
      write(160,"(2i4,x,2f9.3)") lp,ld,c2x,c2
      ldes(lp)=fidls(ld,1)
      if (kcpl.eq.2) ldes(lp)=fidjj(ld,1)
      if (c(ld,lp).gt.0.0) go to 2339
      do 1339 l=1,nls
 1339 c(l,lp)=-c(l,lp)
c          Determine expediency number (special for Norm Magee)
 2339 if (ielpun.lt.2) go to 340
      if (scrj8.gt.abs(scrl(ld,nosubc)-scrs(ld,nosubc))) go to 340
      if (nntrm.eq.0) go to 4339
      do 3339 n1=1,nntrm
      if (ldes(lp).eq.ldesn(n1)) go to 5339
 3339 continue
 4339 nntrm=nntrm+1
      n1=nntrm
      ldesn(n1)=ldes(lp)
      nexp(n1)=0
 5339 nexp(n1)=nexp(n1)+1
      do 7339 l1=1,nmult
      if (ldes(lp).ne.fidmult(l1,k)) go to 7339
      do 6339 k1=1,nosubc
      if (nals(ld,k1).ne.ials(l1,k1,k)) go to 7339
      if (scrl(ld,k1).ne.sl(l1,k1,k)) go to 7339
      if (scrs(ld,k1).ne.ss(l1,k1,k)) go to 7339
 6339 continue
      nexped(l1,k)=nexp(n1)
      etrm(l1,k)=eig(lp)
 7339 continue
c
  340 continue
c
c          Print eigenvalues and vectors
c
      if (iprint.ge.9) go to 350
      if (iprint.ge.7) go to 342
      if (iengyd.lt.2) go to 342
      if (nls.le.11) go to 342
      if (eig(nls).gt.9999.0) go to 341
      write (iw,30) scrj8,(eig(l),l=1,nls)
      write (105,30) scrj8,(eig(l),l=1,nls) 
   30 format (15h1  eigenvalues ,5x,3h(j=,f4.1,1h)/(/28x,1000f9.3))
      go to 345
  341 write (iw,31) scrj8,(eig(l),l=1,nls)
      write (105,31) scrj8,(eig(l),l=1,nls)
   31 format (15h1  eigenvalues ,5x,3h(j=,f4.1,1h)/(/28x,1000f9.2))
      go to 345
  342 if (eig(nls).gt.9999.0) go to 343
      write (iw,32) scrj8,(eig(l),l=1,nls)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!-----��������ܼ�----(E-cowan)------------Print eigenvalues-----
      write (105,32) scrj8,(eig(l),l=1,nls)      
!      write (150,3200) (eig(l),l=1,nls)         !SuMG 20120822
! 3200 format (11x,1000f9.3)	                  !SuMG 20120822 
      write (109,"(f4.1,5x,I3)") scrj8,nls
      write (110,"(1000f9.3)")(eig(l),l=1,nls)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!-------su in ireland(2007-5-30)
      write (117,"(i3,i3,f4.1,f9.3)") (kk,ncfg(l),scrj8,eig(l),l=1,nls)

   32 format (15h0  eigenvalues ,5x,3h(j=,f4.1,1h)/(/28x,1000f9.3))
      go to 345
  343 write (iw,33) scrj8,(eig(l),l=1,nls) 
c      write (105,33) scrj8,(eig(l),l=1,nls)
   33 format (15h0  eigenvalues ,5x,3h(j=,f4.1,1h)/(/28x,1000f9.3))
  345 write (iw,34) (lcser(l), l=1,nls)

c      write (105,34) (lcser(l), l=1,nls)
   34 format (15h   config. no. /(25x,1000i9))
c
c          Print free-electron kinetic energies
c
      if (lx.eq.0.or.lx.eq.nls) go to 350
      write (8,2809)nls-jx+1
      write (8,33)scrj8,(eig(ijk),ijk=jx,nls)
c      write (889,"(I5)")nls-jx+1
      write (888,"(f4.1,4x,1000f9.3)")scrj8,(eig(ijk),ijk=jx,nls)
      write (8,34) (lcser(l), l=jx,nls)
      llx=nls-lx
      lmin=2+11*((llx-11)/11)
      write (8,2809)llx
 2809 format(i5)
      do 349 lp=1,llx
      do 347 l=lmin,nls
      ekin(l)=0.0
      if (l.le.llx) go to 347
      ijj=lcser(lp)
      ekin(l)=eig(l)+e0kin(ijj)-eig(lp)
  347 continue
      write (iw,28) (elem(l1,ijj,k), l1=1,3),
     1  ldes(lp),(ekin(l),l=lmin,nls)
c DONG,1998.51
      write (8,28) (elem(l1,ijj,k), l1=1,3),
     1  ldes(lp),(ekin(l),l=jx,nls)
   28 format (' keV for core  ',2a6,a2,1x,a8,10f9.3
     1  /(28x,11f9.3))
c      write (8,*)ddjj(lp,1)
  349 continue
  350 kpar=4
  355 write (ie) scrj8,nls, (eig(lp), (c(l,lp),l=1,nls), lp=1,nls),
     1  lcser,ldes
      iewr=iewr+1
  358 if (iprint.ge.8) go to 359
      call sprin
  359 if (ielpun.eq.1) write (11,35) (elem(l,1,k), l=1,3),
     1  scrj8,nls, (eig(l), l=1,nls)
   35 format (3a6,2x,f5.1,i5/(6f12.3))
c
c          Calculate autoionization transition probabilities
c
      do 360 lp=1,nls
      aa(lp,jx)=0.0
      aa(lp,jxp1)=0.0
      do 360 i=1,kexc
  360 gaaxc(lp,i)=0.0
      if (lx.eq.0.or.lx.eq.nls) go to 380
      if (nls.gt.kmx) write (iw,36) nls,kmx
   36 format (//10h *****nls=,i3,29h .gt. max allowable value of ,
     1  i3,18h for aa calcn*****//)
      backspace ie
      read (ie) scrj8,nls, (eig(lp), (c(l,lp),l=1,nls), lp=1,nls)
       aamx=0.0
      do 362 lp=1,nls
      do 362 j=lxp1,nls
      i=j-lx
      sum=0.0
      do 361 l=1,lx
  361 sum=sum+c(l,lp)*ci(l,i)
  362 cii(lp,j)=sum
      do 365 lp=1,nls
      do 364 i=1,nls
      if (eig(i).gt.-4000.0) go to 364
      aa(lp,i)=0.0
      if (eig(i).lt.-8000.0.or.emina.eq.0.0) go to 2362
      if (eig(lp).lt.emina) go to 364
      j=lcser(i)
      jj=npav(j)
      etemp=eig(i)-vpar(jj,k)
c          Include following statement only in special cases
c     if (etemp.gt.0.0) go to 364
c
 2362 sum=0.0
      do 363 l=lxp1,nls
  363 sum=sum+cii(lp,l)*c(l,i)
      aa(lp,i)=((sum*uenrgy/109735.3)**2)*6.28318*2066.0
      if (eig(i).lt.-8000.0) aa(lp,jx)=aa(lp,jx)+aa(lp,i)
      aa(lp,jxp1)=aa(lp,jxp1)+aa(lp,i)
  364 continue
  365 aamx=max(aa(lp,jxp1),aamx)
      eras=1.0
      l=13
      if (aamx.lt.0.1) l=10
      if (aamx.gt.999.9) l=16
      l1=l
      if (l.eq.13) go to 367
      eras=10.0**(13-l)
      do 366 lp=1,nls
      do 366 i=1,jxp1
  366 aa(lp,i)=eras*aa(lp,i)
  367 if (iprint.ge.9) go to 371
      write(8,37) l
      write (iw,37) l
   37 format (17h aa(units of 10**,i2,5h/sec))
      lmin=1+11*((llx-11)/11)
      i=0
c      write (889,3707)nlsp1-lx-1,nls-jx+1
      write (889,"(I4,I5)")nls-jx+1,nlsp1-lx-1
	write (8,3707)nlsp1-lx-1
 3707 format(i5)
      do 370 j=lx,nlsp1
      i=i+1
      if (nls.eq.lxp1.and.i.ge.2) go to 370
      if (kcpld(1)+kcpld(2).lt.3) go to 368
      if (i.lt.jx.and.(nls-lx).gt.2.and.nls.gt.11) go to 370
  368 if (j.ge.nls) go to 369
      n1=lcser(i)
      write (8,38) (elem(i1,n1,k),i1=2,3), ldes(i),
     1      (aa(lp,i),lp=jx,nls)
      write (888,"(8x,1000f9.4)") 
     1      (aa(lp,i),lp=jx,nls)
      write (iw,38) (elem(i1,n1,k),i1=2,3), ldes(i), 
     1     (aa(lp,i),lp=lmin,nls)
   38 format (8x,2a6,a8,11f9.4/(29x,11f9.4))
c      write (8,*)ddjj(i,1)
      go to 370
  369 itemp=-8000
      if (j.eq.nlsp1) itemp=-4000
c      write (8,39) itemp, (aa(lp,i),lp=jx,nls)
      write (iw,39) itemp, (aa(lp,i),lp=lmin,nls)
   39 format (12x,11h tot, e.lt.,i5,11f9.4/(29x,11f9.4))
  370 continue
  371 eras=1.0e13/eras
      gg=2.0*scrj8+1.0
      do 372 lp=1,nls
      aa(lp,jx)=eras*aa(lp,jx)
      aa(lp,jxp1)=eras*aa(lp,jxp1)
      sumgaa=sumgaa+gg*aa(lp,jx)
  372 sumgaat=sumgaat+gg*aa(lp,jxp1)
      eras=gg*eras
      jxm1=jx-1
      do 378 l=1,jxm1
      if (eig(l).gt.-4000.0) go to 378
      j=lcser(l)
      jj=npav(j)
      etemp=eig(l)-vpar(jj,k)
      if (ixc.eq.0) go to 375
      do 374 i=1,ixc
      if (abs(etemp-exc(i)).lt.0.01.and.j.eq.jexc(i)) go to 376
  374 continue
  375 ixc=ixc+1
      i=ixc
      exc(i)=etemp
      jexc(i)=j
  376 do 377 lp=1,nls
  377 gaaxc(lp,i)=gaaxc(lp,i)+eras*aa(lp,l)
  378 continue
      ixc1=max0(ixc,1)
      if (iprint.ge.9) go to 380
      write (iw,40) sumgaa,sumgaat
   40 format (/20x,7hsumgaa=,1pe13.5,10x,8hsumgaat=,e13.5//
     1  10x,11hexc   gaaxc/)
  380 write (ie) lx, (aa(lp,jx),aa(lp,jxp1), lp=1,nls)
     1  ,nlst,ixc,ixc1, (exc(i), (gaaxc(lp,i),lp=jx,nls), i=1,ixc1)
      nlst=nlst+lx
      if (iprint.ge.9) go to 399
      if (nls.le.1) go to 397
      if (ixc.eq.0) go to 388
      if (lx.eq.0.or.lx.eq.nls) go to 388
      eras=10.0**(-l1)
      do 386 i=1,ixc
      do 384 lp=1,nls
  384 gaaxc(lp,i)=eras*gaaxc(lp,i)
  386 write (iw,41) jexc(i),exc(i), (gaaxc(lp,i), lp=lmin,nls)
   41 format (13x,i3,f12.4,11f9.4/(29x,11f9.4))
  388 continue
c
c          Calculate level distribution
c
      fnls=nls
      sum=0.0
      do 391 l=1,nls
  391 sum=sum+eig(l)
      aveeig=sum/(fnls+1.0e-10)
      sum=0.0
      sum3=0.0
      do 392 l=1,nls
      delta=eig(l)-aveeig
      delta2=delta**2
      sum=sum+delta2
  392 sum3=sum3+delta2*delta
      rms1=sqrt(sum/fnls)
      sum3=sum3/fnls
      alf3=sum3/(rms1**3+1.0e-10)
      nlsm1=nls-1
      fnlsm1=nlsm1
      do 393 l=1,nlsm1
  393 dele(l)=eig(l+1)-eig(l)
      sum=0.0
      do 394 l=1,nlsm1
  394 sum=sum+dele(l)
      avedel=sum/fnlsm1
      sum=0.0
      do 395 l=1,nlsm1
  395 sum=sum+(dele(l)-avedel)**2
      rms2=sqrt(sum/fnlsm1)
      call clock(time)
      delt=time-time0
      write (iw,42) aveeig,rms1,alf3,avedel,rms2,delt,tdiag
   42 format (//17h0aveeig,rms,alf3=,2f12.3,f9.4,5x,11havedel,rms=,
     1  2f12.3,7x,15htime, diagtime=,f6.3,f8.5,4h min)
c
c 397 if (iv.ne.0) call overlay(2hg9,8,2)
  397 if (iv.ne.0) call calcv
c
  399 continue
c           Write dummy record, required by system bug on IBM Stretch
      write (ie) (eig(l), l=1,20)
c
      do 400 j=1,j1x
  400 cgengy(j,k)=cgengy(j,k)*uenrgy/((swt(j,k)+0.00000001)*109737.31)
      avcg(k)=avcg(k)/sumwt
      aveig(k)=aveig(k)/sumwt
      do 410 i=1,9
      if (fnt(i,k).eq.0.0) go to 410
      avp(i,k)=avp(i,k)/fnt(i,k)
  410 continue
      if (avp(1,k).gt.0) go to 415
      do 412 i=1,9
  412 avp(i,k)=1.0
  415 if (k.eq.1.and.nsconf(1,2).gt.0.and.iprint.ge.7) go to 430
      write  (iw,43) (coupl(i), i=1,7)
   43 format (///13h ave purities,29x,9(a6,2x)/)
      do 420 k1=1,k
      j1x=nsconf(2,k1)
      if (j1x.lt.2) j1x=2
      j1=j1x-1

  420 write (iw,44) ((elem(i,jn,k1), i=1,3), jn=1,j1x,j1),
     1  (avp(i,k1), i=1,7), avcg(k1),aveig(k1)
      
   44 format (1x,3a6,3h---,3a6,7f8.3,5x,6h  eav=,f10.4/101x,6haveig=,
     1  f10.4)
      enk(k)=emin
      exk(k)=emax
c
c 430 if (ispecc.ge.8) call overlay(2hg9,8,1)
  430 if (ispecc.ge.8) call lvdist
c
      rewind ie
      if (imag.ne.k.and.imag.lt.3) go to 450
c     call overlay(2hg9,8,4)
      iarg1=0
      iarg2=ie
      iarg3=ie
      call spectr
  450 if (iquad.ne.k.and.iquad.lt.3) go to 470
c     call overlay(2hg9,8,4)
      iarg1=2
      iarg2=ie
      iarg3=ie
      irmn=irnq
      call spectr
c     if (igen.ge.5) call overlay(2hg9,8,5)
      if (igen.ge.5) call born
  470 if (nsconf(1,2).le.0) go to 100
      if (ie.eq.ilb) go to 500
  480 il=ilb
      ie=ilb
      k=2
      go to 101
c
c 500 call overlay(2hg9,8,4)
  500 iarg1=iiprty
      iarg2=ila
      iarg3=ilb
      irmn=irnd
      emean=0.5*(max(enk(1),enk(2))+max(exk(1),exk(2)))
      call spectr
c          Write multiplet line strength on tape 19 (special for Norm Magee)
      if (ielpun.lt.2) go to 515
      stot=0.0
      do 505 nn=1,nmult
  505 stot=stot+sums(nn)
      write (19,50) ((llijk(i,1,k),nijk(i,1,k),i=1,3), k=1,2),
     1  nmult,stot,ssopi2
   50 format (2x,3(a1,i2,2x),' - ',3(a1,i2,2x),'     nmult=',i3,
     1  '     stot=',f9.5,'     theory=',f9.5)
      do 510 nn=1,nmult
  510 write (19,51) (fidmult(nn,k),nexped(nn,k),etrm(nn,k), k=1,2),
     1  sums(nn)
   51 format (2x,a8,i5,f12.5,5x,a8,i5,f12.5,f15.5)
c
c     if (igen.ge.5) call overlay(2hg9,8,5)
  515 if (igen.ge.5) call born
      if (ikkk.le.8) go to 100
      do 520 i=1,icrd
  520 backspace ic
      go to 480
c
c 800 call overlay(2hg9,8,6)
  800 call rceinp
      go to 100
c
  900 return
      end
c     overlay(g9,10,1)
      subroutine lvdist
c
c          Plot level distribution on microfilm (obsolete)
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      parameter (kcc=kiser/4,klc4=2*kiser+1)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c3d/ecut(42),eplot(82),icut(42),gcut(42),title(20),gplt(82)
      common    elem(3,kc,2),vpar(kpr,2),avp(9,2),aveig(2),avcg(2),
     1  npark(2),npav(kc),    eig(kmx),elem1(3),fnt(9,2),i1,i2
     2  ,ifact(4),fact(4)
      common/c6/emin,emax,sumwt,flbdn,flbdx,fnunp,fnuxp,nlev,iewr
      common/cje07/ixl,ixr,iyt,iyb,xmn,xmx,ymx,ymn
c
  100 if (nlev.lt.10) go to 900
      k=kk
      fn=40.0
      del=0.0005*(emax-emin)
      emin=emin-del
      emax=emax+del
      dele=(emax-emin)/fn
      ecut(1)=emin
      eplot(1)=emin-0.5*dele
      np2=fn+2.0
      do 150 j=1,np2
      if (j.eq.1) go to 140
      ecut(j)=ecut(j-1)+dele
      eplot(j)=eplot(j-1)+dele
  140 icut(j)=0
  150 gcut(j)=0.0
c
      rewind ie
      disp=0.0
      third=0.0
      do 300 nn=1,nscrj8
      read (ie) scrj8,nls, (eig(l), (b, lp=1,nls), l=1,nls)
      read (ie)
      wt=2.0*scrj8+1.0
      jcut=2
      do 230 n=1,nls
  210 if (eig(n).lt.ecut(jcut)) go to 220
      jcut=jcut+1
      go to 210
  220 icut(jcut)=icut(jcut)+1
      gcut(jcut)=gcut(jcut)+wt
      eras1=eig(n)-aveig(k)
      eras2=wt*eras1*eras1
      disp=disp+eras2
  230 third=third+eras2*eras1
  300 continue
      disp=disp/sumwt
      rms=sqrt(disp)
      third=third/sumwt
      alf3=third/(rms**3)
      write (iw,30)
   30 format (//1h0,8x,1hj,7x,4hecut,8x,5heplot,7x,4hicut,6x,4hgcut,8x,
     1  5hsumwt,7x,4hdisp,9x,3hrms,8x,4half3/)
      do 310 j=1,np2
      gcut(j)=gcut(j)/sumwt
      write(iw,31)j,ecut(j),eplot(j),icut(j),gcut(j),sumwt,disp,rms,alf3
   31 format (i10,2f12.3,i10,f12.6,f12.0,2f12.3,f12.4)
  310 continue
c     np1=np2-1
c     l=0
c     do 320 j=1,np1
c     l1=j-1
c     do 320 j1=1,2
c     l=l+1
c     l1=l1+1
c     eplot(l)=ecut(j)
c 320 gplt(l)=gcut(l1)
c     np1t2=2*np1
c
c     j1x=max0(nsconf(2,k),2)
c     j1=j1x-1
c     encode (44,40,title) ((elem(i,jn,k),i=1,3), jn=1,j1x,j1)
c  40 format (6x,3a6,2h--,3a6)
c     encode (111,41,title(6)) nlev,sumwt,rms,alf3
c  41 format (50x,5hnlev=,i4,4x,6hsumwt=,f7.0,4x,4hrms=,f10.3,4x,
c    1  5half3=,f8.4)
c     call plojb(eplot,gplt,np1t2,1,0,28,0.0,1.0,0.93,title,161,
c    1  13he (1000 cm-1),13,29hfractional statistical weight,29)
c     do 420 i=1,3
c     fi=i
c     eplot(i)=avcg(k)+(fi-2.0)*rms
c 420 gcut(i)=0.0
c     call plojb(eplot,gcut,3,1,1,-24,0.0,1.0,0.93,title,0,
c    1  b,0,b,0)
c     call lincnt(59)
c     write (12,42) (coupl(i), i=1,7)
c  42 format (10x,13h ave purities,29x,9(a6,2x)/)
c     write (12,44) ((elem(i,jn,k), i=1,3), jn=1,j1x,j1),
c    1  (avp(i,k), i=1,7), avcg(k)
c  44 format (11x,3a6,3h---,3a6,7f8.3,5x,6h  eav=,f10.4)
c
c          Plot skewed-gaussian curve
c
c     de=(xmx-xmn)/81.0
c     eplot(1)=xmn
c     do 505 j=2,82
c 505 eplot(j)=eplot(j-1)+de
c     c=(ecut(2)-ecut(1))/(rms*sqrt(2.0*3.14159))
c     do 510 j=1,82
c     x=(eplot(j)-aveig(k))/rms
c     x2=x*x
c     y=1.0-0.5*alf3*(x-x*x2/3.0)
c 510 gplt(j)=c*y*exp(-0.5*x2)
c     call plojb(eplot,gplt,82,1,0,-28,0.0,1.0,0.95,title,0,b,0,b,0)
  900 return
      end
      subroutine plojb(x,y,npts,inc,lnn,nsym,c,xaa,yaa,labelz,nzl,label
     1  x,nxl,labely,nyl)
      implicit real*8 (a-h,o-z)
      eplot=7
      a=eplot
      return
      end
c     overlay(g9,10,2)
      subroutine calcv
c
c          Calc. v matrix (derivatives of eigenvalues wrt parameters)
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      parameter (kcc=kiser/4,klc4=2*kiser+1)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2/ll(ks),ni(ks),fll(ks),mult(klsc,ks),lbcd(klsc,ks),
     1  ialf(klsc,ks),fl(klsc,ks),s(klsc,ks),ntrmk(klsp),fllrhop,fllsigp
      common/c3a/isubj(kc),muls(ks),lhs(ks),
     1  nals(kmx,ks),ncfg(kmx),nalsj(kmx,ks),scrl(kmx,ks),scrs(kmx,ks),
     2  fj(kmx,ks),scrj(kmx,ks), mul(ks),lh(ks),lf(klsp),nsjk(110),
     3  fk(kmx),fkj(kmx),scrl6(kmx),scrs6(kmx),fk6(kmx),lhqq(kmx),
     4  multqq(kmx),nalsjp(kjp,ks),pj(kjp,ks),noicrd
      common       c(kmx,kmx)
      common/c3lc2/tmx(kmx,kmx)
      common/c3lc3/ct4(kmx,kmx)
      common/c3lc4/vect(kmx,kmx)
      common/c3lcd/dumlc5
      common    elem(3,kc,2),vpar(kpr,2),avp(9,2),aveig(2),avcg(2),
     1  npark(2),npav(kc),    eig(kmx),elem1(3),fnt(9,2),i1,i2
     2  ,ifact(4),fact(4)
      character*10 parnam(kpr,2)
      character*8 fidls(kmx,2),fidjj(kmx,2),ldes(kmx),ldesp(kmx)
      common/char/parnam,fidls,fidjj,ldes,ldesp
      dimension illp(kmx**2),coeff(kmx**2),ddjj(kmx,1)
      common/djj/ddjj
      equivalence (tmx,illp),(c,coeff)
c
      dimension v(100,64)
c     equivalence (c,v)
c          NOTE---v(kpr,kmx) spills over into /c3lc2/
c
      if (nls.eq.1) vect(1,1)=1.0
      m=noicrd
      if (m.eq.0) go to 900
      k=kk
      do 100 jj=1,m
  100 backspace ic
      nlst=min0(nls,nevmax)
c
c          calc v matrix
c
      do 229 ipar=1,npar
      do 205 j=1,j1x
      if (ipar.ne.npav(j)) go to 205
      do 202 l=1,nls
      do 201 lp=1,nls
  201 ct4(l,lp)=0.0
      if (ncfg(l).eq.j) ct4(l,l)=1.0
  202 continue
      go to 212
  205 continue
c
c     read (ic) ((ct4(l,lp),l=lp,nls), lp=1,nls)
c     do 210 l=1,nls
c     do 210 lp=1,l
c 210 ct4(lp,l)=ct4(l,lp)
      do 207 l=1,nls
      do 207 lp=1,nls
  207 ct4(l,lp)=0.0
      read (ic) ncoeff,(illp(i),coeff(i),i=1,ncoeff)
      do 210 i=1,ncoeff
      l=illp(i)/10000
      lp=illp(i)-10000*l
      ct4(l,lp)=coeff(i)
  210 ct4(lp,l)=ct4(l,lp)
c
  212 do 220 m=1,nlst
      v(ipar,m)=0.0
      do 220 l=1,nls
      a=0.0
      do 215 lp=1,nls
  215 a=a+ct4(l,lp)*vect(lp,m)
  220 v(ipar,m)=v(ipar,m)+vect(l,m)*a
  229 continue
c
c
c
      write (iw,35)
   35 format (////9h v matrix)
      lx=0
  310 write (iw,36)
   36 format (1h )
      ln=lx+1
      lx=lx+11
      if (lx.gt.nlst) lx=nlst
      do 320 i=1,npar
  320 write (iw,37) parnam(i,k), (v(i,l), l=ln,lx)
   37 format (1x,a10,4x,11f9.5)
      if (lx.lt.nlst) go to 310
c
      m=noicrd-npar+j1x
      if (m.le.0) go to 900
      do 400 i=1,m
  400 read (ic) a
c
  900 call clock(time)
      delt=time-time0
      write (iw,93) delt
   93 format (11x,5htime=,f6.3,4h min)
      return
      end
c     overlay(g9,10,3)
      subroutine mlew
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      parameter (kcc=kiser/4,klc4=2*kiser+1,klc42=kmx**2,kexc=999)
      parameter (kbgks=41,kenrgs=21,kcase=50,ktran=100000,klam=10000)
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c3a/isubj(kc),muls(ks),lhs(ks),
     1  nals(kmx,ks),ncfg(kmx),nalsj(kmx,ks),scrl(kmx,ks),scrs(kmx,ks),
     2  fj(kmx,ks),scrj(kmx,ks), mul(ks),lh(ks),lf(klsp),nsjk(110),
     3  fk(kmx),fkj(kmx),scrl6(kmx),scrs6(kmx),fk6(kmx),lhqq(kmx),
     4  multqq(kmx),nalsjp(kjp,ks),pj(kjp,ks),noicrd
      common       c(kmx,kmx)
      common/c3lc4/vect(kmx,kmx)
      common    elem(3,kc,2),vpar(kpr,2),avp(9,2),aveig(2),avcg(2),
     1  npark(2),npav(kc),    eig(kmx),elem1(3),fnt(9,2),i1,i2,
     2  ifact(4),fact(4),lcser(kmx),x(kmx)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
c
      call tred2(kmx,nls,c,eig,fk,c)
      call tql2(kmx,nls,eig,fk,c,m)
      if (m.ne.0) write (iw,10) m
   10 format (36h*****Error in diagonalization, ierr=,i4)
      return
      end
      subroutine tred2(nm,n,a,d,e,z)                                    tred2  3
c***begin prologue  tred2                                               tred2  4
c***date written   760101   (yymmdd)                                    tred2  5
c***revision date  830518   (yymmdd)                                    tred2  6
c***category no.  d4c1b1                                                tred2  7
c***keywords  eigenvalues,eigenvectors,eispack                          tred2  8
c***author  Smith, B. T., et al.                                        tred2  9
c***purpose  Reduce real symmetric matrix to symmetric tridiagonal      tred2 10
c            matrix using and accumulating orthogonal transformation    tred2 11
c***description                                                         tred2 12
c                                                                       tred2 13
c     This subroutine is a translation of the ALGOL procedure tred2,    tred2 14
c     Num. Math. 11, 181-195(1968) by Martin, Reinsch, and Wilkinson.   tred2 15
c     Handbook for Auto. Comp., Vol.ii-Linear Algebra, 212-226(1971).   tred2 16
c                                                                       tred2 17
c     This subroutine reduces a real symmetric matrix to a              tred2 18
c     symmetric tridiagonal matrix using and accumulating               tred2 19
c     orthogonal similarity transformations.                            tred2 20
c                                                                       tred2 21
c     On input                                                          tred2 22
c                                                                       tred2 23
c        nm must be set to the row dimension of two-dimensional         tred2 24
c          array parameters as declared in the calling program          tred2 25
c          dimension statement.                                         tred2 26
c                                                                       tred2 27
c        n is the order of the matrix.                                  tred2 28
c                                                                       tred2 29
c        a contains the real symmetric input matrix.  only the          tred2 30
c          lower triangle of the matrix need be supplied.               tred2 31
c                                                                       tred2 32
c     On output                                                         tred2 33
c                                                                       tred2 34
c        d contains the diagonal elements of the tridiagonal matrix.    tred2 35
c                                                                       tred2 36
c        e contains the subdiagonal elements of the tridiagonal         tred2 37
c          matrix in its last n-1 positions.  e(1) is set to zero.      tred2 38
c                                                                       tred2 39
c        z contains the orthogonal transformation matrix                tred2 40
c          produced in the reduction.                                   tred2 41
c                                                                       tred2 42
c        a and z may coincide.  if distinct, a is unaltered.            tred2 43
c                                                                       tred2 44
c     Questions and comments should be directed to B. S. Garbow,        tred2 45
c     Applied Mathematics Division, Argonne National Laboratory         tred2 46
c     ------------------------------------------------------------------tred2 47
c***references  B. T. Smith, J. M. Boyle, J. J. Dongarra, B. S. Garbow, tred2 48
c                 Y. Ikebe, V. C. Klema, C. B. Moler, *Matrix Eigen-    tred2 49
c                 system Routines - Eispack Guide*, Springer-Verlag,    tred2 50
c                 1976.                                                 tred2 51
c***routines called  (none)                                             tred2 52
c***end prologue  tred2                                                 tred2 53
c                                                                       tred2 54
      implicit real*8 (a-h,o-z)
      integer i,j,k,l,n,ii,nm,jp1                                       tred2 55
      dimension a(nm,n),d(n),e(n),z(nm,n)                               tred2 56
c     real a(nm,n),d(n),e(n),z(nm,n)                                    tred2 56
c     real f,g,h,hh,scale                                               tred2 57
c                                                                       tred2 58
c***first executable statement  tred2                                   tred2 59
      do 100 i = 1, n                                                   tred2 60
c                                                                       tred2 61
         do 100 j = 1, i                                                tred2 62
            z(i,j) = a(i,j)                                             tred2 63
  100 continue                                                          tred2 64
c                                                                       tred2 65
      if (n .eq. 1) go to 320                                           tred2 66
c     .......... for i=n step -1 until 2 do -- ..........               tred2 67
      do 300 ii = 2, n                                                  tred2 68
         i = n + 2 - ii                                                 tred2 69
         l = i - 1                                                      tred2 70
         h = 0.0e0                                                      tred2 71
         scale = 0.0e0                                                  tred2 72
         if (l .lt. 2) go to 130                                        tred2 73
c     .......... scale row (algol tol then not needed) ..........       tred2 74
         do 120 k = 1, l                                                tred2 75
  120    scale = scale + abs(z(i,k))                                    tred2 7
c                                                                       tred2 77
         if (scale .ne. 0.0e0) go to 140                                tred2 78
  130    e(i) = z(i,l)                                                  tred2 79
         go to 290                                                      tred2 80
c                                                                       tred2 81
  140    do 150 k = 1, l                                                tred2 82
            z(i,k) = z(i,k) / scale                                     tred2 83
            h = h + z(i,k) * z(i,k)                                     tred2 84
  150    continue                                                       tred2 85
c                                                                       tred2 86
         f = z(i,l)                                                     tred2 87
         g = -sign(sqrt(h),f)                                           tred2 88
         e(i) = scale * g                                               tred2 89
         h = h - f * g                                                  tred2 90
         z(i,l) = f - g                                                 tred2 91
         f = 0.0e0                                                      tred2 92
c                                                                       tred2 93
         do 240 j = 1, l                                                tred2 94
            z(j,i) = z(i,j) / h                                         tred2 95
            g = 0.0e0                                                   tred2 96
c     .......... form element of a*u ..........                         tred2 97
            do 180 k = 1, j                                             tred2 98
  180       g = g + z(j,k) * z(i,k)                                     tred2 99
c                                                                       tred2100
            jp1 = j + 1                                                 tred2101
            if (l .lt. jp1) go to 220                                   tred2102
c                                                                       tred2103
            do 200 k = jp1, l                                           tred2104
  200       g = g + z(k,j) * z(i,k)                                     tred2105
c     .......... form element of p ..........                           tred2106
  220       e(j) = g / h                                                tred2107
            f = f + e(j) * z(i,j)                                       tred2108
  240    continue                                                       tred2109
c                                                                       tred2110
         hh = f / (h + h)                                               tred2111
c     .......... form reduced a ..........                              tred2112
         do 260 j = 1, l                                                tred2113
            f = z(i,j)                                                  tred2114
            g = e(j) - hh * f                                           tred2115
            e(j) = g                                                    tred2116
c                                                                       tred2117
            do 260 k = 1, j                                             tred2118
               z(j,k) = z(j,k) - f * e(k) - g * z(i,k)                  tred2119
  260    continue                                                       tred2120
c                                                                       tred2121
  290    d(i) = h                                                       tred2122
  300 continue                                                          tred2123
c                                                                       tred2124
  320 d(1) = 0.0e0                                                      tred2125
      e(1) = 0.0e0                                                      tred2126
c     .......... accumulation of transformation matrices ..........     tred2127
      do 500 i = 1, n                                                   tred2128
         l = i - 1                                                      tred2129
         if (d(i) .eq. 0.0e0) go to 380                                 tred2130
c                                                                       tred2131
         do 360 j = 1, l                                                tred2132
            g = 0.0e0                                                   tred2133
c                                                                       tred2134
            do 340 k = 1, l                                             tred2135
  340       g = g + z(i,k) * z(k,j)                                     tred2136
c                                                                       tred2137
            do 360 k = 1, l                                             tred2138
               z(k,j) = z(k,j) - g * z(k,i)                             tred2139
  360    continue                                                       tred2140
c                                                                       tred2141
  380    d(i) = z(i,i)                                                  tred2142
         z(i,i) = 1.0e0                                                 tred2143
         if (l .lt. 1) go to 500                                        tred2144
c                                                                       tred2145
         do 400 j = 1, l                                                tred2146
            z(i,j) = 0.0e0                                              tred2147
            z(j,i) = 0.0e0                                              tred2148
  400    continue                                                       tred2149
c                                                                       tred2150
  500 continue                                                          tred2151
c                                                                       tred2152
      return                                                            tred2153
      end                                                               tred2154
      subroutine tql2(nm,n,d,e,z,ierr)                                  tql2   3
c***begin prologue  tql2                                                tql2   4
c***date written   760101   (yymmdd)                                    tql2   5
c***revision date  830518   (yymmdd)                                    tql2   6
c***category no.  d4a5,d4c2a                                            tql2   7
c***keywords  eigenvalues,eigenvectors,eispack                          tql2   8
c***author  Smith, B. T., et al.                                        tql2   9
c***purpose  Compute eigenvalues and eigenvectors of symmetric          tql2  10
c            tridiagonal matrix.                                        tql2  11
c***description                                                         tql2  12
c                                                                       tql2  13
c     This subroutine is a translation of the ALGOL procedure tql2,     tql2  14
c     Num. Math. 11, 293-306(1968) by Bowdler, Martin, Reinsch, and     tql2  15
c     Wilkinson.                                                        tql2  16
c     Handbook for Auto. Comp., Vol.ii-Linear Algebra, 227-240(1971).   tql2  17
c                                                                       tql2  18
c     This subroutine finds the eigenvalues and eigenvectors            tql2  19
c     of a symmetric tridiagonal matrix by the ql method.               tql2  20
c     The eigenvectors of a full symmetric matrix can also              tql2  21
c     be found if  tred2  has been used to reduce this                  tql2  22
c     full matrix to tridiagonal form.                                  tql2  23
c                                                                       tql2  24
c     On input                                                          tql2  25
c                                                                       tql2  26
c        nm must be set to the row dimension of two-dimensional         tql2  27
c          array parameters as declared in the calling program          tql2  28
c          dimension statement.                                         tql2  29
c                                                                       tql2  30
c        n is the order of the matrix.                                  tql2  31
c                                                                       tql2  32
c        d contains the diagonal elements of the input matrix.          tql2  33
c                                                                       tql2  34
c        e contains the subdiagonal elements of the input matrix        tql2  35
c          in its last n-1 positions.  e(1) is arbitrary.               tql2  36
c                                                                       tql2  37
c        z contains the transformation matrix produced in the           tql2  38
c          reduction by  tred2, if performed.  if the eigenvectors      tql2  39
c          of the tridiagonal matrix are desired, z must contain        tql2  40
c          the identity matrix.                                         tql2  41
c                                                                       tql2  42
c      On output                                                        tql2  43
c                                                                       tql2  44
c        d contains the eigenvalues in ascending order.  if an          tql2  45
c          error exit is made, the eigenvalues are correct but          tql2  46
c          unordered for indices 1,2,...,ierr-1.                        tql2  47
c                                                                       tql2  48
c        e has been destroyed.                                          tql2  49
c                                                                       tql2  50
c        z contains orthonormal eigenvectors of the symmetric           tql2  51
c          tridiagonal (or full) matrix.  if an error exit is made,     tql2  52
c          z contains the eigenvectors associated with the stored       tql2  53
c          eigenvalues.                                                 tql2  54
c                                                                       tql2  55
c        ierr is set to                                                 tql2  56
c          zero       for normal return,                                tql2  57
c          j          if the j-th eigenvalue has not been               tql2  58
c                     determined after 30 iterations.                   tql2  59
c                                                                       tql2  60
c     calls pythag(a,b) for sqrt(a**2 + b**2).                          tql2  61
c                                                                       tql2  62
c     Questions and comments should be directed to B. S. Garbow,        tql2  63
c     Applied Mathematics Division, Argonne National Laboratory         tql2  64
c     ------------------------------------------------------------------tql2  65
c***references  B. T. Smith, J. M. Boyle, J. J. Dongarra, B. S. Garbow, tql2  66
c                 Y. Ikebe, V. C. Klema, C. B. Moler, *Matrix Eigen-    tql2  67
c                 system Routines - Eispack Guide*, Springer-Verlag,    tql2  68
c                 1976.                                                 tql2  69
c***routines called  pythag                                             tql2  70
c***end prologue  tql2                                                  tql2  71
c                                                                       tql2  72
      implicit real*8 (a-h,o-z)
      integer i,j,k,l,m,n,ii,l1,l2,nm,mml,ierr                          tql2  73
      dimension d(n),e(n),z(nm,n)                                       tql2  74
c     real d(n),e(n),z(nm,n)                                            tql2  74
c     real b,c,c2,c3,dl1,el1,f,g,h,p,r,s,s2                             tql2  75
c     real pythag                                                       tql2  76
c                                                                       tql2  77
c***first executable statement  tql2                                    tql2  78
      ierr = 0                                                          tql2  79
      if (n .eq. 1) go to 1001                                          tql2  80
c                                                                       tql2  81
      one=1.0
      do 100 i = 2, n                                                   tql2  82
  100 e(i-1) = e(i)                                                     tql2  83
c                                                                       tql2  84
      f = 0.0e0                                                         tql2  85
      b = 0.0e0                                                         tql2  86
      e(n) = 0.0e0                                                      tql2  87
c                                                                       tql2  88
      do 240 l = 1, n                                                   tql2  89
         j = 0                                                          tql2  90
         h = abs(d(l)) + abs(e(l))                                      tql2  91
         if (b .lt. h) b = h                                            tql2  92
c     .......... look for small sub-diagonal element ..........         tql2  93
         do 110 m = l, n                                                tql2  94
            if (b + abs(e(m)) .eq. b) go to 120                         tql2  95
c     .......... e(n) is always zero, so there is no exit               tql2  96
c                through the bottom of the loop ..........              tql2  97
  110    continue                                                       tql2  98
c                                                                       tql2  99
  120    if (m .eq. l) go to 220                                        tql2 100
  130    if (j .eq. 30) go to 1000                                      tql2 101
         j = j + 1                                                      tql2 102
c     .......... form shift ..........                                  tql2 103
         l1 = l + 1                                                     tql2 104
         l2 = l1 + 1                                                    tql2 105
         g = d(l)                                                       tql2 106
         p = (d(l1) - g) / (2.0e0 * e(l))                               tql2 107
c        r = pythag(p,1.0e0)                                            tql2 108
           pp=max(abs(p),one)                                           pythag14
           qq=min(abs(p),one)                                           pythag15
           if (qq.eq.0.0) go to 20                                      pythag16
   10      continue                                                     pythag17
           rr=(qq/pp)**2                                                pythag18
           tt=4.0+rr                                                    pythag19
           if (tt.eq.4.0) go to 20                                      pythag20
           ss=rr/tt                                                     pythag21
           pp=pp+2.0*pp*ss                                              pythag22
           qq=qq*ss                                                     pythag23
           go to 10                                                     pythag24
   20    r=pp                                                           pythag25
         d(l) = e(l) / (p + sign(r,p))                                  tql2 109
         d(l1) = e(l) * (p + sign(r,p))                                 tql2 110
         dl1 = d(l1)                                                    tql2 111
         h = g - d(l)                                                   tql2 112
         if (l2 .gt. n) go to 145                                       tql2 113
c                                                                       tql2 114
         do 140 i = l2, n                                               tql2 115
  140    d(i) = d(i) - h                                                tql2 116
c                                                                       tql2 117
  145    f = f + h                                                      tql2 118
c     .......... ql transformation ..........                           tql2 119
         p = d(m)                                                       tql2 120
         c = 1.0e0                                                      tql2 121
         c2 = c                                                         tql2 122
         el1 = e(l1)                                                    tql2 123
         s = 0.0e0                                                      tql2 124
         mml = m - l                                                    tql2 125
c     .......... for i=m-1 step -1 until l do -- ..........             tql2 126
         do 200 ii = 1, mml                                             tql2 127
            c3 = c2                                                     tql2 128
            c2 = c                                                      tql2 129
            s2 = s                                                      tql2 130
            i = m - ii                                                  tql2 131
            g = c * e(i)                                                tql2 132
            h = c * p                                                   tql2 133
            if (abs(p) .lt. abs(e(i))) go to 150                        tql2 134
            c = e(i) / p                                                tql2 135
            r = sqrt(c*c+1.0e0)                                         tql2 136
            e(i+1) = s * p * r                                          tql2 137
            s = c / r                                                   tql2 138
            c = 1.0e0 / r                                               tql2 139
            go to 160                                                   tql2 140
  150       c = p / e(i)                                                tql2 141
            r = sqrt(c*c+1.0e0)                                         tql2 142
            e(i+1) = s * e(i) * r                                       tql2 143
            s = 1.0e0 / r                                               tql2 144
            c = c * s                                                   tql2 145
  160       p = c * d(i) - s * g                                        tql2 146
            d(i+1) = h + s * (c * g + s * d(i))                         tql2 147
c     .......... form vector ..........                                 tql2 148
            do 180 k = 1, n                                             tql2 149
               h = z(k,i+1)                                             tql2 150
               z(k,i+1) = s * z(k,i) + c * h                            tql2 151
               z(k,i) = c * z(k,i) - s * h                              tql2 152
  180       continue                                                    tql2 153
c                                                                       tql2 154
  200    continue                                                       tql2 155
c                                                                       tql2 156
         p = -s * s2 * c3 * el1 * e(l) / dl1                            tql2 157
         e(l) = s * p                                                   tql2 158
         d(l) = c * p                                                   tql2 159
         if (b + abs(e(l)) .gt. b) go to 130                            tql2 160
  220    d(l) = d(l) + f                                                tql2 161
  240 continue                                                          tql2 162
c     .......... order eigenvalues and eigenvectors ..........          tql2 163
      do 300 ii = 2, n                                                  tql2 164
         i = ii - 1                                                     tql2 165
         k = i                                                          tql2 166
         p = d(i)                                                       tql2 167
c                                                                       tql2 168
         do 260 j = ii, n                                               tql2 169
            if (d(j) .ge. p) go to 260                                  tql2 170
            k = j                                                       tql2 171
            p = d(j)                                                    tql2 172
  260    continue                                                       tql2 173
c                                                                       tql2 174
         if (k .eq. i) go to 300                                        tql2 175
         d(k) = d(i)                                                    tql2 176
         d(i) = p                                                       tql2 177
c                                                                       tql2 178
         do 280 j = 1, n                                                tql2 179
            p = z(j,i)                                                  tql2 180
            z(j,i) = z(j,k)                                             tql2 181
            z(j,k) = p                                                  tql2 182
  280    continue                                                       tql2 183
c                                                                       tql2 184
  300 continue                                                          tql2 185
c                                                                       tql2 186
      go to 1001                                                        tql2 187
c     .......... set error -- no convergence to an                      tql2 188
c                eigenvalue after 30 iterations ..........              tql2 189
 1000 ierr = l                                                          tql2 190
 1001 return                                                            tql2 191
      end                                                               tql2 192
c     overlay(g9,10,4)
      subroutine spectr
c
c
c        Calc. spectrum for magnetic dipole(ii=0), electric dipole(ii=1),
c             or electric quadrupole(ii=2) transitions
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      parameter (kcc=kiser/4,klc4=2*kiser+1,klam=10000,kexc=999)
      parameter (kbgks=41,kenrgs=21,kcase=50,ktran=100000)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c2b/ncfg(kmx),ncfgp(kmx),pmup(kc,kc),eig(kmx),eigp(kmx),
     1  lcser(kmx),lcserp(kmx)
      common/c9/l1,l2,cflag(kc,2),cgengy(kc,2),swt(kc,2),imax
      common/c3b/t(klam),tp(klam),s2(klam),soabss(klam),
     1  aa(kmx),aap(kmx),gaa(klam),gaap(klam),brnch(klam),
     2  icut(66),sgfcut(66),sfcut(66),didgf(66),dsgfdgf(66),title(20),
     3  ficut(66),fnucut(66),fnuplt(82),sgf(66),fiplt(82),sgfplt(82),
     4  ncser(klam),aat(kmx),aapt(kmx)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      common/c6/emin,emax,sumwt,flbdn,flbdx,fnunp,fnuxp,nlev,iewr
      common       d(kmx,kmx)
      common/c3lc2/v(kmx,kmx)
      common/c3lc3/ct4(kmx,kmx)
      common/c3lc4/cta(kmx,kmx)
      common/c3lc5/goss(ktran,kbgks)
      common/c3lc6/gaaxc(kmx,kexc),brnchx(kexc,kexc)
      common/c3lcd/dumlc5
      common    elem(3,kc,2),vpar(kpr,2),avp(9,2),aveig(2),avcg(2),
     1  npark(2),npav(kc),fjt(klam),fjtp(klam),ncserp(klam),
     2  gaat(klam),gaapt(klam)
      common/ctkev/nptkev,ntkev,tkev(6),tunrgy(6),brnchl(6),brncht(6),
     1  eionry
      common/sortdum/dum(2),idum(2)
      dimension gfcut(66)
      dimension x(klam),fnu(klam),flam(klam),sumfj(kc)
      equivalence (cta,x,fnu),(ct4,flam)
      dimension spid(3)
      common/c7/g1,sumgaa,sumgar,sumgaat
      common/c8/exc(kexc),jexc(kexc),mexc(kexc)
      common/energies/etot(kc,2),ee8(kc,2),e0kin(kc),ekin(kmx)
      common/pwborn/nbigks,nenrgs,ekminl,ekmaxl,delekl,bigks(kbgks),
     1  xmin,xmax,tev(25),corr(kenrgs),ibk,ipwr,i1
      dimension iser(klam),exc1(kexc),jexc1(kexc),elemj(kexc),delm1(kc)
      integer h18
      character*10 parnam(kpr,2)
      character br1*9,idfg(15)*11
      character*8 fidls(kmx,2),fidjj(kmx,2),ldes(kmx),ldesp(kmx)
      character*8 lldes(klam),lldesp(klam)
      common/char/parnam,fidls,fidjj,ldes,ldesp
      dimension ddjj(kmx,1)
      common/djj/ddjj
      data h1/1h /,h2/4h ---/,h3/6hintens/,h4/3hity/,h5/6hwavenu/,
     1  h6/4hmber/,h7/6h(cm  )/,h8/6hwavele/,h9/4hngth/,h10/3h(a)/,
     2  h11/2h =/,h12/6hoscill/,h13/8hator str/,h14/8hength (g/,
     3  h15/2hf)/,h17/2h-1/,h18/1h(/,h19/7hf.10+6)/
      data (spid(i),i=1,3) /8h mag dip,8helec dip,8helec qud/
c
c
c     kmx=5000
c     kexc=999
c     klam=10000
c     ktran=100000
c
c          For special Lund Univ. print formats (on level-sort
c               line lists), set ilund=1; otherwise, set ilund=0.
c
      ilund=0
c
c          For paper with 66 lines per page, headings on every page,
c               set jlines=52.
c          For paper with 51 lines per page, headings every second
c               page, set jlines=84.
c
      jlines=52
c
c
cc                                87 06 02  joe
c          If dmin.lt.0, delete upward transitions for level sorts.
c          If abs(dmin) gt 1.0 and le 50.0, delete weak lines on the
c               basis of ga<10**abs(dmin) rather than gf<abs(dmin).
      negtp=0
      if (dmin.lt.0.0) negtp=1
      dminga=abs(dmin)
      if (dminga.gt.1.0.and.dminga.le.50.0) then
        iminga=dminga
        dminga=10**iminga
        dmin=0.0
      else
        dminga=0.0
      endif
      write (8,5009)
 5009 format('   -1')
cc                                 slut
      if (iarg1.eq.0) go to 92
      if (igen.lt.5) go to 92
      read (ir,8) nbigks,ekminl,ekmaxl,delekl,nenrgs,xmin,xmax
!       write(122,8) nbigks,ekminl,ekmaxl,delekl,nenrgs,xmin,xmax

    8 format (i5,3f15.10,i10,2f10.2)
      write (iw,9) nbigks,ekminl,ekmaxl,delekl,nenrgs,xmin,xmax
    9 format (//i5,3f15.10,i10,2f10.2)
      do 90 i=1,ktran
      do 90 j=1,nbigks
   90 goss(i,j)=0.0
   92 ii=iarg1
      ie1=iarg2
      ie2=iarg3
      tunrgy(1)=9.9e10
      do 94 i=2,6
   94 tunrgy(i)=tkev(i)*8065479/uenrgy
      uenrev=uenrgy/8065.479
      gold=0.0
      hold=0.0
      ipwr=1
      ibk=0
c
c          Read reduced mupole matrix elements
c
      iread=0
      if (ii.eq.0) go to 104
  100 read (ir,12) ieras,n
      write(122,12) ieras,n
      
   12 format (50x,a1,6x,i1)

      backspace ir
      if (ieras.ne.h18) go to 999
      if (igen.lt.5.and.n.ne.ii) go to 999
      ipwr=n
      iptg=0
      if (ibk.eq.0.or.(ipwr.gt.irmn.and.ibk.eq.1)) iptg=1
      if (ii.ne.1) iptg=0
      if (iptg.eq.1) write (iw,13) spid(ii+1)
   13 format (1h1,59x,a9,9h spectrum////)
      iback=iread
      if (igen.ge.5.and.n.ne.irmn) iback=0
      if (iback.eq.0) go to 104
      do 102 i=1,iread
  102 backspace ic
      iread=0
  104 l1=ie1-ila+1
      l2=ie2-ila+1
      jnx1=nsconf(2,l1)
      jnx2=nsconf(2,l2)
      jnx=max0(jnx1,jnx2)
      do 110 i=1,jnx1
      do 110 j=1,jnx2
      pmup(i,j)=1.0
      if (ii.eq.0) go to 110
  105 read (ir,14) a,b,c,z,e,f, pmup(i,j), g,h, frac, pid
      write(122,14) a,b,c,z,e,f, pmup(i,j), g,h, frac, pid
        
   14 format (3a6,2x,3a6,2x, f10.5, a6,a8, f6.4, a2,2e4.1)
  106 if (iptg.eq.1) write(iw,15) i,a,b,c,j,z,e,f,g,h,pmup(i,j),frac,pid
   15 format (i5,5x,3a6,i10,5x,3a6,10x,a6,a8,1h=,f15.5,6x,5hfrac=,f7.4,
     1  5x,a2)
      if (frac.eq.0.0) frac=1.0e-5
      if (pmup(i,j).ne.0.0) delm1(j)=1.0/frac**2
      csigma=0.0
      if (g.eq.gold.and.h.eq.hold) csigma=8.06662e-18
      gold=g
      hold=h
  110 continue
c          csigma.gt.0.0 for photoionization cross-section calc (sigma)
      if (nsconf(3,2).ge.0.or.l1.eq.l2.or.texcit.gt.0.0) csigma=0.0
c
  120 gfcut(1)=0.0
      eras=-14.0
      del=0.25
      do 130 j=2,65
      eras=eras+del
  130 gfcut(j)=exp(2.302585093*eras)
      gfcut(66)=1.0e10
      fnux=1.0e8/(flbdn*uenrgy)
      fnun=1.0e8/(flbdx*uenrgy)
      assign 57 to ifmt1
      assign 58 to ifmt2
      if (csigma.gt.0.0) go to 150
      assign 56 to ifmt1
      if (texcit.eq.0.0) go to 150
      assign 51 to ifmt1
      assign 53 to ifmt2
c
c
c
  150 rewind ie1
      rewind ie2
      rewind 20
      fnunp=1.0e20
      fnuxp=0.0
      sj31=100.0
      sj32=100.0
      pmax=sqrt(2.0/3.0)
      pmax=0.0001
      do 160 i=1,jnx1
      do 160 j=1,jnx2
      if (abs(pmup(i,j)).gt.abs(pmax)) pmax=pmup(i,j)
  160 continue
      a=1.0/pmax
      psq=3.0375e-6*(pmax**2)
      if (ii.eq.0) psq=psq*(0.5/137.04)**2
      if (igen.ge.5) go to 162
      if (ii.eq.2) psq=psq*((3.14159*0.529)**2)/5.0
      go to 163
  162 psq=psq*3.0
  163 sums2=0.0
      sums2n=0.0
      sums2m=0.0
      sumgf=0.0
      sumf=0.0
      sumgar=0.0
      jcutx=0
      do 170 j=1,66
      icut(j)=0
      sgfcut(j)=0.0
  170 sfcut(j)=0.0
      i=0
      i0=0
      i0n=0
      i0x=0
      ijjp=0
      ilostt=0
      icdlt=0
      ibrnch=0
      d0max=0.0
      do 175 l=1,kmx
      do 175 j=1,kexc
  175 gaaxc(l,j)=0.0
  180 if (iptg.eq.1) write (iw,18)
   18 format (////18x,12hno. of lines/
     1  5x,1hj,5x,2hjp,5x,4hj-jp,3x,5htotal,3x,4hklam,4x,5hilost,
     2  8x,4hdmin,6x,3hi0 ,5x,3hi0n,5x,3hi0x,3x,6hitrunc,3x,5hntkev/)
c
c          Read dipole matrix for basis vectors
c
  200 read (ic) scrj8,scrj8p,nls,nlsp, ((d(l,lp),l=1,nls), lp=1,nlsp),
     1  ncfg,ncfgp
      iread=iread+1
      if (scrj8.lt.0.0) go to 560
      do 220 l=1,nls
      do 220 lp=1,nlsp
      in=ncfg(l)
      jn=ncfgp(lp)
  220 d(l,lp)=d(l,lp)*a*pmup(in,jn)
  250 itrunc=i
      i00=i0
      i0n0=i0n
      i0x0=i0x
      ijjp0=ijjp
      sums20=sums2
      sumsn0=sums2n
      sumsm0=sums2m
      ilost=0
c
c          Read eigenvalues and vectors,
c               and calc mupole matrix for actual eigenvectors
c
  300 if (scrj8-sj31) 301,302,305
  301 continue
  302 rewind ie1
c 301 backspace ie1
c     backspace ie1
c 302 backspace ie1
c     backspace ie1
  305 read (ie1) sj31,nls, (eig(lp), (v(l,lp),l=1,nls), lp=1,nls),
     1  lcser,ldes
      read (ie1) lx, (aa(lp),aat(lp), lp=1,nls)
      if (scrj8-sj31) 301,308,305
  308 if (ie1.eq.ie2) sj32=sj31
      if (lx.ne.0.and.lx.ne.nls) ibrnch=7
      do 360 l=1,nls
      do 360 lp=1,nlsp
      cta(l,lp)=0.0
      ct4(l,lp)=0.0
      do 355 k=1,nls
      eras=v(k,l)*d(k,lp)
      cta(l,lp)=cta(l,lp)+abs(eras)
  355 ct4(l,lp)=ct4(l,lp)+eras
  360 continue
  400 if (scrj8p-sj32) 401,402,405
  401 continue
  402 rewind ie2
c 401 backspace ie2
c     backspace ie2
c 402 backspace ie2
c     backspace ie2
  405 read (ie2) sj32,nlsp, (eigp(lp), (v(l,lp),l=1,nlsp), lp=1,nlsp),
     1  lcserp,ldesp
      read (ie2) lxp, (aap(lp),aapt(lp), lp=1,nlsp)
     1  ,nlst,ixc,ixc1, (exc(j), (gaaxc(lp+nlst,j),lp=1,lxp), j=1,ixc1)
      if (scrj8p-sj32) 401,408,405
  408 if (ie1.eq.ie2) sj31=sj32
      if (lxp.ne.0.and.lxp.ne.nlsp) ibrnch=7
c
c          Calculate spectrum
c
      ijjp=0
      deldmin=0.1
      icontin=0
      do 520 l=1,nls
      do 520 lp=1,nlsp
      if (eig(l).gt.-4000.0.and.eigp(lp).gt.-4000.0) go to 450
      icontin=7
      go to 520
  450 if (ie1.eq.ie2.and.scrj8.eq.scrj8p.and.l.gt.lp) go to 520
      erasa=0.0
      eras=0.0
      do 455 k=1,nlsp
      erasa=erasa+cta(l,k)*abs(v(k,lp))
  455 eras=eras+ct4(l,k)*v(k,lp)
      erass=eras*abs(eras)
      eras=eras*eras
      sums2=sums2+eras
      if (ie1.ne.ie2) go to 490
      if (scrj8.ne.scrj8p) go to 480
      if (l.eq.lp) go to 520
  480 sums2=sums2+eras
  490 continue
      d0=eras
      eras1=abs(eig(l)-eigp(lp))
      if (lcser(l).le.nck(1).and.lcserp(lp).le.nck(2)) go to 494
      if (l1.ne.l2) go to 492
      if (lcserp(lp).le.nck(1).and.lcser(l).le.nck(2)) go to 494
  492 icdlt=icdlt+1
      go to 520
  494 sums2n=sums2n+eras
      if (l1.eq.l2.and.scrj8.eq.scrj8p) sums2n=sums2n+eras
      if (eras1.ge.fnun) go to 498
      i0n=i0n+1
      go to 520
  498 if (eras1.le.fnux) go to 499
      i0x=i0x+1
      go to 520
  499 if (texcit.le.0.0) go to 501
      temp=eras1*uenrgy
      ga=0.6698*psq*eras*(temp**3)
      d0=ga*exp(-(max(eig(l),eigp(lp))-emean)/texcit)
  501 if (d0.ge.dmin) go to 510
      i0=i0+1
      if (d0.gt.d0max) d0max=d0
      go to 520
  510 if (i.lt.klam) go to 515
      if (itrunc.gt.0) go to 511
      if (itrunc.eq.0) go to 513
  511 i=itrunc
      i0=i00
      i0n=i0n0
      i0x=i0x0
      sums2=sums20
      sums2n=sumsn0
      sums2m=sumsm0
      if (dmin.le.0.0.and.ntkev.eq.0) go to 560
      if (dmin.le.0.0.and.texcit.gt.0.0) dmin=1.0e4
      if (dmin.le.0.0) dmin=0.00001
      do 512 i=1,iread
  512 backspace ic
      iread=0
      dmin=dmin+min(dmin,deldmin)
      if (dmin.gt.4.0) dmin=2.0*dmin
      go to 150
  513 ilost=ilost+1
      go to 520
  515 i=i+1
      ijjp=ijjp+1
      eras1=1.e-6*(scrj8+0.01*l)
      t(i)=eig(l)+eras1
      fjt(i)=scrj8
      eras2=1.e-6*(scrj8p+0.01*lp)
      tp(i)=eigp(lp)+eras2
      fjtp(i)=scrj8p
      if (igdlev.eq.0.or.i.eq.1) go to 518
      if (t(i).eq.t(1)) go to 518
      if (t(i).lt.t(1)) go to 517
      i=i-1
      ijjp=max0(ijjp-1,0)
      go to 520
  517 t(1)=t(i)
      fjt(1)=fjt(i)
      tp(1)=tp(i)
      fjtp(1)=fjtp(i)
      ijjp=max0(ijjp-i+1,0)
      i=1
      sums2m=0.0
  518 gaa(i)=(2.0*scrj8+1.0)*aa(l)
      gaap(i)=(2.0*scrj8p+1.0)*aap(lp)
      gaat(i)=(2.0*scrj8+1.0)*aat(l)
      gaapt(i)=(2.0*scrj8p+1.0)*aapt(lp)
      s2(i)=eras
      sums2m=sums2m+eras
      soabss(i)=(erass+1.0e-30)/(erasa*erasa+1.0e-30)
      iser(i)=lp-(nlsp-lxp)+nlst
      ncser(i)=lcser(l)
      ncserp(i)=lcserp(lp)
      lldes(i)=ldes(l)
      lldesp(i)=ldesp(lp)
  519 if (ie1.ne.ie2.or.t(i).lt.tp(i)) go to 520
      t(i)=eigp(lp)+eras2
      fjt(i)=scrj8p
      tp(i)=eig(l)+eras1
      fjtp(i)=scrj8
      eras=gaa(i)
      gaa(i)=gaap(i)
      gaap(i)=eras
      eras=gaat(i)
      gaat(i)=gaapt(i)
      gaapt(i)=eras
      ncser(i)=lcserp(lp)
      ncserp(i)=lcser(l)
      lldes(i)=ldesp(lp)
      lldesp(i)=ldes(l)
  520 continue
  550 if (iptg.eq.1.and.dmin.le.9999.0) write (iw,52) scrj8,scrj8p,ijjp,
     1  i,klam,ilost,dmin,i0,i0n,i0x,itrunc,ntkev
   52 format (1h ,2f6.1,4i8,f15.6,i6,4i8)
      if (iptg.eq.1.and.dmin.gt.9999.0) write (iw,49) scrj8,scrj8p,ijjp,
     1  i,klam,ilost,dmin,i0,i0n,i0x,itrunc,ntkev
   49 format (1h ,2f6.1,4i8,1p,e15.3,i6,4i8)
      if (i.eq.klam.and.ilost.gt.0) go to 560
      go to 200
c
c          Sort lines by levels of first parity
c
  560 imax=i
      if (imax.eq.0) go to 980
      ilostt=ilostt+ilost
      ipt=0
      if (mod(ispecc,2).ne.0) ipt=1
      if (ispecc.eq.9) ipt=0
      if (igen.ge.5) ipt=iptg
      if (ipt.eq.0.and.igen.lt.5) go to 567
      do 562 i=1,imax
  562 x(i)=1.0e8*t(i)+tp(i)
      call sort2(imax,12,x,d,iser,t,ncser,ncserp,tp,fjt,fjtp,s2,soabss,
     1  gaa,gaap,gaat)	 
      if (imax.le.1) go to 563
      call order2(imax,d,gaapt)	  
      call orderch(imax,d,lldes)	  
      call orderch(imax,d,lldesp)
  563 if (igen.lt.5) go to 567
      if (imax.le.ktran) go to 565
      write (iw,54) ktran,imax
   54 format (//26h0*****WARNING-- only first,i5,3h of,i6,
     1  42h lines retained, for lack of storage space///)
      imax=ktran
  565 if (ipwr.ne.irmn) go to 567
      ek=ekminl+delekl*ibk
      ibk=ibk+1
      if (ibk.gt.kbgks) stop 57
      bigks(ibk)=ek
  567 sumfiu=0.0
      sumfid=-0.0
      sumgfph=0.0
      jcx=min0(nsconf(2,2),nck(2))
      do 570 jc=1,jcx
  570 sumfj(jc)=0.0
      sumga=0.0
      s2max=0.0
      gfmax=0.0
      i1=1
      j=0
      jnxx=jnx
      ijoe=1
      do 599 i=1,imax
      if (j.gt.0) go to 575
      if (ipt.eq.0) go to 575
      if (ilund.ne.0.and.i.gt.1) go to 575
      write (iw,55) spid(ii+1),uenrgy,uenrev,
     1  (jn, (elem(l,jn,l1),l=1,3), (elem(l,jn,l2),l=1,3), jn=1,jnxx)
   55 format (1h1,9x,a8,9h spectrum,5x,21h(energies in units of,
     1  f8.1,7h cm-1 =,f8.2,4h ev)//(i5,6x,3a6,12h   ---      ,3a6))
      if (ilund.eq.0) go to 572
      write (iw,1056)
 1056 format (/'            e      j     level        delta e ',
     1   ' lambda(a)  log gf ga(sec-1) cf/br'/)
      go to 575
  572 if (texcit.eq.0.0) write (iw,ifmt1)
      if (texcit.gt.0.0) write (iw,ifmt1) texcit
   51 format (/1h0,8x,7h   e   , 3x,8hj   conf,11x,8h   ep   , 2x,
     1  4h jp ,6h confp,10x,
     2  8h delta e,3x,9hlambda(a),10h s/pmax**2,3x,2hgf,10h ga*bltzmn,
     3  10h ga(sec-1),9h cf,brnch/103x,6h(texc=,f7.1,1h))
   56 format (/1h0,8x,7h   e   , 3x,8hj   conf,11x,8h   ep   , 2x,
     1  4h jp ,6h confp,10x,
     2  8h delta e,3x,9hlambda(a),1x,9hs/pmax**2,3x,2hgf,4x,6hlog gf,1x,
     3  9hga(sec-1),9h cf,brnch/)
   57 format (/1h0,8x,7h   e   , 3x,8hj   conf,11x,8h   ep   , 2x,
     1  4h jp ,6h confp,10x,
     2  8h delta e,3x,9hlambda(a),1x,9hs/pmax**2,3x,2hgf,4x,6hlog gf,1x,
     3  10hsigma(cm2),5h   cf/)
      j=jlines-jnxx
      jnxx=min0(5,jnx)
  575 fnu(i)=abs(t(i)-tp(i))
      eras1=fnu(i)*uenrgy
      flam(i)=1.0e8/eras1
      if (s2(i).gt.s2max) s2max=s2(i)
      gf=psq*s2(i)*eras1
      if (igen.ge.5) goss(i,ibk)=goss(i,ibk)+gf
      if (igen.lt.5.and.ii.eq.2) gf=gf/(flam(i)**2)
      alggf=-99.999
      if (gf.gt.0.0) alggf=log10(gf)
      ga=0.66698*gf*eras1*eras1
      if (texcit.gt.0.0) alggf=ga*exp(-(max(t(i),tp(i))-emean)/texcit)
      jc=ncserp(i)
      if (csigma.gt.0.0) ga=csigma*gf*delm1(jc)/(2.0*fjt(i)+1.0)
      if (gf.gt.gfmax) gfmax=gf
      sumgf=sumgf+gf
      sumf=sumf+gf/(2.0*fjt(i)+1.0)
      if (ipt.eq.0) go to 599
      if (ilund.eq.0) go to 577
      nccc=ncser(i)
      if (ijoe.gt.0) write (iw,1057) t(i),fjt(i),nccc,lldes(i),
     1  (elem(l,nccc,l1),l=1,3)
 1057 format (5x,'* * *  ',f10.3,f5.1,i4,1x,a8,5x,3a6,' * * *',/)
      ijoe=0
      if (t(i).lt.tp(i).and.negtp.eq.1) go to 578
      if (ga.lt.dminga) go to 578
      write (iw,1058) i,tp(i),fjtp(i),
     1  ncserp(i),lldesp(i),fnu(i),flam(i),alggf,ga,soabss(i)
 1058 format (1h ,i4,f11.3,f5.1,i3,1x,a8,f12.3,
     1  f11.3,f8.3,1pe10.3,0pf6.2)
      go to 578
  577 write (iw,ifmt2) i,t(i),fjt(i),ncser(i),lldes(i),tp(i),fjtp(i),
     1  ncserp(i),lldesp(i),fnu(i),flam(i),s2(i),gf,alggf,ga,soabss(i)
   53 format (1h ,i4,f11.4,f5.1,i3,1x,a8,f13.4,f5.1,i3,1x,a8,f13.4,
     1  f12.4,f8.3,f9.4,1p,2e9.2,0p,f8.4)
   58 format (1h ,i4,f11.4,f5.1,i3,1x,a8,f13.4,f5.1,i3,1x,a8,f13.4,
     1  f12.4,f8.3,f9.4,f8.3,1pe10.3,0pf8.4)
      j=j-1
  578 if (t(i).gt.tp(i)) go to 580
      sumfiu=sumfiu+gf
      sumfj(jc)=sumfj(jc)+gf
      go to 584
  580 sumga=sumga+ga
      sumfid=sumfid-gf
  584 continue
      if (abs(iw6).le.6) go to 585
      if (tp(i).le.t(i)) go to 1584
      sumgfph=sumgfph+gf
 1584 if (i.eq.imax) go to 2584
      if (abs(tp(i+1)-tp(i)).lt.1.0e-6*tp(i)) go to 585
 2584 jjj=ncser(i)
      jjjp=ncserp(i)
      ephoton=etot(jjjp,2)-etot(jjj,1)
      ebd=tp(i)-ee8(jjjp,2)*109737.31/uenrgy
      delebdbd=ebd-t(i)
      ek=ephoton-delebdbd
      write (iw,4584) ephoton,ebd,delebdbd,sumgfph,ek
 4584 format (' ephoton(av)=',f9.4,5x,'   ebound=',f9.4,8x,
     1  '   dele-bdbd=',f9.4,12x,'  sumgf=',f9.4,6x,'   ekin=',f9.4)
      sumgfph=0.0
  585 if (i.eq.imax) go to 586
      if (t(i+1).eq.t(i)) go to 599
  586 eras=2.0*fjt(i)+1.0
      flife=9.9946e33
      if (sumga.gt.0.0) flife=eras/sumga
      eras=1.0/eras
      sumfiu=sumfiu*eras
      sumfid=sumfid*eras
      sumfi=sumfiu+sumfid
      if (ilund.eq.0) go to 588
      ijoe=1
      write (iw,1059) sumfiu,sumfid,sumfi,flife,sumga
 1059 format (/1x,6hsumfi=,f7.4,f8.4,2h =,f8.4,2x,
     1  9hrad.life=,1pe10.3,4h sec,2x,6hsumga=,e10.3/)
      go to 589
  588 write (iw,59) t(i),fjt(i),sumfiu,sumfid,sumfi
     1,flife,sumga
      write (8,509) fjt(i),t(i),sumga/(2.*fjt(i)+1.)
  509 format (5x,3h J=,f5.1,5x,3hEJ=,f9.3,5x,4hArt=,e10.3)
   59 format (5x,f13.4,f5.1,17x,6hsumfi=,f7.4,f8.4,2h =,f8.4,5x,
     1  9hlifetime=,1pe10.3,4h sec,5x,6hsumga=,e10.3)
  589 do 590 jc=1,jcx
  590 sumfj(jc)=sumfj(jc)*eras
      if (jcx.gt.1) write (iw,60) (sumfj(jc),jc, jc=1,jcx)
   60 format (6x,13hsumf by conf=,10(f8.4,i3)/19x,10(f8.4,i3))
      do 592 l=i1,i
      brnch(l)=0.0
      if (t(l).lt.tp(l)) go to 592
      brnch(l)=gaat(l)+sumga
      if (brnch(l).le.0.0) go to 592
      eras1=fnu(l)*uenrgy
      brnch(l)=gaa(l)*0.66698*psq*s2(l)*(eras1**3)/brnch(l)
  592 continue
      i1=i+1
      sumfiu=0.0
      sumfid=-0.0
      do 595 jc=1,jcx
  595 sumfj(jc)=0.0
      sumga=0.0
      write (iw,61)
   61 format (1h )
      if (ilund.eq.0) go to 598
      ijoe=1
      write (iw,2061)
 2061 format ('      =  =  =  =  =  =  =  =  =  =  =  =  =  =  ='/)
      go to 599
  598 j=j-2
      if (jcx.gt.1) j=j-(jcx+9)/10
  599 continue
      call clock(time)
      delt=time-time0
c      if (iw6.lt.0) write (6,2059) delt
 2059 format (' Finished first-parity sort at time=',f8.3,' min')
c
c          Sort lines by levels of second parity
c
      if (csigma.gt.0.0) assign 56 to ifmt1
      ipt=0
      if (ispecc.ge.8.or.icontin.ne.0) ipt=1
      if (mod(ispecc/2,2).ne.0) ipt=2
      if (ipt.eq.0) go to 700
      brnchr=0.0
      do 602 i=1,6
  602 brncht(i)=0.0
      brncha=0.0
      do 605 j=1,kexc
      do 604 i=1,kexc
  604 brnchx(i,j)=0.0
      mexc(j)=j
      eras=10000*jexc(j)
  605 v(j,23)=eras+exc(j)
      call sort2(ixc1,3,v(1,23),d,mexc,exc,jexc,idum,dum,dum,dum,dum,
     1  dum,dum,dum,dum)
      do 608 i=1,imax
  608 v(i,23)=t(i)+1.0e9*tp(i)
      call sort2(imax,12,v(1,23),d,iser,t,ncser,ncserp,tp,fjt,fjtp,
     1  s2,soabss,gaa,gaap,gaat)
      if (imax.le.1) go to 609
      call order2(imax,d,gaapt)
      call order2(imax,d,brnch)
      call orderch(imax,d,lldes)
      call orderch(imax,d,lldesp)
  609 sumfiu=0.0
      sumfid=-0.0
      sumga=0.0
      i1=1
      j=0
      jnxx=jnx
      ijoe=1
      do 640 i=1,imax
      fnu(i)=abs(t(i)-tp(i))
      eras1=fnu(i)*uenrgy
      flam(i)=1.0e8/eras1
      if (j.gt.0) go to 610
      if (ipt.lt.2) go to 610
      if (ilund.ne.0.and.i.gt.1) go to 610
      write (iw,55) spid(ii+1),uenrgy,uenrev,
     1  (jn, (elem(l,jn,l1),l=1,3), (elem(l,jn,l2),l=1,3), jn=1,jnxx)
      if (ilund.eq.0) go to 607
      write (iw,1056)
      go to 610
  607 if (texcit.eq.0.0) write (iw,ifmt1)
      if (texcit.gt.0.0) write (iw,ifmt1) texcit
      j=jlines-jnxx
      jnxx=min0(5,jnx)
  610 gf=psq*s2(i)*eras1
      if (igen.lt.5.and.ii.eq.2) gf=gf/(flam(i)**2)
      alggf=-99.999
      if (gf.gt.0.0) alggf=log10(gf)
      ga=0.66698*gf*eras1*eras1
      if (texcit.gt.0.0) alggf=ga*exp(-(max(t(i),tp(i))-emean)/texcit)
      if (ipt.lt.2) go to 612
      if (ilund.eq.0) go to 611
      nccc=ncserp(i)
      if (ijoe.gt.0) write (iw,1057) tp(i),fjtp(i),nccc,lldesp(i),
     1  (elem(l,nccc,l2),l=1,3)
      ijoe=0
cc
      if (t(i).gt.tp(i).and.negtp.eq.1) go to 612
      if (ga.lt.dminga) go to 612
      write (iw,1058) i,t(i),fjt(i),ncser(i),lldes(i),
     1  fnu(i),flam(i),alggf,ga,soabss(i)
      go to 612
  611 write (iw,ifmt2) i,t(i),fjt(i),ncser(i),lldes(i),tp(i),fjtp(i),
     1  ncserp(i),lldesp(i),fnu(i),flam(i),s2(i),gf,alggf,ga,soabss(i)
      j=j-1
  612 if (t(i).lt.tp(i)) go to 615
      sumfiu=sumfiu+gf
      go to 617
  615 sumga=sumga+ga
      sumgar=sumgar+ga
      sumfid=sumfid-gf
  617 continue
      if (i.eq.imax) go to 620
      if (tp(i+1).eq.tp(i)) go to 640
  620 eras=2.0*fjtp(i)+1.0
      flife=9.9946e33
      if (sumga.gt.0.0) flife=eras/sumga
      eras=1.0/eras
      sumfiu=sumfiu*eras
      sumfid=sumfid*eras
      sumfi=sumfiu+sumfid
      if (ilund.eq.0) go to 621
      ijoe=1
      if (ipt.ge.1)
     1  write (iw,1059) sumfiu,sumfid,sumfi,flife,sumga
      go to 1621
  621 if (ipt.ge.1)
     1  write (iw,62) tp(i),fjtp(i),sumfiu,sumfid,sumfi,flife,sumga
      if (ipt.ge.1)
     1 write (8,509) fjtp(i),tp(i),sumga/(2.*fjtp(i)+1.)
       write (890,509) fjtp(i),tp(i),sumga/(2.*fjtp(i)+1.)
   62 format (12x,f13.3,f6.1,9x,6hsumfi=,f7.4,f8.4,2h =,f8.4,5x,
     1  14hrad. lifetime=,1pe10.3,4h sec,5x,6hsumga=,e10.3)
 1621 brnch(i)=gaapt(i)+sumga
      if (brnch(i).le.0.0) go to 630
      brncha=brncha+gaap(i)*(gaapt(i)-gaap(i))/brnch(i)
      brion=gaapt(i)/brnch(i)
      if (ipt.lt.1.or.brion.le.0.0) go to 622
      flife=1.0/(eras*(sumga+gaapt(i)))
      write (iw,63) brion,flife,gaapt(i)
!!!!!!sumg-ireland
     
      write (200,"(f9.3,'$',e10.3,'$',f6.3)") tp(i),gaapt(i),
     !  (6.582*(1e-16)*gaapt(i))/2
      write (201,"(f9.3,2x,f9.3)") tp(i), (6.582*(1e-16)*gaapt(i))/2
!!!!!!end


   63 format (55x,6hbrion=,1pe10.3,5x,14htot. lifetime=,e10.3,
     1  4h sec,4x,7hgaatot=,e10.3)
      j=j-1
  622 if (ixc.eq.0) go to 625
      j2=iser(i)
      do 624 jj=1,ixc
      m1=mexc(jj)
      jexc1(jj)=jexc(jj)
      exc1(jj)=exc(jj)
      do 624 jk=1,ixc
      m2=mexc(jk)
      brnchx(jj,jk)=brnchx(jj,jk)+gaaxc(j2,m1)*gaaxc(j2,m2)/brnch(i)
  624 continue
  625 eras=0.0
      do 627 l=i1,i
      ga=0.0
      if (t(l).gt.tp(l)) brnch(l)=0.0
      if (t(l).gt.tp(l)) go to 627
      ga=0.66698*psq*s2(l)*((fnu(l)*uenrgy)**3)
      brnch(l)=gaap(i)*ga/brnch(i)
      brnchr=brnchr+brnch(l)
      eras=eras+brnch(l)
  627 continue
c          Print t-dependence of brnch, summed over both
c               upper and lower levels
      if (ntkev.eq.0) go to 630
      nc=ncserp(i)
      ll=npav(nc)
      eras1=vpar(ll,l2)-tp(i)
      np1=ntkev+1
      do 629 l=1,np1
      brnchl(l)=eras*exp(eras1/tunrgy(l))
  629 brncht(l)=brncht(l)+brnchl(l)
      if (nptkev.gt.1) write (iw,64) (tkev(l),brnchl(l), l=1,np1)
   64 format (18h t(kev), brnch=   ,6(0pf6.1,1pe11.4))
      j=j-1
  630 continue
      i1=i+1
      sumfiu=0.0
      sumfid=-0.0
      sumga=0.0
      if (ilund.eq.0) go to 639
      ijoe=1
      write (iw,2061)
      go to 640
  639 write (iw,61)
      j=j-2
  640 continue
      jnxx=jnx
      if (nptkev.gt.0.and.brnchr.gt.0.0)
     1  write (iw,55) spid(ii+1),uenrgy,uenrev,
     2  (jn, (elem(l,jn,l1),l=1,3), (elem(l,jn,l2),l=1,3), jn=1,jnxx)
c
      write (iw,65) brnchr,brncha
   65 format (//14x,10h gm*frbar=,1pe11.4,10x,9hgm*fabar=,e11.4)
      np1=ntkev+1
      if (ntkev.gt.0) write (iw,64) (tkev(l),brncht(l), l=1,np1)
      if (nptkev.eq.0.or.nptkev.eq.2) go to 670
      jnxx=min0(jnxx,3)
      write (13,71) (elem(l,1,1),l=1,3),((elem(l,jn,2),l=1,3),jn=1,jnxx)
   71 format (4(3a6,2x))
      write (13,72) (tkev(l), l=2,np1)
   72 format (37x,11ht(kev)=inf.,2x,5f6.2)
      gm=1.0
      nn=nsconf(2,2)
      ll=0
      do 642 i=1,nosubc
      mm=nosubc-i+1
      eras=nijk(mm,nn,2)
      if (eras.gt.0.0) ll=ll+1
      if (ll.eq.1) go to 642
      eras1=4.0*fllijk(mm,nn,2)+2.0
      gm=gm*fctrl(eras1)/(fctrl(eras)*fctrl(eras1-eras))
  642 continue
c     decode (6,73,elem(2,nn,2)) ek
      write (11,173) elem(2,nn,2)
  173 format (a6)
      backspace 11
      read (11,73) ek
      backspace 11
   73 format (f6.2)
      ek=ek*0.0136058
      do 644 l=2,np1
  644 brncht(l)=brncht(l)/brncht(1)
      brncht(1)=brncht(1)/gm
c     encode (10,74,idfg) brncht(1)
      write (idfg,74) brncht(1)
   74 format (1pe10.3)
c     decode (10,75,idfg) a1,a2
      read (idfg,75) a1,a2
   75 format (a6,1x,a3)
c     encode (9,76,a3) a1,a2
      write (br1,76) a1,a2
   76 format (a6,a3)
      nc=ncserp(imax)
      ll=npav(nc)
      ekev=vpar(ll,l2)*uenrgy/8065479.0
      dekev=0.0
      if (eionry.ne.0.0) dekev=eionry*0.0136058+ek-ekev
      ekev=ekev+dekev
      if (brncht(np1).ge.1.0) write (13,77) (elem(l,1,1),l=1,2),
     1  ekev,gm,(elem(l,1,2),l=2,3),ek,br1,(brncht(l),l=2,np1)
   77 format (2a6,f8.4,f4.1,1x,a6,a3,f7.3,a9,5f6.3)
      if (brncht(np1).lt.1.0) write (13,78) (elem(l,1,1),l=1,2),
     1  ekev,gm,(elem(l,1,2),l=2,3),ek,br1,(brncht(l),l=2,np1)
   78 format (2a6,f8.4,f4.1,1x,a6,a3,f7.3,a9,5f6.4)
c          Sum brnch over upper levels
c               (for various t, and for each lower level)
      do 645 i=1,imax
  645 v(i,23)=t(i)
      call sort2(imax,12,v(1,23),d,iser,t,ncser,ncserp,tp,fjt,fjtp,
     1  s2,soabss,gaa,gaap,brnch)
      if (imax.le.1) go to 646
      call order2(imax,d,lldes)
      call order2(imax,d,lldesp)
  646 write (iw,66) (tkev(l),l=2,6)
   66 format (/8x,11hlower level, 13h  t(kev)=inf.,5f17.2)
      do 650 l=1,6
  650 brnchl(l)=1.0e-20
      do 665 i=1,imax
      fnu(i)=abs(t(i)-tp(i))
      nc=ncserp(i)
      ll=npav(nc)
      eras1=vpar(ll,l2)-tp(i)
      if (t(i).ge.tp(i)) go to 656
      do 654 l=1,np1
  654 brnchl(l)=brnchl(l)+brnch(i)*exp(eras1/tunrgy(l))
  656 if (i.eq.imax) go to 658
      if (t(i+1).eq.t(i)) go to 665
  658 write (iw,67) ncser(i),t(i),fjt(i), (brnchl(l), l=1,np1)
   67 format (i5,f13.4,f5.1,1pe12.4,5e17.4)
      do 660 l=2,np1
  660 brnchl(l)=brnchl(l)/brnchl(1)
      brnchl(1)=brnchl(1)/gm
c     encode (10,74,idfg) brnchl(1)
      write (idfg,74) brnchl(1)
c     decode (10,75,idfg) a1,a2
      read (idfg,75) a1,a2
c     encode (9,76,a3) a1,a2
      write (br1,76) a1,a2
      ekev=t(i)*uenrgy/8065479.0+dekev
      nc=ncser(i)
      if (brnchl(np1).ge.1.0) write (13,77) (elem(l,nc,1),l=1,2),
     1  ekev,fjt(i),(elem(l,1,2),l=2,3),ek,br1,(brnchl(l),l=2,np1)
      if (brnchl(np1).lt.1.0) write (13,78) (elem(l,nc,1),l=1,2),
     1  ekev,fjt(i),(elem(l,1,2),l=2,3),ek,br1,(brnchl(l),l=2,np1)
      do 663 l=1,6
  663 brnchl(l)=1.0e-20
  665 continue
      eras=-1.0
      write (13,77) h1,h1,eras
c          Write branching factors for autoionization
c               contributions to collisional excitation
  670 if (ixc.eq.0) go to 699
      write (iw,81) (jexc(j),exc(j), j=1,ixc)
   81 format (//25x,3hexc,6x,6hbrnchx//(32x,10(i3,f7.2)))
      write (iw,82)
      do 672 i=1,ixc
      j=jexc(i)
  672 write (iw,82) j, (elem(m,j,2),m=1,2), exc(i),(brnchx(i,l),l=1,ixc)
   82 format (i3,2x,2a6,f12.4,3x,1p,10e10.2/(32x,1p,10e10.2))
      if (ixc.le.1) go to 699
      ixc2=0
      if (nsconf(2,2).le.2) go to 690
c          Sum over l of continuum electron
      do 673 j=1,ixc
      n=jexc(j)
  673 elemj(j)=elem(2,n,2)
      netot=0
      do 675 n=1,nosubc
  675 netot=netot+nijk(n,1,2)
      nc=jexc(ixc)-jexc(1)
      if (nc.le.0) go to 690
      ixc1=ixc
      mixc=jexc(ixc)
      i=0
  676 i=i+1
      if (i.ge.ixc1) go to 684
      mi=jexc1(i)
      if (mi.eq.mixc) go to 684
      j=i
  678 j=j+1
      if (j.gt.ixc1) go to 676
      mj=jexc1(j)
      if (mj.eq.mi) go to 678
      if (abs(exc1(j)-exc1(i)).gt.0.01) go to 678
      ne=0
      do 679 n=1,nosubc
      ne=ne+max0(nijk(n,mi,2),nijk(n,mj,2))
      if (ne.ge.netot) go to 681
      if (nijk(n,mi,2).ne.nijk(n,mj,2)) go to 678
  679 continue
  681 do 682 n1=1,ixc
  682 brnchx(n1,i)=brnchx(n1,i)+brnchx(n1,j)
      ixc1=ixc1-1
      do 683 n=j,ixc1
      jexc1(n)=jexc1(n+1)
      exc1(n)=exc1(n+1)
      elemj(n)=elemj(n+1)
      do 683 n1=1,ixc
  683 brnchx(n1,n)=brnchx(n1,n+1)
      j=j-1
      go to 678
  684 if (ixc1.eq.ixc) go to 690
  685 write (iw,81) (jexc1(j),exc1(j), j=1,ixc1)
  686 write (iw,82)
      do 687 i=1,ixc
      j=jexc(i)
  687 write (iw,82) j,(elem(m,j,2),m=1,2), exc(i),(brnchx(i,l),l=1,ixc1)
      if (ixc2.gt.0) go to 699
c          Sum over levels within the core
  690 i=0
      ixc2=ixc1
  691 i=i+1
      if (i.eq.ixc2) go to 695
      mi=jexc1(i)
      j=i+1
  692 mj=jexc1(j)
      if (mj.ne.mi) go to 691
      do 693 n=1,ixc
  693 brnchx(n,i)=brnchx(n,i)+brnchx(n,j)
      ixc2=ixc2-1
      if (i.eq.ixc2) go to 695
      do 694 j1=j,ixc2
      jexc1(j1)=jexc1(j1+1)
      exc1(j1)=exc1(j1+1)
      do 694 n=1,ixc
  694 brnchx(n,j1)=brnchx(n,j1+1)
      go to 692
  695 if (ixc2.eq.ixc1) go to 699
      do 697 j=1,ixc2
      n=jexc1(j)
  697 elemj(j)=elem(2,n,2)
      write (iw,87) (jexc1(j),elemj(j), j=1,ixc2)
   87 format(//25x,3hexc,6x,6hbrnchx//(32x,10(i3,2x,a5)))
      ixc1=ixc2
      go to 686
  699 call clock(time)
      delt=time-time0
c      if (iw6.lt.0) write (6,2069) delt
 2069 format (' Finished second-parity sort at time=',f8.3,' min')
c
c          Sort lines by wavenumber
c
  700 ipt=0
      if (ispecc.ge.4) ipt=2
      if (ispecc.eq.9) ipt=1
      if (ipt.eq.0) go to 980
      call sort2(imax,12,fnu,d,iser,t,ncser,ncserp,tp,fjt,fjtp,
     1  s2,soabss,gaa,gaap,brnch)
      if (imax.gt.1) call orderch(imax,d,lldes)
      if (imax.gt.1) call orderch(imax,d,lldesp)
      fnunp=min(fnunp,fnu(1))
      fnuxp=max(fnuxp,fnu(imax))
      if (ispecc.ge.8) write (20) imax,psq, (fnu(i),s2(i),
     1  brnch(i), i=1,imax)
c
  708 j=0
      jnxx=jnx
      do 720 i=1,imax
      eras1=fnu(i)*uenrgy
      flam(i)=1.0e8/eras1
      gf=psq*s2(i)*eras1
      if (igen.lt.5.and.ii.eq.2) gf=gf/(flam(i)**2)
      alggf=-99.999
      if (gf.gt.0.0) alggf=log10(gf)
      ga=0.66698*gf*eras1*eras1
      if (texcit.gt.0.0) alggf=ga*exp(-(max(t(i),tp(i))-emean)/texcit)
      if (ilund.gt.0.and.i.gt.1) go to 710
      if (j.gt.0) go to 710
      if (ipt.eq.1) go to 709
      write (iw,55) spid(ii+1),uenrgy,uenrev,
     1  (jn, (elem(l,jn,l1),l=1,3), (elem(l,jn,l2),l=1,3), jn=1,jnxx)
      if (texcit.eq.0.0) write (iw,ifmt1)
      if (texcit.gt.0.0) write (iw,ifmt1) texcit
  709 j=jlines-jnxx
      jnxx=min0(5,jnx)
  710 j=j-1
      if (ipt.lt.2) go to 720
      if (ibrnch.eq.0) go to 715
!     output spec.dat
      write (iw,88) t(i),fjt(i),ncser(i),lldes(i),tp(i),fjtp(i),
     1  ncserp(i),lldesp(i),fnu(i),flam(i),s2(i),gf,alggf,ga,brnch(i)
c**************************************************************************
c**************************************************************************
       if(gf.ge. 0.0001 ) then
      write (102,"(f9.3,'$',f5.1,'$',i3,'$',a8,'$',f9.3,'$',f5.1,'$',
     1 i3,'$',a8,'$',f9.3,'$',
     1 f9.4,'$',e10.3)")t(i),fjt(i),ncser(i),lldes(i),tp(i),fjtp(i),
     1 ncserp(i),lldesp(i),fnu(i)/8.065479,gf,ga




      write (222,"(3f9.3,f9.4,2I3,2f5.1)")t(i),tp(i),fnu(i)/8.065479,gf
     !      ,ncser(i),ncserp(i),fjt(i),fjtp(i)

      write (223,"(f9.3,f5.1,i3,1x,a8,f13.3,f5.1,i3,1x,a8,f13.3,f9.4)")
     !  t(i),fjt(i),ncser(i),lldes(i),tp(i),fjtp(i), ncserp(i),
     !  lldesp(i),fnu(i)/8.065479,gf

     
      write(116,"(f9.3,f9.4,2x,e10.3,f5.1,f9.3)")fnu(i)/8.065479,
     !   gf,ga,fjt(i),t(i)

      write (112,779)t(i),tp(i)
 

      write (103,"(f12.4,f9.4)")1239.85*10/flam(i),gf
      write (118,"(f12.4,f9.4,2f5.1)")1239.85*10/flam(i),
     !                      gf*fjt(i)/fjtp(i)
      write (119,"(f12.4,f9.4)")1239.85*10/flam(i),gf


	write (104,"(x,I2,x,I2,f12.4,f9.4)")ncser(i),ncserp(i),
     X   1239.85*10/flam(i),gf
	endif 

c**************************************************************************
c**************************************************************************

      
	if(flam(i).gt.4.5.and.flam(i).lt.5.2) then
      write (16,88) t(i),fjt(i),ncser(i),lldes(i),tp(i),fjtp(i),
     1  ncserp(i),lldesp(i),fnu(i),flam(i),s2(i),gf,alggf,ga,brnch(i)
      end if
   88 format (1h ,f11.3,f5.1,i3,1x,a8,f13.3,f5.1,i3,1x,a8,f13.3,
     1  f12.4,f8.3,f9.4,f8.3,1p,e10.3,e9.2)
      go to 720

  715 write (iw,ifmt2) i,t(i),fjt(i),ncser(i),lldes(i),tp(i),fjtp(i),
     1  ncserp(i),lldesp(i),fnu(i),flam(i),s2(i),gf,alggf,ga,soabss(i)
c**************************************************************************
c**************************************************************************
      if(gf.ge. 0.0001 ) then
      write (102,"(f6.3,'$',f5.1,'$',i3,'$',a8,'$',f9.3,'$',f5.1,'$',
     1 i3,'$',a8,'$',f9.3,'$',
     1 f9.4,'$',e10.3)")t(i),fjt(i),ncser(i),lldes(i),tp(i),fjtp(i),
     1 ncserp(i),lldesp(i),fnu(i)/8.065479,gf,ga

      write (222,"(3f9.3,f9.4,2I3,2f5.1)")t(i),tp(i),fnu(i)/8.065479,gf
     &      ,ncser(i),ncserp(i),fjt(i),fjtp(i)

      write (223,"(f9.3,f5.1,i3,1x,a8,f13.3,f5.1,i3,1x,a8,f13.3,f9.4)")
     &  t(i),fjt(i),ncser(i),lldes(i),tp(i),fjtp(i), ncserp(i),
     &  lldesp(i),fnu(i)/8.065479,gf


      write(116,"(f9.3,f9.4,2x,e10.3,f5.1,f9.3)")
     !  fnu(i)/8.065479,gf,ga,fjt(i),t(i)

      write (112,779)t(i),tp(i)
  779 format (f9.3,1x,f9.3)

      write (103,"(f12.4,f9.4)")1239.85*10/flam(i),gf
      write (118,"(f12.4,f9.4,2f5.1)")1239.85*10/flam(i),
     !   gf*fjt(i)/fjtp(i)
      write (119,"(f12.4,f9.4)")1239.85*10/flam(i),gf

	write (104,"(x,I2,x,I2,f12.4,f9.4)")ncser(i),ncserp(i),
     1   1239.85*10/flam(i),gf
	endif

  888 format (f5.1,i3,1x,a8,f5.1,i3,1x,a8,
     1  f12.4,f9.4)

C---------------sumaogen 2006.3.23
c**************************************************************************
c**************************************************************************
  720 continue


c
c
      call clock(time)
      delt=time-time0
      if (iptg.eq.1) write (iw,95) delt
   95 format (//' Finished wavelength sort at time=',f7.3,4h min//)
      if (iw6.lt.0) write (6,2095) delt
 2095 format (' Finished wavelength sort at time=',f9.3,4h min//)
  980 if (scrj8.lt.0.0) go to 985
      i=0
      if (imax.ne.itrunc) go to 180
      iread=iread-1
      backspace ic
      go to 200
c
  985 read (ic) sopi2
      iread=iread+1
      ssopx2=0.0
      do 986 i=1,jnx1
      do 986 j=1,jnx2
  986 ssopx2=ssopx2+sopi2(i,j)*(pmup(i,j)**2)
      ssopx2=ssopx2*(a**2)
      if (ispecc.lt.8) go to 988
      if (imax.eq.0) go to 988
      iras=5
      eras=-1.0
      write (20) iras,eras, (eras,eras,eras, i=1,iras)
      call wndist(ii)
  988 continue
c
      if (iptg.eq.0) go to 991
      call clock(time)
      delt=time-time0
      write (iw,96) delt,time,pmax,ssopx2,sums2n,sums2,sums2m,sumgf,
     1  sumf,sumgar,dmin,i0,d0max,i0n,flbdx,i0x,flbdn,ilostt,icdlt,nck
   96 format (//6h time=,f7.3,4h min,2x,10h(abs time=,f8.3,1h),5x,
     1   9hfor pmax=,f9.5,1h,,f17.4,f11.5/57x,12hsums2,sumgf=,f10.4,
     2  f11.5,f9.4/64x,5hsumf=,f30.4,9x,7hsumgar=,1pe11.4/57x,6hs2min=,
     3  0pf27.5//29x,i5,28h lines omitted, with max s2=,f28.5//29x,i5,
     4  31h lines omitted, with lambda.gt.,f14.4/29x,i5,
     5  31h lines omitted, with lambda.lt.,f14.4/29x,i5,
     6  31h lines omitted, insuff storage /29x,i5,
     7  36h lines omitted, conf serial nos .gt.,i4,1h,,i4)
      if (iw6.lt.0) write (6,96) delt,time,pmax,ssopx2,sums2n,sums2,
     1  sums2m,sumgf,sumf,sumgar,dmin,i0,d0max,i0n,flbdx,i0x,flbdn,
     2  ilostt,icdlt,nck
      write (iw,97) (coupl(i), i=1,7)
   97 format (///13h ave purities,29x,9(a6,2x)/)
      do 990 k1=l1,l2
      j1x=nsconf(2,k1)
      if (j1x.lt.2) j1x=2
      j1=j1x-1
      write(iw,98) ((elem(i,jn,k1), i=1,3), jn=1,j1x,j1),
     1  (avp(i,k1), i=1,7), avcg(k1),aveig(k1)

   98 format (1x,3a6,3h---,3a6,7f8.3,5x,6h  eav=,f10.4/101x,6haveig=,
     1  f10.4)
  990 continue
c
  991 if (ii.eq.0) return
      if (igen.lt.5) go to 100
      if (igen.gt.7.or.mod(ibk-1,5).ne.0) go to 100
      imax=min0(imax,30)
  992 write (iw,99) ibk,bigks(ibk),ipwr,imax, (goss(i,ibk), i=1,imax)
   99 format (/46h0weighted generalized osc. strengths at bigks(,i3,
     1  2h)=,f12.7,8h   ipwr=,i1,12h   for first,i3,6h lines//(10f12.8))
      go to 100
c
  999 return
      end
      subroutine wndist(ii)
c
c          Plot wavenumber distribution on microfilm (obsolete)
c               (special version for gaussian smear)
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      parameter (kcc=kiser/4,klc4=2*kiser+1,klam=10000)
      parameter (kw=104,kp=2*kw+2)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c3b/t(klam),tp(klam),s2(klam),soabss(klam),
     1  aa(kmx),aap(kmx),gaa(klam),gaap(klam),brnch(klam),
     2  icut(66),sgfcut(66),sfcut(66),didgf(66),dsgfdgf(66),title(20),
     3  ficut(66),fnucut(66),fnuplt(82),dum(66),fiplt(82),sgfplt(82),
     4  ncser(klam),aadum(kmx),aapt(kmx)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      common/c6/emin,emax,sumwt,flbdn,flbdx,fnunp,fnuxp,nlev,iewr
      common       d(kmx,kmx)
      common/c3lc2/v(kmx,kmx)
      common/c3lc3/ct4(kmx,kmx)
      common/c3lc4/cta(kmx,kmx)
      common/c3lcd/dumlc5
      common    elem(3,kc,2),vpar(kpr,2),avp(9,2),aveig(2),avcg(2),
     1  npark(2),npav(kc),fjt(klam),fjtp(klam)
c
      dimension x(klam),fnu(klam),flam(klam), fnut(klam)
      equivalence (cta,x,fnu),(ct4,flam), (d,fnut)
      dimension fnus(100),gamma(7)
      equivalence (t,fnus)
      dimension eplt(klam),sgf(klam)
      equivalence (tp,eplt),(soabss,sgf)
      common/c7/g1,sumgaa,sumgar,sumgaat
      character*10 parnam(kpr,2)
      character iel*8
      character*8 fidls(kmx,2),fidjj(kmx,2),ldes(kmx),ldesp(kmx)
      common/char/parnam,fidls,fidjj,ldes,ldesp
      dimension ddjj(kmx,1)
      common/djj/ddjj
      data igf,idi/2hgf,2hdi/
c
c          dele in kev,  fnun and fnunp in cm-1
c
      dele=delekev
      if (dele.le.0.0) dele=0.0005
  100 del=0.0005*(1.002*fnuxp-fnunp)
      fnun=fnunp-del
      fnux=fnuxp+del
  105 delnu=8065470.0*dele/uenrgy
      ieras=(fnux-fnun)/delnu
      np2=ieras+3
      if (np2.le.klam/2) go to 110
      if (ieras.gt.klam-5) write (2,10) ((elem(i,1,j),i=1,3),j=1,2),
     1  fnuxp,fnunp,dele
   10 format (///5h*****,3a6,3h - ,3a6,2f15.1,6h dele=,f7.5,
     1  10h too small///)
      dele=2.0*dele
      go to 105
  110 imin=fnunp/delnu
      fimin=imin
      eplt(1)=fimin*dele
      do 150 j=1,np2
      eplt(j+1)=eplt(j)+dele
  150 sgf(j)=0.0
c
      rewind 20
      itot=0
      gftot=0.0
      sbr=0.0
  200 read (20) imax,psq, (fnu(i),s2(i), brnch(i), i=1,imax)
      if (psq.lt.0.0) go to 300
      do 205 i=1,imax
  205 sbr=sbr+brnch(i)
      do 230 i=1,imax
      eras1=fnu(i)*uenrgy
      gf=psq*s2(i)*eras1
      if (ii.eq.2.and.igen.lt.5) gf=gf*((1.0e-8*eras1)**2)
      if (sbr.gt.0.0) gf=brnch(i)
      j=fnu(i)/delnu+1.5
      j=j-imin
      if (j.lt.1.or.j.gt.np2) write (2,20) np2,j, fnu(i),delnu
   20 format (10x,2i10,2f15.1)
      sgf(j)=sgf(j)+gf
      itot=itot+1
  230 gftot=gftot+gf
      go to 200
c
  300 fitot=itot
  305 do 310 j=1,np2
      sgf(j)=sgf(j)/(gftot+1.0e-10)
  310 continue
      iii=1
      gamma(1)=0.0
      imx=np2
      id=igf
      if (sbr.gt.0.0) id=idi
c     encode (8,91,iel) elem(1,1,1),id
      write (iel,91) elem(1,1,1),id
   91 format (a6,a2)
      brfac=0.0
      if (sbr.gt.0.0) brfac=gftot/sumgaa
      write (iw,92) (elem(j,1,1),j=1,3), id,gamma(iii),g1,gftot,
     1  eplt(1),dele,imx,brfac
   92 format (//1h0,3a6,2x,a2,2f5.0,10x,1p,e10.3,0p,2f10.6,i10,10x,
     1  6hbrfac=,f10.6)
      write (11,94) (elem(j,1,1),j=1,3), id,gamma(iii),g1,gftot,
     1  eplt(1),dele,imx
   94 format (3a6,a2,2f5.0,10x,1p,e10.3,0p,2f10.6,i10)
      jx=0
      i=0
  865 jn=jx+1
      jx=min0(jn+6,imx)
      i=i+1
  866 write (iw,93) iel,i, (sgf(j), j=jn,jx)
   93 format (1x,a8,i4,7f10.7)
      write (11,95) iel,i, (sgf(j), j=jn,jx)
   95 format (a8,i2,7f10.7)
      if (jx.lt.imx) go to 865
  868 continue
c
c
      if (sbr.eq.0.0) go to 900
      nosubc=nsconf(1,2)
      gj=1.0
      do 880 i=1,nosubc
      w=nijk(i,1,2)
      fll=fllijk(i,1,2)
      wf=4.0*fll+2.0
  880 gj=gj*fctrl(wf)/(fctrl(w)*fctrl(wf-w))
      aat=sumgaa/gj
      art=sumgar/gj
      papp=aat*art/(aat+art)
      pdet=gftot/gj
      bapp=aat/(aat+art)
      bdet=gftot/(sumgar+1.0e-10)
      rr=bdet/bapp
      aateff=art/(1.0/bdet-1.0)
      write (iw,88) ((elem(i,1,j),i=1,3), j=1,2), gj,aat,art,papp,pdet,
     1  bapp,bdet,rr,aateff
      write (3,88) ((elem(i,1,j),i=1,3), j=1,2), gj,aat,art,papp,pdet,
     1  bapp,bdet,rr,aateff
   88 format (1h0,44x,2hgj,5x,3haat,8x,3hart,5x,9haa*ar/sum,4x,
     1  6hp(det),4x,6hb(app),4x,6hb(det),4x,7hdet/app,3x,8haat(eff)/
     2  1x,3a6,3h---,2x,3a6,f5.0,1p,4e11.3,0p,3f10.7,1p,e11.3)
      if (sumgaa.ge.sumgaat) go to 883
      aatt=sumgaat/gj
      papp=aat*art/(aatt+art)
      bapp=papp/art
      rr=bdet/bapp
      write (iw,88) ((elem(i,1,j),i=1,3), j=1,2), gj,aatt,art,papp,pdet,
     1  bapp,bdet,rr,aateff
      write (3,88) ((elem(i,1,j),i=1,3), j=1,2), gj,aatt,art,papp,pdet,
     1  bapp,bdet,rr,aateff
  883 jx=max0(nsconf(2,1),nsconf(2,2))
      if (jx.lt.2) go to 900
      do 885 jj=2,jx
      write (iw,89) ((elem(i,jj,j),i=1,3), j=1,2)
      write (3,89) ((elem(i,jj,j),i=1,3), j=1,2)
   89 format (1x,3a6,3h---,2x,3a6)
  885 continue
  900 return
      end
c     overlay(g9,10,5)
      subroutine born
c
c          A routine to integrate generalised oscillator strengths
c               to give plane-wave Born collision strengths
c                    (W. D. Robb and R. D. Cowan, 1980)
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kpr=2200,kmx=5000,klam=10000)
      parameter (kbgks=41,kenrgs=21,kcase=50,ktran=100000)
      common       d(kmx,kmx)
      common    elem(3,kc,2),vpar(kpr,2),avp(9,2),aveig(2),avcg(2),
     1  npark(2),npav(kc),fjt(klam),fjtp(klam),ncserp(klam)
      common/c3lc5/goss(ktran,kbgks)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,intdum,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c3b/t(klam),tp(klam),s2(klam),soabss(klam),
     1  aa(kmx),aap(kmx),gaa(klam),gaap(klam),brnch(klam),
     2  icut(66),sgfcut(66),sfcut(66),didgf(66),dsgfdgf(66),title(20),
     3  ficut(66),fnucut(66),fnuplt(82),sgf(66),fiplt(82),sgfplt(82),
     4  ncser(klam),aat(kmx),aapt(kmx)
      common/akn/xbar,n,m,ybar
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      common/c9/l1,l2,cflag(kc,2),cgengy(kc,2),swt(kc,2),imax
      common/pwborn/nbigks,nenrgs,ekminl,ekmaxl,delekl,bigks(kbgks),
     1  xmin,xmax,tev(25),corr(kenrgs),ibk,ipwr,i1
      dimension fst(kbgks),en(kenrgs),ncs(kcase,2)
      dimension xs(kenrgs),cs(kenrgs,kcase),csm(kenrgs,kcase),
     1  gfst(kcase),csm2(kenrgs),decswt(kcase),cswt(kcase),c1(kenrgs),
     2  c2(kenrgs),fk(51),yk(51),fmxel(51),sumi(51),ratem2(kenrgs)
      equivalence (cs,gaa),(csm,gaap),(fst,aa),
     1  (decswt,aap)
      data t1,t2,t3,t4,t5/6h cowan,6h mpwb ,6h total,6h mod2 ,6h  pwb /
c
c          Set punch quantities
c
c     kcase=50
      m1=-nenrgs
      m2=30
      m3=0
      m4=1
      m5=-m1
      an=nenrgs-1
      m=3
      npts=nbigks-1
      nk=nenrgs+1
      nk2=nk/2
      mm=1
c
c          Initialize arrays
c
      ics=1
      ncs(ics,1)=ncser(1)
      ncs(ics,2)=ncserp(1)
      do 110 k=1,kcase
      gfst(k)=0.0
      decswt(k)=0.0
      cswt(k)=0.0
      do 110 i=1,nenrgs
      csm(i,k)=0.0
  110 cs(i,k)=0.0
      enmax=exp(2.0*ekmaxl)
      do 120 i=1,nbigks
  120 fst(i)=exp(bigks(i))
      write (iw,12) nbigks,enmax, (fst(i),i=1,nbigks)
   12 format (1h1//20h k-values,   nbigks=,i3,8h  enmax=,f14.7//
     1  (10f12.7))
c
c          Loop over the transitions
c
      ipwr=mod(ipwr,2)
      ten=10.0
      swt0=0.0
      tr0=-9999999.0
      fjtr0=-1.0
      do 490 it=1,imax
      tr=t(it)
      tpr=tp(it)
      fjtr=fjt(it)
      fjtpr=fjtp(it)
      if (tr.ne.tr0.or.fjtr.ne.fjtr0) swt0=swt0+2.0*fjtr+1.0
      tr0=tr
      fjtr0=fjtr
      do 200 i=1,ibk
  200 fst(i)=goss(it,i)
      fnu=abs(tpr-tr)
      eras1=fnu*uenrgy
      deltae=eras1/109737.31
      c=3.0/deltae
      if (ipwr.eq.0) c=15.0*c
      flam=1.0e8/eras1
      nc1=ncser(it)
      nc2=ncserp(it)
      ict=0
      do 220 id=1,ics
      ni1=ncs(id,1)
      ni2=ncs(id,2)
      if (nc1.eq.ni1.and.nc2.eq.ni2) ict=id
  220 continue
      if (ict.gt.0) go to 230
      ics=ics+1
      ncs(ics,1)=nc1
      ncs(ics,2)=nc2
      ict=ics
  230 continue
c
c          Integrate the gen.osc.str. over a logarithmic mesh for
c               various incident electron energies
c
      gf=goss(it,1)
      gfst(ict)=gfst(ict)+gf
      e1=xmin*deltae
      e2=xmax*deltae
      e1l=log(e1)
      e2l=log(e2)
      ei=(e2l-e1l)/an
      do 300 k=1,nenrgs
      el=e1l+(k-1)*ei
  300 en(k)=exp(el)
      write (iw,30)
   30 format (/1h0,14x,7h   e   , 4x,2hj ,10x,8h   ep   , 3x,3h jp,12x,
     1  8h delta e,3x,9hlambda(a),2x,9hs/pmax**2,4x,2hgf,5x,6hlog gf,3x,
     2  9hga(sec-1)/)
      alggf=-99.999
      if (gf.gt.0.0) alggf=log10(gf)
      ga=0.66698*gf*eras1*eras1
      write (iw,32) it,nc1,nc2,tr,fjtr,tpr,fjtpr,fnu,flam,
     1  s2(it),gf,alggf,ga
   32 format (1h ,i4,2i2,f13.3, f6.1,f18.3, f6.1,f20.2,f11.3,f11.5,
     1  f9.4,f9.4,1pe12.3)
      if (igen.lt.9) write (iw,33) (goss(it,k), k=1,nbigks)
   33 format (36h0weighted generalized osc. strengths/(10f12.8))
      write (iw,34)
   34 format (//16x,2h x,11x,5he(ry),10x,5homega,7x,8homega*fx,
     1  7x,7homegam2,10x,5ht(ev),3x,15hratem2(cm3/sec),2x,9hcorr(pct)/)
      n=nbigks
      ek0=deltae*3.0
      do 480 ken=1,nk
      ken1=ken-1
      if (ken.gt.1) ek0=en(ken1)
      ekn=ek0-deltae
      ak0=sqrt(ek0)
      akn=sqrt(ekn)
      akmax=ak0+akn
      akmin=ak0-akn
      akmaxl=log(akmax)
      akminl=log(akmin)
      akintl=(akmaxl-akminl)/npts
      xbar=akminl-akintl
      akxx=1.000001*akmaxl
      am=1.0
      sum=0.0
      ii=0
  350 xbar=xbar+akintl
      if (xbar.gt.akxx) go to 390
      call aknint(bigks,fst)
      sum=sum+ybar*am
      if (am.gt.3.0) go to 370
      am=4.0
      if (ken.ne.nk) go to 350
      ii=ii+1
      fk(ii)=exp(xbar)
      yk(ii)=ybar
      eras=c*ybar
      if (ipwr.eq.0) eras=eras/(fk(ii)**2)
      fmxel(ii)=0.0
      if (eras.gt.0.0) fmxel(ii)=sqrt(eras)
      if (eras.lt.0.0) fmxel(ii)=-sqrt(-eras)
      sumi(ii)=sum-ybar
      go to 350
  370 am=2.0
      go to 350
  390 sum=sum-ybar
      sum=sum*akintl/3.0
c
c          Evaluate, store, and modify the pwB collision strength
c
      colls=8.0*sum/deltae
      xe=ek0/deltae
      if (ken.eq.1) collm=colls
      xe1=(1.0-xe)*0.07702
      fx=1.0-0.2*exp(xe1)
      collsm=colls*fx
      if (xe.lt.3.0) collsm=collm*fx
      if (ken.eq.1) go to 480
      xs(ken1)=xe
      c1(ken1)=colls
      c2(ken1)=collsm
      cs(ken1,ict)=cs(ken1,ict)+colls
      csm(ken1,ict)=csm(ken1,ict)+collsm
  480 continue
      decswt(ict)=decswt(ict)+deltae*c1(nk2)
      cswt(ict)=cswt(ict)+c1(nk2)
      n=nenrgs
      do 485 i=1,nenrgs
      csm2(i)=0.0
      if ((c1(i)+c2(i)).eq.0.0) go to 485
      xbar=xs(i)+3.0/(1.0+xs(i))
      call aknint(xs,c1)
      csm2(i)=ybar
  485 continue
      eras=2.0*fjtr+1.0
      call rcoeff(xs,csm2,ratem2,deltae,eras,uenrgy)
      do 486 i=1,nenrgs
      i2=i+i1
  486 write (iw,48) xs(i),en(i),c1(i),c2(i),csm2(i),tev(i2),ratem2(i),
     1  corr(i)
   48 format (8x,5f14.7,f15.1,1pe15.4,0pf11.1)
      if (igen.gt.5) go to 490
      iii=1
      if (ii.gt.ila) iii=2
      do 488 i=1,ii,iii
  488 sumi(i)=sumi(i)/(sumi(ii)+1.0e-15)
      write (iw,49) akmin,akmax,(fk(i),yk(i),fmxel(i),sumi(i),i=1,ii)
   49 format (//2f12.6,16x,1hk,12x,2hgf,10x,6hmxelem,9x,3hint/
     1  (30x,4f14.8))
  490 continue
c
c          Punch the total collision strength
c
      n=nenrgs
      do 890 jtn=1,ics
      nc1=ncs(jtn,1)
      nc2=ncs(jtn,2)
      fprt=0.0
      if (l1.ne.l2) fprt=gfst(jtn)/swt(nc1,1)
      deav=abs(cgengy(nc2,l2)-cgengy(nc1,l1))
      de1=abs(cgengy(nc2,l2)-t(1)*uenrgy/109737.31)
      de2=0.0
      if (cswt(jtn).gt.0.0) de2=decswt(jtn)/cswt(jtn)
      do 810 i=1,nenrgs
      xbar=xs(i)+3.0/(1.0+xs(i))
      call aknint(xs,cs(1,jtn))
  810 csm2(i)=ybar
      deltae=max(deav,de2)
      if (deltae.eq.0.0) deltae=de1
      call rcoeff(xs,csm2,ratem2,deltae,swt0,uenrgy)
      write (iw,60)
   60 format (1h1,//20x,44h ****     Total collision strengths     ****
     1  ////)
      write (iw,81) m1,m2,m3,m4,t1,t2,(elem(l,nc1,l1),l=1,3),
     1  cflag(nc1,l1),cflag(nc2,l2),(elem(l,nc2,l2),l=1,3),t3
   81 format (4i5,5a6,a1,4h -- ,a1,4a6)
      write (iw,84) deav,fprt,de1,de2,deltae
   84 format (/6h deav=,f15.8,12h ry,    fav=,f14.10,3f15.8///
     1  13x,1hx,13x,2hcs,13x,3hcsm,6x,14hxeff=x+3/(1+x),
     2  10x,5ht(ev),3x,15hratem2(cm3/sec),2x,9hcorr(pct)/)
      do 850 i=1,nenrgs
      i2=i+i1
  850 write (iw,86) xs(i),cs(i,jtn),csm(i,jtn),csm2(i),
     1  tev(i2),ratem2(i),corr(i)
   86 format (3x,4f15.9,f17.1,1pe15.4,0pf11.1)
      write (11,81) m5,m2,m3,m3,t1,t5,(elem(l,nc1,l1),l=1,3),
     1  cflag(nc1,l1),cflag(nc2,l2),(elem(l,nc2,l2),l=1,3),t3
      write (11,88) (xs(i),i=1,nenrgs)
      write (11,88) (cs(i,jtn),i=1,nenrgs)
   88 format (5e16.8)
      write (11,81) m5,m2,m3,m3,t1,t2,(elem(l,nc1,l1),l=1,3),
     1  cflag(nc1,l1),cflag(nc2,l2),(elem(l,nc2,l2),l=1,3),t3
      write (11,88) (xs(i),i=1,nenrgs)
      write (11,88) (csm(i,jtn),i=1,nenrgs)
      write (11,81) m1,m2,m3,m4,t1,t4,(elem(l,nc1,l1),l=1,3),
     1  cflag(nc1,l1),cflag(nc2,l2),(elem(l,nc2,l2),l=1,3),t3
      write (11,88) deav,fprt,de1,de2
      write (11,88) (xs(i),i=1,nenrgs)
      write (11,88) (csm2(i),i=1,nenrgs)
  890 continue
      call clock(time)
      delt=time-time0
      write (iw,89) delt
   89 format (//6h time=,f6.3,4h min//)
      return
      end
      subroutine aknint(x,y)
c                                                                     
c          Aitken repeated interpolation                        
c                                                              
c   xbar = abscissa at which interpolation is desired        
c   iabs(in) = no. of values in table                      
c   im   = degree of approximating polynomial              
c   x    = vector of iabs(in) values of abscissa                
c   y    = vector of iabs(in) values of ordinate                       
c   t    = temporary storage vector of 4*(m+1) locations)         
c                                                                  
      implicit real*8 (a-h,o-z)
      parameter (kbgks=41)
c
      dimension x(kbgks),y(kbgks),t(80)
      common/akn/xbar,n,m,yb                                     
c                                                                
      do 10 j=1,n                                               
      if (xbar.le.x(j)) go to 11                                 
   10 continue
      j=n                                                       
   11 k=m+1                                                    
      j=j-k/2                                                    
      j=min0(j,n-m)                                         
      j=max0(j,1)                                             
      mend=j+m                                                 
      do 12 i=j,mend                                             
      kk=i-j+1                                                   
      t(kk) = y(i)                                                
   12 t(kk+k)=x(i)-xbar                                            
      do 13 i=1,m                                                  
      kk=i+1                                                       
      do 13 jj=kk,k                                                  
      t(jj)=(t(i)*t(jj+k) -t(jj)*t(i+k))/(x(jj+j-1) - x(i+j-1))      
   13 continue                                                      
      yb=t(k)
      return                                                     
      end                                                       
      subroutine rcoeff(x,y,z,deltae,swt0,uenrgy)
c
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kpr=2200,kmx=5000,klam=10000)
      parameter (kbgks=41,kenrgs=21,kcase=50,ktran=100000)
      common       d(kmx,kmx)
      common    elem(3,kc,2),vpar(kpr,2),avp(9,2),aveig(2),avcg(2),
     1  npark(2),npav(kc),fjt(klam),fjtp(klam),ncserp(klam)
      common/c3b/t(klam),tp(klam),s2(klam),soabss(klam),
     1  aa(kmx),aap(kmx),gaa(klam),gaap(klam),brnch(klam),
     2  icut(66),sgfcut(66),sfcut(66),didgf(66),dsgfdgf(66),title(20),
     3  ficut(66),fnucut(66),fnuplt(82),sgf(66),fiplt(82),sgfplt(82),
     4  ncser(klam),aat(kmx),aapt(kmx)
      common/c5/iarg1,iarg2,iarg3,igen,irnq,irxq,irnd,irxd,irmn,irmx,
     1  delekev,deleav,scale,fact0(5),emina,scrlkp(14,2),
     2  scrskp(14,2),nclskp(2),nolskp
      common/c9/l1,l2,cflag(kc,2),cgengy(kc,2),swt(kc,2),imax
      common/pwborn/nbigks,nenrgs,ekminl,ekmaxl,delekl,bigks(kbgks),
     1  xmin,xmax,tev(25),corr(kenrgs),ibk,ipwr,i1
      dimension x(kenrgs),y(kenrgs),z(kenrgs)
c
      i1=0
      eras=(tp(imax)-t(1))*uenrgy/8065.479
      if ((ncser(1).eq.ncserp(imax).and.iarg1.eq.2).and.eras.gt.25.)i1=4
      if ((ncser(1).ne.ncserp(imax).or.iarg1.eq.1).and.eras.gt.250.)i1=4
      d1=log(x(2)/x(1))/3.0
c
      do 900 i=1,nenrgs
      i2=i+i1
      tryd=tev(i2)/13.605
      c1=deltae/tryd
      c2=2.1717e-8/(swt0*sqrt(tryd))
      c3=c1*c2
c          Integrate to xmax via Simpson's rule
      sum=(x(1)-1.0)*y(1)*exp(-c1*x(1))/d1
      sum0=c3*d1*sum
      a1=1.0
      j=0
  150 j=j+1
      if (j.gt.nenrgs) go to 190
      eras=y(j)*x(j)*exp(-c1*x(j))
      sum=sum+a1*eras
      if (a1.eq.4.0) go to 160
      a1=4.0
      go to 150
  160 a1=2.0
      go to 150
  190 sum=sum-eras
      sum=c3*sum*d1
c          Add integral from xmax to infinity
      aln1=log(c1*x(nenrgs-2))
      x0=c1*x(nenrgs)
      aln2=log(x0)
      a=(y(nenrgs)-y(nenrgs-2))/(aln2-aln1)
      if (a.lt.0.0) a=0.0
      b=y(nenrgs)-a*aln2
      eras=y(nenrgs)*exp(-x0)+a*e1(x0)
      z(i)=sum+c2*eras
      sum2=c2*eras
      corr(i)=100.0*(sum0+sum2)/(z(i)+1.0e-30)
  900 continue
      return
      end
      function e1(x)
c
c          Computes the exponential integral e1(x).
c
c      July 1977 edition.  W. Fullerton, C-3, Los Alamos Scientific Lab.
c           Modified March 1982 by R.D. Cowan for x.gt.-1 only
c                and with abbreviated series for only 5-figure accuracy
c
c
c
c          series for e12        on the interval -1.le.x.le.+1
c
c          series for ae13       on the interval  +1.le.x.le.4
c
c          series for ae14       on the interval  4.le.x.le.100
c
c
      implicit real*8 (a-h,o-z)
      dimension e12cs(7),ae13cs(7),ae14cs(7)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
c
      data e12 cs( 1) /  -0.0373902147 /
      data e12 cs( 2) /   0.0427239860 /
      data e12 cs( 3) /   -.1303182079 /
      data e12 cs( 4) /    .0144191240 /
      data e12 cs( 5) /   -.0013461707 /
      data e12 cs( 6) /    .0001073102 /
      data e12 cs( 7) /   -.0000074299 /
      data ae13cs( 1) /   -.6057732466 /
      data ae13cs( 2) /   -.1125352434 /
      data ae13cs( 3) /    .0134322662 /
      data ae13cs( 4) /   -.0019268451 /
      data ae13cs( 5) /    .0003091183 /
      data ae13cs( 6) /   -.0000535641 /
      data ae13cs( 7) /    .0000098278 /
      data ae14cs( 1) /   -.1892918000 /
      data ae14cs( 2) /   -.0864811785 /
      data ae14cs( 3) /    .0072241015 /
      data ae14cs( 4) /   -.0008097559 /
      data ae14cs( 5) /    .0001099913 /
      data ae14cs( 6) /   -.0000171733 /
      data ae14cs( 7) /    .0000029856 /
      data xmax,nte12,ntae13,ntae14 /100.0,7,7,7/
c
c     if (xmax.ne.0) go to 40
c     nte12=7
c     ntae13=7
c     ntae14=7
c     xmax=100.0
c
 40   if (x.gt.1.) go to 50
      if (x.eq.0.0) write (iw,1)
    1 format (24h *****error in e1, x=0.0)
c
c          e1(x) = -ei(-x) for -1. .lt. x .le. 1.,  x .ne. 0.
c
      e1=(-log(abs(x))-0.6875+x)+csevl(x,e12cs,nte12)
      return
c
 50   if (x.gt.4.) go to 60
c
c          e1(x) = -ei(-x) for 1. .lt. x .le. 4.
c
      e1 = exp(-x)/x * (1.+csevl ((8./x-5.)/3., ae13cs, ntae13))
      return
c
 60   if (x.gt.xmax) go to 70
c
c          e1(x) = -ei(-x) for 4. .lt. x .le. xmax
c
      e1 = exp(-x)/x * (1. + csevl (8./x-1., ae14cs, ntae14))
      return
c
c          e1(x) = -ei(-x) for x .gt. xmax
c
   70 e1=0.0
      return
      end
      function csevl (x,cs,n)
c          April 1977 version. W. Fullerton, C-3, Los Alamos Scientific Lab.
c
c          evaluate the n-term chebyshev series cs at x. adapted from
c          R. Broucke, Algorithm 446, C.A.C.M., 16, 254 (1973).  Also see Fox
c          and Parker, Chebyshev Polys in Numer. Analysis, Oxford Press, p.56.
c
c          input arguments --
c               x    value at which the series is to be evaluated.
c               cs   array of n terms of a chebyshev series. in eval-
c                      uating cs, only half the first coef is summed.
c               n    number of terms in array cs.
c
c
      implicit real*8 (a-h,o-z)
      dimension cs(1)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
c
      if (n.lt.1.or.n.gt.1000) write (iw,1) n
    1 format (24h *****error in csevl, n=,i7)
      if (x.lt.-1.0.or.x.gt.1.0) write (iw,2) x
    2 format (24h *****error in csevl, x=,f10.5)
c
       b1=0.
       b0=0.
       twox=2.*x
       do 10 i=1,n
       b2=b1
       b1=b0
       ni=n+1-i
       b0=twox*b1-b2+cs(ni)
 10    continue
c
       csevl = 0.5 * (b0-b2)
c
       return
      end
c     overlay(g9,10,6)
      subroutine rceinp
c
c          Set up tape2e for binary input to RCE,
c               and file outgine for bcd input to RCE
c
c          If nlsmax.gt.0, nls.le.nlsmax, kcpld(i)=0, and all other
c               kcpld=1, then coef matrices will be written on tape2e in
c               coupling i and transformation matrix will be tmx(i,LS).
c          Otherwise, if kcpl=1, coef matrices will be in LS, tmx(LS,JJ),
c          if kcpl=2, coef matrices will be in JJ, tmx(JJ,LS).
c
c
      implicit real*8 (a-h,o-z)
      parameter (ks=8,kc=50,kls1=500,klsp1=kls1+1,klsp=8000,
     1  kjk=400,kjp=1000,kmx=5000,klc1=kmx**2-(kls1**2)*9,kiser=10000,
     2  kpr=2200,kjjt=50,kpc=90000,klc2=kmx**2-(kls1**2)*7-kpc,
     3  kls2=17,kls3=17,kls4=8,kls5=8,kls6=8,klsc=kls1+kls2+kls3+26)
      parameter (kcc=kiser/4,klc4=2*kiser+1,klc42=kmx**2,kmx2=kmx/2)
      common/idskno/ir,iw,id2,id3,id4,ila,ilb,il,ic,ie
      common/c1/kcpl,nocset,nsconf(3,2),iabg,iv,nlsmax,nlt11,nevmax,
     1  kcpld(9),sjn,sjx,imag,iquad,uenrgy,dmin,ielpun,ilncuv,iplev,
     2  icpc,icfc,idip,iengyd,ispecc,ipct,ictc,ictbcd,kcpl1,coupl(12),
     3  lsymb(24),nosubc,kk,time0,time,delt,ndifft,notott,
     4  sj8mn,sj8mx,igdlev,nscrj8,scrj8,scrj8p,nls,nlsp,njj,
     5  nnn,ndifsj,kpar,npar,ix,cave,sums20,nopc,j1a,j1b,
     6  nijk(ks,kc,2),notsj1(ks,100),not,nlt,norcd,a,lci,lcip,j1x,
     7  icnvrt(2),nlastt(ks),ndiffj(ks),nototj(ks),ntottj(100),
     8  ntotjj(ks,100),llijk(ks,kc,2),iiprty,fllijk(ks,kc,2),
     9  ssopi2,sopi2(kc,kc),nck(2),texcit,emean,
     *  zero,half,one,thrhal,two,iplotc,iw6,noicwr,noic(2),noicmup(2)
      common/c3a/isubj(kc),muls(ks),lhs(ks),
     1  nals(kmx,ks),ncfg(kmx),nalsj(kmx,ks),scrl(kmx,ks),scrs(kmx,ks),
     2  fj(kmx,ks),scrj(kmx,ks), mul(ks),lh(ks),lf(klsp),nsjk(110),
     3  fk(kmx),fkj(kmx),scrl6(kmx),scrs6(kmx),fk6(kmx),lhqq(kmx),
     4  multqq(kmx),nalsjp(kjp,ks),pj(kjp,ks),noicrd
      common/c6/emin,emax,sumwt,flbdn,flbdx,fnunp,fnuxp,nlev,iewr
      common       c(kmx,kmx)
      common/c3lc2/tmx(kmx,kmx)
      common/c3lc3/ct4(kmx,kmx)
      common/c3lc4/dumlc4(klc42)
      common/c3lcd/dumlc5
      common    elem(3,kc,2),vpar(kpr,2),avp(9,2),aveig(2),avcg(2),
     1  npark(2),npav(kc),    eig(kmx),elem1(3),fnt(9,2),i1,i2,
     2  ifact(4),fact(4),lcser(kmx),x(kmx)
      dimension nparj(kc,kc)
      equivalence (dumlc4(klc4),nparj)
      dimension illp(klc42),coeff(klc42)
      equivalence (ct4,coeff)
      character*8 sj8
      character*10 parnam(kpr,2),parnm(kpr)
      character*8 fidls(kmx,2),fidjj(kmx,2),ldes(kmx),ldesp(kmx)
      character*8 yiden(kmx,2)
      common/char/parnam,fidls,fidjj,ldes,ldesp
      dimension ddjj(kmx,1)
      common/djj/ddjj
c
c
      call clock(time)
      delt=time-time0
      if (iw6.lt.0) write (6,95) delt
   95 format (//' start rceinp at time=',f7.3,4h min/)
      rewind 2
      nocset = iabs(nocset)
      if (nocset.eq.0) nocset=1
      k=1
      il=ila
  100 j1x = nsconf(2,k)
      npar = 0
      do 140 mzq=1,j1x
      npar = npar+nparj(mzq,mzq)
      do 140 nzq=mzq,j1x
      if (nzq.eq.mzq) go to 140
      npar = npar+nparj(mzq,nzq)
  140 continue
      write (2) nocset,nscrj8,npar,j1x,((nparj(l,lp),lp=l,j1x),
     1 l=1,j1x)
      npar = npar-j1x
      nord=noic(k)+1
      ispace=0
      itrans=0
      if (nosubc.eq.1) go to 151
      ii=7
      if (nosubc.lt.3) ii=4
      do 150 i=3,ii
      if (kcpld(i).ne.0) go to 150
      ispace=ispace+1
      jjj=i
  150 continue
      if (ispace.ne.1) go to 151
      itrans=1
      kcprce=jjj
c
c
  151 do 400 mzq=1,nscrj8
c               Read tmx(ls,jj)
      read (ic) scrj8,nls, ((tmx(l,lp),l=1,nls), lp=1,nls),
     1  ((nals(l,i),scrl(l,i),scrs(l,i),
     2  i=1,nosubc), ncfg(l),fidls(l,1),fidjj(l,1), l=1,nls)
      nord=nord+1
      i1=1
      i2=2
      if (kcpl.eq.1) go to 152
      i1=2
      i2=1
  152 do 160 l=1,nls
      yiden(l,i1)=fidls(l,1)
      yiden(l,i2)=fidjj(l,1)
c     encode (8,18,sj8) scrj8
      write (sj8,18) scrj8
   18 format (2x,2hj=,f4.1)
c               calc g-matrix, and transform if kcpl=2
      do 154 lp=1,nls
  154 c(l,lp)=0.0
      if (scrj8.eq.0.0) go to 160
      c(l,l)=0.50116*(scrs(l,nosubc)**2+scrs(l,nosubc)-scrl(l,nosubc)**2
     1  -scrl(l,nosubc))/(scrj8**2+scrj8)+1.50116
  160 continue
      if (kcpl.eq.1) go to 165
      do 162 l=1,nls
      do 162 lp=1,nls
      ct4(l,lp)=0.0
      do 161 lpp=1,nls
  161 ct4(l,lp)=ct4(l,lp)+c(l,lpp)*tmx(lpp,lp)
  162 continue
c               Transpose from tmx(ls,jj) to tmx(jj,ls)
      do 163 l=1,nls
      do 163 lp=l,nls
      a=tmx(l,lp)
      tmx(l,lp)=tmx(lp,l)
  163 tmx(lp,l)=a
      do 164 l=1,nls
      do 164 lp=1,nls
      c(l,lp)=0.0
      do 164 lpp=1,nls
      c(l,lp)=c(l,lp)+tmx(l,lpp)*ct4(lpp,lp)
  164 continue
c               Write g-matrix on 19
  165 close (19,status='delete')
      open (19,status='scratch',form='unformatted')
      rewind 19
      write (19) ((c(l,lp),l=lp,nls), lp=1,nls)
      if (itrans.eq.0) go to 188
      if (nls.gt.nlsmax) go to 188
      do 170 l=1,nls
      yiden(l,2)=yiden(l,1)
  170 continue
      i2=i1
      i1=kcprce
      if (nls.eq.1) go to 188
  171 do 175 i=1,npar
  175 read (ic) dumdcg
c               Read tmx(i,kcpl)
      read (ic) ((tmx(lp,l),lp=1,nls),fk(l),fkj(l),scrj(l,1),scrj(l,2),
     1  scrl6(l),fk6(l),scrs6(l),lhqq(l),multqq(l),l=1,nls)
      go to (176,176,176,178,180,182,184) kcprce
  176 do 177 l=1,nls
      write (yiden(l,1),21) scrj(l,1),fkj(l)
   21 format(f3.1,1hk,f4.1)
  177 continue
      go to 186
  178 do 179 l=1,nls
      lp1=scrl(l,nosubc)+1.0
      lhs4=lsymb(lp1)
      write (yiden(l,1),22) lhs4,fk(l)
   22 format(1x,a1,1h(,f4.1,1h))
  179 continue
      go to 186
  180 do 181 l=1,nls
      write (yiden(l,1),21) scrj(l,1),fk(l)
  181 continue
      go to 186
  182 do 183 l=1,nls
      write (yiden(l,1),23) scrj(l,2),lhqq(l),fk6(l),multqq(l)
   23 format(f3.1,a1,f3.1,i1)
  183 continue
      go to 186
  184 do 185 l=1,nls
      write (yiden(l,1),24) scrj(l,2),multqq(l),lhqq(l),scrj(l,1)
   24 format(f3.1,i1,a1,f3.1)
  185 continue
  186 npars=npar+1
c     do 187 i=1,npars
c 187 backspace ic
      rewind ic
c     nord=noic(k)+2+(mzq-1)*(npar+2)
      do 187 i=1,nord
  187 read (ic) dumdcg
c               Write tmx(i,kcpl), or (if itrans=0 or nls.gt.nlsmax)
c                 tmx(LS,JJ) if kcpl=1 or tmx(JJ,LS) if kcpl=2.
  188 write (2) sj8,nls, ((tmx(l,lp),l=1,nls), lp=1,nls),
     1  (ncfg(l),l=1,nls),((yiden(l,nzq),l=1,nls),nzq=1,2)
      if (nls.eq.1) nonlseq1=nonlseq1+1
      npars=npar+1
      do 250 nzq=1,npars
      i=ic
c     if (nzq.ne.npars) go to 204
      if (nzq.ne.npars) go to 205
      i=19
      rewind 19
c               Read coeff (nzq.lt.npars) or g (nzq.eq.npars) matrix
  204 read (i) ((c(l,lp),l=lp,nls), lp=1,nls)
      go to 210
  205 read (i) ncoeff,(illp(n),coeff(n),n=1,ncoeff)
      nord=nord+1
      do 206 lp=1,nls
      do 206 l=lp,nls
  206 c(l,lp)=0.0
      do 207 n=1,ncoeff
      l=illp(n)/10000
      lp=illp(n)-10000*l
  207 c(l,lp)=coeff(n)
  210 if(itrans.eq.0) go to 240
      if (nls.eq.1) go to 240
      if (nls.gt.nlsmax) go to 240
c               If itrans.gt.0 and nls.le.nlsmax, transf matrix to i.
      do 220 l=2,nls
      ls=l-1
      do 220 lp=1,ls
  220 c(lp,l)=c(l,lp)
      do 230 l=1,nls
      do 230 lp=1,nls
      ct4(l,lp)=0.0
      do 229 lpp=1,nls
  229 ct4(l,lp)=ct4(l,lp)+tmx(l,lpp)*c(lpp,lp)
  230 continue
      do 235 l=1,nls
      do 235 lp=1,l
      c(l,lp)=0.0
      do 234 lpp=1,nls
  234 c(l,lp)=c(l,lp)+ct4(l,lpp)*tmx(lp,lpp)
  235 continue
c 240 write (2) ((c(l,lp),l=lp,nls), lp=1,nls)
  240 ncoeff=0
      do 245 lp=1,nls
      do 245 l=lp,nls
      if (c(l,lp).eq.0.0) go to 245
      ncoeff=ncoeff+1
      illp(ncoeff)=10000*l+lp
      coeff(ncoeff)=c(l,lp)
  245 continue
      if (ncoeff.gt.0) go to 247
      ncoeff=1
      illp(1)=10001
      coeff(1)=0.0
  247 write (2) ncoeff,(illp(i),coeff(i),i=1,ncoeff)
  250 continue
      call clock(time)
      delt=time-time0
      if (iw6.lt.0) write (6,15) mzq,nscrj8,delt,nls,npars
   15 format (' end calc of matrix',i3,' of',i3,';   time=',
     1  f8.3',   size=',i3,',   npars=',i4)
      if (ispace.eq.0) go to 400
      if (nls.eq.1) go to 400
      if (nls.gt.nlsmax) go to 400
      do 399 i=1,ispace
  399 read (ic) dumdcg
      nord=nord+ispace
  400 continue
      call clock(time)
      delt=time-time0
      write (iw,40) nocset,delt,coupl(i1),coupl(i2)
   40 format (12h0cset number,i4,27h written on tape 2 at time=,f7.3,
     1  17h  for couplings  ,a8,7h  and  ,a8//)
      if (iw6.lt.0) write (6,40) nocset,delt,coupl(i1),coupl(i2)
c
c          Write input for RCE on disk 11, using (if a diagonalization
c               has been made) computed instead of experimental levels,
c               and using the theoretical parameter values
c               as preliminary estimates; if no diagonalization,
c               then use zeroes for the above quantities.
c
  500 nocypr=1
      nocycr=30
      nocyce=5
      write (11,51) nocypr,nocycr,nocyce,iw6
   51 format (3i5,5x,i5)
      ncdes=nocset
      idenom=0
      iprnv=1
      iprna=1
      wmax=0.0
      iprnx=1
      iprnsq=1
      scale=1.0
      write (11,52) ncdes,idenom,iprnv,iprna,wmax,iprnx,iprnsq,scale
   52 format (4i5,f10.3,2i5,f10.4)
      write (11,53) elem(1,1,k),(elem(2,i,k),elem(3,i,k), i=1,j1x)
   53 format (a8,2x,6(a6,a4)/7(a6,a4))
      npar=npar+j1x
      j=0
      do 530 i=1,npar
      write (parnm(i),523) parnam(i,k)
  523 format (a10)
      if (parnm(i)(1:3).ne.'eav') go to 530
      j=j+1
      write (parnm(i),524) elem(2,j,k)
  524 format (4heav ,a6)
  530 continue
      write (11,54) (parnm(i), i=1,npar)
   54 format (7a10)
      rewind il
      if (iewr.gt.0) go to 550
      do 540 lp=1,kmx
  540 eig(lp)=0.0
      do 545 i=1,kpr
  545 vpar(i,k)=0.0
      read (il)
  550 gre=0.0
      do 552 i=1,npar
  552 gre=max(vpar(i,k),gre)
      do 560 n=1,nscrj8
      if (iewr.gt.0) go to 558
      read (il) sj,nls
      go to 559
  558 read (il) sj,nls, (eig(lp), (eras,l=1,nls), lp=1,nls)
      read (il)
  559 if (gre.le.7.0e3) write (11,55) (eig(lp), lp=1,nls)
   55 format (7f10.4)
      if (gre.gt.7.0e3.and.gre.le.7.0e4) write(11,56) (eig(lp),lp=1,nls)
   56 format (7f10.3)
      if (gre.gt.7.0e4) write (11,57) (eig(lp), lp=1,nls)
   57 format (7f10.2)
  560 write (11,58) (lp, lp=1,nls)
   58 format (7i10)
      npar=0
      do 565 mzq=1,j1x
  565 npar=npar+nparj(mzq,mzq)
      j=-50
      do 570 i=1,npar
      multqq(i)=0
      if (iewr.eq.0.or.i.eq.1.or.vpar(i,k).gt.0.0) go to 570
      multqq(i)=-99
  570 continue
      if (j1x.eq.1) go to 600
      j1x1=j1x-1
      do 590 mzq=1,j1x1
      mzq1=mzq+1
      npar2=0
      do 585 mp=mzq1,j1x
  585 npar2=npar2+nparj(mzq,mp)
      npar2=npar+npar2
      npar=npar+1
      j=j-1
      do 588 i=npar,npar2
  588 multqq(i)=j
  590 npar=npar2
  600 write (11,58) (multqq(i), i=1,npar)
      xmax=0.0
      write (11,55) (xmax, i=1,npar)
      if (gre.le.7.0e3) write (11,55) (vpar(i,k), i=1,npar)
      if (gre.gt.7.0e3.and.gre.le.7.0e4)
     1  write (11,56) (vpar(i,k), i=1,npar)
      if (gre.gt.7.0e4) write (11,57) (vpar(i,k), i=1,npar)
      f0=1.0
      fm=0.0
      f1=-1.0
      delf=0.0
      nofmax=1000
      gmax=1.0
      dxmax=10000.0
      crit1=0.3
      crit=0.00
      icrit2=-1
      write (11,60) f0,fm,f1,delf,nofmax,gmax,dxmax,crit1,crit,icrit2
   60 format (3f10.1,f5.2,i5,f10.3,f10.2,2f5.2,i2)
      ncdes=-1
      write (11,52) ncdes
c
      if (k.eq.2) go to 900
      k=2
      il=ilb
      if (nsconf(1,k).eq.0) go to 900
      if (noicmup(1).eq.0) go to 710
      ispace=noicmup(1)
      do 700 i=1,ispace
  700 read (ic) dumdcg
  710 nocset=nocset+1
      read (ic) notsj1,nscrj8,sj8mn,sj8mx,npar,nparj,parnam
      go to 100
c
  900 return
      end
