
%bcond_without	tests

%define		_ver 2.0.2
%define		_svnrel 566
Summary:	AppArmor userlevel parser utility
Summary(pl.UTF-8):	Narzędzie przestrzeni użytkownika do przetwarzania AppArmor
Name:		apparmor-parser
Version:	%{_ver}.%{_svnrel}
Release:	0.3
Epoch:		1
License:	GPL
Group:		Applications/System
Source0:	http://forge.novell.com/modules/xfcontent/private.php/apparmor/LKML_Submission-April_07/%{name}-%{_ver}-%{_svnrel}.tar.gz
# Source0-md5:	9851ad9eec502a04b5d01998492e92f7
Source1:	%{name}.init
Patch0:		%{name}-init-args.patch
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	libcap-devel
BuildRequires:	perl-Test-Harness >= 2.64
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
%setup -q -n %{name}-%{_ver}
%patch0 -p2

%build
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags}"

%{?with_tests:%{__make} tests}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{apparmor,rc.d/init.d},/sbin,/subdomain,/var/lib/apparmor}

install apparmor_parser $RPM_BUILD_ROOT/sbin
install subdomain.conf $RPM_BUILD_ROOT%{_sysconfdir}/apparmor
install rc.apparmor.functions $RPM_BUILD_ROOT%{_sysconfdir}/apparmor
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/apparmor

%{__make} -C po install \
	DESTDIR=$RPM_BUILD_ROOT \
	NAME=%{name}
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
%doc README
%attr(755,root,root) /sbin/apparmor_parser
%dir %{_sysconfdir}/apparmor
%{_sysconfdir}/apparmor/rc.apparmor.functions
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apparmor/subdomain.conf
%attr(754,root,root) /etc/rc.d/init.d/apparmor
#%attr(754,root,root) /etc/rc.d/init.d/aaeventd
/subdomain
/var/lib/apparmor
