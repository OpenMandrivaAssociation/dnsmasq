Name:		dnsmasq
Version:	2.39
Release:	%mkrel 1
License:	GPL
Group:		System/Servers
URL:		http://www.thekelleys.org.uk/dnsmasq
Conflicts:	bind
Source0:	http://www.thekelleys.org.uk/dnsmasq/%{name}-%{version}.tar.bz2
Source1:    dnsmasq.sysconfig
Source2:    dnsmasq.init
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Summary:	A lightweight dhcp and caching nameserver
Requires(preun):		rpm-helper
Requires(post):         rpm-helper

%description
Dnsmasq is lightweight, easy to configure DNS forwarder and DHCP server. It 
is designed to provide DNS and, optionally, DHCP, to a small network. It can
serve the names of local machines which are not in the global DNS. The DHCP 
server integrates with the DNS server and allows machines with DHCP-allocated
addresses to appear in the DNS with names configured either in each host or 
in a central configuration file. Dnsmasq supports static and dynamic DHCP 
leases and BOOTP for network booting of diskless machines.

%prep
%setup -q

%build
%make

%install
rm -rf $RPM_BUILD_ROOT
install -m755 %{SOURCE2} -D $RPM_BUILD_ROOT%{_initrddir}/%{name}
install -m644 %{SOURCE1} -D $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

install -m644 dnsmasq.conf.example -D $RPM_BUILD_ROOT%{_sysconfdir}/dnsmasq.conf

install -m755 -D src/dnsmasq $RPM_BUILD_ROOT%{_sbindir}/dnsmasq
#ln -sf ../../%{_initrddir}/%{name} $RPM_BUILD_ROOT/%{_sbindir}/rcdnsmasq
install -m644 man/dnsmasq.8 -D $RPM_BUILD_ROOT%{_mandir}/man8/dnsmasq.8

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%defattr(-,root,root)
%doc CHANGELOG COPYING FAQ doc.html setup.html 
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/dnsmasq.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/%{name}
%doc %{_mandir}/man8/%{name}*


