
%bcond_without	tests

Summary:	AppArmor userlevel parser utility
Summary(pl.UTF-8):	Narzędzie przestrzeni użytkownika do przetwarzania AppArmor
Name:		apparmor-parser
Version:	2.6.1
Release:	2
Epoch:		1
License:	GPL
Group:		Applications/System
Source0:	http://launchpad.net/apparmor/2.6/%{version}/+download/apparmor-%{version}.tar.gz
# Source0-md5:	e2dabce946cb8258834f90f0a6c87726
Source1:	%{name}.init
Patch0:		%{name}-bzr.patch
Patch1:		%{name}-pld.patch
URL:		http://apparmor.wiki.kernel.org/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	libcap-devel
BuildRequires:	libstdc++-devel
# for apparmor_profile which links statically sometimes
BuildRequires:	libstdc++-static
BuildRequires:	perl-Test-Harness
BuildRequires:	perl-tools-devel
BuildRequires:	perl-tools-pod
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
AppArmor Parser is a userlevel program that is used to load in program
profiles to the AppArmor Security kernel module. This package is part
of a suite of tools that used to be named SubDomain.

%description -l pl.UTF-8
AppArmor Parser to program przestrzeni użytkownika służący do
wczytywania profili programów dla modułu bezpieczeństwa AppArmor jądra
Linuksa. Ten pakiet jest częścią zestawu narzędzi nazywanych
SubDomain.

%prep
%setup -q -n apparmor-%{version}
# reenable when needed
#%patch0 -p0
%patch1 -p0

%build
%{__make} -C parser main manpages \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}"

%{?with_tests:%{__make} -C parser tests}

%install
rm -rf $RPM_BUILD_ROOT
cd parser

install -d $RPM_BUILD_ROOT{%{_mandir}/man{5,7,8},%{_sysconfdir}/{apparmor,rc.d/init.d},/sbin,/subdomain,/var/lib/apparmor}

install apparmor_parser $RPM_BUILD_ROOT/sbin
install subdomain.conf $RPM_BUILD_ROOT%{_sysconfdir}/apparmor
install rc.apparmor.functions $RPM_BUILD_ROOT%{_sysconfdir}/apparmor
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/apparmor
install *.5 $RPM_BUILD_ROOT%{_mandir}/man5
install *.7 $RPM_BUILD_ROOT%{_mandir}/man7
install *.8 $RPM_BUILD_ROOT%{_mandir}/man8

%{__make} -C po install \
	DESTDIR=$RPM_BUILD_ROOT \
	NAME=%{name}

cd ..
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add apparmor

%preun
if [ "$1" = "0" ]; then
        /sbin/chkconfig --del apparmor
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc parser/README
%attr(755,root,root) /sbin/apparmor_parser
%dir %{_sysconfdir}/apparmor
%{_sysconfdir}/apparmor/rc.apparmor.functions
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apparmor/subdomain.conf
%attr(754,root,root) /etc/rc.d/init.d/apparmor
/subdomain
/var/lib/apparmor
%{_mandir}/man[578]/*.[578]*
