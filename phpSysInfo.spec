Summary:	phpSysInfo is a PHP script that displays information about the host being accessed
Summary(pl):	phpSysInfo jest skryptem PHP wy¶wietlaj±cym informacje o wywo³anym hoscie
Name:		phpSysInfo
Version:	2.3
Release:	2
License:	GPL
# not sure about this Group:
Group:		Networking/Utilities
Vendor:		Uriah Welcome <precision@users.sourceforge.net>
Source0:	http://dl.sourceforge.net/phpsysinfo/phpsysinfo-%{version}.tar.gz
# Source0-md5:	8e9a2b7a099e26cbd85f140475512ccc
Source1:	%{name}.conf
Source2:	%{name}-PLD.gif
Patch0:		%{name}-PLD.patch
URL:		http://phpsysinfo.sourceforge.net/
Requires:	issue
Requires:	php
Requires:	php-xml
Requires:	php-pcre
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysinfodir	%{_datadir}/%{name}
%define		_sysconfdir	/etc/%{name}

%description
PHPSysInfo is a customizable PHP Script that parses /proc, and formats
information nicely. It will display information about system facts
like Uptime, CPU, Memory, PCI devices, SCSI devices, IDE devices,
Network adapters, Disk usage, and more.

%description -l pl
PHPSysInfo jest skryptem PHP, który mo¿emy dopasowaæ do naszych
potrzeb. Przetwarza on /proc, i w ³adny sposób pokazuje informacje
m.in. na temat: uptime, procesora, pamiêci, urz±dzeñ PCI, SCSI, IDE,
interfejsów sieciowych czy dysków.

%prep
%setup -q -n phpsysinfo-dev
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysinfodir}/images \
	$RPM_BUILD_ROOT%{_sysinfodir}/includes/{lang,mb,os,xml} \
	$RPM_BUILD_ROOT{%{_sysconfdir},/etc/httpd}

install config.php.new index.php phpsysinfo.dtd $RPM_BUILD_ROOT%{_sysinfodir}
install images/*.gif %{SOURCE2} $RPM_BUILD_ROOT%{_sysinfodir}/images
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysinfodir}/images/PLD.gif
install includes/*.php $RPM_BUILD_ROOT%{_sysinfodir}/includes
install includes/lang/*.php $RPM_BUILD_ROOT%{_sysinfodir}/includes/lang
install includes/mb/*.php $RPM_BUILD_ROOT%{_sysinfodir}/includes/mb
install includes/os/*.php $RPM_BUILD_ROOT%{_sysinfodir}/includes/os
install includes/xml/*.php $RPM_BUILD_ROOT%{_sysinfodir}/includes/xml

cp -r templates $RPM_BUILD_ROOT%{_sysinfodir}/templates
rm $RPM_BUILD_ROOT%{_sysinfodir}/templates/index.html

install config.php.new $RPM_BUILD_ROOT%{_sysconfdir}/config.php
ln -sf %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_sysinfodir}/config.php

install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	fi
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%config(noreplace) %verify(not md5 mtime size) /etc/httpd/%{name}.conf
%dir %{_sysinfodir}
%{_sysinfodir}/config.php
%{_sysinfodir}/index.php
%{_sysinfodir}/phpsysinfo.dtd
%{_sysinfodir}/images
%{_sysinfodir}/includes
%{_sysinfodir}/templates
