#
# Conditional build:
%bcond_with	mozjs		# use Mozilla JavaScript (>= 1.9)
%bcond_with	v8		# use Chrome V8 JavaScript
#
Summary:	PACrunner - Proxy configuration daemon
Summary(pl.UTF-8):	PACrunner - demon do konfiguracji proxy
Name:		pacrunner
Version:	0.5
Release:	1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://www.kernel.org/pub/linux/network/connman/%{name}-%{version}.tar.xz
# Source0-md5:	bca9a5c84afe66a03c621af424501160
# pacrunner.org is dead
URL:		http://www.ohloh.net/p/pacrunner
BuildRequires:	curl-devel >= 7.16
BuildRequires:	dbus-devel >= 1.2
BuildRequires:	glib2-devel >= 1:2.16
BuildRequires:	libcap-ng-devel
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
%{?with_v8:BuildRequires:	v8-devel}
%{?with_mozjs:BuildRequires:	xulrunner-devel >= 1.9}
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PACrunner provides a daemon for processing proxy configuration and
providing information to clients over D-Bus.

%description -l pl.UTF-8
PACrunner zawiera demona do przetwarzania konfiguracji proxy i
udostępniania informacji klientom poprzez D-Bus.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	--enable-capng \
	--enable-curl \
	%{?with_mozjs:--enable-mozjs} \
	%{?with_v8:--enable-v8}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO doc/*.txt
%attr(755,root,root) %{_sbindir}/pacrunner
/etc/dbus-1/system.d/pacrunner.conf
/usr/share/dbus-1/system-services/pacrunner.service
