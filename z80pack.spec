Summary:	Z80 assembler and simulator
Summary(pl):	Asembler oraz symulator dla procesora Z80
Name:		z80pack
Version:	1.1
Release:	1
License:	non-commercial (see license* files)
Group:		Development/Tools
Source0:	ftp://ftp.gefoekom.de/pub/unix/emulators/computer/misc/%{name}.tgz
# Source0-md5:	a0d624a2cc76e0b34c0ec2dcdf3a2118
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains Z80 crossassembler (z80asm), Z80 simulator
(z80sim) and Z80 simlulator capable of running CP/M (cpmsim).

%description -l pl
Ten pakiet zawiera asembler skro¶ny dla procesora Z80 (z80asm),
symulator procesora Z80 (z80sim) oraz symulator procesora pozwalaj±cy
na uruchomienie systemu CP/M (cpmsim).

%prep
%setup -q -n %{name}

sed -i -e 's/"receive"/"cpmreceive"/g' cpmsim/srcsim/iosim.c

%build
%{__make} -C z80asm \
	CFLAGS="%{rpmcflags} -c" \
	LFLAGS="%{rpmldflags}" \

%{__make} -C z80sim -f Makefile.usv \
	CFLAGS="%{rpmcflags} -c" \
	LFLAGS="%{rpmldflags}"

mkfifo cpmsim/{auxin,auxout}
cd cpmsim/srcsim
./lnsrc
%{__make} \
	CFLAGS="%{rpmcflags} -c" \
	LFLAGS="%{rpmldflags}"
cd ../..

ln -sf bios64.asm cpmsim/srccpm/bios.asm
ln -sf boot64.asm cpmsim/srccpm/boot.asm
%{__make} -C cpmsim/srccpm \
	PATH="../../z80asm:$PATH" \
	CFLAGS="%{rpmcflags} %{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/cpmsim/disks}

install z80asm/z80asm z80sim/z80sim cpmsim/cpmsim $RPM_BUILD_ROOT%{_bindir}
install cpmsim/receive $RPM_BUILD_ROOT%{_bindir}/cpmreceive
install cpmsim/send $RPM_BUILD_ROOT%{_bindir}/cpmsend

mkfifo $RPM_BUILD_ROOT%{_datadir}/cpmsim/{auxin,auxout}
install cpmsim/disks/drivea.cpm $RPM_BUILD_ROOT%{_datadir}/cpmsim/disks

mv -f cpmsim/README cpmsim.README
mv -f z80asm/README z80asm.README
mv -f z80asm/license.de z80asm.license.de
mv -f z80asm/license.us z80asm.license.us
mv -f z80sim/license.de z80sim.license.de
mv -f z80sim/license.us z80sim.license.us

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *README* *.license.us
%lang(de) %doc *.license.de
%attr(755,root,root) %{_bindir}/*
%{_datadir}/cpmsim
