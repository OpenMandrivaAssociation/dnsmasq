%define debug_package %{nil}
Summary:	A lightweight dhcp and caching nameserver
Name:		dnsmasq
Version:	2.67
Release:	3
License:	GPLv2 or GPLv3
Group:		System/Servers
Url:		http://www.thekelleys.org.uk/dnsmasq
Source0:	http://www.thekelleys.org.uk/dnsmasq/%{name}-%{version}.tar.xz
Source1:	dnsmasq.sysconfig
Source2:	dnsmasq.service
Source4:	README.update.urpmi

BuildRequires:	pkgconfig(dbus-1)
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
%setup -q

%build
#(tpg) enable dbus support
sed -i 's|/\* #define HAVE_DBUS \*/|#define HAVE_DBUS|g' src/config.h

%serverbuild
%make

%install
install -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -m644 %{SOURCE2} -D %{buildroot}/lib/systemd/system/%{name}.service
install -m644 dnsmasq.conf.example -D %{buildroot}%{_sysconfdir}/dnsmasq.conf
install -m755 -D src/dnsmasq %{buildroot}%{_sbindir}/dnsmasq
install -m644 man/dnsmasq.8 -D %{buildroot}%{_mandir}/man8/dnsmasq.8
install -m644 %{SOURCE4} README.update.urpmi

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%config(noreplace) %{_sysconfdir}/dnsmasq.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
/lib/systemd/system/%{name}.service
%doc README.update.urpmi

%files base
%doc CHANGELOG FAQ COPYING COPYING-v3 doc.html setup.html
%{_sbindir}/%{name}
%doc %{_mandir}/man8/%{name}*

