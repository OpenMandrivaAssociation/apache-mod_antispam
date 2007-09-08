#Module-Specific definitions
%define mod_name mod_antispam
%define mod_conf A41_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Mod_antispam is an apache module which can control referer spam
Name:		apache-%{mod_name}
Version:	1.0
Release:	%mkrel 6
Group:		System/Servers
License:	Apache License
URL:		http://bluecoara.net/item44/cat9.html
Source0:	http://bluecoara.net/download/mod_antispam/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		mod_antispam-1.0-apache220.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= 2.2.0
Requires(pre):  apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:  apache-devel >= 2.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
mod_antispam is an Apache-2/Apache-2.1 module that can control
spam access. By using white/black lists, you can allow/deny
clients that have invalid HTTP_REFERER. In future versions, DNSBL
and BerkeleyDB will be supported.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0

%build
%{_sbindir}/apxs -DDEBUG -c %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}/var/log/httpd

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

touch %{buildroot}/var/log/httpd/antispam.white
touch %{buildroot}/var/log/httpd/antispam.black
touch %{buildroot}/var/log/httpd/antispam.black.auto
touch %{buildroot}/var/log/httpd/antispam.white.auto

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS CHANGES INSTALL README TODO httpd.conf.sample
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
# this is prone to change later, leave as is for now
%attr(0644,apache,apache) %config(noreplace) /var/log/httpd/antispam.white
%attr(0644,apache,apache) %config(noreplace) /var/log/httpd/antispam.black
%attr(0644,apache,apache) %config(noreplace) /var/log/httpd/antispam.black.auto
%attr(0644,apache,apache) %config(noreplace) /var/log/httpd/antispam.white.auto
