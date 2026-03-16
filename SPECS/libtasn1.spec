%global package_speccommit bbfac2bf634ede3df5946e3145cb5128a79c2116
%global usver 4.21.0
%global xsver 1
%global xsrel %{xsver}%{?xscount}%{?xshash}
# Do not build docs by default
%bcond_with docs
Summary:	The ASN.1 library used in GNUTLS
Name:		libtasn1
Version:	4.21.0
Release: %{?xsrel}~XCPNG2989.3%{?dist}

# The libtasn1 library is LGPLv2+, utilities are GPLv3+
License:	GPLv3+ and LGPLv2+
URL:		http://www.gnu.org/software/libtasn1/
Source0: libtasn1-4.21.0.tar.gz
Source1: libtasn1-4.21.0.tar.gz.sig
Patch0: libtasn1-3.4-rpath.patch
#Source2:	gpgkey-1F42418905D8206AA754CCDC29EE58B996865171.gpg
#Source2:	gpgkey-99415CE1905D0E55A9F88026860B7FBB32F8119D.gpg
Source2: gpgkey-B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE.gpg

BuildRequires:	gnupg2
BuildRequires:	gcc
BuildRequires:	bison, pkgconfig
BuildRequires:	autoconf, automake, libtool
BuildRequires:	valgrind-devel
BuildRequires:  make
BuildRequires:  texinfo
%if %{with docs}
BuildRequires:  gtk-doc
%endif
# Wildcard bundling exception https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib) = 20130324

%package devel
Summary:	Files for development of applications which will use libtasn1
Requires:	%{name}%{?_isa} = %{version}-%{release}

Requires:	%name = %version-%release
Requires:	%{name}-tools = %{version}-%{release}
Requires:	pkgconfig


%package tools
Summary:	Some ASN.1 tools
License:	GPLv3+
Requires:	%{name}%{?_isa} = %{version}-%{release}


%description
A library that provides Abstract Syntax Notation One (ASN.1, as specified
by the X.680 ITU-T recommendation) parsing and structures management, and
Distinguished Encoding Rules (DER, as per X.690) encoding and decoding functions.

%description devel
This package contains files for development of applications which will
use libtasn1.


%description tools
This package contains simple tools that can decode and encode ASN.1
data.


%prep
# GPG in XS8 does not support the signature algorithm used, signature has been
# checked externally before the source was fixed so does not require checking
# here.
%if 0%{?xenserver} >= 9
gpgv2 --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%endif
%autosetup -p1


%build
%if %{with docs}
# Doing this forces you to have gtkdoc installed
autoreconf -v -f --install
%endif
%configure --disable-static \
	--disable-silent-rules
# libtasn1 likes to regenerate docs
touch doc/stamp_docs

%make_build


%install
%make_install

rm -f $RPM_BUILD_ROOT{%_libdir/*.la,%_infodir/dir}


%check
make check

%files
%license COPYING COPYING.LESSERv2
%doc AUTHORS NEWS README.md
%{_libdir}/*.so.6*

%files tools
%{_bindir}/asn1*
%{_mandir}/man1/asn1*

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_infodir}/*.info.*
%{_mandir}/man3/*asn1*


%changelog
* Fri Jan 09 2026 Alex Brett <alex.brett@citrix.com> - 4.21.0-1
- CA-422581: Update to libtasn1 v4.21.0

* Fri Sep 06 2024 AshwinH  <ashwin.h@cloud.com> - 4.19.0-2
- CP-50735: Remove legacy Buildrequires help2man

* Wed Jul 12 2023 Tim Smith <tim.smith@citrix.com> - 4.19.0-1
- Initial import

