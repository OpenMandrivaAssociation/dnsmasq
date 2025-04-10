Summary:	A lightweight dhcp and caching nameserver
Name:		dnsmasq
Version:	2.91
Release:	1
License:	GPLv2 or GPLv3
Group:		System/Servers
Url:		https://www.thekelleys.org.uk/dnsmasq
Source0:	http://www.thekelleys.org.uk/dnsmasq/%{name}-%{version}.tar.xz
Source1:	dnsmasq.sysconfig
Source2:	dnsmasq.service
Patch0:		dnsmasq-2.80-compile.patch

BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libidn)
BuildRequires:	rpm-helper
Requires:	%{name}-base = %{version}-%{release}
Requires(preun,post):	rpm-helper
Conflicts:	bind

%description
Dnsmasq is lightweight, easy to configure DNS forwarder and DHCP server. It
is designed to provide DNS and, optionally, DHCP, to a small network. It can
serve the names of local machines which are not in the global DNS. The DHCP
server integrates with the DNS server and allows machines with DHCP-allocated
addresses to appear in the DNS with names configured either in each host or
in a central configuration file. Dnsmasq supports static and dynamic DHCP
leases and BOOTP for network booting of diskless machines.

%package	base
Summary:	A lightweight dhcp and caching nameserver - base files without init scripts
Group:		Networking/Remote access

%description	base
Dnsmasq is lightweight, easy to configure DNS forwarder and DHCP server. It
is designed to provide DNS and, optionally, DHCP, to a small network. It can
serve the names of local machines which are not in the global DNS. The DHCP
server integrates with the DNS server and allows machines with DHCP-allocated
addresses to appear in the DNS with names configured either in each host or
in a central configuration file. Dnsmasq supports static and dynamic DHCP
leases and BOOTP for network booting of diskless machines.

This package contains the base files of the Dnsmasq server, without the init
scripts and global configuration files.

%prep
%autosetup -p1

%build
#fedya
sed -i -r 's:lua5.[0-9]+:lua:' Makefile

#(tpg) enable dbus support
sed -i 's|/\* #define HAVE_DBUS \*/|#define HAVE_DBUS|g' src/config.h

# fedya
# use /var/lib/dnsmasq instead of /var/lib/misc
for file in dnsmasq.conf.example man/dnsmasq.8 man/es/dnsmasq.8 src/config.h; do
    sed -i 's|/var/lib/misc/dnsmasq.leases|/var/lib/dnsmasq/dnsmasq.leases|g' "$file"
done

#enable IDN support
sed -i 's|/\* #define HAVE_IDN \*/|#define HAVE_IDN|g' src/config.h

# RH bugzilla
#enable /etc/dnsmasq.d fix bz 526703
sed -i 's|#conf-dir=/etc/dnsmasq.d|conf-dir=/etc/dnsmasq.d|g' dnsmasq.conf.example

%serverbuild
%make CC=%{__cc} CFLAGS="%{optflags}" LDFLAGS="%ldflags"

%install
install -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -m644 %{SOURCE2} -D %{buildroot}/lib/systemd/system/%{name}.service
install -m644 dnsmasq.conf.example -D %{buildroot}%{_sysconfdir}/dnsmasq.conf
install -m755 -D src/dnsmasq %{buildroot}%{_sbindir}/dnsmasq
install -m644 man/dnsmasq.8 -D %{buildroot}%{_mandir}/man8/dnsmasq.8
install -d %{buildroot}/%{_sysconfdir}/dnsmasq.d/
install -d %{buildroot}/var/lib/%{name}/

%pre
%_pre_useradd %{name} /dev/null /sbin/nologin
%_pre_groupadd %{name} %{name}
%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}
%_postun_groupdel %{name} %{name}

%files
%config(noreplace) %{_sysconfdir}/dnsmasq.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%dir %{_sysconfdir}/dnsmasq.d/
%dir /var/lib/%{name}
/lib/systemd/system/%{name}.service

%files base
%doc CHANGELOG FAQ COPYING COPYING-v3 doc.html setup.html
%{_sbindir}/%{name}
%doc %{_mandir}/man8/%{name}*
