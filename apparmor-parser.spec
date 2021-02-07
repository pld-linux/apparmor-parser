#
# Conditional build:
%bcond_with	tests	# don't perform "make tests"
%bcond_with	dynamic	# link libstdc++ and libgcc dynamically
#
Summary:	AppArmor userlevel parser utility
Summary(pl.UTF-8):	Narzędzie przestrzeni użytkownika do przetwarzania AppArmor
Name:		apparmor-parser
Version:	3.0.1
Release:	1
Epoch:		1
License:	GPL v2
Group:		Applications/System
Source0:	http://launchpad.net/apparmor/3.0/%{version}/+download/apparmor-%{version}.tar.gz
# Source0-md5:	e05eab22bdd1dfc64854856a7292cf09
Source1:	%{name}.init
Patch0:		%{name}-pld.patch
# Drop when upstream does cache rebuild based on hash and not on mtime
Patch1:		%{name}-cache-rebuild.patch
Patch2:		cap.patch
URL:		http://wiki.apparmor.net/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-tools
BuildRequires:	libapparmor-devel >= 1:%{version}
BuildRequires:	libcap-devel
BuildRequires:	libstdc++-devel
# for apparmor_profile which links statically sometimes
%if %{without dynamic}
BuildRequires:	libapparmor-static
BuildRequires:	libstdc++-static
%endif
BuildRequires:	perl-tools-pod
%if %{with tests}
%if %(test -e /sys/kernel/security/apparmor/features ; echo $?)
# apparmor enabled kernel running and fs mounted
BuildRequires:	/sys/kernel/security/apparmor/features
%endif
BuildRequires:	perl-Locale-gettext
BuildRequires:	perl-Test-Harness
BuildRequires:	perl-tools-devel
%endif
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
%patch0 -p1
%patch1 -p1
%patch2 -p1

# avoid unnecessary rebuilding on install
%{__sed} -i -e '/^\.PHONY: af_names.h/d' parser/Makefile
%{__sed} -i -e '/^\.\(PHONY\|SILENT\): \$(AAREOBJECT)/d' parser/Makefile

%build
%{__make} -j1 -C parser \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	%{?with_dynamic:AAREOBJECTS='$(AAREOBJECT)' AARE_LDFLAGS= AALIB=-lapparmor} \
	USE_SYSTEM=1

%if %{with tests}
%{__make} -j1 -C parser tests \
	CC="%{__cc}" \
	%{?with_dynamic:AAREOBJECTS='$(AAREOBJECT)' AARE_LDFLAGS=-lstdc++ AALIB=-lapparmor} \
	USE_SYSTEM=1
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/lib/apparmor,/var/cache/apparmor}

%{__make} -C parser install \
	DESTDIR=$RPM_BUILD_ROOT \
	DISTRO=systemd \
	SYSTEMD_UNIT_DIR=$RPM_BUILD_ROOT%{systemdunitdir} \
	USE_SYSTEM=1

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/apparmor

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
%attr(755,root,root) %{_sbindir}/aa-teardown
%dir %{_sysconfdir}/apparmor
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apparmor/parser.conf
%attr(754,root,root) /etc/rc.d/init.d/apparmor
%{systemdunitdir}/apparmor.service
%dir /lib/apparmor
/lib/apparmor/rc.apparmor.functions
%attr(754,root,root) /lib/apparmor/apparmor.systemd
%attr(700,root,root) %dir /var/cache/apparmor
%dir /var/lib/apparmor
%{_mandir}/man5/apparmor.d.5*
%{_mandir}/man7/apparmor.7*
%{_mandir}/man7/apparmor_xattrs.7*
%{_mandir}/man8/aa-teardown.8*
%{_mandir}/man8/apparmor_parser.8*
