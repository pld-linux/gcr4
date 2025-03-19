#
# Conditional build:
%bcond_without	apidocs	# API documentation

Summary:	GObject and GUI library for high level crypto parsing and display
Summary(pl.UTF-8):	Biblioteka GObject i GUI do wysokopoziomowej analizy i wyświetlania danych kryptograficznych
Name:		gcr4
Version:	4.4.0.1
Release:	1
License:	LGPL v2+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gcr/4.4/gcr-%{version}.tar.xz
# Source0-md5:	01da4445b5b16801c6dcc7d8945b4cc4
URL:		https://gitlab.gnome.org/GNOME/gcr
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	gi-docgen
BuildRequires:	glib2-devel >= 1:2.74
BuildRequires:	gobject-introspection-devel >= 1.34.0
BuildRequires:	gtk4-devel >= 4
# or gnutls>=3.8.5 with -Dcrypto=gnutls
BuildRequires:	libgcrypt-devel >= 1.4.5
BuildRequires:	libsecret-devel >= 0.20
BuildRequires:	libtasn1-devel
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 0.59
BuildRequires:	ninja >= 1.5
# to configure ssh-add,ssh-agent paths
BuildRequires:	openssh-clients
BuildRequires:	p11-kit-devel >= 0.19.0
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	systemd-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.20.0
BuildRequires:	xz
Requires(post,preun,postun):	systemd-units >= 1:250.1
Requires:	gnupg2 >= 2.0
Requires:	libsecret >= 0.20
Requires:	systemd-units >= 1:250.1
Conflicts:	gnome-keyring < 3.3.0
Provides:	gcr = %{version}
Obsoletes:	gcr < 4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gcr is a library for displaying certificates, and crypto UI, accessing
key stores. It also provides a viewer for crypto files on the GNOME
desktop.

gck is a library for accessing PKCS#11 modules like smart cards.

%description -l pl.UTF-8
gcr to biblioteka do wyświetlania certyfikatów oraz kryptograficznego
interfejsu użytkownika, pozwalającego na dostęp do kluczy. Zapewnia
tekże przeglądarkę plików kryptograficznych dla środowiska GNOME.

gck to biblioteka dostepu do modułów PKCS#11, takich jak karty
procesorowe.

%package libs
Summary:	gcr and gck libraries
Summary(pl.UTF-8):	Biblioteki gcr i gck
Group:		Libraries
Requires:	glib2 >= 1:2.74
Requires:	libgcrypt >= 1.4.5
Requires:	p11-kit >= 0.19.0
Obsoletes:	gnome-keyring-libs < 3.3.0

%description libs
This package provides gcr and gck libraries.

%description libs -l pl.UTF-8
Ten pakiet dostarcza biblioteki gcr i gck.

%package devel
Summary:	Header files for gcr and gck libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek gcr i gck
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.74
Requires:	p11-kit-devel >= 0.19.0
Obsoletes:	gcr-static < 3.36.0
Obsoletes:	gcr-ui-static < 3.36.0
Obsoletes:	gnome-keyring-devel < 3.3.0

%description devel
Header files for gcr and gck libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek gcr i gck.

%package -n vala-gcr4
Summary:	gcr and gck API for Vala language
Summary(pl.UTF-8):	API gcr i gck dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.20.0
BuildArch:	noarch

%description -n vala-gcr4
gcr and gck API for Vala language.

%description -n vala-gcr4 -l pl.UTF-8
API gcr i gck dla języka Vala.

%package apidocs
Summary:	gcr and gck API documentation
Summary(pl.UTF-8):	Dokumentacja API bibliotek gcr i gck
Group:		Documentation
Obsoletes:	gnome-keyring-apidocs < 3.3.0
BuildArch:	noarch

%description apidocs
API and gck documentation for gcr library.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek gcr i gck.

%prep
%setup -q -n gcr-%{version}

%build
%meson \
	-Dgpg_path=%{__gpg} \
	-Dgtk_doc=%{__true_false apidocs} \
	-Dsystemd=enabled

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/{gck-2,gcr-4} $RPM_BUILD_ROOT%{_gidocdir}
%endif

# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang gcr-4

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_user_post gcr-ssh-agent.service

%preun
%systemd_user_preun gcr-ssh-agent.service

%postun
%systemd_user_postun_with_restart gcr-ssh-agent.service

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f gcr-4.lang
%defattr(644,root,root,755)
%doc CONTRIBUTING.md NEWS README.md
%attr(755,root,root) %{_bindir}/gcr-viewer-gtk4
%attr(755,root,root) %{_libexecdir}/gcr-ssh-agent
%attr(755,root,root) %{_libexecdir}/gcr4-ssh-askpass
%{systemduserunitdir}/gcr-ssh-agent.service
%{systemduserunitdir}/gcr-ssh-agent.socket

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgck-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgck-2.so.2
%attr(755,root,root) %{_libdir}/libgcr-4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgcr-4.so.4
%{_libdir}/girepository-1.0/Gck-2.typelib
%{_libdir}/girepository-1.0/Gcr-4.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgck-2.so
%attr(755,root,root) %{_libdir}/libgcr-4.so
%{_datadir}/gir-1.0/Gck-2.gir
%{_datadir}/gir-1.0/Gcr-4.gir
%{_includedir}/gck-2
%{_includedir}/gcr-4
%{_pkgconfigdir}/gck-2.pc
%{_pkgconfigdir}/gcr-4.pc

%files -n vala-gcr4
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gck-2.deps
%{_datadir}/vala/vapi/gck-2.vapi
%{_datadir}/vala/vapi/gcr-4.deps
%{_datadir}/vala/vapi/gcr-4.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/gck-2
%{_gidocdir}/gcr-4
%endif
