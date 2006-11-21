Summary:	phpSysInfo is a PHP script that displays information about the host being accessed
Summary(pl):	phpSysInfo jest skryptem PHP wy¶wietlaj±cym informacje o wywo³anym hoscie
Name:		phpSysInfo
Version:	2.5.1
Release:	6
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/phpsysinfo/phpsysinfo-%{version}.tar.gz
# Source0-md5:	3b42b9df6685c81241d807a8ec8b1254
Source1:	%{name}.conf
Source2:	%{name}-PLD.gif
Source3:	%{name}-lighttpd.conf
Patch0:		%{name}-PLD.patch
URL:		http://phpsysinfo.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	issue
Requires:	php(pcre)
Requires:	php(xml)
Requires:	webapps
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		phpsysinfo
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

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
%setup -q -n phpsysinfo
%patch0 -p0

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/{images,includes/{lang,mb,os,xml}}}

install index.php phpsysinfo.dtd distros.ini $RPM_BUILD_ROOT%{_appdir}
install images/*.gif images/*.png %{SOURCE2} $RPM_BUILD_ROOT%{_appdir}/images
install %{SOURCE2} $RPM_BUILD_ROOT%{_appdir}/images/PLD.gif
install includes/*.php $RPM_BUILD_ROOT%{_appdir}/includes
install includes/lang/*.php $RPM_BUILD_ROOT%{_appdir}/includes/lang
install includes/mb/*.php $RPM_BUILD_ROOT%{_appdir}/includes/mb
install includes/os/*.php $RPM_BUILD_ROOT%{_appdir}/includes/os
install includes/xml/*.php $RPM_BUILD_ROOT%{_appdir}/includes/xml

cp -a templates $RPM_BUILD_ROOT%{_appdir}/templates
rm $RPM_BUILD_ROOT%{_appdir}/templates/index.html

install config.php.new $RPM_BUILD_ROOT%{_sysconfdir}/config.php
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%triggerpostun -- %{name} < 2.5.1-1.5
# rescue app config
if [ -f /etc/%{name}/config.php.rpmsave ]; then
	mv -f %{_sysconfdir}/config.php{,.rpmnew}
	mv -f /etc/%{name}/config.php.rpmsave %{_sysconfdir}/config.php
fi

# nuke very-old config location (this mostly for Ra)
if [ -f /etc/httpd/httpd.conf ]; then
	sed -i -e "/^Include.*%{name}.conf/d" /etc/httpd/httpd.conf
fi

# migrate from httpd (apache2) config dir
if [ -f /etc/httpd/%{name}.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	mv -f /etc/httpd/%{name}.conf.rpmsave %{_sysconfdir}/httpd.conf
fi

rm -f /etc/httpd/httpd.conf/99_%{name}.conf
/usr/sbin/webapp register httpd %{_webapp}
%service -q httpd reload

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%dir %{_appdir}
%{_appdir}/index.php
%{_appdir}/phpsysinfo.dtd
%{_appdir}/distros.ini
%{_appdir}/images
%{_appdir}/includes
%{_appdir}/templates
