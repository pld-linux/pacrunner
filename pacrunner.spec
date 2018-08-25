#
# Conditional build:
%bcond_with	mozjs		# use Mozilla JavaScript
%bcond_with	v8		# use Chrome V8 JavaScript
%bcond_with	libproxy	# build libproxy compatible library
#
Summary:	PACrunner - Proxy configuration daemon
Summary(pl.UTF-8):	PACrunner - demon do konfiguracji proxy
Name:		pacrunner
Version:	0.14
Release:	1
License:	GPL v2
Group:		Applications/Networking
Source0:	https://www.kernel.org/pub/linux/network/connman/%{name}-%{version}.tar.xz
# Source0-md5:	74303b95b056d8d630dd45e6668d24d2
# pacrunner.org is dead
URL:		http://www.ohloh.net/p/pacrunner
BuildRequires:	curl-devel >= 7.16
BuildRequires:	dbus-devel >= 1.2
BuildRequires:	glib2-devel >= 1:2.16
%{?with_mozjs:BuildRequires:	mozjs38-devel >= 38}
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
%{?with_v8:BuildRequires:	v8-devel}
BuildRequires:	xz
Requires:	curl-libs >= 7.16
Requires:	dbus >= 1.2
Requires:	glib2 >= 1:2.16
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PACrunner provides a daemon for processing proxy configuration and
providing information to clients over D-Bus.

%description -l pl.UTF-8
PACrunner zawiera demona do przetwarzania konfiguracji proxy i
udostępniania informacji klientom poprzez D-Bus.

%package libproxy
Summary:	PACrunner based proxy configuration library
Summary(pl.UTF-8):	Biblioteka do konfiguracji proxy oparta na PACrunnerze
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description libproxy
PACrunner based proxy configuration library (compatible with
libproxy).

%description libproxy -l pl.UTF-8
Biblioteka do konfiguracji proxy oparta na PACrunnerze (zgodna z
libproxy).

%package libproxy-devel
Summary:	Header file for PACrunner libproxy library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki PACrunnera libproxy
Group:		Development/Libraries
Requires:	%{name}-libproxy = %{version}-%{release}

%description libproxy-devel
Header file for PACrunner libproxy library.

%description libproxy-devel -l pl.UTF-8
Plik nagłówkowy biblioteki PACrunnera libproxy.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	--enable-curl \
	--enable-duktape \
	%{?with_libproxy:--enable-libproxy} \
	%{?with_mozjs:--enable-mozjs} \
	%{?with_v8:--enable-v8}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with libproxy}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libproxy.la
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libproxy -p /sbin/ldconfig
%postun	libproxy -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO doc/*.txt
%attr(755,root,root) %{_sbindir}/pacrunner
/etc/dbus-1/system.d/pacrunner.conf
/usr/share/dbus-1/system-services/org.pacrunner.service

%if %{with libproxy}
%files libproxy
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/manual-proxy-test
%attr(755,root,root) %{_bindir}/proxy
%attr(755,root,root) %{_libdir}/libproxy.so.1.0.0
%attr(755,root,root) %ghost %{_libdir}/libproxy.so.1

%files libproxy-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libproxy.so
%{_includedir}/proxy.h
%{_pkgconfigdir}/libproxy-1.0.pc
%endif
