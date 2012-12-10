#Module-Specific definitions
%define mod_name mod_antispam
%define mod_conf A41_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache module which can control referer spam
Name:		apache-%{mod_name}
Version:	1.0
Release:	17
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

%description
mod_antispam is an Apache-2/Apache-2.1 module that can control
spam access. By using white/black lists, you can allow/deny
clients that have invalid HTTP_REFERER. In future versions, DNSBL
and BerkeleyDB will be supported.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0

%build
%{_bindir}/apxs -DDEBUG -c %{mod_name}.c

%install

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

%files
%doc AUTHORS CHANGES INSTALL README TODO httpd.conf.sample
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
# this is prone to change later, leave as is for now
%attr(0644,apache,apache) %config(noreplace) /var/log/httpd/antispam.white
%attr(0644,apache,apache) %config(noreplace) /var/log/httpd/antispam.black
%attr(0644,apache,apache) %config(noreplace) /var/log/httpd/antispam.black.auto
%attr(0644,apache,apache) %config(noreplace) /var/log/httpd/antispam.white.auto


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0-17mdv2012.0
+ Revision: 772550
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0-16
+ Revision: 678252
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-15mdv2011.0
+ Revision: 587910
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-14mdv2010.1
+ Revision: 516035
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0-13mdv2010.0
+ Revision: 406516
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0-12mdv2009.1
+ Revision: 325530
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0-11mdv2009.0
+ Revision: 234613
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0-10mdv2009.0
+ Revision: 215522
- fix rebuild
- fix buildroot

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0-9mdv2008.1
+ Revision: 181663
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.0-8mdv2008.1
+ Revision: 170701
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Dec 14 2007 Thierry Vignaud <tv@mandriva.org> 1.0-7mdv2008.1
+ Revision: 119819
- rebuild b/c of missing package on ia32

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-6mdv2008.0
+ Revision: 82511
- rebuild

* Sat Aug 18 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-5mdv2008.0
+ Revision: 65616
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-4mdv2007.1
+ Revision: 140603
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0-3mdv2007.1
+ Revision: 79308
- Import apache-mod_antispam

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0-3mdv2007.0
- rebuild

* Tue Dec 13 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0-2mdk
- rebuilt against apache-2.2.0

* Fri Oct 21 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0-1mdk
- initial Mandriva package

