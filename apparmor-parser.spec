%define		_ver 2.0
%define		_svnrel 25
Summary:	AppArmor userlevel parser utility
Summary(pl):	Narz�dzie przestrzeni u�ytkownika do przetwarzania AppArmor
Name:		apparmor-parser
Version:	%{_ver}.%{_svnrel}
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	http://forge.novell.com/modules/xfcontent/private.php/apparmor/Development%20-%20April%20Snapshot/%{name}-%{_ver}-%{_svnrel}.tar.gz
# Source0-md5:	1486ed6062435ff82340d6d9967b4df6
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	libcap-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
AppArmor Parser is a userlevel program that is used to load in program
profiles to the AppArmor Security kernel module. This package is part
of a suite of tools that used to be named SubDomain.

%description -l pl
AppArmor Parser to program przestrzeni u�ytkownika s�u��cy do
wczytywania profili program�w dla modu�u bezpiecze�stwa AppArmor j�dra
Linuksa. Ten pakiet jest cz�ci� zestawu narz�dzi nazywanych SubDomain.

%prep
%setup -q -n %{name}-%{_ver}

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/apparmor,/sbin,/subdomain,/var/lib/apparmor}
install apparmor_parser $RPM_BUILD_ROOT/sbin
install subdomain.conf $RPM_BUILD_ROOT%{_sysconfdir}/apparmor
%{__make} -C po install \
	DESTDIR=$RPM_BUILD_ROOT \
	NAME=%{name}
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) /sbin/apparmor_parser
%dir %{_sysconfdir}/apparmor
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apparmor/subdomain.conf
#%attr(754,root,root) /etc/rc.d/init.d/aaeventd
#%attr(754,root,root) /etc/rc.d/init.d/apparmor
/subdomain
/var/lib/apparmor
