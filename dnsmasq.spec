Name:		dnsmasq
Version:	2.50
Release:	%mkrel 1
License:	GPLv2 or GPLv3
Group:		System/Servers
URL:		http://www.thekelleys.org.uk/dnsmasq
Conflicts:	bind
Source0:	http://www.thekelleys.org.uk/dnsmasq/%{name}-%{version}.tar.gz
Source1:	dnsmasq.sysconfig
Source2:	dnsmasq.init
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Summary:	A lightweight dhcp and caching nameserver
Requires:	%{name}-base = %{version}-%{release}
Requires(preun):	rpm-helper
Requires(post):	rpm-helper

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
Conflicts:	dnsmasq < 2.45-2mdv

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
%make

%install
rm -rf %{buildroot}
install -m755 %{SOURCE2} -D %{buildroot}%{_initrddir}/%{name}
install -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/sysconfig/%{name}

install -m644 dnsmasq.conf.example -D %{buildroot}%{_sysconfdir}/dnsmasq.conf

install -m755 -D src/dnsmasq %{buildroot}%{_sbindir}/dnsmasq
#ln -sf ../../%{_initrddir}/%{name} %{buildroot}/%{_sbindir}/rcdnsmasq
install -m644 man/dnsmasq.8 -D %{buildroot}%{_mandir}/man8/dnsmasq.8


%clean
rm -rf %{buildroot}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%defattr(-,root,root)
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/dnsmasq.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%files base
%doc CHANGELOG FAQ doc.html setup.html
%{_sbindir}/%{name}
%doc %{_mandir}/man8/%{name}*
